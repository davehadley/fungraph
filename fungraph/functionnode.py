import itertools
from contextlib import suppress
from copy import deepcopy
from types import MappingProxyType
from typing import Any, Callable, Iterator, Mapping, Optional, Tuple, Union

from dask import delayed
from dask.delayed import Delayed

from fungraph.cache import DEFAULT_CACHE_PATH, cachecontext
from fungraph.cacheabc import Cache
from fungraph.error import InvalidFunctionError
from fungraph.internal import scan
from fungraph.internal.util import (
    call_if_arg_not_none,
    rsplitornone,
    splitornone,
    toint,
)
from fungraph.keywordargument import KeywordArgument
from fungraph.name import Name


class FunctionNode:
    """Represents a node in a graph of delayed functions.

    May be composed with other nodes to build up a graph.
    See :ref:`examples` of how to do this.
    Do not directly call this constructor directly. Use `fungraph.fun` instead.

    See Also
    --------
    fungraph.fun
    :ref:`examples`

    """

    def __init__(self, f: Callable[..., Any], *args: Any, **kwargs: Any):
        if not callable(f):
            raise InvalidFunctionError("function node given a non-callable object", f)
        self._f = f
        self._args = list(args)
        self._kwargs = dict(kwargs)

    @property
    def args(self) -> Tuple[Any, ...]:
        """The positional arguments provided to this function."""
        return tuple(self._args)

    @property
    def kwargs(self) -> MappingProxyType:
        """The keyword arguments provided to this function."""
        return MappingProxyType(self._kwargs)

    @property
    def f(self) -> Callable[..., Any]:
        """The function to be called when this node is evaluated."""
        return self._f

    def __getitem__(self, key: Union[str, int, Name, KeywordArgument]):
        """Alias for the `get` method.

        See Also
        --------
        fungraph.functionnode.FunctionNode.get
        """
        return self.get(key)

    def __setitem__(self, key: Union[str, int, Name, KeywordArgument], value: Any):
        """Alias for the `set` method.

        See Also
        --------
        fungraph.functionnode.FunctionNode.set
        """
        return self.set(key, value)

    def get(self, key: Union[str, int, Name, KeywordArgument]) -> Any:
        """Get a parameter of this function (or other function node in the graph).

        See :ref:`examples` for examples of how to use this.
        """
        key, continuation = self._parsekey(key, reverse=False)
        item = self._justgetone(key)
        return item if continuation is None else item.get(continuation)

    def getall(self, key: Union[str, Name]) -> Iterator[Any]:
        """Get all nodes in the graph matching a name. """
        key = key if isinstance(key, Name) else Name(key)
        key, continuation = self._parsekey(key, reverse=False)
        for match in self._justget(key, recursive=True):
            yield match if continuation is None else match.get(continuation)

    def _parsekey(self, key, reverse=False):
        if isinstance(key, Name):
            wrapper = call_if_arg_not_none(Name)
            key = key.value
        elif isinstance(key, KeywordArgument):
            wrapper = call_if_arg_not_none(KeywordArgument)
            key = key.value
        else:

            def wrapper(o):
                return o

        split = rsplitornone if reverse else splitornone
        lhs, rhs = map(toint, split(key))
        return wrapper(lhs), wrapper(rhs)

    def _justgetone(
        self, key: Union[str, int, Name, KeywordArgument], recursive: bool = False
    ) -> Any:
        try:
            return next(self._justget(key, recursive=recursive))
        except StopIteration:
            raise KeyError(f"no item {key} in {self}")

    def _justget(
        self, key: Union[str, int, Name, KeywordArgument], recursive: bool = False
    ) -> Iterator[Any]:
        try:
            yield from self._getarg(
                key
                if not isinstance(key, KeywordArgument)
                else key.value  # type: ignore
            )
        except (KeyError, IndexError):
            yield from self._getnamed(
                key if not isinstance(key, Name) else key.value,  # type: ignore
                recursive=recursive,
            )

    def set(self, key: Union[str, int, Name, KeywordArgument], value: Any) -> None:
        """Set a parameter of this function (or other function node in the graph).

        See :ref:`examples` for examples of how to use this.
        """
        getfirst, key = self._parsekey(key, reverse=True)
        node = self if getfirst is None else self._justgetone(getfirst)
        return node._justsetone(key, value)

    def setall(self, key: Union[str, Name], value: Any):
        """Replace all nodes in the graph matching a name with the same value."""
        key = key if isinstance(key, Name) else Name(key)
        getfirst, key = self._parsekey(key, reverse=True)
        node = (self,) if getfirst is None else self._justget(getfirst)
        for n in node:
            n._justset(key, value)

    def _justsetone(
        self, key: Union[str, int, Name, KeywordArgument], value: Any
    ) -> None:
        return self._justset(key, value, recursive=False)

    def _justset(
        self,
        key: Union[str, int, Name, KeywordArgument],
        value: Any,
        recursive: bool = True,
    ) -> None:
        try:
            return self._setarg(
                key
                if not isinstance(key, KeywordArgument)
                else key.value,  # type: ignore
                value,
            )
        except (KeyError, IndexError):
            return self._setnamed(
                key if not isinstance(key, Name) else key.value,  # type: ignore
                value,
                recursive=recursive,
            )

    def _getarg(self, key: Union[str, int]) -> Iterator[Any]:
        try:
            yield self._args[key]  # type: ignore
        except TypeError:
            try:
                yield self._kwargs[key]  # type: ignore
            except KeyError:
                raise KeyError(f"{self} has no argument {key}")

    def _setarg(self, key: Union[str, int], value: Any):
        try:
            self._args[key] = value  # type: ignore
            return
        except TypeError:
            if key in self._kwargs:
                self._kwargs[key] = value  # type: ignore
                return
        raise KeyError(f"{self} has no argument {key}")

    def _iterchildnodes(self) -> Iterator[Tuple[Union[str, int], "FunctionNode"]]:
        return (
            (k, n)
            for k, n in itertools.chain(enumerate(self.args), self.kwargs.items())
            if isinstance(n, FunctionNode)
        )

    def _getnamed(self, name: str, recursive: bool = True) -> "Iterator[FunctionNode]":
        for _, a in self._iterchildnodes():
            with suppress(Exception):
                if name == a.name:  # type: ignore
                    yield a
        if recursive:
            for _, a in self._iterchildnodes():
                with suppress(Exception):
                    yield from a._getnamed(name, recursive=recursive)

    def _setnamed(self, name: str, value: Any, recursive: bool = True):
        found = False
        for index, a in self._iterchildnodes():
            with suppress(Exception):
                if name == a.name:  # type: ignore
                    found = True
                    self[index] = value
                    if not recursive:
                        return
        if recursive:
            for index, a in self._iterchildnodes():
                with suppress(Exception):
                    a._setnamed(name, value, recursive=recursive)
                    found = True
        if not found:
            raise KeyError(f'{self} does not contain "{name}"')

    def todelayed(self) -> Delayed:
        """Convert this function node to a dask delayed object."""
        args = []
        for a in self.args:
            if isinstance(a, FunctionNode):
                a = a.todelayed()
            args.append(a)
        kwargs = {}
        for key, a in self.kwargs.items():
            if isinstance(a, FunctionNode):
                a = a.todelayed()
            kwargs[key] = a
        result = delayed(self.f)(*args, **kwargs)
        return result

    def __call__(self, cache: Union[str, Cache, None] = DEFAULT_CACHE_PATH):
        """An alias for `cachedcompute`.

        See Also
        --------
        fungraph.functionnode.FunctionNode.cachedcompute
        """
        return self.cachedcompute(cache=cache)

    def compute(self, *args: Any, **kwargs: Any) -> Any:
        """Evaluate this function (and any depencies) without automatically caching.

        Parameters
        ----------

        *args : Any
            Passed on to dask `Delayed.compute`.
        **kwargs : Any
            Passed on to dask `Delayed.compute`.

        Returns
        -------
        result : Any
            The function return value.
        """
        return self.todelayed().compute(*args, **kwargs)

    def cachedcompute(self, cache: Union[str, Cache, None] = DEFAULT_CACHE_PATH) -> Any:
        """Evaluate this function (and any dependencies).

        By default caches results.

        Parameter
        ---------
        cache : Union[str, Cache, None]
            passed to `fungraph.cachecontext` to enable automatic caching.

        See Also
        --------
        fungraph.cachecontext
        """
        with cachecontext(cache):
            return self.todelayed().compute()

    def __repr__(self):
        return f"FunctionNode({self._funcname}, args={self.args}, kwargs={self.kwargs})"

    def clone(self) -> "FunctionNode":
        """Make a deep copy of this function graph."""
        return deepcopy(self)

    def scan(
        self, arguments: Mapping[str, Any], name: Optional[str] = None
    ) -> "FunctionNode":
        """Reproduce this graph with the provided arguments modified.

        Parameters
        ----------
        arguments: Mapping[str, Any]
            a map of the arguments names to modify and a list of new values.

        Returns
        -------
        listofresults : fungraph.functionnode.FunctionNode
            a function node that when evaluated returns a tuple of the results with
            the modified parameter values.
        """
        return scan.scan(self, arguments, name)

    @property
    def _funcname(self) -> str:
        if isinstance(self._f, Delayed):
            return str(self._f.key)
        try:
            return self._f.__name__
        except AttributeError:
            return str(self._f)
