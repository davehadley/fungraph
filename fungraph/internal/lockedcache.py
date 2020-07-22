import os
import shelve
import threading

from filelock import FileLock

class LockedCache:
    def __init__(self, dirname: str, timeout=120):
        self._timeout = timeout
        os.makedirs(dirname, exist_ok=True)
        self.filename = os.sep.join((dirname, "fungraphcache.shelve.db"))
        #self._threadlock = threading.RLock()

    @property
    def _lockname(self):
        return f"{self.filename}.lock"

    def _lock(self):
        return FileLock(self._lockname)

    def __getitem__(self, key):
        #with self._threadlock:
            with self._lock().acquire(self._timeout):
                with shelve.open(self.filename) as s:
                    return s[key]

    def __setitem__(self, key, value):
        #with self._threadlock:
            with self._lock().acquire(self._timeout):
                with shelve.open(self.filename) as s:
                    s[key] = value