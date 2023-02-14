import socket
import datetime
import selectors
from typing import Iterable
from .protocols import *


class TaskDispatchServer:

    def __init__(self) -> None:
        self._conn = selectors.DefaultSelector()
        self.task_queue: list(str) = []
        self.origin: list(TaskDispatchProtocol) = []

    def log(self, text: str) -> None:
        now = datetime.datetime.now()
        Q = len(self.task_queue)
        print(f'[{now}] [Queue size: {Q}] {text}')

    def reenlist(self, task, origin) -> None:
        self.task_queue.insert(0, task)
        self.origin.insert(0, origin)
        self.log('Re-enlisted task.')

    def service_client(self, tdp: TaskDispatchProtocol) -> None:
        try:
            first = True
            while True:
                msg = tdp.receive(blocking=first)
                self.log(f'Received {msg.type.name}.')
                first = False

                if msg.type == Message.Type.dispatch:
                    if isinstance(msg.content, Iterable):
                        self.task_queue.extend(msg.content)
                        self.origin.extend([tdp] * len(msg.content))
                    else:
                        self.task_queue.append(msg.content)
                        self.origin.append(tdp)
                    self.log('Added tasks.')
                elif msg.type == Message.Type.request:
                    if self.task_queue:
                        task = self.task_queue.pop(0)
                        origin = self.origin.pop(0)
                        tdp.session.data = (task, origin)
                        tdp.respond(task)
                        self.log('Sent task.')
                    else:
                        tdp.deny()
                        self.log('Sent no task.')
                elif msg.type == Message.Type.report:
                    task, origin = tdp.session.data
                    tdp.session.data = None
                    origin.report(msg.content)
                    self.log('Forwarded result.')
                elif msg.type == Message.Type.report_fail:
                    self.reenlist(*tdp.session.data)
        except NoDataAvailable:
            pass
        except Exception as e:
            if tdp.session.data is not None:
                self.reenlist(*tdp.session.data)
            self._conn.unregister(tdp.session.sock)
            self.log(f'Connection lost. Error {e}')
        
    def run(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 12350))
        sock.listen()
        self._conn.register(sock, selectors.EVENT_READ, None)
        self.log('Server running...')

        while True:
            for key, _ in self._conn.select():
                sock = key.fileobj
                if key.data is None:
                    # accept
                    conn, addr = sock.accept()
                    conn.setblocking(False)
                    tdp = TaskDispatchProtocol(HeaderPresentation, StatefulSession(HeaderSizeTransport), conn)
                    self._conn.register(conn, selectors.EVENT_READ, tdp)
                else:
                    self.service_client(key.data)
