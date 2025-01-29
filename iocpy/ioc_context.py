"""
Module for the IocContext class implementing IIocContext and IInstanceProvider.
"""

from contextlib import ExitStack, contextmanager
import logging
from typing import Any, Generator, Type, TypeVar
from iocpy.interfaces.behavior_registry import IBehaviorRegistry
from iocpy.interfaces.instance_provider import IInstanceProvider
from iocpy.interfaces.ioc_context import IIocContext


T = TypeVar("T")


class IocContext(IInstanceProvider, IIocContext):
    """The IocContext is used for the implementation of scopes.
    Every scope represents a new context that can be used to resolve instances.

    The newly resolved instances will be stored in the context and will be 
    cleaned up when the context is closed.
    The parent argument is used to recursively get the root context.


    Args:
        IInstanceProvider (_type_): 
        Minimal interface to resolve instances with `.get(<type>)`
        IIocContext (_type_): 
        The context interface is the public facing interface to the IOC container.
    """

    def __init__(self, registry: IBehaviorRegistry,
                 parent: IIocContext | None = None, stack: ExitStack | None = None):
        self._registry = registry
        self._parent = parent
        self._stack: ExitStack | None = stack
        self._instances: dict[Type, object] = {}
        self._logger = logging.getLogger(__name__)

    def get_root(self) -> IIocContext:
        """Get the root context throng recursion

        Returns:
            IIocContext: The root context.
        """
        if self._parent is None:
            return self
        return self._parent.get_root()

    @contextmanager
    def create_scope(self) -> Generator[IIocContext, Any, None]:
        """Create a new scope with this scope as its parent.

        Returns:
            ContextManager[IIocContext]: 
            Context manager containing the new scope.
_
        """
        return self.create_generator_scope()

    def create_generator_scope(self) -> Generator[IIocContext, None, None]:
        """Create a new generator scope.

        Yields:
            Generator[IIocContext, None, None]: The generator scope.
        """
        with ExitStack() as stack:
            context = IocContext(self._registry, self, stack)
            try:
                yield context
            finally:
                self._logger.debug("Leaving scope, cleaning up")
        self._instances.clear()

    def get(self, type_: Type[T]) -> T:
        """Resolve a instance from the container.

        Args:
            type_ (Type[T]): The interface or class to resolve.

        Raises:
            ValueError: Invalid resolve type error.

        Returns:
            T: The resolved instance `T` for the given type.
        """
        self._logger.debug("Getting instance of %s", type_)
        behavior = self._registry.get_behavior(type_)
        instance = behavior.resolve(self)

        if not isinstance(instance, type_):
            raise ValueError(f"The resolved instance is not of type {type_}")
        return instance

    @property
    def stack(self) -> ExitStack | None:
        """The exit stack for the scoped dependencies.
        This stack is used to manage the lifecycle of the scoped dependencies.

        Returns:
            ExitStack | None: The exit stack for the scoped dependencies.
        """
        return self._stack

    @property
    def instances(self) -> dict[Type, object]:
        """Registered scoped instances for this scope

        Returns:
            dict[Type, object]: 
            Resolved and registered scoped instances.
        """
        return self._instances
