from datetime import timedelta
from os import path
from typing import Any, Dict, Optional

import enoslib as en
from enoslib import Roles
from prefect import task
from prefect.context import TaskRunContext
from prefect.utilities.hashing import hash_objects

from app.core.config import BASE_DIR, env
from app.scheduler.utils import with_redirect_stdout_to_run_logger


def task_input_hash_no_roles(
    context: "TaskRunContext", arguments: Dict[str, Any]
) -> Optional[str]:
    """
    A task cache key implementation which hashes all inputs
    to the task using a JSON or
    cloudpickle serializer. If any arguments are not JSON
    serializable, the pickle
    serializer is used as a fallback. If cloudpickle fails,
    this will return a null key
    indicating that a cache key could not be generated for the given inputs.

    Arguments:
        context: the active `TaskRunContext`
        arguments: a dictionary of arguments to be passed to
        the underlying task

    Returns:
        a string hash if hashing succeeded, else `None`
    """
    return hash_objects(
        # We use the task key to get the qualified name for the task and
        # include the task functions `co_code` bytes to avoid caching
        # when the underlying function changes
        context.task.task_key,
        context.task.fn.__code__.co_code.hex(),
        without_keys(arguments, "roles"),
    )


def without_keys(d, keys):
    return {k: d[k] for k in d.keys() - keys}


@task(
    name="Run one step of the pipeline",
    retries=2,
    retry_delay_seconds=10,
    cache_key_fn=task_input_hash_no_roles,
    cache_expiration=timedelta(
        hours=2
    ),  # TODO: add an env variable for this, should be the duration of the g5k job
)
def run_step(_picture_obj_key: str, step_idx: int, roles: "Roles"):
    """Run one step of the pipeline"""
    with with_redirect_stdout_to_run_logger():
        en.run_ansible(
            [path.join(BASE_DIR, "g5kecotype-node-step-playbook.yml")],
            roles=roles,
            extra_vars={"step_idx": step_idx},
        )


@task(name="Setup node", retries=1)
def setup_node(pictures_hash: str):
    with with_redirect_stdout_to_run_logger():
        en.check()
        network = en.G5kNetworkConf(
            type="prod",
            roles=["naomesh"],
            site=env("NAOMESH_ORCHESTRATOR_GRID5000_SITE"),
        )

        task_name = f"naomesh_task_{pictures_hash}"

        conf = (
            en.G5kConf()
            .from_settings(job_name=task_name)
            .add_network_conf(network)
            .add_machine(
                primary_network=network,
                cluster="ecotype",
                nodes=1,
                roles=[pictures_hash],
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
            agent=roles[pictures_hash],
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
