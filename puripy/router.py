from dataclasses import dataclass, field
from typing import Callable

from puripy.http import HttpRequest, HttpResponse

type RouteHandler = Callable[[HttpRequest], HttpResponse]


@dataclass
class Router:
    handlers: dict[str, RouteHandler] = field(default_factory=dict)

    def handle(self, request: HttpRequest) -> HttpResponse:
        handler = self.handlers.get(request.path)

        if handler is None:
            return HttpResponse(404, "Not Found", {}, "")

        response = handler(request)

        # Set default headers by merging dicts
        response.headers = {
            "Content-Type": "text/plain",
            "Content-Length": str(len(response.body)),
        } | response.headers

        return response

    def route(self, path: str) -> Callable[[RouteHandler], RouteHandler]:
        def decorator(handler: RouteHandler) -> RouteHandler:
            def wrapper(request: HttpRequest) -> HttpResponse:
                return handler(request)

            self.handlers[path] = wrapper
            return wrapper

        return decorator
