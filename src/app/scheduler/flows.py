import logging
from contextlib import ExitStack

import enoslib as en

from app.orion.naomesh_orchestration_policy import EnergyPolicy, QualityPolicy
from app.scheduler.tasks import run_step, setup_node
from prefect import flow, get_run_logger, tags
from prefect.task_runners import SequentialTaskRunner


@flow(
    name="Photogrammetry v0.0.1 flow",
    version="0.0.1",
    log_prints=True,
    persist_result=True,
    task_runner=SequentialTaskRunner(),
    retries=1,
)
def photogrammetry_flow(
    job_id: str,
    picture_obj_key,
    politic_energy_name: str = EnergyPolicy.GREEN.value,
    politic_quality_name: str = QualityPolicy.GOOD.value,
):
    """Photogrammetry flow"""
    print(get_run_logger())
    en.init_logging(level=logging.INFO).getLogger()

    result = setup_node.submit(
        job_id, picture_obj_key, politic_energy_name, politic_quality_name
    )
    roles, provider, host = result.result()
    # SEQUENTIAL: 0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15
    with ExitStack() as _:
        # 0. Intrinsics analysis (openMVG_main_SfMInit_ImageListing)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            0,
            roles,
        ).result()

        # 1. Compute features (openMVG_main_ComputeFeatures)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            1,
            roles,
        ).result()

        # 2. Compute pairs (openMVG_main_PairGenerator)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            2,
            roles,
        ).result()

        # 3. Compute matches (openMVG_main_ComputeMatches)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            3,
            roles,
        ).result()

        # 4. Filter matches (openMVG_main_GeometricFilter)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            4,
            roles,
        ).result()

        # 5. Incremental reconstruction (openMVG_main_IncrementalSfM)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            5,
            roles,
        ).result()

        # 6. Global reconstruction (openMVG_main_GlobalSfM)
        # run_step(picture_obj_key, 6, roles)
        # 7. Colorize Structure (openMVG_main_ComputeSfM_DataColor)
        # run_step(picture_obj_key, 7, roles)
        # 8. Structure from Known Poses
        # (openMVG_main_ComputeStructureFromKnownPoses)
        # run_step(picture_obj_key, 8, roles)
        # 9. Colorized robust triangulation (openMVG_main_ComputeSfM_DataColor)
        # run_step(picture_obj_key, 9, roles)
        # 10. Control Points Registration
        # (ui_openMVG_control_points_registration)
        # run_step(picture_obj_key, 10, roles)

        # 11. Export to openMVS (openMVG_main_openMVG2openMVS)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            11,
            roles,
        ).result()

        # 12. Densify point-cloud (DensifyPointCloud)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            12,
            roles,
        ).result()

        # 13. Reconstruct the mesh (ReconstructMesh)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            13,
            roles,
        ).result()

        # 14. Refine the mesh (RefineMesh)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            14,
            roles,
        ).result()

        # 15. Texture the mesh (TextureMesh)
        run_step.submit(
            picture_obj_key,
            politic_energy_name,
            politic_quality_name,
            host,
            15,
            roles,
        ).result()

        # 16. Estimate disparity-maps (DensifyPointCloud)
        # run_step(picture_obj_key, 16, roles)
        # 17. Fuse disparity-maps (DensifyPointCloud)
        # run_step(picture_obj_key, 17, roles)

    # provider.destroy()


def start_photogrammetry_flow_with_tags(
    job_id: str,
    picture_obj_key,
    politic_energy_name: str = EnergyPolicy.GREEN.value,
    politic_quality_name: str = QualityPolicy.GOOD.value,
):
    with tags(politic_energy_name, politic_quality_name):
        photogrammetry_flow(
            job_id, picture_obj_key, politic_energy_name, politic_quality_name
        )
