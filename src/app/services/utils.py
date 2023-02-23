def extract_from_task_name_infos(task_name: str) -> dict[str, str]:
    """Extract from task name infos
    p:/job_201904251000_0001/uploads|n:ecotype-42|s:3|j:job_201904251000_0001|n:0
    into a dict
    """
    keys = [(splat[:1], splat[2:]) for splat in task_name.split("|")]
    return dict(keys)


def map_node_uid_to_seduce_uid(node_uid: str) -> str:
    """Map node uid to seduce uid"""

    # TODO: remove this mapping when seduce will be updated
    # and use a file to map node uid to seduce uid
    mapping = {
        "ecotype-1": "ecotype-1_pdu-Z1.5",
        "ecotype-2": "ecotype-2_pdu-Z1.5",
        "ecotype-3": "ecotype-3_pdu-Z1.5",
        "ecotype-4": "ecotype-4_pdu-Z1.5",
        "ecotype-5": "ecotype-5_pdu-Z1.5",
        "ecotype-6": "ecotype-6_pdu-Z1.5",
        "ecotype-7": "ecotype-7_pdu-Z1.5",
        "ecotype-8": "ecotype-8_pdu-Z1.5",
        "ecotype-9": "ecotype-9_pdu-Z1.5",
        "ecotype-10": "ecotype-10_pdu-Z1.5",
        "ecotype-11": "ecotype-11_pdu-Z1.5",
        "ecotype-12": "ecotype-12_pdu-Z1.5",
        "ecotype-13": "ecotype-13_pdu-Z1.4",
        "ecotype-14": "ecotype-14_pdu-Z1.4",
        "ecotype-15": "ecotype-15_pdu-Z1.4",
        "ecotype-16": "ecotype-16_pdu-Z1.4",
        "ecotype-17": "ecotype-17_pdu-Z1.4",
        "ecotype-18": "ecotype-18_pdu-Z1.4",
        "ecotype-19": "ecotype-19_pdu-Z1.4",
        "ecotype-20": "ecotype-20_pdu-Z1.4",
        "ecotype-21": "ecotype-21_pdu-Z1.4",
        "ecotype-22": "ecotype-22_pdu-Z1.4",
        "ecotype-23": "ecotype-23_pdu-Z1.4",
        "ecotype-24": "ecotype-24_pdu-Z1.4",
        "ecotype-25": "ecotype-25_pdu-Z1.2",
        "ecotype-26": "ecotype-26_pdu-Z1.2",
        "ecotype-27": "ecotype-27_pdu-Z1.2",
        "ecotype-28": "ecotype-28_pdu-Z1.2",
        "ecotype-29": "ecotype-29_pdu-Z1.2",
        "ecotype-30": "ecotype-30_pdu-Z1.2",
        "ecotype-31": "ecotype-31_pdu-Z1.2",
        "ecotype-32": "ecotype-32_pdu-Z1.2",
        "ecotype-33": "ecotype-33_pdu-Z1.2",
        "ecotype-34": "ecotype-34_pdu-Z1.2",
        "ecotype-35": "ecotype-35_pdu-Z1.2",
        "ecotype-36": "ecotype-36_pdu-Z1.2",
        "ecotype-37": "ecotype-37_pdu-Z1.1",
        "ecotype-38": "ecotype-38_pdu-Z1.1",
        "ecotype-39": "ecotype-39_pdu-Z1.1",
        "ecotype-40": "ecotype-40_pdu-Z1.1",
        "ecotype-41": "ecotype-41_pdu-Z1.1",
        "ecotype-42": "ecotype-42_pdu-Z1.1",
        "ecotype-43": "ecotype-43_pdu-Z1.1",
        "ecotype-44": "ecotype-44_pdu-Z1.1",
        "ecotype-45": "ecotype-45_pdu-Z1.1",
        "ecotype-46": "ecotype-46_pdu-Z1.1",
        "ecotype-47": "ecotype-47_pdu-Z1.1",
        "ecotype-48": "ecotype-48_pdu-Z1.1",
    }
    return mapping.get(node_uid, node_uid)
