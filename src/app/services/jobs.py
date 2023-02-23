from datetime import datetime
import threading

import tomodachi
from app.orion.naomesh_orchestration_policy import EnergyPolicy, QualityPolicy

from app.scheduler.flows import start_photogrammetry_flow_with_tags

# HACK: yet another monkey patch
from app.services.amqp import AmqpTransport  # noqa: F401
from app.services.json_base import JsonBase
from app.services.options import global_options
from app.services.utils import (
    extract_from_task_name_infos,
    map_node_uid_to_seduce_uid,
)
from datetime import timezone
from prefect.client.orion import get_client
from prefect.orion.schemas.filters import (
    FlowRunFilter,
    FlowRunFilterState,
    FlowRunFilterStateName,
    FlowRunFilterStateType,
    Operator,
    TaskRunFilter,
    TaskRunFilterState,
    TaskRunFilterStateName,
    TaskRunFilterStateType,
)

# NOTE: See asynapi schema for the message format of onion

JOBS_SERVICE_NAME = "jobs-amqp-service"


class JobsService(tomodachi.Service):
    name = JOBS_SERVICE_NAME

    options = global_options
    message_envelope = JsonBase
    exchange_type = "direct"
    orion_client = get_client()

    @tomodachi.amqp(
        routing_key="orchestration.jobs.requests",
        exchange_name="amq.direct",
        competing=True,
        queue_name="jobsrequests",
    )
    async def receive_job_request(
        self,
        message,
        envelope,
        routing_key,
    ):
        """Receive a job request from and process it on a new thread"""

        # TODO: validate messages here with a json scheme
        # TODO: check that we send an ack to the queue
        # TODO: add a thread limit ? a thread pool ?

        # NOTE: spawning a new thread is not the best way to do this
        # but it's the easiest way to do it for now
        # It is because ansible and enoslib are not async

        t1 = threading.Thread(
            target=start_photogrammetry_flow_with_tags,
            args=[
                message["job_id"],
                message["pictures_obj_key"],
                message["politic"]["energy"],
                message["politic"]["quality"],
            ],
        )
        t1.start()

    @tomodachi.schedule(interval=1)
    async def send_job_status(
        self,
    ):
        """Send the job status to the client every second"""

        # running tasks
        res = await self.orion_client.read_task_runs(
            task_run_filter=TaskRunFilter(
                operator=Operator.or_,
                state=TaskRunFilterState(
                    name=TaskRunFilterStateName(any_=["Running", "Scheduled"]),
                    type=TaskRunFilterStateType(),
                ),
            )
        )

        # awaiting flows
        res_scheduled = await self.orion_client.read_flow_runs(
            flow_run_filter=FlowRunFilter(
                state=FlowRunFilterState(
                    name=FlowRunFilterStateName(
                        any_=["Scheduled", "AwaitingRetry"]
                    ),
                    type=FlowRunFilterStateType(),
                )
            )
        )
        running_tasks = filter(lambda x: x.state_name == "Running", res)
        number_of_running_jobs = len(list(running_tasks))

        # TODO: whoever reading this, please, refactor it
        jobs_flows = [  # array of paused jobs, it should be
            {
                "job_id": flow_run.parameters["job_id"],
                "state": map_prefect_state_name_to_onion_state(
                    (flow_run.state_name or "running").lower()
                ),
                "last_paused_date": 0,  # TODO: implement last_paused_date
                "last_started_date": int(
                    (
                        flow_run.start_time or datetime.now(timezone.utc)
                    ).timestamp()
                    * 1000
                ),
                "step_idx": 0,  # this is a not started flow, so step_idx is 0
                "pictures_quantity": 0,
                "node_id": None,
                "politic": {
                    "quality": list(
                        filter(
                            lambda tag: tag
                            in [
                                QualityPolicy.GOOD.value,
                                QualityPolicy.BAD.value,
                            ],
                            flow_run.tags,
                        )
                    )[
                        0
                    ],  # TODO: refactor this, don't use [0]
                    "energy": list(
                        filter(
                            lambda tag: tag
                            in [
                                EnergyPolicy.BYPASS.value,
                                EnergyPolicy.GREEN.value,
                            ],
                            flow_run.tags,
                        )
                    )[
                        0
                    ],  # TODO: refactor this, don't use [0]
                },
                "consumption": -1,  # TODO: implement consumption
                "pictures_obj_key": flow_run.parameters["picture_obj_key"],
            }
            for flow_run in res_scheduled
        ]
        jobs_tasks = [
            {
                "job_id": metadata["j"],
                "state": map_prefect_state_name_to_onion_state(
                    (task_run.state_name or "running").lower()
                ),
                "last_paused_date": 0,  # TODO: implement last_paused_date
                "last_started_date": int(
                    (
                        task_run.start_time or datetime.now(timezone.utc)
                    ).timestamp()
                    * 1000
                ),
                "step_idx": int(metadata["s"]),
                "pictures_quantity": int(metadata["n"]),
                "node_id": map_node_uid_to_seduce_uid(metadata["i"]),
                "politic": {
                    "quality": list(
                        filter(
                            lambda tag: tag
                            in [
                                QualityPolicy.GOOD.value,
                                QualityPolicy.BAD.value,
                            ],
                            task_run.tags,
                        )
                    ),
                    "energy": list(
                        filter(
                            lambda tag: tag
                            in [
                                EnergyPolicy.BYPASS.value,
                                EnergyPolicy.GREEN.value,
                            ],
                            task_run.tags,
                        )
                    ),
                },
                "consumption": -1,  # TODO: implement consumption
                "pictures_obj_key": metadata["p"],
            }
            for task_run in res
            if (
                metadata := (
                    task_run.name.startswith("p:")
                    and extract_from_task_name_infos(task_run.name)
                )
            )
        ]

        message = {
            "number_of_running_jobs": number_of_running_jobs,
            "jobs": [*jobs_tasks, *jobs_flows],
        }
        await tomodachi.amqp_publish(
            self,
            routing_key="orchestration.jobs.status",
            exchange_name="amq.direct",
            data=message,
        )

    async def send_job_finished(
        self,
        job_id: str,
        node_uses: list[dict],
        model_obj_key: str,
        texture_obj_key: str,
        politic: dict,
    ):
        """Send a job finished message to the rabbitmq queue"""

        # TODO
        message = {
            "job_id": job_id,
            "node_uses": node_uses,
            "model_obj_key": model_obj_key,
            "texture_obj_key": texture_obj_key,
            "politic": politic,
        }
        await tomodachi.amqp_publish(
            self,
            routing_key="orchestration.jobs.requests",
            exchange_name="amq.direct",
            data=message,
        )


def map_prefect_state_name_to_onion_state(state: str):
    mapping = {
        "scheduled": "paused",
        "awaitingretry": "paused",
    }
    return mapping.get(state, state)
