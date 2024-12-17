

import random
from unittest import TestCase
from unittest.mock import MagicMock

from iocpy.ioc_container import IOCContainer


class TestIoCContainer(TestCase):

    def test_RegisterSingleton_ReturnsSameInstance(self):
        # Arrange
        container = IOCContainer()
        call_spy = MagicMock(side_effect=[1, 2, 3, 4])
        container.register_singleton(int, lambda x: call_spy())

        # Act
        instance1 = container.get(int)
        instance2 = container.get(int)

        # Assert
        self.assertEqual(instance1, instance2)
        self.assertEqual(call_spy.call_count, 1)

    def test_RegisterTransient_ReturnsDifferentInstances(self):
        # Arrange
        container = IOCContainer()
        call_spy = MagicMock(side_effect=[1, 2, 3, 4])
        container.register_transient(int, lambda x: call_spy())

        # Act
        instance1 = container.get(int)
        instance2 = container.get(int)

        # Assert
        self.assertNotEqual(instance1, instance2)
        self.assertEqual(call_spy.call_count, 2)

    def test_RegisterInstances_ThrowsExistsError(self):
        # Arrange
        container = IOCContainer()
        container.register_instance(int, 1)

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.register_instance(int, 1)

        self.assertEqual(str(ex.exception),
                         "Type <class 'int'> already registered")

    def test_RetrieveInstance_ThrowsNotExistsError(self):
        # Arrange
        container = IOCContainer()

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.get(int)

        self.assertEqual(str(ex.exception),
                         "Type <class 'int'> not registered")

    def test_RetrieveWithIncompatibleTypeInstance_ThrowsError(self):
        # Arrange
        container = IOCContainer()
        container.register_instance(int, "abc")

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.get(int)

        self.assertEqual(str(ex.exception),
                         "The resolved instance is not of type <class 'int'>")
