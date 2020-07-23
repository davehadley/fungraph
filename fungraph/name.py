from typing import NamedTuple


class Name(NamedTuple):
    """Use to explicitly search for a named function node when getting objects from a graph.

    This is useful in cases where named function names and keyword argument names clash.

    See Also
    --------
    fungraph.KeywordArgument
    """
    value: str
