import asyncio
from datetime import datetime, timedelta
from os import path

import tomodachi

import enoslib as en
from app.core.config import BASE_DIR, env
from app.models.results import Result, insert_result
from app.scheduler.utils import (
    task_input_hash_no_roles_node,
    with_redirect_stdout_to_run_logger,
)
from enoslib import Roles
from prefect import task
from prefect.context import FlowRunContext


@task(
    name="Run one step of the pipeline",
    # HACK: kind of a hack to get the task params in the task name
    task_run_name="p:{picture_obj_key}|i:{node_id}|s:{step_idx}|j:{job_id}|n:{number_of_pics}",  # noqa: E501
    retries=2,
    retry_delay_seconds=10,
    cache_key_fn=task_input_hash_no_roles_node,
    # TODO: add an env variable for this, should be the duration of the g5k job
    cache_expiration=timedelta(hours=2),
    persist_result=True,
)
def run_step(
    picture_obj_key: "str",
    politic_energy_name: "str",
    politic_quality_name: "str",
    job_id: "str",
    number_of_pics: "int",
    node_id: "str",
    step_idx: "int",
    roles: "Roles",
):
    """Run one step of the pipeline"""
    with with_redirect_stdout_to_run_logger():
        print(f"Running step {step_idx} on node {node_id}")
        en.run_ansible(
            [path.join(BASE_DIR, "g5kecotype-node-step-playbook.yml")],
            roles=roles,
            extra_vars={
                "step_idx": step_idx,
                "quality_policy": politic_quality_name,
            },
        )


@task(
    name="Push results to s3",
    retries=2,
    task_run_name="p:{picture_obj_key}|i:{node_id}|s:99|j:{job_id}|n:{number_of_pics}",  # noqa: E501
    retry_delay_seconds=10,
    persist_result=True,
)
def push_results(
    picture_obj_key: "str",
    politic_energy_name: "str",
    politic_quality_name: "str",
    job_id: "str",
    number_of_pics: "int",
    node_id: "str",
    roles: "Roles",
):
    """Push results"""
    with with_redirect_stdout_to_run_logger():
        # TODO: add minimal callback plugin to output stdout
        # https://serverfault.com/a/842944
        en.run_ansible(
            [path.join(BASE_DIR, "g5kecotype-node-finish-playbook.yml")],
            roles=roles,
            extra_vars={
                "s3_host": env("AWS_S3_URL"),
                "s3_bucket_name": env("AWS_S3_BUCKET"),
                "s3_access_key": env("AWS_S3_ACCESS_KEY_ID"),
                "s3_secret_key": env("AWS_S3_SECRET_ACCESS_KEY"),
                "picture_obj_key": picture_obj_key,
                "job_id": job_id,
            },
        )
    print("Results pushed to s3")
    print("Publishing finished message AMQP")
    service = tomodachi.get_service("jobs-amqp-service")
    politic = {
        "energy": politic_energy_name,
        "quality": politic_quality_name,
    }
    parent_flow_run_context = FlowRunContext.get()
    start_time = (
        ((parent_flow_run_context.start_time or datetime.now()))
        if parent_flow_run_context
        else datetime.now()
    )

    end_time = datetime.now()
    node_uses = [
        {
            "node_id": node_id,
            "start_time": int(start_time.timestamp()),
            "end_time": int(end_time.timestamp()),
        }
    ]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(
        asyncio.gather(
            service.send_job_finished(  # publish to amqp
                job_id,
                node_uses,
                f"/{job_id}/results/scene_dense_mesh.ply",
                f"/{job_id}/results/scene_dense_mesh_texture.png",
                politic,
            ),
            insert_result(
                Result(  # insert in db
                    job_id=job_id,
                    total_consumption_kwh=0,  # TODO
                    model_obj_key=f"/{job_id}/results/scene_dense_mesh.ply",
                    texture_obj_key=f"/{job_id}/results/scene_dense_mesh_texture.png",  # noqa: E501
                    total_production_kwh=0,  # TODO
                    node_id=node_id,
                    start_time=start_time,
                    end_time=end_time,
                    pictures_quantity=number_of_pics,
                )
            ),
        )
    )
    loop.close()


@task(
    name="Setup node",
    retries=1,
    task_run_name="p:{picture_obj_key}|i:N/A|s:-1|j:{job_id}|n:-1",  # noqa: E501
)
def setup_node(
    job_id: "str",
    picture_obj_key: "str",
    politic_energy_name: "str",
    politic_quality_name: "str",
):
    with with_redirect_stdout_to_run_logger():
        if env("NAOMESH_ORCHESTRATOR_ENOSLIB_ENABLE_AUTOJUMP"):
            en.check()  # NOTE: This will not work inside g5k
        network = en.G5kNetworkConf(
            type="prod",
            roles=["naomesh"],
            site=env("NAOMESH_ORCHESTRATOR_GRID5000_SITE"),
        )

        task_name = f"naomesh_task_{job_id}"

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
            extra_vars={
                "s3_host": env("AWS_S3_URL"),
                "s3_bucket_name": env("AWS_S3_BUCKET"),
                "s3_access_key": env("AWS_S3_ACCESS_KEY_ID"),
                "s3_secret_key": env("AWS_S3_SECRET_ACCESS_KEY"),
                "picture_obj_key": picture_obj_key,
            },
            roles=roles,
        )
    return roles, provider
