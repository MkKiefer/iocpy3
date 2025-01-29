"""This module implements the IIocRegistry interface."""
from typing import Any, Callable, Generator
from iocpy.behaviors.scoped import IocScoped
from iocpy.behaviors.singleton import IocSingleton
from iocpy.behaviors.transient import IocTransient
from iocpy.interfaces.behavior_registry import IBehaviorRegistry
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


class IocRegistry(IBehaviorRegistry):
    """
    The ioc registry contains all behavior like 
    singleton, transient, and scoped instances.
    The registry in mainly used by the `IocContext` to resolve instances.

    The class might change and is not a public API.
    Use the `IocContainer` to register instances that wraps this registry.

    Args:
        IBehaviorRegistry (_type_): 
        The behavior registry is used to register different types of behaviors
    """

    def __init__(self):
        self._registry: dict[type, IInstanceBehavior] = {}

    def register(self, type_: type, instance: IInstanceBehavior) -> None:
        """Register a custom instance behavior implementing `IInstanceBehavior`.

        Args:
            type_ (type): The type that should resolve to the instance
            instance (IInstanceBehavior): The instance behavior

        Raises:
            ValueError: The type is already registered.
        """
        if type_ in self._registry:
            raise ValueError(f"Type {type_} already registered")
        self._registry[type_] = instance

    def get_behavior(self, type_: type) -> IInstanceBehavior:
        """Get the instance behavior for a type.

        Args:
            type_ (type): The type to get the behavior for.

        Raises:
            ValueError: The type is not registered.

        Returns:
            IInstanceBehavior: The instance behavior for the type.
        """
        if type_ not in self._registry:
            raise ValueError(f"Type {type_} not registered")
        return self._registry[type_]

    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        """Register a singleton instance in the container.

        Example:
        ```PYTHON
        container = IOCContainer()
        container.register_singleton(MyInterface, MyImplementation())
        container.register_singleton(MyInterfaceWrapper, 
            lambda provider: MyWrapper(provider.get(MyInterface))
        )

        my_instance = container.get(MyInterface)
        my_instance_wrapper = container.get(MyInterfaceWrapper)

        ```
        :param type_: The type (this can be a interface or a class)
        :type type_: type
        :param instance: The instance or a callable that returns the instance
        :type instance: object | Callable[[IInstanceProvider], object]
        """
        singleton = IocSingleton(type_, instance)
        self.register(type_, singleton)

    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        """Register a transient instance in the container.
        This will create a new instance every time `get` is called.

        Example:
        ```PYTHON
        container = IOCContainer()
        container.register_transient(MyInterface, lambda provider: MyImplementation())

        my_instance = container.get(MyInterface)

        :param type_: _description_
        :type type_: type
        :param instance: _description_
        :type instance: Callable[[IInstanceProvider], object]
        """
        transient = IocTransient(type_, instance)
        self.register(type_, transient)

    def register_scoped(self, type_: type, instance:
                        Callable[[IInstanceProvider], object] |
                        Callable[[IInstanceProvider],
                                 Callable[[IInstanceProvider], Generator[Any, None, None]]] |
                        Callable[[IInstanceProvider],
                                 Generator[Any, None, None]]
                        ) -> None:
        """Register a scoped instance in the container.
        This will create only one instance per scope.

        Errors will be raised if the instance is resolved outside of a scope.

        Example:
        ```PYTHON
        container = IOCContainer()
        container.register_scoped(MyInterface, lambda provider: MyImplementation())

        my_instance = container.get(MyInterface)

        ```
        show in to the `README.md` file for more complex examples with sessions and generators.

        :param type_: _description_
        :type type_: type
        :param instance: _description_
        :type instance: Callable[[IocContext], object]
        """
        scoped = IocScoped(type_, instance)
        self.register(type_, scoped)
