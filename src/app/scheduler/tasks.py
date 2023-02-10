from datetime import timedelta
from os import path

import enoslib as en
from enoslib import Roles
from prefect import task

from app.core.config import BASE_DIR, env
from app.scheduler.utils import (
    task_input_hash_no_roles,
    with_redirect_stdout_to_run_logger,
)


@task(
    name="Run one step of the pipeline",
    retries=2,
    retry_delay_seconds=10,
    cache_key_fn=task_input_hash_no_roles,
    # TODO: add an env variable for this, should be the duration of the g5k job
    cache_expiration=timedelta(hours=2),
)
def run_step(
    _picture_obj_key: str, _politic_name: str, step_idx: int, roles: "Roles"
):
    """Run one step of the pipeline"""
    with with_redirect_stdout_to_run_logger():
        en.run_ansible(
            [path.join(BASE_DIR, "g5kecotype-node-step-playbook.yml")],
            roles=roles,
            extra_vars={"step_idx": step_idx},
        )


@task(name="Setup node", retries=1)
def setup_node(picture_obj_key: str, _politic_name: str):
    with with_redirect_stdout_to_run_logger():
        en.check()
        network = en.G5kNetworkConf(
            type="prod",
            roles=["naomesh"],
            site=env("NAOMESH_ORCHESTRATOR_GRID5000_SITE"),
        )

        task_name = f"naomesh_task_{picture_obj_key}"

        conf = (
            en.G5kConf()
            .from_settings(job_name=task_name)
            .add_network_conf(network)
            .add_machine(
                primary_network=network,
                cluster="ecotype",
                nodes=1,
                roles=[picture_obj_key],
            )
            .finalize()
        )

        provider = en.G5k(conf)
        roles, _ = provider.init()

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
            agent=roles[picture_obj_key],
            bind_var_docker="/tmp/docker",
            registry_opts=registry_opts,
            credentials=docker_credentials,
        )

        # Deploy base docker
        docker.deploy()

        # Install docker-compose and pull files on the node
        en.run_ansible(
            [path.join(BASE_DIR, "g5kecotype-node-entry-playbook.yml")],
            roles=roles,
        )

    return roles, provider
