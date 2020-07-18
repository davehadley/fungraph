from typing import Callable, Any

import fungraph.functionnode
import fungraph.namedfunctionnode


def named(name: str, f: Callable[..., Any], *args: Any, **kwargs: Any) -> "fungraph.namedfunctionnode.NamedFunctionNode":
    return fungraph.namedfunctionnode.NamedFunctionNode(name, f, *args, **kwargs)


def fun(f: Callable[..., Any], *args: Any, **kwargs: Any) -> "fungraph.functionnode.FunctionNode":
    return fungraph.functionnode.FunctionNode(f, *args, **kwargs)
