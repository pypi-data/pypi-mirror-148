from __future__ import annotations

from typing import Any
from typing import List
from typing import Optional

import pandas as pd

from tidybear.selectors import _ColumnList
from tidybear.utils import get_column_names


class GroupBy:
    """Simplified API for performing groupby and summarise opperations in pandas.

    Parameters
    ----------
    df : DataFrame
        The dataframe to group.
    groups : str, List[str]
        Used to determine the groups for the groupby.

    Properties
    ----------
    groups : str, List[str]
        The grouping variables that were used.
    <df_columns> :
        You can access the columns of the DataFrameGroupBy object using the 'dot' syntax.
        To get the grouped columns with the string name, use `get` method.

    Functions
    ----------
    size : get group sizes
    get : get the grouped column by name
    summarise or summarize : cocatenate all active stats into a single dataframe.

    Examples
    ----------
    ```
    >>> import pandas as pd
    >>> import tidybear as tb
    >>>
    >>> df = pd.DataFrame({
    ...     "gr": list("AAABBBB"),
    ...     "val": [1, 2, 3, 7, 8, 8, 9]
    ... })
    >>>
    >>> with tb.GroupBy(df, "gr") as g:
    ...     tb.Stat.size()
    ...     summary = g.summarise()
        n
    gr
    A   3
    B   4
    ```
    """

    def __init__(self, df: pd.DataFrame, groups: _ColumnList) -> None:
        """Creates an active grouping that can track and summarise provided Stats.
        Must be used within a with statement.

        Parameters
        ----------
        df : DataFrame
            The dataframe to group.
        groups : str, List[str]
            Used to determine the groups for the groupby
        """
        self.__groups = get_column_names(df.columns, groups)
        self.__groupby_obj = df.groupby(self.__groups)

        self.__stats: List[pd.Series] = []

    def __enter__(self) -> GroupBy:
        return self

    def __exit__(self, *args: Any) -> None:
        self.__stats = []

    @property
    def groups(self) -> List[str]:
        """Get the grouping variables

        Returns
        -------
        str, List[str]
        """
        return list(self.__groups)

    def get(self, column: str) -> pd.Series:
        """Access a grouped column by name

        Parameters
        ----------
        column : str
            The name of the column

        Returns
        -------
        pd.Series
            The grouped column
        """
        return self.__groupby_obj[column]

    def summarise(self) -> pd.DataFrame:
        """Concatenate all active stats into a single dataframe.
        It will naturally join on the grouped columns.

        ```
        return pd.concat(active_stats, axis=1)
        ```

        Returns
        -------
        pd.DataFrame
            Final summary of all stats
        """
        return pd.concat(self.__stats, axis=1)

    def summarize(self) -> pd.DataFrame:
        """Concatenate all active stats into a single dataframe.
        It will naturally join on the grouped columns.

        ```
        return pd.concat(active_stats, axis=1)
        ```

        Returns
        -------
        pd.DataFrame
            Final summary of all stats
        """
        return self.summarise()

    def __add_stat(self, name: str, series: pd.Series) -> pd.Series:
        self.__stats.append(series.rename(name))
        return series.rename(name)

    def stat(self, name: str, series: pd.Series) -> pd.Series:
        return self.__add_stat(name, series)

    def n(self, name: Optional[str] = None) -> pd.Series:
        """Compute group sizes."""
        name = "n" if not name else name
        return self.__add_stat(name, self.__groupby_obj.size())

    def agg(
        self,
        column: str,
        func: Any,
        decimals: Optional[int] = None,
        name: Optional[str] = None,
        name_prefix: Optional[str] = None,
    ) -> pd.Series:
        """Aggregate one or more columns using one or more operations.

        Parameters
        ----------
        func : function, str, or list
            Function(s) to use for aggregating the data. See pd.Series.agg for acceptable strings.
        column : str or list
            Name of column to aggregate
        decimals : int, optional
            Number of decimals to round to, by default None
        name : str, optional
            New name of series, by default None. If none and the function provided is a string
            the name will be "{func}_{column}".
            If multiple funcions are provided this parameter is ignored.
        name_prefix: str, optional
            If passing multiple columns to agg with a custom function you can pass
            name_prefix to help name the summary columns
        temp : bool, optional, by default False
            If False, the Stat is appended to the GroupBy.
            If True, no Stat is appended, and instead the renamed series
            is returned for further operation.

        Returns
        -------
        Series or NoneType
        """

        if isinstance(func, list):
            for f in func:
                self.agg(column, f, decimals=decimals)
            return

        if isinstance(column, list):
            for c in column:
                self.agg(c, func, decimals=decimals)
            return

        if not name:
            if isinstance(func, str):
                name = func + "_" + column
            elif name_prefix:
                name = name_prefix + "_" + column
            else:
                name = column

        agg = self.get(column).agg(func)

        if decimals is not None:
            agg = agg.round(decimals)

        return self.__add_stat(name, agg)

    def n_distinct(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute number of unique values in group."""
        if "name_prefix" not in kwargs:
            kwargs["name_prefix"] = "n_distinct"

        return self.agg(column, lambda x: len(x.unique()), **kwargs)

    def sum(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute sum of group values."""
        return self.agg(column, "sum", **kwargs)

    def mean(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute mean of group values."""
        return self.agg(column, "mean", **kwargs)

    def median(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute median of group values."""
        return self.agg(column, "median", **kwargs)

    def max(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute max of group values."""
        return self.agg(column, "max", **kwargs)

    def min(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute min of group values."""
        return self.agg(column, "min", **kwargs)

    def var(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute variance of group values."""
        return self.agg(column, "var", **kwargs)

    def std(self, column: str, **kwargs: Any) -> pd.Series:
        """Compute standard deviation of group values."""
        return self.agg(column, "std", **kwargs)

    def __str__(self) -> str:
        return f"GroupBy({self.groups})"
