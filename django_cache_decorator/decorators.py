import typing as t
from functools import wraps

from django.core.cache import cache
from django.db.models import Model

from .utils import attrs_to_dict


def build_cache_key(instance: Model,
                    field_names: t.Sequence[str],
                    func_name: str) -> str:
    if isinstance(instance, Model):
        fields_pattern = ':'.join('{0}:%({0})s'.format(f) for f in field_names)
        fields_part = fields_pattern % attrs_to_dict(instance, field_names)
        cache_key = ':'.join([
            instance.__class__._meta.app_label,
            instance.__class__.__name__,
            fields_part,
            func_name
        ])
    elif issubclass(instance, Model):
        cache_key = ':'.join([
            instance._meta.app_label,
            instance.__name__,
            func_name,
        ])
    else:
        raise NotImplementedError("Can't build cache key for", instance)
    cache_key = cache_key.replace(' ', '_')
    return cache_key


def build_func_cache_key(func_name, *args, **kwargs):
    parts = [func_name] + list(args)
    for k in sorted(kwargs):
        parts.append(k)
        parts.append(kwargs[k])
    return ';'.join(map(lambda s: str(s).replace(' ', '_'), parts))


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
            cache_key = build_cache_key(self, field_names, func_name)
            val = cache.get(cache_key)
            if val is not None and callable(on_cache_hit):
                on_cache_hit(val)
                return val
            val = func(*args, **kwargs)
            cache.set(cache_key, val, timeout)
            return val

        def invalidate(instance):
            cache_key = build_cache_key(instance, field_names, func_name)
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
            if val is not None and callable(on_cache_hit):
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
