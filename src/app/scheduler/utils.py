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
