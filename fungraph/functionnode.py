import itertools
from contextlib import suppress
from copy import deepcopy
from types import MappingProxyType
from typing import Callable, Any, Tuple, Optional, Union, Iterator, Mapping

import graphchain
import dask
from dask import delayed

from fungraph.internal import scan
from fungraph.internal.util import rsplitornone, splitornone, toint, call_if_arg_not_none
from fungraph.keywordargument import KeywordArgument
from fungraph.name import Name
from fungraph.error import InvalidFunctionError


def _context() -> dask.config.set:
    return dask.config.set(scheduler="sync",
                           delayed_optimize=graphchain.optimize)


class FunctionNode:

    def __init__(self, f: Callable[..., Any], *args: Any, **kwargs: Any):
        if not callable(f):
            raise InvalidFunctionError("function node given a non-callable object", f)
        self._f = f
        self._args = list(args)
        self._kwargs = dict(kwargs)

    @property
    def args(self) -> Tuple[Any]:
        return tuple(self._args)

    @property
    def kwargs(self) -> MappingProxyType:
        return MappingProxyType(self._kwargs)

    @property
    def f(self) -> Callable[..., Any]:
        return self._f

    def __getitem__(self, key: Union[str, int, Name, KeywordArgument]):
        return self.get(key)

    def __setitem__(self, key: Union[str, int, Name, KeywordArgument], value: Any):
        return self.set(key, value)

    def get(self, key: Union[str, int, Name, KeywordArgument]) -> Any:
        key, continuation = self._parsekey(key, reverse=False)
        item = self._justgetone(key)
        return item if continuation is None else item.get(continuation)

    def getall(self, key: Union[str, Name]) -> Iterator[Any]:
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

    def _justgetone(self, key: Union[str, int, Name, KeywordArgument], recursive:bool=False) -> Any:
        try:
            return next(self._justget(key, recursive=recursive))
        except StopIteration:
            raise KeyError(f"no item {key} in {self}")

    def _justget(self, key: Union[str, int, Name, KeywordArgument], recursive: bool=False) -> Iterator[Any]:
        try:
            yield from self._getarg(key if not isinstance(key, KeywordArgument) else key.value)
        except (KeyError, IndexError):
            yield from self._getnamed(key if not isinstance(key, Name) else key.value, recursive=recursive)

    def set(self, key: Union[str, int, Name, KeywordArgument], value: Any) -> None:
        getfirst, key = self._parsekey(key, reverse=True)
        node = self if getfirst is None else self._justgetone(getfirst)
        return node._justsetone(key, value)

    def setall(self, key: Union[str, Name], value: Any):
        key = key if isinstance(key, Name) else Name(key)
        getfirst, key = self._parsekey(key, reverse=True)
        node = (self,) if getfirst is None else self._justget(getfirst)
        for n in node:
            n._justset(key, value)

    def _justsetone(self, key: Union[str, int, Name, KeywordArgument], value: Any) -> None:
        return self._justset(key, value, recursive=False)

    def _justset(self, key: Union[str, int, Name, KeywordArgument], value: Any, recursive: bool=True) -> None:
        try:
            return self._setarg(key if not isinstance(key, KeywordArgument) else key.value, value)
        except (KeyError, IndexError):
            return self._setnamed(key if not isinstance(key, Name) else key.value, value, recursive=recursive)

    def _getarg(self, key: Union[str, int]) -> Iterator[Any]:
        try:
            yield self._args[key]
        except TypeError:
            try:
                yield self._kwargs[key]
            except KeyError:
                raise KeyError(f"{self} has no argument {key}")

    def _setarg(self, key: Union[str, int], value: Any):
        try:
            self._args[key] = value
            return
        except TypeError:
            if key in self._kwargs:
                self._kwargs[key] = value
                return
        raise KeyError(f"{self} has no argument {key}")

    def _iterchildnodes(self) -> Iterator[Tuple[Union[str, int], "FunctionNode"]]:
        return ((k, n) for k, n in itertools.chain(enumerate(self.args), self.kwargs.items())
                if isinstance(n, FunctionNode)
                )

    def _getnamed(self, name: str, recursive: bool = True) -> "Iterator[FunctionNode]":
        for _, a in self._iterchildnodes():
            with suppress(Exception):
                if name == a.name:
                    yield a
        if recursive:
            for _, a in self._iterchildnodes():
                with suppress(Exception):
                    yield from a._getnamed(name, recursive=recursive)

    def _setnamed(self, name: str, value: Any, recursive: bool = True):
        found = False
        for index, a in self._iterchildnodes():
            with suppress(Exception):
                if name == a.name:
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
            raise KeyError(f"{self} does not contain \"{name}\"")

    def todelayed(self) -> delayed:
        args = []
        for a in self.args:
            with suppress(AttributeError):
                a = a.todelayed()
            args.append(a)
        args = tuple(args)
        kwargs = {}
        for key, a in self.kwargs.items():
            with suppress(AttributeError):
                a = a.todelayed()
            kwargs[key] = a
        result = delayed(self.f)(*args, **kwargs)
        return result

    def __call__(self):
        return self.compute()

    def compute(self, cachedir: str = ".fungraphcache") -> Any:
        with _context():
            return self.todelayed().compute(location=cachedir)

    def __repr__(self):
        return f"FunctionNode({self.f.__name__}, args={self.args}, kwargs={self.kwargs})"

    def clone(self):
        return deepcopy(self)

    def scan(self, arguments: Mapping[str, Any], name: Optional[str] = None):
        return scan.scan(self, arguments, name)
