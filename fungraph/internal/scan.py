from typing import Any, Mapping, Optional

import fungraph.functionnode
from fungraph import nodefactory
from fungraph.internal.util import ziporraise


def scan(
    node: "fungraph.functionnode.FunctionNode",
    arguments: Mapping[str, Any],
    name: Optional[str] = None,
) -> "fungraph.functionnode.FunctionNode":
    points = []
    newargs = (
        ziporraise(arguments.keys(), values)
        for values in ziporraise(*(arguments.values()))
    )
    for a in newargs:
        clone = node.clone()
        for k, v in a:
            clone.set(k, v)
        points.append(clone)
    if name:
        return nodefactory.named(name, lambda *args: tuple(args), *points)
    else:
        return nodefactory.fun(lambda *args: tuple(args), *points)
