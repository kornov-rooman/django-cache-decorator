

def dotval(obj, dottedpath: str, default=None):
    """
    Возвращает значение аттрибута объекта или элемента словаря по его пути в формате 'a.b.c'
    Примеры:

    obj = {'item1': {'nested': 123, 'other': 456}}
    >>> dotval(obj, 'item1.nested')
    123

    >>> dotval(obj, 'item2')
    None
    """
    val = obj
    sentinel = object()
    for attr in dottedpath.split('.'):
        if isinstance(val, dict):
            val = val.get(attr, sentinel)
            if val is sentinel:
                return default
        else:
            val = getattr(val, attr, sentinel)
            if val is sentinel:
                return default
    return val


def attrs_to_dict(obj, attrib_names: Sequence[str]) -> dict:
    """
    Возвращает словарь атрибутов и их значений.

    attrs_to_dict(some_obj, ['id', 'field']) -> {'id': 12, 'field': 'value'}
    """
    return {name: dotval(obj, name) for name in attrib_names}