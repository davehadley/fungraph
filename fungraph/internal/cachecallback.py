from dask.callbacks import Callback

from fungraph.internal.dsktohash import dsktohash


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
