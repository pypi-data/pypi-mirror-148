from __future__ import annotations

from pandas import DataFrame

from tidybear.selectors import _ColumnList
from tidybear.utils import get_column_names


def count(
    df: DataFrame,
    columns: _ColumnList,
    *,
    sort: bool = False,
    name: str = "n",
) -> DataFrame:
    """Quickly count the unique values of one or more variables.

    Parameters
    ----------
    df : DataFrame
        The dataframe to use
    columns : str, TidySelectors, or list or str, TidySelectors
        The column(s) to group by.
    sort : bool
        If True, will show the largest groups at the top, by default False
    name: str
        What to rename the new column with counts. By default "n" is used.
    """

    groupby_cols = get_column_names(df.columns, columns)
    counts = df.groupby(groupby_cols).size().rename(name).reset_index()

    if sort:
        return counts.sort_values(name, ascending=False)
    else:
        return counts.sort_values(columns)
