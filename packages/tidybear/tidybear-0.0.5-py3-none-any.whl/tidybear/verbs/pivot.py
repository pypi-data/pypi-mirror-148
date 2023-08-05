from typing import Any
from typing import List
from typing import Optional
from typing import Union

import pandas as pd

from tidybear.selectors import _ColumnList
from tidybear.utils import get_column_names


def pivot_wider(
    df: pd.DataFrame,
    *,
    names_from: str = "name",
    values_from: Union[List[str], str] = "value",
    fill_value: Optional[Any] = None,
    prefix_names: bool = False,
) -> pd.DataFrame:
    """
    Transform a dataframe from long to wide

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    names_from : str
        The column name to pivot on
    values_from : str, List[str]
        The column name to pivot on
        If multiple names are passed, the columns will be <value>_<name>
    fill_value : Optional[Any]
        The value to fill in the new column

    >>> df = pd.DataFrame({"idx": [1, 2], "name": ["a", "a"], "value": [3, 4]})
    >>> pivot_wider(df)
       idx  a
    0    1  3
    1    2  4

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    if isinstance(values_from, str):
        values_from = [values_from]

    index_cols = [c for c in df.columns if c not in [names_from, *values_from]]
    df = df.pivot(index=index_cols, columns=names_from, values=values_from)

    if len(values_from) == 1 and not prefix_names:
        df.columns = [name for _, name in df.columns.to_flat_index()]
    else:
        df.columns = [f"{value}_{name}" for value, name in df.columns.to_flat_index()]

    if fill_value is not None:
        df = df.fillna(fill_value)

    return df.reset_index()


def pivot_longer(
    df: pd.DataFrame,
    cols: _ColumnList,
    *,
    names_to: str = "name",
    values_to: str = "value",
    drop_na: bool = True,
    cols_are_index: bool = False,
) -> pd.DataFrame:
    """
    Transform a dataframe from wide to long

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe to transform
    cols : str, list[str], TidySelector
        The columns to pivot on, use all the others as the index
    names_to : str
        The new name for the name column
    values_to : str
        the new name for the value column
    drop_na : bool, optional
        Whether to drop rows with missing values, default True
    cols_are_index : bool, optional
        Whether the columns are the index or the columns to pivot on, default False

    Examples
    --------

    >>> df = pd.DataFrame({"idx": [1, 2], "a": [1, 2], "b": [1, 2]})
    >>> pivot_longer(df, index="idx")
       idx name  value
    0    1    a      1
    1    1    b      1
    2    2    a      2
    3    2    b      2

    Returns
    -------
    pandas.DataFrame
        The transformed dataframe
    """

    df = df.copy()

    columns = get_column_names(df.columns, cols)
    index_columns = (
        columns if cols_are_index else [c for c in df.columns if c not in columns]
    )

    if len(index_columns) > 0:
        df.set_index(index_columns, inplace=True)

    df = df.stack(dropna=False).reset_index()
    df.columns = [*index_columns, names_to, values_to]

    if drop_na:
        df = df.dropna(subset=[values_to])

    return df
