import fungraph


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


if __name__ == "__main__":
    f = fungraph.fun(
        add,
        fungraph.fun(mul, 1, 2),
        fungraph.fun(mul, 3, 4),
    )

    # get positional arguments
    print(f[0])  # prints: FunctionNode(mul, args=(1, 2), kwargs={})
    print(f[0][1])  # prints 2

    g = fungraph.fun(
        add,
        x=fungraph.fun(mul, x=1, y=2),
        y=fungraph.fun(mul, x=3, y=4),
    )

    # get keyword arguments
    print(g["x"])  # prints FunctionNode(mul, args=(), kwargs={'x': 1, 'y': 2})
    print(g["x"]["y"])  # prints 2
    print(g["x/y"])  # more convenient syntax, equivalent to the previous line
