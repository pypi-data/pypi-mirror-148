from typing import Any, Callable, Dict, Iterable


def get_meta(instance: Any) -> Dict[str, Any]:
    """
    Returns object xjsonrpc metadata.
    """

    return getattr(instance, '__xjsonrpc_meta__', {})


def set_meta(instance: Any, **meta) -> Dict[str, Any]:
    """
    Updates object xjsonrpc metadata.
    """

    if not hasattr(instance, '__xjsonrpc_meta__'):
        instance.__xjsonrpc_meta__ = {}

    instance.__xjsonrpc_meta__.update(meta)

    return instance.__xjsonrpc_meta__


def remove_prefix(s: str, prefix: str) -> str:
    """
    Removes a prefix from a string.

    :param s: string to be processed
    :param prefix: prefix to be removed
    :return: processed string
    """

    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s


def remove_suffix(s: str, suffix: str) -> str:
    """
    Removes a suffix from a string.

    :param s: string to be processed
    :param suffix: suffix to be removed
    :return: processed string
    """

    if suffix and s.endswith(suffix):
        return s[0:-len(suffix)]
    else:
        return s


def join_path(path, *paths) -> str:
    result = path
    for path in paths:
        if path:
            result = f'{result.rstrip("/")}/{path.lstrip("/")}'

    return result


def unique(*iterables, key: Callable) -> Iterable:
    items_map = {}
    for iterable in iterables:
        for item in iterable:
            items_map[key(item)] = item

    return items_map.values()
