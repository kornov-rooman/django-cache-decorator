import pytest

from django_cache_decorator.key_builders import (
    build_func_cache_key, build_model_cache_key
)

from .models import SomeModel

pytestmark = [
    pytest.mark.unit,
    pytest.mark.key_builders,
]


# noinspection PyMethodMayBeStatic
class BuildModelCacheKeyTest:
    @pytest.mark.django_db
    def test_ok(self):
        instance = SomeModel.objects.create(some_field='one two three value')
        cache_key = build_model_cache_key(instance, ['some_field'], 'some_method_name')

        assert cache_key == 'tests:SomeModel:some_field:one_two_three_value:some_method_name'


# noinspection PyMethodMayBeStatic
class BuildFuncCacheKeyTest:
    def test_ok(self):
        cache_key = build_func_cache_key('some_function_name', 1, 2, 'three', say='hello')

        assert cache_key == 'some_function_name:1:2:three:say:hello'
