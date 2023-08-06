
========================================================
Interface for quick access to the logging functionality
========================================================

The sample:

.. code:: python

    from lxg import Loggable

    MyClass:

        def method1(self):
            ...

    MyClassToo(MyClass, Loggable):

        def method1(self):
            self.debug(f'Do method1')
            super().method1()

