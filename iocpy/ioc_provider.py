"""Instance registry"""
from typing import Type, TypeVar

from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


T = TypeVar("T")


class InstanceRegistry(IInstanceProvider):
    """Register and resolve the instance of the type"""

    def __init__(self) -> None:
        self._type_behaviors: dict[type, IInstanceBehavior] = {}

    def get(self, type_: Type[T]) -> T:
        """Get the instance of a type"""
        if type_ not in self._type_behaviors:
            raise ValueError(f"Type {type_} not registered")
        resolved_instance = self._type_behaviors[type_].resolve(self)
        if not issubclass(type(resolved_instance), type_):
            raise ValueError(f"The resolved instance is not of type {type_}")
        return resolved_instance

    def set(self, type_: Type[T], instance: IInstanceBehavior) -> None:
        """Set behavior for a type"""
        if type_ in self._type_behaviors:
            raise ValueError(f"Type {type_} already registered")

        if not isinstance(instance, IInstanceBehavior):
            raise ValueError(
                f"Instance must be an instance of {IInstanceBehavior} got {type(instance)}")
        self._type_behaviors[type_] = instance
