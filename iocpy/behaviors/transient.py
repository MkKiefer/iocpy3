"""Transient behavior implementation."""
# pylint: disable=too-few-public-methods
from typing import Callable
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.ioc_context import IocContext


class IocTransient(IInstanceBehavior):
    """Transient behavior
        This behavior will create a new instance every time it is resolved.
    """

    def __init__(self, type_: type, instance: Callable[[IocContext], object]):
        self._type = type_
        self._instance = instance

    def resolve(self, context: IocContext) -> object:
        """Get the instance and follow dependency"""
        return self._instance(context)
