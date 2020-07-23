import fungraph


def add(x, y):
    return x + y

if __name__ == '__main__':
    f = fungraph.fun(add, 1, y=2)
    print(f())  # prints 3
