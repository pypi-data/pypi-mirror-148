from unittest import TestCase

from lxg import Loggable


class MyClass:

    def method1(self):
        ...


class LoggableTest(TestCase):

    def test_debug(self):

        class B(MyClass, Loggable):

            def method1(self):
                self.debug(f'Start method1')
                super().method1()
                self.debug(f'Finish method1')
                return 'Ok'

        self.assertIsNotNone(B().method1())
