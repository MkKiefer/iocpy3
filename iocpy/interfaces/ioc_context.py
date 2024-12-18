

from abc import ABC, abstractmethod
from contextlib import ExitStack
from typing import Generator, Type, TypeVar, ContextManager


T = TypeVar("T")


class IIocContext(ABC):

    @abstractmethod
    def get_root(self) -> 'IIocContext':
        ...

    @abstractmethod
    def create_scope(self) -> ContextManager['IIocContext']:
        ...

    @abstractmethod
    def create_generator_scope(self) -> Generator['IIocContext', None, None]:
        ...

    @abstractmethod
    def get(self, type_: Type[T]) -> T:
        ...

    @property
    @abstractmethod
    def stack(self) -> ExitStack | None:
        ...

    @property
    @abstractmethod
    def instances(self) -> dict[Type, object]:
        ...
