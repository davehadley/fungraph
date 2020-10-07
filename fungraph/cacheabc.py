from abc import ABC, abstractmethod
from typing import Any, Container


class Cache(Container, ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        pass
