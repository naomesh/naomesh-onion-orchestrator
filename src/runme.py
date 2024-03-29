import asyncio
import logging
import os
import textwrap
from functools import partial

import anyio
import anyio.abc
import nest_asyncio
from tomodachi.launcher import ServiceLauncher

# HACK: ahead
import app.enoslib.login  # noqa
from app.models.results import push_schema
import prefect
from app._version import get_versions
from app.orion.config import apply_prefect_config_settings  # noqa
from app.orion.database import upgrade_database  # noqa
from app.scheduler.deployments import apply_deployments
from app.services import SERVICES_TO_RUN
from prefect.client.orion import get_client
from prefect.settings import (
    PREFECT_LOGGING_SERVER_LEVEL,
    PREFECT_ORION_API_HOST,
    PREFECT_ORION_API_PORT,
    PREFECT_ORION_SERVICES_LATE_RUNS_ENABLED,
    PREFECT_ORION_SERVICES_SCHEDULER_ENABLED,
    PREFECT_ORION_UI_ENABLED,
)
from prefect.utilities.processutils import kill_on_interrupt, run_process

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO)


def generate_welcome_blurb(base_url, ui_enabled: bool):
    __version__ = get_versions()["version"]

    blurb = textwrap.dedent(
        r"""
                    /~    NAOMESH ONION ORCHESTRATOR
                    \  \ /**     VERSION {version} BUNDLED WITH
                    \ ////        ___ ___ ___ ___ _____________    ___ ___ ___  __   _  _
                    // //        | _ \ _ \ __| __| __/ __|_   _|  / _ \| _ \_ _/ _ \| \| |
                    // //        |  _/   / _|| _|| _| (__  | |   | (_) |   /| | (_) | .` |
                ///&//           |_| |_|_\___|_| |___\___| |_|    \___/|_|_\___\___/|_|\_|
                / & /\ \         Configure Prefect to communicate with the server with:
                /  & .,,  \          prefect config set PREFECT_API_URL={api_url}
            /& %  :       \      View the API reference documentation at {docs_url}
            /&  %   :  ;     `\
        /&' &..%   !..    `.\
        /&' : &''" !  ``. : `.\
        /#' % :  "" * .   : : `.\
        I# :& :  !"  *  `.  : ::  I
        I &% : : !%.` '. . : : :  I
        I && :%: .&.   . . : :  : I
        I %&&&%%: WW. .%. : :     I
        \&&&##%%%`W! & '  :   ,'/
        \####ITO%% W &..'  #,'/
            \W&&##%%&&&&### %./
                ++///~~\//_
                \\ \ \ \  \_
                /  /    \
        """  # noqa: E501
    ).format(
        api_url=f"{base_url}/api",
        docs_url=f"{base_url}/docs",
        version=__version__,
    )

    visit_dashboard = textwrap.dedent(
        f"""
        Check out the dashboard at {base_url}"""
    )

    dashboard_not_built = textwrap.dedent(
        """
        The dashboard is not built.
        It looks like you're on a development version.
        See `prefect dev` for development commands.
        """
    )

    dashboard_disabled = textwrap.dedent(
        """
        The dashboard is disabled.
        Set `PREFECT_ORION_UI_ENABLED=1` to reenable it.
        """
    )

    if not os.path.exists(prefect.__ui_static_path__):
        blurb += dashboard_not_built
    elif not ui_enabled:
        blurb += dashboard_disabled
    else:
        blurb += visit_dashboard

    return blurb


async def start_orion_and_tomodachi(
    host: str = "0.0.0.0",
    port: int = PREFECT_ORION_API_PORT.value(),
    log_level: str = PREFECT_LOGGING_SERVER_LEVEL.value(),
    scheduler: bool = PREFECT_ORION_SERVICES_SCHEDULER_ENABLED.value(),
    analytics: bool = False,
    late_runs: bool = PREFECT_ORION_SERVICES_LATE_RUNS_ENABLED.value(),
    ui: bool = PREFECT_ORION_UI_ENABLED.value(),
):
    """Start an Orion server"""

    server_env = os.environ.copy()
    server_env["PREFECT_ORION_SERVICES_SCHEDULER_ENABLED"] = str(scheduler)
    server_env["PREFECT_ORION_ANALYTICS_ENABLED"] = str(analytics)
    server_env["PREFECT_ORION_SERVICES_LATE_RUNS_ENABLED"] = str(late_runs)
    server_env["PREFECT_ORION_SERVICES_UI"] = str(ui)
    server_env["PREFECT_LOGGING_SERVER_LEVEL"] = log_level
    base_url = f"http://{host}:{port}"
    print(generate_welcome_blurb(base_url, ui_enabled=ui))
    print("Applying prefect config settings to current profile...")
    apply_prefect_config_settings()
    print("...OK")

    print("Running upgrade migrations ..")
    await upgrade_database()
    await push_schema()
    print("...OK")

    async with anyio.create_task_group() as tg:
        orion_process_id = await tg.start(
            partial(
                run_process,
                command=[
                    "uvicorn",
                    "--factory",
                    "prefect.orion.api.server:create_app",
                    "--host",
                    host,
                    "--port",
                    str(port),
                ],
                env=server_env,
                stream_output=True,
                cwd=prefect.__module_path__.parent,
            )
        )

        await apply_deployments()

        # NOTE: delete flow runs at startup to avoid orphaned flow runs
        flows = await get_client().read_flow_runs()
        for flow in flows:
            await get_client().delete_flow_run(flow.id)
        print("Starting tomodachi services...")
        await tg.start(start_tomodachi_services)
        print("...OK")
        print("😎 Onion started! Press Ctrl+C to stop. 😎")

        # Explicitly handle the interrupt signal here, as it will allow us to
        # cleanly stop the Orion uvicorn server. Failing to do that may cause a
        # large amount of anyio error traces on the terminal, because the
        # SIGINT is handled by Typer/Click in this process (the parent process)
        # and will start shutting down subprocesses:
        # https://github.com/PrefectHQ/orion/issues/2475

        kill_on_interrupt(orion_process_id, "Orion", print)  # type: ignore

    print("Orion stopped!")
    ServiceLauncher.stop_services()


async def start_tomodachi_services(task_status):
    task_status.started()
    ServiceLauncher.run_until_complete(SERVICES_TO_RUN, None, None)


asyncio.get_event_loop().run_until_complete(
    asyncio.gather(start_orion_and_tomodachi())
)
