import operator

import fungraph

if __name__ == "__main__":
    f = fungraph.fun(operator.add, 1, 2)
    print(f())  # prints 3
