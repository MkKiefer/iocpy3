"""IOC Context interface module.
The context interface is the public facing interface to the IOC container.
"""

from abc import ABC, abstractmethod
from contextlib import ExitStack
from typing import Generator, Type, TypeVar, ContextManager


T = TypeVar("T")


class IIocContext(ABC):
    """
    The context interface is the public facing 
    interface to the IOC container.
    """

    @abstractmethod
    def get_root(self) -> 'IIocContext':
        """Get the root context.
        The root context contains all singleton instances.

        Returns:
            IIocContext: The root context.
        """

    @abstractmethod
    def create_scope(self) -> ContextManager['IIocContext']:
        """Create a scope using a context manager.
        The scope will be cleaned up after the context manager is done.
        """

    @abstractmethod
    def create_generator_scope(self) -> Generator['IIocContext', None, None]:
        """Create a new generator scope.
        This scope type can be used to integrate with other frameworks
        or in combination with the context manager decorator.
        """

    @abstractmethod
    def get(self, type_: Type[T]) -> T:
        """
        Resolve a instance from the registry.

        Args:
            type_ (Type[T]): The interface or class to resolve.

        Returns:
            T: The resolved instance.
        """

    @property
    @abstractmethod
    def stack(self) -> ExitStack | None:
        """Exit stack for scoped dependencies."""

    @property
    @abstractmethod
    def instances(self) -> dict[Type, object]:
        """Instance dictionary for the (scoped) context."""
