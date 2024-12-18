"""IOC Container module."""

from typing import Any, Callable, Generator, Type, TypeVar, ContextManager
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider
from iocpy.ioc_context import IocContext
from iocpy.ioc_registry import IocRegistry


T = TypeVar("T")


class IocContainer:
    def __init__(self):
        self._registry = IocRegistry()
        self._root_context = IocContext(self._registry)

    def register(self, type_: type, instance: IInstanceBehavior) -> None:
        self._registry.register(type_, instance)

    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        self._registry.register_singleton(type_, instance)

    def register_instance(self, type_: type, instance: object) -> None:
        self._registry.register_singleton(type_, instance)

    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        self._registry.register_transient(type_, instance)

    def register_scoped(self, type_: type,
                        instance: Callable[[IocContext], object] | Callable[[IocContext], Generator[Any, None, None]]) -> None:
        self._registry.register_scoped(type_, instance)

    def get(self, type_: Type[T]) -> T:
        return self._root_context.get(type_)

    def create_scope(self) -> ContextManager[IocContext]:
        return self._root_context.create_scope()
