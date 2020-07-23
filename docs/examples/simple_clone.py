import fungraph

def add(x, y):
    return x + y

if __name__ == '__main__':
    f = fungraph.fun(add, x=1, y=2)
    g = f.clone()
    g["x"] = 2
    print(f()) # prints 3
    print(g()) # prints 4