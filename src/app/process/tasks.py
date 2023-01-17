import logging
import enoslib as en
from app.core.config import env


def reserve():
    en.init_logging(level=logging.INFO)
    en.check()

    # api = en.g5k_api_utils.get_api_client()
    # print(api.sites[site].clusters["econome"])

    network = en.G5kNetworkConf(
        type="prod",
        roles=["naomesh"],
        site=env("NAOMESH_ORCHESTRATOR_GRID5000_SITE"),
    )

    conf = (
        en.G5kConf()
        .from_settings(job_type="allow_classic_ssh", job_name="naomesh_task_1")
        .add_network_conf(network)
        .add_machine(
            primary_network=network,
            cluster="ecotype",
            nodes=1,
            roles=["control"],
        )
        .finalize()
    )

    provider = en.G5k(conf)
    roles, networks = provider.init()

    # Install docker
    registry_opts = dict(
        type="external", ip="docker-cache.grid5000.fr", port=80
    )

    # login to bypass docker-hub rate-limiting
    docker_credentials = dict(
        login=env("NAOMESH_ORCHESTRATOR_DOCKER_USERNAME"),
        password=env("NAOMESH_ORCHESTRATOR_DOCKER_PASSWORD"),
    )

    # create the docker instance with the credentials
    docker = en.Docker(
        agent=roles["control"],
        bind_var_docker="/tmp/docker",
        registry_opts=registry_opts,
        credentials=docker_credentials,
    )

    docker.deploy()

    # Start an openmvs docker container on the node
    with en.actions(roles=roles) as t:
        t.raw("modprobe ifb")
        t.docker_container(
            name="openmvs",
            image="openmvs/openmvs-ubuntu",
            state="started",
            command="echo 'ready'",
            capabilities=["NET_ADMIN"],
        )

    results = en.run_command("whoami", roles=roles)
    result = results.filter(host=roles["control"][0].alias)[0]

    print(
        f"stdout = {result.stdout}\n",
        f"stderr={result.stderr}\n",
        f"return code = {result.rc}",
    )

    provider.destroy()
