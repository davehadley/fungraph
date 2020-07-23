from typing import Callable, Any, Optional, Union

from fungraph.functionnode import FunctionNode
from fungraph.namedfunctionnode import NamedFunctionNode

AnyNode = Union[FunctionNode, NamedFunctionNode]


def named(name: str, f: Callable[..., Any], *args: Any, **kwargs: Any) -> NamedFunctionNode:
    """Create a named fungraph node.

    Parameters
    ----------
    name : str
        The name used to reference this node.
    f : Callable[..., Any]
        The function to be called when this fungraph node is evaluated.
    *args : Any
        Positional arguments to the function `f`.
    **kwargs : Any
        Keyword arguments to the function `f`.

    Returns
    -------
    fungraph.NamedFunctionNode
        The named fungraph node.

    See Also
    --------
    fungraph.fun
    """
    return NamedFunctionNode(name, f, *args, **kwargs)


def fun(f: Callable[..., Any], *args: Any, **kwargs: Any) -> FunctionNode:
    """Create an anonymous fungraph node.

        Parameters
        ----------
        f : Callable[..., Any]
            The function to be called when this fungraph node is evaluated.
        *args : Any
            Positional arguments to the function `f`.
        **kwargs : Any
            Keyword arguments to the function `f`.

        Returns
        -------
        fungraph.NamedFunctionNode
            The named fungraph node.

        See Also
        --------
        fungraph.named
    """
    return FunctionNode(f, *args, **kwargs)


def _maybenamed(name: Optional[str], f: Callable[..., Any], *args: Any, **kwargs: Any) -> AnyNode:
    if name:
        return named(name, f, *args, **kwargs)
    else:
        return fun(f, *args, **kwargs)


def just(value: Any, name: Optional[str] = None) -> AnyNode:
    """Create a function node with no arguments that, when evaluated, returns the given value.

            Parameters
            ----------
            value : Any
                The value to be returned when this fungraph node is evaluated.
            name : Optional[str]
                If given, a named node is returned.

            Returns
            -------
            fungraph.functionnode.FunctionNode or fungraph.namedfunctionnode.NamedFunctionNode
                Resulting fungraph node.

            See Also
            --------
            fungraph.fun
        """
    def justvalue() -> Any:
        return value

    return _maybenamed(name, justvalue)
