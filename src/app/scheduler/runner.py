from prefect.task_runners import BaseTaskRunner
from typing import Any, Awaitable, Callable, Dict, Optional

from prefect.utilities.collections import AutoEnum

if TYPE_CHECKING:
    from anyio.abc import TaskGroup

from prefect.futures import PrefectFuture
from prefect.orion.schemas.core import TaskRun
from prefect.orion.schemas.states import State
from prefect.states import exception_to_crashed_state
from prefect.utilities.asyncutils import A
from prefect.utilities.collections import AutoEnum

R = TypeVar("R")


class TaskConcurrencyType(AutoEnum):
    SEQUENTIAL = AutoEnum.auto()
    CONCURRENT = AutoEnum.auto()
    PARALLEL = AutoEnum.auto()


class SequentialDirectoryBackupTaskRunner(BaseTaskRunner):
    """
    A simple task runner that executes calls as they are submitted.
    If writing synchronous tasks, this runner will always execute tasks sequentially.
    If writing async tasks, this runner will execute tasks sequentially unless grouped
    using `anyio.create_task_group` or `asyncio.gather`.
    """

    def __init__(self) -> None:
        super().__init__()
        self._results: Dict[str, State] = {}

    @property
    def concurrency_type(self) -> TaskConcurrencyType:
        return TaskConcurrencyType.SEQUENTIAL

    async def submit(
        self,
        task_run: TaskRun,
        run_key: str,
        run_fn: Callable[..., Awaitable[State[R]]],
        run_kwargs: Dict[str, Any],
        asynchronous: A = True,
    ) -> PrefectFuture[R, A]:
        # Run the function immediately and store the result in memory
        try:
            result = await run_fn(**run_kwargs)
        except BaseException as exc:
            result = exception_to_crashed_state(exc)

        self._results[run_key] = result

        return PrefectFuture(
            task_run=task_run,
            run_key=run_key,
            task_runner=self,
            asynchronous=asynchronous,
        )

    async def wait(
        self, prefect_future: PrefectFuture, timeout: float = None
    ) -> Optional[State]:
        return self._results[prefect_future.run_key]
