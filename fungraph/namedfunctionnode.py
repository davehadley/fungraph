from typing import Callable, Any

from fungraph.functionnode import FunctionNode


class NamedFunctionNode(FunctionNode):
    def __init__(self, name: str, f: Callable[..., Any], *args: Any, **kwargs: Any):
        super().__init__(f, *args, **kwargs)
        self.name = name

    def __repr__(self):
        return f"NamedFunctionNode({self.name}, {self._funcname}, args={self.args}, kwargs={self.kwargs})"
