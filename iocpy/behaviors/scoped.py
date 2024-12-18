
from contextlib import ExitStack, contextmanager
import inspect
from typing import Any, Callable, Generator
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.ioc_context import IocContext


class IocScoped(IInstanceBehavior):
    """Scoped behavior
        This behavior will create only one instance per scope / context.
    """

    def __init__(self, type_: type, factory:
                 Callable[[IocContext], object] | Callable[[
                     IocContext], Generator[Any, None, None]]
                 ):
        self._type = type_
        self._factory = factory

    def resolve(self, context: IocContext) -> object:
        """Get the instance and follow dependency"""

        if context.stack is None:
            raise ValueError(
                "Scoped instances can't be resolved outside of a scope")

        scoped = context._instances.get(self._type, None)
        if scoped is not None:
            return scoped

        if inspect.isgeneratorfunction(self._factory):
            scoped = self.solve_generator(
                context, self._factory, context.stack)
            context._instances[self._type] = scoped
            return scoped

        if callable(self._factory):
            scoped = self._factory(context)
            context._instances[self._type] = scoped
            return scoped

        raise ValueError("Failed to resolve, invalid factory")

    def solve_generator(self, context: IocContext,
                        factory: Callable[[IocContext],
                                          Generator[Any, None, None]],
                        stack: ExitStack
                        ) -> object:

        cm = contextmanager(factory)(context)
        scoped = stack.enter_context(cm)
        return scoped
