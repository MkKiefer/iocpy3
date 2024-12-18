from abc import ABC, abstractmethod
from typing import Callable

from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


class IBehaviorRegistry(ABC):

    @abstractmethod
    def get_behavior(self, type_: type) -> IInstanceBehavior:
        ...

    @abstractmethod
    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        ...

    @abstractmethod
    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        ...

    def register_scoped(self, type_: type, instance: Callable[[IInstanceProvider], object]) -> None:
        ...
