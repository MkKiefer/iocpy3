"""interfaces/instance_provider.py"""
# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar("T")


class IInstanceProvider(ABC):
    """Instance provider interface, provides instances of the specified type."""

    @abstractmethod
    def get(self, type_: Type[T]) -> T:
        """Get an instance of the specified type."""
