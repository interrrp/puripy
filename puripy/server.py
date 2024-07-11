from dataclasses import dataclass

from puripy.handler import ConnectionHandler
from puripy.listener import ConnectionListener
from puripy.logger import Logger


@dataclass(frozen=True)
class Server:
    logger: Logger
    connection_listener: ConnectionListener
    connection_handler: ConnectionHandler

    def start(self) -> None:
        self.connection_listener.start()

        while True:
            try:
                connection = self.connection_listener.accept()
            except KeyboardInterrupt:
                self.logger.info("Stopping")
                break

            self.connection_handler.handle(connection)

        self.connection_listener.close()
