# TidyBear

A tidier approach to pandas.

This package was originally a collection of functions, routines, and processes that I found myself often repeating. It has since evolved into a desire to work my way through the tidyverse to reimplement my favorite tidy features in python. This project is not aimed at creating a _better_ experience for every pandas task, but rather just a different one that sometimes feels more natural to me. I hope something here can be useful to you.

## Installation

```bash
pip install tidybear
```

## Usage

```python
import pandas as pd
import tidybear as tb
```

### Verbs

```python
# rename columns
tb.rename(data, old="new")

# select columns
tb.select(data, ["col1", "col2"])

# count number of rows across multiple columns
tb.count(data, ["col1", "col2"])

# pivot long to wide or wide to long
tb.pivot_longer(data, ["val1", "val2"], names_to="val_type")
tb.pivot_wider(data, names_from="val_type", values_from="value")

# slice rows
tb.slice_max(data, order_by="val1", n=10)
tb.slice_min(data, order_by="val1", n=10, groupby="col1")

# join dataframes
tb.left_join(data1, data2, "colA") #  use "colA" as key
tb.right_join(data1, data2, col1A="col1B") #  use "col1A" from left and "col1B" from right

tb.cross_join(data1, data2)
```

#### Groupby and Summarise API

```python
with tb.GroupBy(df, "group_var") as g:
    g.n()
    g.sum("value", name="total_value")
    g.n_distinct("ids", name="n_unique_ids")

    summary = g.summarise()
```

### TidySelectors

- `everything()` - Select all columns
- `last_col` - Select last column
- `first_col` - Select first column
- `contains(pattern)` - Select columns that contain the literal string
- `matches(pattern)` - Select columns that match the regular expression pattern
- `starts_with(pattern)` - Select columns that start with the literal string
- `ends_with` - Select all columns that end with the literal srting
- `num_range` - Select all columns that match a numeric range like x01, x02, x03

These can be used in a variety of tidybear verbs

```python
from tidybear.selectors import contains, everything

# select all columns that contain "foo"
tb.select(data, contains("foo"))

# pivot all columns to long format
tb.pivot_longer(data, everything())
```

You can also negate these, so if you wanted everything except one columns, you could do:

```python
from tidybear.selectors import last_col

tb.select(data, -last_col())
```

## Coming Soon (maybe)

- Method chaining
- Tribbles!
