"""
This module contains the interface for the behavior registry.
The behavior registry is used to register different types of behaviors
like singleton, transient, etc.
This is used then used by the IIOContext to resolve instances.
"""

from abc import ABC, abstractmethod
from typing import Callable

from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


class IBehaviorRegistry(ABC):
    """
    The behavior registry is used to register different types of behaviors
    """

    @abstractmethod
    def get_behavior(self, type_: type) -> IInstanceBehavior:
        """Get the behavior for a type.
        The behavior is warping the registered callables and instances.
        """

    @abstractmethod
    def register_singleton(self, type_: type,
                           instance: object | Callable[[IInstanceProvider], object]) -> None:
        """
        Register a singleton instance.

        Args:
            type_ (type): The interface or class to register for.
            instance (object | Callable[[IInstanceProvider], object]): 
            The instance or callable to resolve the type for.
        """

    @abstractmethod
    def register_transient(self, type_: type,
                           instance: Callable[[IInstanceProvider], object]) -> None:
        """
        Register a transient.

        Args:
            type_ (type): The interface or class to register for. 
            instance (Callable[[IInstanceProvider], object]):
            The callable to resolve the type for.
        """

    @abstractmethod
    def register_scoped(self, type_: type, instance: Callable[[IInstanceProvider], object]) -> None:
        """
        Register a scoped instance.

        Args:
            type_ (type): The interface or class to register for.
            instance (Callable[[IInstanceProvider], object]):
            The callable to resolve the type for.
        """
