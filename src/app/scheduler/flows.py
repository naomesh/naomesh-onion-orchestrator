import logging
from contextlib import ExitStack

import enoslib as en
from prefect import flow, get_run_logger
from prefect.task_runners import SequentialTaskRunner

from app.scheduler.tasks import run_step, setup_node


@flow(
    name="Photogrammetry v0.0.1 flow",
    task_runner=SequentialTaskRunner(),
    log_prints=True,
)
def reserve(picture_obj_key: str = "hashhhhh"):
    """_summary_

    Args:
        picture_obj_key (str, optional): _description_. Defaults to "hash".
    """
    print(get_run_logger())
    en.init_logging(level=logging.INFO).getLogger()

    roles, provider = setup_node(picture_obj_key)
    # SEQUENTIAL: 0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15
    with ExitStack() as _:
        # 0. Intrinsics analysis (openMVG_main_SfMInit_ImageListing)
        run_step(picture_obj_key, 0, roles)

        # 1. Compute features (openMVG_main_ComputeFeatures)
        run_step(picture_obj_key, 1, roles)

        # 2. Compute pairs (openMVG_main_PairGenerator)
        run_step(picture_obj_key, 2, roles)

        # 3. Compute matches (openMVG_main_ComputeMatches)
        run_step(picture_obj_key, 3, roles)

        # 4. Filter matches (openMVG_main_GeometricFilter)
        run_step(picture_obj_key, 4, roles)

        # 5. Incremental reconstruction (openMVG_main_IncrementalSfM)
        run_step(picture_obj_key, 5, roles)

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
        run_step(picture_obj_key, 11, roles)

        # 12. Densify point-cloud (DensifyPointCloud)
        run_step(picture_obj_key, 12, roles)

        # 13. Reconstruct the mesh (ReconstructMesh)
        run_step(picture_obj_key, 13, roles)

        # 14. Refine the mesh (RefineMesh)
        run_step(picture_obj_key, 14, roles)

        # 15. Texture the mesh (TextureMesh)
        run_step(picture_obj_key, 15, roles)

        # 16. Estimate disparity-maps (DensifyPointCloud)
        # run_step(picture_obj_key, 16, roles)
        # 17. Fuse disparity-maps (DensifyPointCloud)
        # run_step(picture_obj_key, 17, roles)

    # provider.destroy()
