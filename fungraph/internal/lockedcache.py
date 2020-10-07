import os
import shelve
import threading

from filelock import FileLock

from fungraph.cacheabc import Cache


class LockedCache(Cache):
    def __init__(self, dirname: str, timeout=120):
        self._timeout = timeout
        os.makedirs(dirname, exist_ok=True)
        self.filename = os.sep.join((dirname, "fungraphcache.shelve.db"))

    @property
    def _threadlock(self):
        try:
            return self._backing_threadlock
        except AttributeError:
            self._backing_threadlock = threading.RLock()
            return self._backing_threadlock

    @property
    def _lockname(self):
        return f"{self.filename}.lock"

    def _lock(self):
        return FileLock(self._lockname)

    def __getitem__(self, key):
        with self._threadlock:
            with self._lock().acquire(self._timeout):
                with shelve.open(self.filename) as s:
                    return s[key]

    def __setitem__(self, key, value):
        with self._threadlock:
            with self._lock().acquire(self._timeout):
                with shelve.open(self.filename) as s:
                    s[key] = value

    def __contains__(self, __x: object) -> bool:
        with self._threadlock:
            with self._lock().acquire(self._timeout):
                with shelve.open(self.filename) as s:
                    return __x in s

    def __getstate__(self):
        return (self._timeout, self.filename)

    def __setstate__(self, state):
        self._timeout, self.filename = state
