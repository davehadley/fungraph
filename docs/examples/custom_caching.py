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

