from typing import Union

import dask
from dask.callbacks import Callback

from fungraph.cacheabc import Cache
from fungraph.internal.delayedoptimize import delayedoptimize
from fungraph.internal.lockedcache import LockedCache

DEFAULT_CACHE_PATH = ".fungraphcache"


def cachecontext(cache: Union[str, Cache, None] = DEFAULT_CACHE_PATH) -> Callback:
    """Enables automatic caching of function node results and values.

    Parameters
    ----------
    cache: Union[str, Cache, None]
        If `str` caches to the file system to a directory corresponding to this string.
        If the directory does not exist it is created.
        If Cache is provided this object is used as the storage for the cache instead
        of the default filesystem method.
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
