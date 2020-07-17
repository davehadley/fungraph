import itertools
from typing import Iterable


def ziporraise(*iterables: Iterable):
    padding = object()
    for zipped in itertools.zip_longest(*iterables, fillvalue=padding):
        if(padding in zipped):
            raise ValueError("iterables lengths are mismatched")
        yield zipped