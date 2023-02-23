from typing import Optional

import pendulum

from app.core.config import env
from app.enoslib.utils import is_there_one_node_available
from app.orion.naomesh_orchestration_policy import EnergyPolicy
from app.seduce.api.default.get_live_production_solar_panels import asyncio
from app.seduce.client import Client
from prefect.orion.orchestration.rules import (
    ALL_ORCHESTRATION_STATES,
    BaseOrchestrationRule,
    FlowOrchestrationContext,
    OrchestrationContext,
    TaskOrchestrationContext,
)
from prefect.orion.schemas import core, states
from prefect.orion.schemas.states import StateType

api_client = Client(base_url=env("NAOMESH_ORCHESTRATOR_SEDUCE_API_URL"))  # type: ignore # noqa: E501


class GreenFlowPolicy(BaseOrchestrationRule):
    """
    Rejects failed states and schedules a retry if the retry limit has not
    been reached.

    This rule rejects transitions into a failed state if `retries` has been
    set and the run count has not reached the specified limit.
    The client will be
    instructed to transition into a scheduled state to retry flow execution.
    """

    FROM_STATES = [StateType.SCHEDULED, StateType.PENDING, StateType.PAUSED]
    TO_STATES = [StateType.RUNNING]

    async def before_transition(
        self,
        initial_state: Optional[states.State],
        proposed_state: Optional[states.State],
        context: FlowOrchestrationContext,
    ) -> None:
        flow_run = await context.flow_run()
        if EnergyPolicy.GREEN.value not in flow_run.tags:
            return
        (
            enough_energy_res,
            production_solar_panel,
            minimum_production_solar_panel,
        ) = await enough_energy()
        node_available = await is_there_one_node_available()
        if enough_energy_res and node_available:
            return
        updated_policy = context.run.empirical_policy.dict()
        updated_policy["resuming"] = False
        updated_policy["pause_keys"] = set()
        context.run.empirical_policy = core.FlowRunPolicy(**updated_policy)
        wait_seconds = 10  # TODO: make this a parameter
        scheduled_start_time = pendulum.now("UTC").add(seconds=wait_seconds)
        await self.delay_transition(
            delay_seconds=wait_seconds,
            reason=f"${production_solar_panel} < ${minimum_production_solar_panel} or no available nodes",  # noqa: E501
        )
        self.context.proposed_state = states.AwaitingRetry(
            scheduled_time=scheduled_start_time
        )


# TODO: implement task transition to pause tasks
class GreenTaskPolicy(BaseOrchestrationRule):
    """
    Check if the task is in the green energy policy and if the
    solar panel production is enough
    """

    FROM_STATES = ALL_ORCHESTRATION_STATES
    TO_STATES = [StateType.RUNNING]

    async def before_transition(
        self,
        initial_state: Optional[states.State],
        validated_state: Optional[states.State],
        context: TaskOrchestrationContext,
    ) -> None:
        return

    async def cleanup(
        self,
        initial_state: Optional[states.State],
        validated_state: Optional[states.State],
        context: OrchestrationContext,
    ) -> None:
        pass


async def enough_energy():
    """
    Check if the solar panel production is enough
    If the api is not available, we assume that the production is enough
    """
    production_solar_panel = -1.0
    minimum_production_solar_panel: int = env(
        "NAOMESH_ORCHESTRATOR_MINIMUM_PRODUCTION_SOLAR_PANELS"
    )
    solar_production_enough = True
    try:
        response = await asyncio(client=api_client)
        production_solar_panel: float = (
            response.data if response is not None else 0.0
        )  # type: ignore

        solar_production_enough = (
            production_solar_panel >= minimum_production_solar_panel
        )
    except Exception:
        print("Could not contact seduce api")
    finally:
        return (
            solar_production_enough,
            production_solar_panel,
            minimum_production_solar_panel,
        )
