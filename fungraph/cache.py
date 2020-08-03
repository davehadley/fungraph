from typing import Union, Mapping, Any, Optional, Iterable

import dask
from dask.callbacks import Callback

from fungraph.internal.delayedoptimize import delayedoptimize
from fungraph.internal.lockedcache import LockedCache

DEFAULT_CACHE_PATH = ".fungraphcache"


def cachecontext(cache: Union[str, Mapping[str, Any], None] = DEFAULT_CACHE_PATH) -> Callback:
    """Enables automatic caching of function node results and values.

    Parameters
    ----------
    cache: Union[str, Mapping[str, Any], None]
        If `str` caches to the file system to a directory corresponding to this string. If the directory does not
        exist it is created.
        If Mapping[str, Any] is provided this object is used as the storage for the cache instead of the default filesystem
        method. For example, a standard dict would provide caching to memory.
        If `None`, no caching is enabled.

    Returns
    -------
    Callback
        a context manager that handles caching of function results and values.
    """
    if cache is None:
        # null callback, does no caching
        return Callback()
    if isinstance(cache, str):
        cache = LockedCache(cache)
    return dask.config.set(delayed_optimize=delayedoptimize(cache=cache))



