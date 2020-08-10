from typing import Any, Optional

from fungraph.nodefactory import AnyNode, named, fun


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
    def justvalue(localvalue=value) -> Any:
        return localvalue

    if name:
        return named(name, justvalue)
    else:
        return fun(justvalue)
