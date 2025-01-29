"""Scoped behavior implementation"""
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
                 Callable[[IocContext], object] |
                 Callable[[IocContext], Callable[[IocContext], Generator[Any, None, None]]] |
                 Callable[[IocContext], Generator[Any, None, None]]
                 ):
        self._type = type_
        self._factory = factory

    def resolve(self, context: IocContext) -> object:
        """Resolve the instance and follow dependencies

        Args:
            context (IocContext): The context used to resolve the instance.

        Raises:
            ValueError: Invalid factory / callable type
            ValueError: Scoped instances can't be resolved outside of a scope

        Returns:
            object: The resolved instance.
        """

        if context.stack is None:
            raise ValueError(
                "Scoped instances can't be resolved outside of a scope")

        scoped = context.instances.get(self._type, None)
        if scoped is not None:
            return scoped

        # TODO: We most likely should cache this in the future for performance reasons
        if inspect.isgeneratorfunction(self._factory):
            scoped = self.handle_generator(
                context, self._factory, context.stack)
            context.instances[self._type] = scoped
            return scoped

        if callable(self._factory):
            scoped = self._factory(context)
            if inspect.isgeneratorfunction(scoped):
                scoped = self.handle_generator(
                    context, scoped, context.stack)
            context.instances[self._type] = scoped
            return scoped

        raise ValueError("Failed to resolve, invalid factory")

    def handle_generator(self, context: IocContext,
                         factory: Callable[[IocContext],
                                           Generator[Any, None, None]],
                         stack: ExitStack
                         ) -> object:
        """Get instance from generator function and 
        add it to the context exit stack

        Args:
            context (IocContext): The context to resolve nested dependencies.
            factory (Callable[[IocContext], Generator[Any, None, None]]): 
            The generator function to resolve.
            stack (ExitStack): The exit stack to add the generator to.

        Returns:
            object: The instance resolved from the generator.
        """
        cm = contextmanager(factory)(context)
        scoped = stack.enter_context(cm)
        return scoped
