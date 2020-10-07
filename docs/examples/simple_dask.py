import operator

from dask import delayed

import fungraph

if __name__ == "__main__":
    # dask delayed may provide the function
    f = fungraph.fun(delayed(operator.add), 1, 2)
    print(f())  # prints 3
    # and dask delayed may provide the arguments
    g = fungraph.fun(operator.add, delayed(2), 3)
    print(g())  # prints 5
