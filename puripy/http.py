from dataclasses import dataclass
from enum import StrEnum


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCh"
    DELETE = "DELETE"


@dataclass(frozen=True)
class HttpRequest:
    method: HttpMethod
    path: str
    headers: dict[str, str]
    body: str
    version: str

    @classmethod
    def from_request(cls, request: str) -> "HttpRequest":
        lines = request.splitlines()
        method, path, version = lines[0].split(" ")

        headers: dict[str, str] = {}
        body = ""
        for line in lines[1:]:
            if line.strip():
                key, value = line.split(": ", 1)
                headers[key] = value
            else:
                # Empty line indicates end of headers
                body = "\n".join(lines[lines.index(line) + 1 :])
                break

        http_method = HttpMethod(method.upper())

        return cls(
            version=version, method=http_method, path=path, headers=headers, body=body
        )


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    status_text: str
    headers: dict[str, str]
    body: str
    version: str = "1.1"

    def to_http(self) -> str:
        status_line = f"HTTP/{self.version} {self.status_code} {self.status_text}\r\n"
        header_lines = [f"{key}: {value}\r\n" for key, value in self.headers.items()]
        headers = "".join(header_lines)
        response = f"{status_line}{headers}\r\n{self.body}"
        return response
