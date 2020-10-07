import timeit
from typing import Any, Callable


def timeonce(f: Callable[[], Any]) -> float:
    return timeit.timeit(f, number=1)
