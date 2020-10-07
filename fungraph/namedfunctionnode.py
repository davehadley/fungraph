from typing import Any, Callable

from fungraph.functionnode import FunctionNode


class NamedFunctionNode(FunctionNode):
    """Represents a named node in a graph of delayed functions.

    May be composed with other nodes to build up a graph.
    See :ref:`examples` of how to do this.
    Do not directly call this constructor directly. Use `fungraph.named` instead.

    See Also
    --------
    fungraph.fun
    fungraph.functionnode.FunctionNode
    :ref:`examples`

    """

    def __init__(self, name: str, f: Callable[..., Any], *args: Any, **kwargs: Any):
        super().__init__(f, *args, **kwargs)
        self.name = name

    def __repr__(self):
        return (
            f"NamedFunctionNode({self.name}, {self._funcname}, args={self.args}, "
            f"kwargs={self.kwargs})"
        )
