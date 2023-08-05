"""
Tidy Selectors

A tidy selector is a function that takes a list of column names,
and returns a new list of filtered column names based on the underlying tidy select function.

Examples
--------
code ::
    import pandas as pd
    import tidybear as tb
    from tidybear.selectors import contains

    data = pd.DataFrame(columns=["x01", "x02", "x03", "y1", "y2"])
    tb.select(data, contains("y"))
"""
from __future__ import annotations

import re
from typing import Iterable
from typing import List
from typing import Protocol
from typing import Sequence
from typing import Union


class TidySelectFunction(Protocol):
    def __call__(self, columns: Iterable[str]) -> Sequence[str]:
        ...


class TidySelector:
    def __init__(self, selector: TidySelectFunction) -> None:
        self.selector = selector

    def __call__(self, columns: Iterable[str]) -> Sequence[str]:
        return self.selector(columns)

    def filter_columns(self, columns: Iterable[str]) -> Sequence[str]:
        return self.selector(columns)

    def __neg__(self) -> TidySelector:
        def neg_selector(columns: Iterable[str]) -> List[str]:
            return [c for c in columns if c not in self.selector(columns)]

        return TidySelector(neg_selector)


_ColumnList = Union[str, TidySelector, Sequence[Union[str, TidySelector]]]


def everything() -> TidySelector:
    """Select all columns

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> everything()(cols)
    ['x01', 'x02', 'x03', 'y1', 'y2']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return list(columns)

    return TidySelector(selector)


def last_col() -> TidySelector:
    """Select only the last column

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> last_col()(cols)
    ['y2']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return [list(columns)[-1]]

    return TidySelector(selector)


def first_col() -> TidySelector:
    """Select only the first column

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> first_col()(cols)
    ['x01']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return [list(columns)[0]]

    return TidySelector(selector)


def contains(pattern: str) -> TidySelector:
    """Select all columns that contain the literal string

    Parameters
    ----------
    pattern : str
        The string to match

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> contains("y")(cols)
    ['y1', 'y2']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return [c for c in columns if pattern in c]

    return TidySelector(selector)


def matches(pattern: str) -> TidySelector:
    """Select all columns that match the regular expression

    pattern : str
        The regular expression to match

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> matches("(x|y)0?2")(cols)
    ['x02', 'y2']
    """
    pattern_re = re.compile(pattern)

    def selector(columns: Iterable[str]) -> List[str]:
        return [c for c in columns if pattern_re.match(c)]

    return TidySelector(selector)


def starts_with(pattern: str) -> TidySelector:
    """Select all columns that start with the literal string

    Parameters
    ----------
    pattern : str
        The string to match

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> starts_with("x")(cols)
    ['x01', 'x02', 'x03']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return [c for c in columns if c.startswith(pattern)]

    return TidySelector(selector)


def ends_with(pattern: str) -> TidySelector:
    """Select all columns that end with the literal srting

    Parameters
    ----------
    pattern : str
        The string to match

    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> ends_with("2")(cols)
    ['x02', 'y2']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        return [c for c in columns if c.endswith(pattern)]

    return TidySelector(selector)


def num_range(prefix: str, values: Iterable[int], width: int = 0) -> TidySelector:
    """Select all columns that match a numeric range like x01, x02, x03

    Parameters
    ----------
    prefix : str
        The prefix of the columns to select

    values : range of integers
        The numeric values in the range

    width : int
        Pad the number with zeros to this width


    Examples
    --------
    >>> cols = ["x01", "x02", "x03", "y1", "y2"]
    >>> num_range("x", range(2, 4), width=2)(cols)
    ['x02', 'x03']
    """

    def selector(columns: Iterable[str]) -> List[str]:
        allowed = [f"{prefix}{str(i).zfill(width)}" for i in values]
        return [c for c in columns if c in allowed]

    return TidySelector(selector)
