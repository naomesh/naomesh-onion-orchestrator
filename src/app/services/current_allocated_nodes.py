import tomodachi
from app.services.json_base import JsonBase
from app.services.options import global_options
from app.services.utils import (
    extract_from_task_name_infos,
    map_node_uid_to_seduce_uid,
)
from prefect.client.orion import get_client
from prefect.orion.schemas.filters import (
    Operator,
    TaskRunFilter,
    TaskRunFilterState,
    TaskRunFilterStateName,
    TaskRunFilterStateType,
)

# NOTE: See asynapi schema for the message format of onion


class CurrentAllocatedNodesService(tomodachi.Service):
    name = "currentallocatednodes-amqp-service"
    options = global_options
    message_envelope = JsonBase
    exchange_type = "topic"
    orion_client = get_client()

    @tomodachi.schedule(interval=1)
    async def send_current_allocated_nodes(
        self,
    ):
        """Send the current allocated nodes to the orchestrator
        every second
        """
        res = await self.orion_client.read_task_runs(
            task_run_filter=TaskRunFilter(
                operator=Operator.or_,
                state=TaskRunFilterState(
                    name=TaskRunFilterStateName(any_=["Running"]),
                    type=TaskRunFilterStateType(),
                ),
            )
        )

        message = {
            "nodes": [
                map_node_uid_to_seduce_uid(
                    extract_from_task_name_infos(node.name).get("i", "")
                )
                for node in res
                if "i" in extract_from_task_name_infos(node.name)
            ]
        }
        await tomodachi.amqp_publish(
            self,
            routing_key="orchestration.currentallocatednodes",
            exchange_name="amq.topic",
            data=message,
        )
