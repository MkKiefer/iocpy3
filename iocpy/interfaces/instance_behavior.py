"""instance behavior interface."""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from iocpy.interfaces.instance_provider import IInstanceProvider


T = TypeVar("T")


class IInstanceBehavior(ABC, Generic[T]):
    """
    The behavior interface is used to resolve the instance
    in different ways like singleton, transient, etc.
    """

    @abstractmethod
    def resolve(self, provider: IInstanceProvider) -> T:
        """Resolves a instance, and recuse over dependency's"""
