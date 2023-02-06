from .abstract_protocols import *
from enum import Enum


class HeaderSizeTransport(TransportProtocol):

    def __init__(self, sock) -> None:
        self.sock = sock

    def send(self, data: bytes) -> None:
        header = len(data).to_bytes(4, 'big')
        self.sock.sendall(header + data)

    def receive(self) -> bytes:
        chunk = self.sock.recv(2048)

        header = chunk[0:4]
        body_size = int.from_bytes(header, 'big')

        body = bytearray(chunk[4:])
        while len(body) < body_size:
            chunk = self.sock.recv(min(body_size - len(body), 2048))
            if chunk == b'':
                raise RuntimeError('Sock connection broken')
            body.append(chunk)
        return body

    
class StatefulSession(SessionProtocol):

    def __init__(self, transport_protocol: TransportProtocol) -> None:
        self.transport_protocol = transport_protocol
        self.data = None

    def start(self, sock: socket.socket) -> None:
        self.sock = sock
        self.transport = self.transport_protocol(self.sock)

    def end(self) -> None:
        self.sock.close()

    def send(self, data: bytes) -> None:
        self.transport.send(data)

    def receive(self) -> bytes:
        return self.transport.receive()
    
    
class HeaderPresentation(PresentationProtocol):

    @staticmethod
    def encode(msg) -> bytes:
        if msg is None:
            return b'\x00'
        if isinstance(msg, bytes):
            return b'\x01' + msg
        if isinstance(msg, int):
            return b'\x02' + msg.to_bytes(8, 'big')
        if isinstance(msg, str):
            return b'\x03' + msg.encode('utf8')
        if isinstance(msg, list):
            data = bytearray(b'\x04')
            data += HeaderPresentation.encode(len(msg))
            for element in msg:
                encoded_element = HeaderPresentation.encode(element)
                data += HeaderPresentation.encode(len(encoded_element))
                data += encoded_element
            return data
        if isinstance(msg, tuple):
            data = bytearray(b'\x05')
            data += HeaderPresentation.encode(len(msg))
            for element in msg:
                encoded_element = HeaderPresentation.encode(element)
                data += HeaderPresentation.encode(len(encoded_element))
                data += encoded_element
            return data
        raise RuntimeError('Unknown message type')

    @staticmethod
    def decode(data: bytes):
        if data.startswith(b'\x00'): # None
            return None
        if data.startswith(b'\x01'): # bytes
            return data[1:]
        if data.startswith(b'\x02'): # int
            return int.from_bytes(data[1:], 'big')
        if data.startswith(b'\x03'): # str
            return data[1:].decode('utf8')
        if data.startswith(b'\x04'): # list
            data = data[1:]
            lst = list()
            length = HeaderPresentation.decode(data[:9])
            data = data[9:]
            for _ in range(length):
                element_length = HeaderPresentation.decode(data[:9])
                data = data[9:]
                element = HeaderPresentation.decode(data[:element_length])
                data = data[element_length:]
                lst.append(element)
            return lst
        if data.startswith(b'\x05'): # tuple
            data = data[1:]
            tpl = tuple()
            length = HeaderPresentation.decode(data[:9])
            data = data[9:]
            for _ in range(length):
                element_length = HeaderPresentation.decode(data[:9])
                data = data[9:]
                element = HeaderPresentation.decode(data[:element_length])
                data = data[element_length:]
                tpl += (element, )
            return tpl

        raise RuntimeError('Unknown message type')
    

class Message:

    class Type(Enum):
        dispatch = 0
        request = 1
        respond = 2
        deny = 3
        report = 4
        report_fail = 5

    def __init__(self, type: Type, content = None) -> None:
        self.type = type
        self.content = content


class TaskDispatchProtocol:

    def __init__(self, presentation: PresentationProtocol, session: SessionProtocol, conn: socket.socket) -> None:
        self.presentation = presentation
        self.session = session
        self.session.start(conn)

    def __send(self, msg_type: Message.Type, msg = None):
        self.session.send(self.presentation.encode([msg_type, msg]))

    def receive(self) -> Message:
        data = self.session.receive()
        msg = self.presentation.decode(data)
        return Message(*msg)

    def dispatch(self, task) -> None:
        self.__send(Message.Type.dispatch, task)

    def request(self) -> None:
        self.__send(Message.Type.request)

    def respond(self, task) -> None:
        self.__send(Message.Type.respont, task)

    def deny(self) -> None:
        self.__send(Message.Type.deny)

    def report(self, task) -> None:
        self.__send(Message.Type.report, task)

    def report_fail(self) -> None:
        self.__send(Message.Type.report_fail)
