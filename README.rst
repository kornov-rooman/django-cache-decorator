Installation
------------
.. code:: bash

    pip install -e git+https://github.com/kornov-rooman/django-cache-decorator.git@#egg=django-cache-decorator


Sample
------

.. code:: python

    @cached_method(['id', 'field1', 'field2'])
    def get_something(self):
        ...

    @cached_method(['id', 'field'], 86400)
    def get_some_data(self):
        ...

    @classmethod
    @cached_method(timeout=86400)
    def get_something(cls):
        ...

