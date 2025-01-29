"""IOC Container module."""

from typing import Any, Callable, Generator, Type, TypeVar, ContextManager
from iocpy.interfaces.instance_provider import IInstanceProvider
from iocpy.interfaces.ioc_context import IIocContext
from iocpy.ioc_context import IocContext
from iocpy.ioc_registry import IocRegistry


T = TypeVar("T")


class IocContainer:
    """
    The IOC container is the main entry point for the IOC container.
    This container contains the root context and the behavior registry.

    This is the main public facing API for the IOC container.

    """

    def __init__(self):
        self._registry = IocRegistry()
        self._root_context = IocContext(self._registry)

    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        """Register a singleton instance in the container.

        The singleton will resolve to the same instance every time it is resolved.

        Example:
        ```PYTHON

        container = IOCContainer()
        container.register_instance(MyInterface, MyImplementation())

        my_instance1 = container.get(MyInterface)
        my_instance2 = container.get(MyInterface)

        assert my_instance1 == my_instance2
        ```

        Args:
            type_ (type): The interface or type that should resolve to the instance
            instance (object | Callable[[IInstanceProvider], object]):
            The instance or a callable that returns the instance
        """
        self._registry.register_singleton(type_, instance)

    def register_instance(self, type_: type, instance: object) -> None:
        """Simple interface to register a singleton instance.

        The singleton will resolve to the same instance every time it is resolved.

        Example:
        ```PYTHON

        container = IOCContainer()
        container.register_instance(MyInterface, MyImplementation())

        my_instance1 = container.get(MyInterface)
        my_instance2 = container.get(MyInterface)

        assert my_instance1 == my_instance2
        ```

        Args:
            type_ (type): The interface or type that should resolve to the instance
            instance (object): The instance to register
        """
        self._registry.register_singleton(type_, instance)

    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        """ Register a transient instance in the container.

        The transient will created a new instance every time it is resolved.

        Example:
        ```PYTHON

        container = IOCContainer()
        container.register_transient(MyInterface, lambda provider: MyImplementation())

        my_instance = container.get(MyInterface)
        my_instance2 = container.get(MyInterface)

        assert my_instance != my_instance2
        ```


        Args:
            type_ (type): The interface or type that should resolve to the instance
            instance (Callable[[IInstanceProvider], object]):
            The callable that returns the instance
        """
        self._registry.register_transient(type_, instance)

    def register_scoped(self, type_: type,
                        instance: Callable[[IInstanceProvider], object] |
                        Callable[[IInstanceProvider],
                                 Callable[[IInstanceProvider], Generator[Any, None, None]]] |
                        Callable[[IInstanceProvider],
                                 Generator[Any, None, None]]
                        ) -> None:
        """
        Register a scoped instance in the container.

        The scoped instance will be created once per scope.
        This means inside the open scope the type will always resolve to the same
        instance.
        example:
        ```PYTHON	

        container = IOCContainer()
        container.register_scoped(MyInterface, lambda provider: MyImplementation())
        container.register_scoped(MyInterfaceWrapper, 
            lambda provider: MyWrapper(provider.get(MyInterface))
        )
        with container.create_scope() as scope:
            my_instance = scope.get(MyInterface)
        ```

        Args:
            type_ (type): The interface or type that should resolve to the instance
            instance (
            Callable[[IInstanceProvider], object] |
            Callable[[IInstanceProvider], Callable[[IInstanceProvider], 
            Generator[Any, None, None]]] |
              Callable[[IInstanceProvider], Generator[Any, None, None]]
              ): The callable that returns the instance
        """
        self._registry.register_scoped(type_, instance)

    def get(self, type_: Type[T]) -> T:
        """Resolve the instance for the given type.

        Args:
            type_ (Type[T]): The interface or class to resolve.

        Returns:
            T: The resolved instance `T` for the given type.
        """
        return self._root_context.get(type_)

    def create_scope(self) -> ContextManager[IIocContext]:
        """Create a new scope using a context manager.

        Returns:
            ContextManager[IIocContext]: The contextmanager
        """
        return self._root_context.create_scope()

    def __call__(self) -> Generator[IIocContext, None, None]:
        # ? We need to call it this way that the function signature is a callable generator
        # pylint: disable=not-context-manager
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
