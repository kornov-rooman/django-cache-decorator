import typing as t


def dot_value(obj, dotted_path: str, default: t.Optional[t.Any] = None) -> t.Any:
    """
    obj = {'item1': {'nested': 123, 'other': 456}}
    >>> dot_value(obj, 'item1.nested')
    123

    >>> dot_value(obj, 'item2')
    None
    """
    val = obj
    sentinel = object()
    for attr in dotted_path.split('.'):
        if isinstance(val, dict):
            val = val.get(attr, sentinel)
            if val is sentinel:
                return default
        else:
            val = getattr(val, attr, sentinel)
            if val is sentinel:
                return default
    return val


def attrs_to_dict(obj, attrib_names: t.Sequence[str]) -> dict:
    """
    attrs_to_dict(some_obj, ['id', 'field']) -> {'id': 12, 'field': 'value'}
    """
    return {name: dot_value(obj, name) for name in attrib_names}
