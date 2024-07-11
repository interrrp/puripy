from puripy.handler import HttpConnectionHandler
from puripy.http import HttpRequest, HttpResponse
from puripy.listener import TcpConnectionListener
from puripy.logger import ConsoleLogger
from puripy.router import Router
from puripy.server import Server

logger = ConsoleLogger()
listener = TcpConnectionListener(logger, "127.0.0.1", 8080)
router = Router()
handler = HttpConnectionHandler(logger, router)
server = Server(logger, listener, handler)


@router.route("/")
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(200, "OK", {}, "Hello, index!")


if __name__ == "__main__":
    server.start()
