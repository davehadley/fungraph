import operator

import fungraph

if __name__ == "__main__":
    f = fungraph.fun(
        operator.add,
        fungraph.fun(operator.mul, 1, 2),
        fungraph.fun(operator.mul, 3, 4),
    )
    print(f())  # prints 14
