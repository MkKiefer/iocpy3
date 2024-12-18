

from contextlib import ExitStack, contextmanager
import logging
from typing import Any, Generator, Type, TypeVar
from iocpy.interfaces.behavior_registry import IBehaviorRegistry
from iocpy.interfaces.instance_provider import IInstanceProvider
from iocpy.interfaces.ioc_context import IIocContext


T = TypeVar("T")


class IocContext(IInstanceProvider, IIocContext):
    def __init__(self, registry: IBehaviorRegistry, root: IIocContext | None = None, stack: ExitStack | None = None):
        self._registry = registry
        self._root = root
        self._stack: ExitStack | None = stack
        self._instances: dict[Type, object] = {}
        self._logger = logging.getLogger(__name__)

    def get_root(self) -> IIocContext:
        """Get the root context throng recursion"""
        if self._root is None:
            return self
        return self._root.get_root()

    @contextmanager
    def create_scope(self) -> Generator[IIocContext, Any, None]:
        return self.create_generator_scope()

    def create_generator_scope(self) -> Generator[IIocContext, None, None]:
        with ExitStack() as stack:
            context = IocContext(self._registry, self, stack)
            try:
                yield context
            finally:
                self._logger.debug("Leaving scope, cleaning up")
        self._instances.clear()

    def get(self, type_: Type[T]) -> T:
        """Get the instance from the registry"""
        self._logger.debug(f"Getting instance of {type_}")
        behavior = self._registry.get_behavior(type_)
        instance = behavior.resolve(self)

        if not isinstance(instance, type_):
            raise ValueError(f"The resolved instance is not of type {type_}")
        return instance

    @property
    def stack(self) -> ExitStack | None:
        return self._stack

    @property
    def instances(self) -> dict[Type, object]:
        return self._instances
