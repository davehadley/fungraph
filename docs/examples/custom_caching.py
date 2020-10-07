import operator

import fungraph

if __name__ == "__main__":
    f = fungraph.fun(operator.add, 2, 2)

    f()  # uses default caching
    f.cachedcompute()  # equivalent to the above line

    f.compute()  # run the computation without any cache

    # manually use the default caching method
    # this could be replaced with an alternative user provided caching context
    with fungraph.cachecontext():
        f.compute()

    # replace the default local disk store with a custom cache.
    class MemoryCache(fungraph.Cache):
        def __init__(self):
            self.dict = dict()

        def __getitem__(self, key):
            return self.dict[key]

        def __setitem__(self, key, value):
            self.dict[key] = value

        def __contains__(self, __x: object) -> bool:
            return __x in self.dict

    memorycache = MemoryCache()
    with fungraph.cachecontext(cache=memorycache):
        f.compute()
    print(memorycache.dict)  # prints: {'bd9a1aa4150cc393207a60e4a06dcac7': 4}
