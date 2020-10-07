import operator

import fungraph


def add(x, y):
    return x + y


if __name__ == "__main__":
    f = fungraph.named(
        "f",
        operator.add,
        fungraph.named("x", operator.mul, 1, 2),
        fungraph.named("y", operator.mul, 3, 4),
    )

    # get named
    print(f["x"])  # prints NamedFunctionNode(x, mul, args=(1, 2), kwargs={})

    # An example with a name clash
    f = fungraph.named(
        "f",
        add,
        x=fungraph.named("y", operator.mul, 1, 2),
        y=fungraph.named("x", operator.mul, 3, 4),
    )

    # in case of function names and keyword argument clashes you may use "Name" and
    # "KeywordArgument"
    print(
        f[fungraph.Name("x")]
    )  # prints NamedFunctionNode(x, mul, args=(3, 4), kwargs={})
    print(
        f[fungraph.KeywordArgument("x")]
    )  # prints NamedFunctionNode(y, mul, args=(1, 2), kwargs={})
