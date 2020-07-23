import fungraph


def add(x, y):
    return x + y


if __name__ == '__main__':
    f = fungraph.fun(add, x=1, y=2)
    # scan 1 parameter
    scan = f.scan({"x": [1, 2, 3]})
    print(scan())  # prints (3, 4, 5)
    # scan multiple parameters
    scan = f.scan({"x": [1, 2, 3], "y": [1, 2, 3]})
    print(scan())  # prints (2, 4, 6)
    # scan does not modify the original function graph
    print(f())  # prints 3
