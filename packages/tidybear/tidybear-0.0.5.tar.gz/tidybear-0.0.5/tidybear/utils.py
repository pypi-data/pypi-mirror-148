from typing import Iterable
from typing import List
from typing import Sequence
from typing import Union

from tidybear.selectors import _ColumnList
from tidybear.selectors import TidySelector


def get_column_name(
    cols: Iterable[str], to_select: Union[str, TidySelector]
) -> Sequence[str]:
    if isinstance(to_select, str):
        return [to_select]

    return to_select(cols)


def get_column_names(cols: Iterable[str], to_select: _ColumnList) -> Sequence[str]:

    if isinstance(to_select, str) or isinstance(to_select, TidySelector):
        return get_column_name(cols, to_select)

    selected: List[str] = []
    for item in to_select:
        selected.extend(get_column_name(cols, item))

    return selected
