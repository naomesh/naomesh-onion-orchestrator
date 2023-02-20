import tomodachi

from app.services.json_base import JsonBase
from app.services.options import global_options


class Service(tomodachi.Service):
    name = "currentallocatednodes-amqp-service"

    options = global_options
    message_envelope = JsonBase
    exchange_type = "topic"

    @tomodachi.amqp(
        routing_key="orchestration.currentallocatednodes",
        exchange_name="amq.topic",
        competing=True,
        queue_name="allocatednodes",
    )
    async def receive_job_request(
        self,
        message,
        delivery_tag,
        routing_key,
    ):
        # TODO
        pass
