from contextlib import _RedirectStream
from logging import Logger
from typing import IO, Any, Dict, Optional

from prefect import get_run_logger
from prefect.context import TaskRunContext
from prefect.utilities.hashing import hash_objects


class LoggerWriter(IO[str]):
    """This class is used to redirect stdout and stderr to the logger."""

    def __init__(self, logfct):
        self.logfct = logfct
        self.buf = []

    def write(self, msg: str) -> None:
        if msg.endswith("\n"):
            self.buf.append(msg.removesuffix("\n"))
            self.logfct("".join(self.buf))
            self.buf = []
        else:
            self.buf.append(msg)

    def flush(self) -> None:
        if self.buf:
            self.logfct("".join(self.buf))
            self.buf = []

    def close(self) -> None:
        self.flush()


class with_redirect_stdout_to_run_logger(_RedirectStream):
    """Context manager for temporarily redirecting stdout to orion's logger."""

    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or get_run_logger()
        self.logger_writer = LoggerWriter(self.logger.info)
        super().__init__(self.logger_writer)

    _stream = "stdout"


def task_input_hash_no_roles_node(
    context: "TaskRunContext", arguments: Dict[str, Any]
) -> Optional[str]:
    """
    A task cache key implementation which hashes all inputs
    to the task using a JSON or
    cloudpickle serializer. If any arguments are not JSON
    serializable, the pickle
    serializer is used as a fallback. If cloudpickle fails,
    this will return a null key
    indicating that a cache key could not be generated for the given inputs.

    Arguments:
        context: the active `TaskRunContext`
        arguments: a dictionary of arguments to be passed to
        the underlying task

    Returns:
        a string hash if hashing succeeded, else `None`
    """
    return hash_objects(
        # We use the task key to get the qualified name for the task and
        # include the task functions `co_code` bytes to avoid caching
        # when the underlying function changes
        context.task.task_key,
        # NOTE: don´t take into account the source code
        # of the function, we don't mind it.
        # context.task.fn.__code__.co_code.hex(),
        without_keys(arguments, ["roles", "node_id"]),
    )


def without_keys(d: Dict, keys: list[str]):
    return {k: d[k] for k in d.keys() - keys}


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
