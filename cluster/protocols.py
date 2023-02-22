import socket
import struct
import errno
from enum import Enum
from .abstract_protocols import *
    

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

    def __init__(self, presentation: PresentationProtocol, session: SessionProtocol) -> None:
        self.presentation = presentation
        self.session = session

    def __send(self, msg_type: Message.Type, msg = None):
        self.session.send(self.presentation.encode([msg_type.value, msg]))

    def receive(self, blocking: bool) -> Message:
        data = self.session.receive(blocking)
        msg = self.presentation.decode(data)
        return Message(Message.Type(msg[0]), msg[1])

    def dispatch(self, task) -> None:
        self.__send(Message.Type.dispatch, task)

    def request(self) -> None:
        self.__send(Message.Type.request)

    def respond(self, task) -> None:
        self.__send(Message.Type.respond, task)

    def deny(self) -> None:
        self.__send(Message.Type.deny)

    def report(self, task) -> None:
        self.__send(Message.Type.report, task)

    def report_fail(self) -> None:
        self.__send(Message.Type.report_fail)
    

    
class PascalMethod(PresentationProtocol):
    """
    Uses 1 byte to denote the type of the message.
    Messages of arbitraty length start with an integer length field followed by the specified amount of bytes.
    """

    def __init__(self) -> None:
        self.__transcoders = [
            (type(None), self.__encode_None, self.__decode_None),
            (bytes, self.__encode_bytes, self.__decode_bytes),
            (bool, self.__encode_bool, self.__decode_bool),
            (int, self.__encode_int, self.__decode_int),
            (float, self.__encode_float, self.__decode_float),
            (str, self.__encode_str, self.__decode_str),
            (list, self.__encode_iterable, self.__decode_list),
            (tuple, self.__encode_iterable, self.__decode_tuple),
            ]
    
    def __encode_None(self, value) -> bytes:
        return b'\x00' # dummy byte
    
    def __decode_None(self, data: bytes):
        return None

    
    def __encode_bytes(self, value) -> bytes:
        return value
    
    def __decode_bytes(self, data: bytes):
        return data

    
    def __encode_bool(self, value) -> bytes:
        return struct.pack('!?', value)
    
    def __decode_bool(self, data: bytes):
        return struct.unpack('!?', data)[0]

    
    def __encode_int(self, value) -> bytes:
        return struct.pack('!q', value)
    
    def __decode_int(self, data: bytes):
        return struct.unpack('!q', data)[0]

    
    def __encode_float(self, value) -> bytes:
        return struct.pack('!d', value)
    
    def __decode_float(self, data: bytes):
        return struct.unpack('!d', data)[0]

    
    def __encode_str(self, value) -> bytes:
        return value.encode('utf8')
    
    def __decode_str(self, data: bytes):
        return data.decode('utf8')

    
    def __encode_iterable(self, value) -> bytes:
        data = bytearray()
        data += self.__encode_int(len(value))
        for element in value:
            encoded_element = self.encode(element)
            data += self.__encode_int(len(encoded_element))
            data += encoded_element
        return data
    
    def __decode_list(self, data: bytes):
        lst = list()
        length = self.__decode_int(data[:8])
        data = data[8:]
        for _ in range(length):
            element_length = self.__decode_int(data[:8])
            data = data[8:]

            element = self.decode(data[:element_length])
            data = data[element_length:]

            lst.append(element)
        return lst
    
    def __decode_tuple(self, data: bytes):
        return tuple(self.__decode_list(data))
    
    def encode(self, value) -> bytes:
        for index, (t_type, encoder, decoder) in enumerate(self.__transcoders):
            if isinstance(value, t_type):
                return struct.pack('!B', index) + encoder(value)
        raise RuntimeError(f'Failed to encode {value}')
    
    def decode(self, data: bytes):
        for index, (t_type, encoder, decoder) in enumerate(self.__transcoders):
            if data.startswith(struct.pack('!B', index)):
                return decoder(data[1:])
        raise RuntimeError(f'Failed to decode {data}')


    
class StatefulSession(SessionProtocol):

    def __init__(self, transporter) -> None:
        self.transporter = transporter
        #self.transporter.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        #self.transporter.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 0)
        #self.transporter.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, int(0.9 * timeout))
        #self.transporter.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 1)
        self.data = None

    def end(self) -> None:
        self.transporter.close()

    def send(self, data: bytes) -> None:
        self.transporter.send(data)

    def receive(self, blocking: bool) -> bytes:
        return self.transporter.receive(blocking)



class BrokenConnection(Exception):
    pass


class NoDataAvailable(Exception):
    pass


class Connector(ConnectProtocol):

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self, port) -> None:
        self.sock.bind(('', port))
        self.sock.listen()

    def connect(self, ip, port) -> TransportProtocol:
        self.sock.connect((ip, port))
        return MessageTransporter(self.sock)

    def accept(self) -> TransportProtocol:
        conn, addr = self.sock.accept()
        return MessageTransporter(conn)


class MessageTransporter(TransportProtocol):
    
    buffer_size = 2048

    def __init__(self, sock) -> None:
        self.sock = sock

    def close(self) -> None:
        self.sock.close()

    def send(self, data: bytes) -> None:
        header = struct.pack('!I', len(data))
        self.sock.sendall(header + data)

    def __try_receive(self, buffer_size) -> bytes:
        try:
            chunk = self.sock.recv(buffer_size)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                raise NoDataAvailable()
            else:
                raise BrokenConnection()

        if chunk:
            return chunk
        else:
            raise BrokenConnection()

    def receive(self, blocking: bool) -> bytes:
        self.sock.setblocking(blocking)

        header = self.__try_receive(4)
        body_size = struct.unpack('!I', header)[0]

        body = bytearray()
        while len(body) < body_size:
            buffer_size = min(body_size - len(body), self.buffer_size)
            body += self.__try_receive(buffer_size)
        return body
