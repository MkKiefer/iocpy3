"""Singleton behavior implementation."""
# pylint: disable=too-few-public-methods
from typing import Callable
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.interfaces.instance_provider import IInstanceProvider


class IocSingleton(IInstanceBehavior):
    """Singleton behavior
        This behavior will create a single instance and return it every time it is resolved.
    :param IInstanceBehavior: _description_
    :type IInstanceBehavior: _type_
    """

    def __init__(self, type_: type, instance: object | Callable[[IInstanceProvider], object]):
        self._type = type_
        self._instance = instance

        self._singleton: object | None = None

    def resolve(self, provider: IInstanceProvider) -> object:
        """Get the instance and follow dependency"""
        if self._singleton is None:
            if callable(self._instance):
                self._singleton = self._instance(provider)
            else:
                self._singleton = self._instance
        return self._singleton
