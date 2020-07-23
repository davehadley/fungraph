import fungraph

def add(x, y):
    return x + y

if __name__ == '__main__':
    f = fungraph.fun(add, x=1, y=2)
    print(f()) # prints 3
    f["x"] = fungraph.fun(add, 3, 4)
    print(f()) # prints 9