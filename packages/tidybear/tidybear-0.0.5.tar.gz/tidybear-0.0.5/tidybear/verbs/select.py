from typing import List
from typing import Union

import pandas as pd

from tidybear.selectors import TidySelector
from tidybear.utils import get_column_names


def select(
    df: pd.DataFrame, *args: Union[str, TidySelector], **kwargs: str
) -> pd.DataFrame:
    """Select columns from a dataframe

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to select columns from
    *args : str
        The column names to select
    **kwargs : str
        The column names to select and rename, new_name="old_name"

    Examples
    --------

    >>> df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    >>> select(df, "A")
       A
    0  1

    1  2
    2  3

    >>> select(df, "A", "A")
       A  A
    0  1  1
    1  2  2
    2  3  3

    >>> select(df, b="B")
       b
    0  4
    1  5
    2  6

    """

    to_select: List[Union[str, TidySelector]] = []

    if args:
        to_select.extend(args)

    if kwargs:
        to_select.extend(kwargs.values())
        rename_dict = {v: k for k, v in kwargs.items()}

    to_select_names = get_column_names(df.columns, to_select)
    selected = df.loc[:, to_select_names].copy()

    if kwargs:
        selected.rename(columns=rename_dict, inplace=True)

    return selected
