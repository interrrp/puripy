from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from socket import socket
from typing import override

from puripy.connection import Connection, TcpConnection
from puripy.logger import Logger


class ConnectionListener(ABC):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def accept(self) -> Connection: ...


@dataclass
class TcpConnectionListener(ConnectionListener):
    logger: Logger
    host: str
    port: int

    _socket: socket = field(init=False)

    def __post_init__(self) -> None:
        self._socket = socket()
        self._socket.bind((self.host, self.port))

    @override
    def start(self) -> None:
        self.logger.info(f"Listening on {self.host}:{self.port}")

        self._socket.listen()
        self._socket.settimeout(1)

    @override
    def stop(self) -> None:
        self._socket.close()

    @override
    def accept(self) -> Connection:
        # The purpose of the short timeout is to allow events like
        # KeyboardInterrupt to propagate. Since this really isn't a timeout for
        # our purposes, we will ignore timeout errors.

        try:
            connection_pair = self._socket.accept()
        except TimeoutError:
            return self.accept()

        client_socket = connection_pair[0]
        address: tuple[str, int] = connection_pair[1]

        return TcpConnection(client_socket, address)
