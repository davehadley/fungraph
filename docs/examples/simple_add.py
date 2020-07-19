import fungraph
import operator

if __name__ == '__main__':
    f = fungraph.fun(operator.add, 1, 2)
    print(f.compute()) # prints 3
