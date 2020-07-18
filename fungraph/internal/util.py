import itertools
from contextlib import suppress
from typing import Iterable, Tuple, Any, Optional, Callable


def ziporraise(*iterables: Iterable):
    padding = object()
    for zipped in itertools.zip_longest(*iterables, fillvalue=padding):
        if (padding in zipped):
            raise ValueError("iterables lengths are mismatched")
        yield zipped


def splitornone(item: str, delimiter: str = "/") -> Tuple[Any, Optional[str]]:
    try:
        first, second = item.split(delimiter, maxsplit=1)
        return (first, second)
    except:
        return (item, None)


def rsplitornone(item: str, delimiter: str = "/") -> Tuple[Any, Optional[str]]:
    try:
        first, second = item.rsplit(delimiter, maxsplit=1)
        return (first, second)
    except:
        return (None, item)


def toint(value: Any) -> Any:
    with suppress(ValueError, TypeError):
        value = int(value)
    return value


def call_if_arg_not_none(f: Callable[[Any], Any]) -> Any:
    def wrapper(x):
        return None if x is None else f(x)
    return wrapper