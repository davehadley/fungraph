import hashlib
from typing import Mapping, Tuple, Any

import cloudpickle
import dask
import joblib
from dask.callbacks import Callback


class CacheCallback(Callback):

    def __init__(self, cache):
        super().__init__()
        self._cache = cache

    def _start(self, dsk):
        self._hashes = dsktohash(dsk)
        for key in dsk:
            try:
                dsk[key] = self._cache[self._hashes[key]]
            except KeyError:
                pass
        return

    def _posttask(self, key, value, dsk, state, id):
        self._cache[self._hashes[key]] = value


def dsktohash(dsk: Mapping[str, Tuple[Any, ...]]) -> Mapping[str, str]:
    # from print import pprint
    # pprint(dsk)
    return {k: _hash(k, dsk) for k in dsk.keys()}


def _hash(daskkey: str, dsk: Mapping[str, Tuple[Any, ...]]) -> str:
    obj = dsk[daskkey]
    if dask.core.istask(obj):
        result = _hashtask(obj, dsk)
    else:
        result = _md5hashpickle(obj)
    return result


def _hashtask(obj: Any, dsk: Mapping[str, Tuple[Any, ...]]):
    md5 = hashlib.md5("_hashtask".encode())
    for o in obj:
        if dask.core.istask(o):
            h = _hashtask(o, dsk)
        elif isinstance(o, str) and o in dsk:
            h = _hash(o, dsk)
        elif callable(o):
            h = _get_callable_src(o)
        elif isinstance(o, list):
            h = _hashtask(o, dsk)
        else:
            h = _md5hashpickle(o)
        md5.update(h.encode())
    return md5.hexdigest()


def _md5hashpickle(obj: Any) -> str:
    return hashlib.md5(cloudpickle.dumps(obj)).hexdigest()


def _get_callable_src(c):
    return joblib.func_inspect.get_func_code(c)[0]
