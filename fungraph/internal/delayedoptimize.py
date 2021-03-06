from typing import Any, Iterable, Mapping, Optional, Union

import dask
from toolz import curry

from fungraph.cacheabc import Cache
from fungraph.internal.cacheafterexecution import CacheAfterExecution
from fungraph.internal.dsktohash import dsktohash


@curry
def delayedoptimize(
    dsk: Mapping[str, Any],
    keys: Optional[Union[str, Iterable[str]]] = None,
    cache: Optional[Cache] = None,
) -> Mapping[str, Any]:
    hashes = dsktohash(dsk)
    result = {}
    for key in dsk:
        if cache is not None and hashes[key] in cache:
            result[key] = (lambda k: cache[k], hashes[key])  # type: ignore
        else:
            c = dsk[key]
            if cache is not None and dask.istask(c):
                result[key] = (CacheAfterExecution(c[0], cache, hashes[key]),) + c[1:]
            else:
                result[key] = dsk[key]
    return result
