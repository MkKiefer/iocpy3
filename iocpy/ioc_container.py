"""IOC Container module."""

from typing import Any, Callable, Generator, Type, TypeVar, ContextManager
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider
from iocpy.interfaces.ioc_context import IIocContext
from iocpy.ioc_context import IocContext
from iocpy.ioc_registry import IocRegistry


T = TypeVar("T")


class IocContainer:
    def __init__(self):
        self._registry = IocRegistry()
        self._root_context = IocContext(self._registry)

    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        self._registry.register_singleton(type_, instance)

    def register_instance(self, type_: type, instance: object) -> None:
        self._registry.register_singleton(type_, instance)

    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        self._registry.register_transient(type_, instance)

    def register_scoped(self, type_: type,
                        instance: Callable[[IInstanceProvider], object] |
                        Callable[[IInstanceProvider], Callable[[IInstanceProvider], Generator[Any, None, None]]] |
                        Callable[[IInstanceProvider],
                                 Generator[Any, None, None]]
                        ) -> None:
        self._registry.register_scoped(type_, instance)

    def get(self, type_: Type[T]) -> T:
        return self._root_context.get(type_)

    def create_scope(self) -> ContextManager[IIocContext]:
        return self._root_context.create_scope()

    def __call__(self) -> Generator[IIocContext, None, None]:
        """Callable generator scope, can be used with FastAPI dependency injection
        Example:
        ```PYTHON

        IOC = IocContainer()

        app.get("/items/{item_id}")
        async def read_item(item_id: int, scope: IIocContext = Depends(IOC)):
            item = scope.get(ItemService).get_item(item_id)
            return item
        ```
        """
        with self.create_scope() as context:
            yield context
