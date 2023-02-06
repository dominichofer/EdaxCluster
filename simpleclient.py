import socket
import datetime
import selectors
from typing import Iterable


class TaskDispatchServer:

    def __init__(self) -> None:
        self._conn = selectors.DefaultSelector()
        self.task_queue: list(str) = []
        self.origin: list(TaskDispatchProtocol) = []

    def log(self, text: str) -> None:
        now = datetime.datetime.now()
        Q = len(self.task_queue)
        print(f'[{now}] [{Q}] {text}')

    def service_client(self, tdp: TaskDispatchProtocol):
        try:
            msg = tdp.receive()
            self.log(f'Received {msg.type.name}.')
            if msg.type == TaskDispatchProtocol.Message.Type.dispatch:
                if isinstance(msg.content, Iterable):
                    self.task_queue.extend(msg.content)
                    self.dispatcher.extend(tdp for _ in msg.content)
                else:
                    self.task_queue.append(msg.content)
                    self.dispatcher.append(tdp)
            elif msg.type == TaskDispatchProtocol.Message.Type.request:
                if self.task_queue:
                    task = self.task_queue.pop(0)
                    origin = self.origin.pop(0)
                    tdp.session.data = (task, origin)
                    tdp.respond(task)
                    self.log('Sent task.')
                else:
                    tdp.deny()
                    self.log('Sent no task.')
            elif msg.type == TaskDispatchProtocol.Message.Type.report:
                task, origin = tdp.session.data
                tdp.session.data = None
                origin.report(msg.content)
                self.log('Forwarded task.')
            elif msg.type == TaskDispatchProtocol.Message.Type.report_fail:
                task, origin = tdp.session.data
                self.task_queue.insert(0, msg.content)
                self.dispatcher.insert(0, tdp)
                self.log('Re-enlisted task.')
        except:
            task, origin = tdp.session.data
            self.task_queue.insert(0, msg.content)
            self.dispatcher.insert(0, tdp)
            self._conn.unregister(tdp.session.sock)
            self.log('Connection lost.')
        
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
                    tdp = TaskDispatchProtocol(HeaderPresentation, StatefulSession(HeaderSizeTransport), conn)
                    self._conn.register(conn, selectors.EVENT_READ, tdp)
                else:
                    self.service_client(key.data)
