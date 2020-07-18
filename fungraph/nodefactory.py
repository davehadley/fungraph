from typing import Callable, Any, Optional, Union

from fungraph.functionnode import FunctionNode
from fungraph.namedfunctionnode import NamedFunctionNode

AnyNode = Union[FunctionNode, NamedFunctionNode]


def named(name: str, f: Callable[..., Any], *args: Any, **kwargs: Any) -> NamedFunctionNode:
    return NamedFunctionNode(name, f, *args, **kwargs)


def fun(f: Callable[..., Any], *args: Any, **kwargs: Any) -> FunctionNode:
    return FunctionNode(f, *args, **kwargs)


def _maybenamed(name: Optional[str], f: Callable[..., Any], *args: Any, **kwargs: Any) -> AnyNode:
    if name:
        return named(name, f, *args, **kwargs)
    else:
        return fun(f, *args, **kwargs)


def just(value: Any, name: Optional[str] = None) -> AnyNode:
    def justvalue() -> Any:
        return value

    return _maybenamed(name, justvalue)
