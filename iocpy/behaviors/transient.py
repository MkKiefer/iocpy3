"""Transient behavior implementation."""
# pylint: disable=too-few-public-methods
from typing import Callable
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


class IocTransient(IInstanceBehavior):
    """Transient behavior
        This behavior will create a new instance every time it is resolved.
    """

    def __init__(self, type_: type, instance: Callable[[IInstanceProvider], object]):
        self._type = type_
        self._instance = instance

    def resolve(self, provider: IInstanceProvider) -> object:
        """Get the instance and follow dependency"""
        return self._instance(provider)
