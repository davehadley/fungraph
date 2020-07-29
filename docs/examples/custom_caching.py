import fungraph
import operator

if __name__ == '__main__':
    f = fungraph.fun(operator.add, 2, 2)

    f() # uses default caching
    f.cachedcompute() # equivalent to the above line

    f.compute()  # run the computation without any cache

    # manually use the default caching method
    with fungraph.cachecontext(): # this line could be replaced with an alternative user provided caching context
        f.compute()

    # replace the default local disk store with a custom cache (in this case a python dictionary, but any
    # Mapping[str, Any] object will be accepted).
    memorycache = dict()
    with fungraph.cachecontext(cache=memorycache):
        f.compute()
    print(memorycache) # prints: {'2f93a3b0692fbbf776b5c51f9160c2f2': 4}

