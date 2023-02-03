from contextlib import _RedirectStream
from logging import Logger
from typing import IO, Optional

from prefect import get_run_logger


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
        self.logger = logger if logger else get_run_logger()
        self.logger_writer = LoggerWriter(self.logger.info)
        super().__init__(self.logger_writer)

    _stream = "stdout"
