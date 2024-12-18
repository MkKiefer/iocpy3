
from unittest import TestCase
from unittest.mock import MagicMock

from iocpy.ioc_container import IocContainer


class TestIocContainer(TestCase):

    def test_RegisterSingleton_ReturnsSameInstance(self):
        # Arrange
        container = IocContainer()
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
        container = IocContainer()
        call_spy = MagicMock(side_effect=[1, 2, 3, 4])
        container.register_transient(int, lambda x: call_spy())

        # Act
        instance1 = container.get(int)
        instance2 = container.get(int)

        # Assert
        self.assertNotEqual(instance1, instance2)
        self.assertEqual(call_spy.call_count, 2)

    def test_RegisterScoped_ReturnsSameInstancePerScope(self):
        # Arrange
        container = IocContainer()
        call_spy = MagicMock(side_effect=[1, 2, 3, 4])
        container.register_scoped(int, lambda x: call_spy())

        # Act & Assert
        with container.create_scope() as scope:
            self.assertEqual(scope.get(int), 1)
            self.assertEqual(scope.get(int), 1)

        with container.create_scope() as scope:
            self.assertEqual(scope.get(int), 2)
            self.assertEqual(scope.get(int), 2)

        # Assert
        self.assertEqual(call_spy.call_count, 2)

    def test_ResolveScopedInRootScope_ThrowsScopeError(self):
        # Arrange
        container = IocContainer()
        container.register_scoped(int, lambda x: 1)

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.get(int)

        self.assertEqual(str(ex.exception),
                         "Scoped instances can't be resolved outside of a scope")

    def test_ScopedSession_ClosedOnScopeExit(self):
        # Arrange
        container = IocContainer()
        enter = MagicMock()
        exit = MagicMock()
        instance = MagicMock(side_effect=[1, 2])

        def create_session(context):
            enter()
            yield instance()
            exit()
        container.register_scoped(int, create_session)

        # Act
        with container.create_scope() as scope:
            instance1 = scope.get(int)
            instance2 = scope.get(int)

        # Assert
        self.assertEqual(instance1, instance2)
        enter.assert_called_once()
        exit.assert_called_once()

    def test_RegisterInstances_ThrowsExistsError(self):
        # Arrange
        container = IocContainer()
        container.register_instance(int, 1)

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.register_instance(int, 1)

        self.assertEqual(str(ex.exception),
                         "Type <class 'int'> already registered")

    def test_RetrieveInstance_ThrowsNotExistsError(self):
        # Arrange
        container = IocContainer()

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.get(int)

        self.assertEqual(str(ex.exception),
                         "Type <class 'int'> not registered")

    def test_RetrieveWithIncompatibleTypeInstance_ThrowsError(self):
        # Arrange
        container = IocContainer()
        container.register_instance(int, "abc")

        # Act & Assert
        with self.assertRaises(ValueError) as ex:
            container.get(int)

        self.assertEqual(str(ex.exception),
                         "The resolved instance is not of type <class 'int'>")
