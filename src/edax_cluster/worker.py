from rte import Worker
from reversi import Edax
from .task import EdaxTask


class EdaxWorker(Worker):
    def execute_task(self, task: bytes) -> bytes:
        edax_task = EdaxTask.from_bytes(task)
        result = Edax(tasks=1, level=edax_task.level).solve_native(edax_task.pos)
        return bytes(result[0])

    def on_cancel(self) -> None:
        pass
