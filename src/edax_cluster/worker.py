from rte import Worker
from reversi import Edax
from .task import EdaxTask


class EdaxWorker(Worker):
    def __init__(self, server, refresh_time, exe_path):
        super().__init__(server, refresh_time)
        self.exe_path = exe_path

    def execute_task(self, task: bytes) -> bytes:
        edax_task = EdaxTask.from_bytes(task)
        result = Edax(self.exe_path, level=edax_task.level).solve_native(edax_task.pos)
        return str(result).encode()

    def on_cancel(self) -> None:
        pass
