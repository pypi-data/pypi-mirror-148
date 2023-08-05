from typing import Any
from typing import List

import pandas as pd
from pandas import DataFrame


def join(
    left: pd.DataFrame,
    right: pd.DataFrame,
    how: str,
    *args: Any,
    **kwargs: str,
) -> pd.DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """

    left_on: List[str] = []
    right_on: List[str] = []

    if args:
        if len(args) > 1 and any([isinstance(arg, list) for arg in args]):
            raise ValueError(
                "Only individual names or one list of names "
                "can be passed as unnamed args"
            )

        if len(args) == 1 and isinstance(args[0], list):
            left_on.extend(args[0])
            right_on.extend(args[0])
        else:
            left_on.extend(args)
            right_on.extend(args)

    if kwargs:
        left_on.extend(kwargs.keys())
        right_on.extend(kwargs.values())

    return left.merge(
        right,
        how=how,
        left_on=left_on,
        right_on=right_on,
    )


def inner_join(
    left: DataFrame, right: DataFrame, *args: Any, **kwargs: str
) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return join(left, right, "inner", *args, **kwargs)


def left_join(
    left: DataFrame, right: DataFrame, *args: Any, **kwargs: str
) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return join(left, right, "left", *args, **kwargs)


def right_join(
    left: DataFrame, right: DataFrame, *args: Any, **kwargs: str
) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return join(left, right, "right", *args, **kwargs)


def outer_join(
    left: DataFrame, right: DataFrame, *args: Any, **kwargs: str
) -> DataFrame:
    """Left join two dataframes on a column

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    *args : str
        The columns to join on
        Can be individual columns, or one list of columns
    **kwargs : str
        The columns to join, left="right"

    Returns
    -------
    pandas.DataFrame
        The joined dataframe

    """
    return join(left, right, "outer", *args, **kwargs)


def cross_join(left: DataFrame, right: DataFrame) -> DataFrame:
    """Cross join two dataframes

    Parameters
    ----------
    left : pandas.DataFrame
        The left dataframe to join
    right : pandas.DataFrame
        The right dataframe to join
    """

    return left.merge(right, how="cross")
