import threading
import tomodachi

from app.scheduler.flows import (
    start_photogrammetry_flow_with_tags,
)

# HACK: yet another monkey patch
from app.services.amqp import AmqpTransport  # noqa: F401
from app.services.json_base import JsonBase
from app.services.options import global_options


class Service(tomodachi.Service):
    name = "jobs-amqp-service"

    options = global_options
    message_envelope = JsonBase
    exchange_type = "direct"

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

        # TODO: validate messages here with a json scheme
        # TODO: check that we send an ack to the queue

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

    async def send_job_status(
        self,
    ):
        # TODO
        pass

    async def send_job_finished(
        self,
    ):
        # TODO
        pass
