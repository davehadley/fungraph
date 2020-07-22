import timeit
from typing import Callable, Any


def timeonce(f: Callable[[], Any]) -> float:
    return timeit.timeit(f, number=1)
