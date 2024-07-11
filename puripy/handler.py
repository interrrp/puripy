from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override

from puripy.connection import Connection
from puripy.http import HttpRequest
from puripy.logger import Logger
from puripy.router import Router


class ConnectionHandler(ABC):
    @abstractmethod
    def handle(self, connection: Connection) -> None: ...


@dataclass(frozen=True)
class HttpConnectionHandler(ConnectionHandler):
    logger: Logger
    router: Router

    @override
    def handle(self, connection: Connection) -> None:
        request = HttpRequest.from_request(connection.read())

        response = self.router.handle(request)
        connection.write(response.to_http())
        connection.close()

        self.logger.info(
            f"{request.method} {request.path} - {response.status_code} {response.status_text}"
        )
