from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from socket import socket
from typing import override


class Connection(ABC):
    @property
    @abstractmethod
    def address(self) -> str: ...

    @abstractmethod
    def read(self) -> str: ...

    @abstractmethod
    def write(self, data: str) -> None: ...

    @abstractmethod
    def close(self) -> None: ...


@dataclass
class TcpConnection(Connection):
    socket: socket
    address_tuple: tuple[str, int]

    _read_buffer: str = field(init=False)

    @property
    @override
    def address(self) -> str:
        return f"{self.address_tuple[0]}:{self.address_tuple[1]}"

    @override
    def read(self) -> str:
        return self.socket.recv(1024).decode()

    @override
    def write(self, data: str) -> None:
        self.socket.sendall(data.encode())

    @override
    def close(self) -> None:
        self.socket.close()
