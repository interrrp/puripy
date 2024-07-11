from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override


class Logger(ABC):
    @abstractmethod
    def info(self, message: str) -> None: ...


@dataclass(frozen=True)
class ConsoleLogger(Logger):
    @override
    def info(self, message: str) -> None:
        print(f"info: {message}")
