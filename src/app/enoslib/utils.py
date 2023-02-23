import time

from enoslib.infra.enos_g5k.error import EnosG5kWalltimeFormatError

from enoslib import g5k_api_utils


async def is_there_one_node_available(start: float = time.time()):
    """This function check if there is one
    node available for the next 2 hours"""

    # TODO: encode this value as an env variable
    walltime = "02:00:00"
    _t = walltime.split(":")
    if len(_t) != 3:
        raise EnosG5kWalltimeFormatError()
    _walltime = int(_t[0]) * 3600 + int(_t[1]) * 60 + int(_t[2])
    try:
        cluster_status = g5k_api_utils.get_clusters_status(["ecotype"])
        nodes = cluster_status["ecotype"].nodes
        available_nodes = [
            node_id
            for node_id, node in nodes.items()
            if node["comment"] == "OK"
        ]
        for node_id in available_nodes:
            if g5k_api_utils.can_start_on_cluster(
                nodes,
                1,
                [node_id],
                start,
                _walltime,
            ):
                return True
    except Exception:
        print("Could not contact g5k api")
    return False
