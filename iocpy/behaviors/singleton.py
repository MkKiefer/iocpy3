"""Singleton behavior implementation."""
# pylint: disable=too-few-public-methods
from typing import Callable
from iocpy.interfaces.instance_behavior import IInstanceBehavior
from iocpy.ioc_context import IocContext


class IocSingleton(IInstanceBehavior):
    """Singleton behavior
        This behavior will create a single instance and return it every time it is resolved.
    :param IInstanceBehavior: _description_
    :type IInstanceBehavior: _type_
    """

    def __init__(self, type_: type, instance: object | Callable[[IocContext], object]):
        self._type = type_
        self._instance = instance

        self._singleton: object | None = None

    def resolve(self, context: IocContext) -> object:
        """Get the instance and follow dependency"""
        root = context.get_root()
        singleton = root.instances.get(self._type, None)
        if singleton is not None:
            return singleton

        if callable(self._instance):
            singleton = self._instance(context)
            root.instances[self._type] = singleton
        else:
            singleton = self._instance
            root.instances[self._type] = singleton
        return singleton
