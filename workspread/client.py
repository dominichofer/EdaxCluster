from typing import Iterable
from .protocols import *


class TaskDispatchClient:

    def __init__(self, ip) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, 12350))
        self.tdp = TaskDispatchProtocol(HeaderPresentation, StatefulSession(HeaderSizeTransport), sock)

    def request_task(self) -> str:
        try:
            self.tdp.request()
            msg = self.tdp.receive()
        except:
            return None
        
        if msg.type == TaskDispatchProtocol.Message.Type.respond:
            return msg.body
        elif msg.type == TaskDispatchProtocol.Message.Type.deny:
            return None

    def report_result(self, result: str) -> None:
        self.tdp.report(result)

    def report_fail(self) -> None:
        self.tdp.report_fail()

    def run(self, tasks) -> list:
        if not isinstance(tasks, Iterable):
            tasks = [tasks]

        tasks = [(i, t) for i, t in enumerate(tasks)]
        results = [None] * len(tasks)

        self.tdp.dispatch(tasks)

        while any(r is None for r in results):
            msg = self.tdp.receive()
            if msg.type == TaskDispatchProtocol.Message.Type.report:
                i, r = msg.content
                results[i] = r
            else:
                raise RuntimeError('Unexpected message type')

        return results
