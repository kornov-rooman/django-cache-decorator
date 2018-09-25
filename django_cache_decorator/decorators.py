import typing as t
from functools import wraps

from django.core.cache import cache

from .key_builders import build_model_cache_key, build_func_cache_key


def cached_method(field_names: t.List[str] = None,
                  timeout: t.Optional[int] = None,
                  on_cache_hit: t.Optional[t.Callable[[t.Any], t.Any]] = None):
    """
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
    """
    field_names = field_names or ['id']

    def _cached(func):
        func_name = func.__code__.co_name

        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            cache_key = build_model_cache_key(self, field_names, func_name)
            val = cache.get(cache_key)

            if val is not None:
                if callable(on_cache_hit):
                    on_cache_hit(val)
                return val

            val = func(*args, **kwargs)
            cache.set(cache_key, val, timeout)
            return val

        def invalidate(instance):
            cache_key = build_model_cache_key(instance, field_names, func_name)
            cache.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper

    return _cached


def cached_func(timeout: t.Optional[int] = None,
                on_cache_hit: t.Optional[t.Callable[[t.Any], t.Any]] = None):
    """
    @cached_func()
    def get_something(arg1, arg2=20):
        ...
    """

    def _cached(func):
        func_name = func.__code__.co_name

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = build_func_cache_key(func_name, *args, **kwargs)
            val = cache.get(cache_key)

            if val is not None:
                if callable(on_cache_hit):
                    on_cache_hit(val)
                return val

            val = func(*args, **kwargs)
            cache.set(cache_key, val, timeout)
            return val

        def invalidate(*args, **kwargs):
            cache_key = build_func_cache_key(func_name, *args, **kwargs)
            cache.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper

    return _cached
