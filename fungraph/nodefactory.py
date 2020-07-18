from typing import Callable, Any, Optional

from fungraph.functionnode import FunctionNode
from fungraph.namedfunctionnode import NamedFunctionNode


def named(name: str, f: Callable[..., Any], *args: Any, **kwargs: Any) -> NamedFunctionNode:
    return NamedFunctionNode(name, f, *args, **kwargs)


def fun(f: Callable[..., Any], *args: Any, **kwargs: Any) -> FunctionNode:
    return FunctionNode(f, *args, **kwargs)


def _maybenamed(name: Optional[str], f: Callable[..., Any], *args: Any, **kwargs: Any) -> FunctionNode:
    if name:
        return named(name, f, *args, **kwargs)
    else:
        return fun(f, *args, **kwargs)


def just(value: Any, name: Optional[str]) -> FunctionNode:
    def justvalue() -> Any:
        return value

    return _maybenamed(name, justvalue)
