"""IOC Container module."""

from typing import Callable, Type, TypeVar

from iocpy.ioc_provider import InstanceRegistry
from iocpy.behaviors.singelton import IocSingleton
from iocpy.behaviors.transient import IocTransient
from iocpy.interfaces.instance_provider import IInstanceProvider


T = TypeVar("T")


class IOCContainer():
    """The ioc container is the main point to register and resolve instances.
    """

    def __init__(self):
        # ? The registry may need a copy options for scoped operations ?
        self._provider = InstanceRegistry()

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
        self._provider.set(type_, singleton)

    def register_instance(self, type_: type, instance: object) -> None:
        """
        Register a instance in the container.
        This is the same as calling register_singleton but with a simplified signature.

        :param type_: The type (this can be a interface or a class)
        :type type_: type
        :param instance: The instance to register
        :type instance: object
        """
        self.register_singleton(type_, instance)

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
        self._provider.set(type_, transient)

    def get(self, type_: Type[T]) -> T:
        """Get a registered instance from the container.

        :param type_: The registered type
        :type type_: Type[T]
        :return: _description_
        :rtype: T
        """
        return self._provider.get(type_)
