import fungraph

def add(x, y):
    return x + y

def mul(x, y):
    return x * y

# contruct a function with positional arguments
f = fungraph.fun(add, 1, 2)
# construct a function with keyword arguments
f = fungraph.fun(add, x=1, y=2)

# functions are lazily evaluated
print(f.compute()) # prints 3

# functions may be nested
f = fungraph.fun(add,
              x=fungraph.fun(mul, x=1, y=2),
              y=fungraph.fun(mul, x=3, y=4),
)

# parameter values may be retrieved
print(f["x"]) # prints FunctionNode(mul, args=(), kwargs={'x': 1, 'y': 2})
print(f["x"]["y"]) # prints 2
print(f["x/y"]) # equivalent to the previous line

# functions may be copied and modified
g = f.clone()
g["x/y"] = fungraph.fun(add, x=5, y=6)
print(g.compute()) # prints 23

# recompute the function with many variations of a parameter
scan = f.scan({"x":[0, 1, 2, 3]})
print(scan.compute()) # prints (12, 13, 14, 15)
