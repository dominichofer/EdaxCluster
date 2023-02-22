from abc import ABC, abstractmethod
from typing import Any


class PresentationProtocol(ABC):

    @abstractmethod
    def encode(self, msg) -> bytes:
        pass

    @abstractmethod
    def decode(self, data: bytes) -> Any:
        pass


class SessionProtocol(ABC):

    @abstractmethod
    def end(self) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        pass

    @abstractmethod
    def receive(self) -> bytes:
        pass
    

class TransportProtocol(ABC):
    
    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        pass
    
    @abstractmethod
    def receive(self) -> bytes:
        pass


class ConnectProtocol(ABC):
    
    @abstractmethod
    def listen(self, port) -> None:
        pass
    
    @abstractmethod
    def connect(self, ip, port) -> None:
        pass
    
    @abstractmethod
    def accept(self) -> TransportProtocol:
        pass
