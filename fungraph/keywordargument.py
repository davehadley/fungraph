from typing import NamedTuple


class KeywordArgument(NamedTuple):
    """Use to explicitly search for a function keyword argument node when getting objects from a graph.

        This is useful in cases where named function names and keyword argument names clash.

        See Also
        --------
        fungraph.Name
    """
    value: str
