import tomodachi
from app.services.json_base import JsonBase
from app.services.options import global_options


class Service(tomodachi.Service):
    name = "currentallocatednodes-amqp-service"
    options = global_options
    message_envelope = JsonBase
    exchange_type = "direct"

    @tomodachi.schedule(interval=1)
    async def send_current_allocated_nodes(
        self,
    ):
        # TODO
        message = {"nodes": []}
        await tomodachi.amqp_publish(
            self,
            routing_key="orchestration.currentallocatednodes",
            exchange_name="amq.topic",
            data=message,
        )
