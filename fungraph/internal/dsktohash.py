import hashlib
from typing import Any, Mapping, Tuple

import dask
import joblib


def dsktohash(dsk: Mapping[str, Tuple[Any, ...]]) -> Mapping[str, str]:
    return _HashDaskGraph(dsk).hashes


class _HashDaskGraph:
    def __init__(self, dsk):
        self._hashes = {}
        self._dsk = dsk
        self._process(dsk)

    @property
    def hashes(self):
        return self._hashes

    def _process(self, dsk):
        for k in dsk.keys():
            self._hash(k)

    def _hash(self, daskkey: str) -> str:
        try:
            return self._hashes[daskkey]
        except KeyError:
            obj = self._dsk[daskkey]
            if dask.istask(obj):
                self._hashes[daskkey] = self._hashtask(obj)
            else:
                self._hashes[daskkey] = self._md5hashpickle(obj)
            return self._hashes[daskkey]

    def _hashtask(self, obj: Any) -> str:
        md5 = hashlib.md5()
        for o in obj:
            if isinstance(o, str) and o in self._dsk:
                h = self._hash(o)
            elif callable(o):
                h = self._get_callable_src(o)
            elif isinstance(o, list) or dask.istask(o):
                h = self._hashtask(o)
            else:
                h = self._md5hashpickle(o)
            md5.update(h.encode())
        return md5.hexdigest()

    def _md5hashpickle(self, obj: Any) -> str:
        return joblib.hash(obj)

    def _get_callable_src(self, c):
        return joblib.func_inspect.get_func_code(c)[0]
