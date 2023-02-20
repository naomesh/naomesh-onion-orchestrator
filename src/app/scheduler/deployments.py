# NOTE: This file is not used in the current version of the project.
# Deployements are created in the database, but they can run only with a agent

from prefect.deployments import Deployment
from app.scheduler.flows import photogrammetry_flow
from app.orion.naomesh_orchestration_policy import EnergyPolicy, QualityPolicy

DEPLOYEMENT_GREEN_GOOD_NAME = "green-good-photogrammetry-flow"
DEPLOYEMENT_GREEN_BAD_NAME = "green-bad-photogrammetry-flow"
DEPLOYEMENT_BYPASS_GOOD_NAME = "bypass-good-photogrammetry-flow"
DEPLOYEMENT_BYPASS_BAD_NAME = "bypass-bad-photogrammetry-flow"


async def apply_deployments():
    await Deployment.build_from_flow(
        flow=photogrammetry_flow,
        name=DEPLOYEMENT_GREEN_GOOD_NAME,
        version="0.0.1",
        parameters={
            "politic_energy_name": EnergyPolicy.GREEN.value,
            "politic_quality_name": QualityPolicy.GOOD.value,
        },
        tags=[EnergyPolicy.GREEN.value, QualityPolicy.GOOD.value],
        apply=True,
    )

    await Deployment.build_from_flow(
        flow=photogrammetry_flow,
        name=DEPLOYEMENT_GREEN_BAD_NAME,
        version="0.0.1",
        parameters={
            "politic_energy_name": EnergyPolicy.GREEN.value,
            "politic_quality_name": QualityPolicy.BAD.value,
        },
        tags=[EnergyPolicy.GREEN.value, QualityPolicy.BAD.value],
        apply=True,
    )

    await Deployment.build_from_flow(
        flow=photogrammetry_flow,
        name=DEPLOYEMENT_BYPASS_GOOD_NAME,
        version="0.0.1",
        parameters={
            "politic_energy_name": EnergyPolicy.BYPASS.value,
            "politic_quality_name": QualityPolicy.GOOD.value,
        },
        tags=[EnergyPolicy.BYPASS.value, QualityPolicy.GOOD.value],
        apply=True,
    )

    await Deployment.build_from_flow(
        flow=photogrammetry_flow,
        name=DEPLOYEMENT_BYPASS_BAD_NAME,
        version="0.0.1",
        parameters={
            "politic_energy_name": EnergyPolicy.BYPASS.value,
            "politic_quality_name": QualityPolicy.BAD.value,
        },
        tags=[EnergyPolicy.BYPASS.value, QualityPolicy.BAD.value],
        apply=True,
    )
