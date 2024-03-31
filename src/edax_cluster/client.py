from typing import Optional
from reversi import EdaxLine
from rte import BatchClient
from .task import EdaxTask


class EdaxBatchClient:
    def __init__(self, server, refresh_time) -> None:
        self.client = BatchClient(server, refresh_time)

    def solve(self, tasks: list[EdaxTask]) -> list[Optional[EdaxLine]]:
        task_bytes = [bytes(task) for task in tasks]
        results = self.client.solve(task_bytes)
        return [EdaxLine.from_bytes(r) if r is not None else None for r in results]
