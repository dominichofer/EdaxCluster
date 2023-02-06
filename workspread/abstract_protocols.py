import socket


class TransportProtocol:

    def send(self, data: bytes) -> None:
        pass
    
    def receive(self) -> bytes:
        pass


class SessionProtocol:

    def __init__(self) -> None:
        self.sock = None

    def start(self, sock: socket.socket) -> None:
        pass

    def end(self) -> None:
        pass

    def send(self, data: bytes) -> None:
        pass

    def receive(self) -> bytes:
        pass


class PresentationProtocol:

    @staticmethod
    def encode(msg) -> bytes:
        pass

    @staticmethod
    def decode(data: bytes):
        pass
