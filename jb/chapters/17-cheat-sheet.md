# Cheat sheet

The NumPy and pandas forms that this book teaches, on one page. Each table gives the forms of one chapter, with
the chapter's number and title, and what each form means in one line. In the tables, `a` stands for a NumPy array,
`s` for a pandas Series, `df` for a DataFrame, `mask` for a Boolean mask and `totals` for a grouped result, such as
`sales.groupby("store")["revenue"].sum()`. `rename`, `drop`, `dropna`, `fillna`, `reset_index`, `sort_values` and
`get_dummies` return a new table (or a new column): assign the result. The examples use the book's data files (see
the appendix *The datasets*). When something fails, see the appendix *Common errors and how to fix them*.

> **In Thonny:** a notebook shows the value of the last line of a cell; a script shows only what you print. Write
> `print(df.head())` where Colab needs only `df.head()`.

## NumPy: creating arrays

Chapter 3, *From lists to NumPy arrays*.

| Form | Meaning |
|---|---|
| `import numpy as np` | Load NumPy, with the short name `np` |
| `np.array([19.99, 5.49, 3.00])` | An array from a list; it holds values of one type |
| `np.arange(5)`, `np.arange(1, 13)` | The whole numbers from the start up to the stop, **without** the stop |
| `type(a)`, `len(a)`, `a.size` | The type of the object; the number of values |
| `a.dtype` | The type of the values: `int64`, `float64`, `bool`, ... |
| `a.tolist()` | The values as a Python list |
| `prices * 1.08` | Each value times 1.08 (no loop) |
| `a + b`, `a * 2` | Add element by element; double each value (for lists: join; repeat) |

## NumPy: indexing, slicing and arithmetic

Chapter 4, *Indexing, slicing and arithmetic*.

| Form | Meaning |
|---|---|
| `a[0]`, `a[-1]` | The first value; the last value |
| `a[1:4]`, `a[:3]`, `a[::2]` | Positions 1 to 3 (the end is not included); the first 3; every second value |
| `a[0] = 25` | Change a value (a float put into an int array is cut) |
| `part = a[1:4].copy()` | A slice is a view of the original; `.copy()` makes it separate |
| `units * prices` | Element by element, for two arrays of the same length |
| `np.round(a, 2)`, `np.sqrt(a)`, `np.abs(a)` | Round to 2 decimals; square root; absolute value, for each value |

## NumPy: masks and summaries

Chapter 5, *Comparisons and Boolean masks*.

| Form | Meaning |
|---|---|
| `prices > 50` | A mask: an array of `True`/`False` (dtype `bool`) |
| `prices[prices > 50]` | The values where the mask is `True` |
| `(a > 1) & (a < 5)`, `(a < 1) \| (a > 5)`, `~mask` | And, or, not; the parentheses are needed (not `and`, `or`, `not`) |
| `a.sum()`, `a.mean()`, `a.min()`, `a.max()`, `np.median(a)` | The total, average, smallest, largest and middle value |
| `a.argmax()` | The position of the largest value |
| `mask.sum()`, `mask.mean()` | How many values are `True`; the share that is `True` |

## NumPy: two-dimensional arrays

Chapter 6, *Two-dimensional arrays*.

| Form | Meaning |
|---|---|
| `np.array([[5, 7, 6], [3, 4, 8]])` | A table of numbers: a list of rows |
| `a.shape`, `a.ndim` | (rows, columns); the number of dimensions |
| `a[1, 2]` | The value in row 1, column 2 |
| `a[1]` or `a[1, :]`; `a[:, 2]` | A whole row; a whole column |
| `a[0:2, 1:4]` | Rows 0 and 1, columns 1 to 3 |
| `a.sum(axis=0)` | One result for each column ("down the rows") |
| `a.sum(axis=1)` | One result for each row; `mean` and `max` take `axis` too |
| `df.to_numpy()` | The NumPy array inside a DataFrame or Series |

## pandas: Series and DataFrames

Chapter 7, *Series and DataFrames*.

| Form | Meaning |
|---|---|
| `import pandas as pd` | Load pandas, with the short name `pd` |
| `pd.Series([120, 95], index=["S1", "S2"], name="sales")` | One column of values with labels (the index) |
| `s.to_numpy()` (`s.values` in older code), `s.index` | The values as an array; the labels |
| `s["S2"]` | The value with the label `S2` |
| `pd.DataFrame({"city": [...], "sales": [...]})` | A table from a dictionary of lists, one list for each column |
| `df["sales"]` | One column, as a Series |
| `df[["city", "sales"]]` | Several columns, as a DataFrame (double brackets) |
| `df.columns`, `df.index`, `df.shape`, `len(df)` | The column names; the row labels; (rows, columns); the number of rows |
| `df.dtypes` | The type of each column (text is `object`, or `str` in pandas 3) |

## pandas: reading and describing data

Chapter 8, *Reading and describing data*.

| Form | Meaning |
|---|---|
| `DATA_URL = "https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/"` | The address of the book's data folder |
| `sales = pd.read_csv(DATA_URL + "sales.csv")` | Read a CSV file into a DataFrame |
| `df.head()`, `df.head(10)`, `df.tail()` | The first 5 rows; the first 10; the last 5 |
| `df.info()` | Rows, columns, non-null counts and dtypes (it prints itself) |
| `df.describe()` | Count, mean, std, min, quartiles and max of the number columns |
| `df["region"].unique()`, `df["region"].nunique()` | The different values of a column; how many there are |

## pandas: selecting with loc and iloc

Chapter 9, *Selecting with loc and iloc*.

| Form | Meaning |
|---|---|
| `df = df.set_index("store")` | Use a column as the row labels |
| `df.loc["S3"]`, `df.loc["S3", "employees"]` | A row by its label; one value by row and column labels |
| `df.loc[["S1", "S4"], ["city", "sales"]]` | Some rows and some columns, by labels |
| `df.loc["S2":"S4"]` | Rows by labels, **including** the end |
| `df.iloc[0]`, `df.iloc[0, 2]` | A row by its position; one value by positions |
| `df.iloc[1:3]`, `df.iloc[:, 0:2]` | Rows by positions, **without** the end; the first two columns |
| `df.loc["S3", "employees"] = 25` | Change one value |

## pandas: filtering rows

Chapter 10, *Filtering rows*.

| Form | Meaning |
|---|---|
| `sales["units"] > 10` | A Boolean Series: a mask with one `True`/`False` for each row |
| `sales[sales["units"] > 10]` | The rows where the mask is `True` |
| `mask.sum()`, `len(sales[mask])` | How many rows match |
| `(sales["units"] > 10) & (sales["region"] == "North")` | Both conditions; `\|` for either, `~` for not |
| `sales["store"].isin(["S1", "S2"])` | `True` where the value is one of the list |
| `sales.loc[mask, ["date", "store", "units"]]` | The matching rows, and only these columns |
| `sales2 = sales.copy()` | A separate copy to change |
| `sales2.loc[mask, "discount"] = 0.5` | Change a column in the matching rows (never `sales2[mask]["discount"] = 0.5`) |

## pandas: new columns and sorting

Chapter 11, *New columns and sorting*.

| Form | Meaning |
|---|---|
| `sales["revenue"] = sales["units"] * sales["price"] * (1 - sales["discount"])` | A new column from other columns |
| `sales["revenue"] = sales["revenue"].round(2)` | Round each value to 2 decimals |
| `sales["month"] = sales["date"].str[:7]` | The first 7 characters of each text value |
| `sales["size"] = "small"`, then `sales.loc[sales["units"] >= 8, "size"] = "large"` | A column from a condition |
| `df = df.rename(columns={"units": "quantity"})` | Rename columns |
| `df = df.drop(columns=["discount"])` | Remove columns |
| `sales.sort_values("revenue", ascending=False)` | Sort the rows, the largest first |
| `sales.sort_values(["store", "revenue"])` | Sort by store, then by revenue within each store |
| `sales.sort_values("revenue", ascending=False).head()` | The top 5 |
| `df = df.reset_index(drop=True)` | Number the rows 0, 1, 2, ... again |
| `sales.nlargest(5, "revenue")` | The 5 rows with the largest revenue |

## pandas: grouping and charts

Chapter 12, *Grouping and summarizing*.

| Form | Meaning |
|---|---|
| `sales["store"].value_counts()` | How many rows have each value |
| `sales["store"].value_counts(normalize=True)` | The share of rows with each value |
| `sales.groupby("store")["revenue"].sum()` | The total revenue of each store; also `.mean()`, `.count()` |
| `sales.groupby("store").size()` | The number of rows in each group |
| `totals.sort_values(ascending=False)` | Sort a grouped result |
| `sales.groupby(["region", "category"])["revenue"].sum()` | One result for each pair of values |
| `sales.groupby("store")["revenue"].agg(["sum", "mean", "count"])` | Several summaries at once |
| `totals.reset_index()` | A grouped result back as a DataFrame |
| `import matplotlib.pyplot as plt` | Load matplotlib, for charts |
| `totals.plot(kind="bar")` | A bar chart of a Series |
| `monthly.plot(kind="line", marker="o")` | A line chart, with a dot for each value (`monthly` is the revenue of each month) |
| `plt.title("...")`, `plt.xlabel("...")`, `plt.ylabel("...")`, `plt.show()` | A title and axis labels; show the chart (always last) |

## pandas: preparing data for machine learning

Chapter 13, *Preparing data for machine learning*.

| Form | Meaning |
|---|---|
| `df.isna().sum()` | The number of missing values in each column |
| `df[df.isna().any(axis=1)]` | The rows with at least one missing value |
| `df = df.dropna()`, `df = df.dropna(subset=["age"])` | Drop the rows with a missing value (anywhere; in `age`) |
| `df["age"] = df["age"].fillna(df["age"].median())` | Fill the missing numbers with the median |
| `df["city"] = df["city"].fillna("Unknown")` | Fill the missing text with `"Unknown"` |
| `df = pd.get_dummies(df, columns=["region"], dtype=int)` | One 0/1 column for each value of a text column |
| `X = df.drop(columns="annual_spend")` | The predictors: every column but the target |
| `y = df["annual_spend"]` | The target: one column |
| `X.isna().sum().sum() == 0` | `True` when `X` has no missing value |
| `X.dtypes`, `X.shape`, `y.shape` | All number columns? The same number of rows in `X` and `y`? |
| `X.to_numpy()` | The 2-D NumPy array inside `X` (as in chapter 6) |

## The model code

Chapter 1, *A first machine-learning example*, and the projects of chapters 14 and 15. `X` and `y` must be ready:
numbers only, no missing values.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

models = [("linear regression", LinearRegression()),
          ("decision tree", DecisionTreeRegressor(max_depth=5, random_state=42)),
          ("random forest", RandomForestRegressor(n_estimators=200, random_state=42))]
for name, model in models:
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(name, mean_absolute_error(y_test, predictions))
```

| Form | Meaning |
|---|---|
| `train_test_split(X, y, test_size=0.25, random_state=42)` | 75% of the rows to learn from, 25% to test on, the same split each time |
| `model.fit(X_train, y_train)` | The model learns from the training set |
| `model.predict(X_test)` | One prediction for each test row |
| `mean_absolute_error(y_test, predictions)` | The MAE: the average size of the errors, in the units of the target |
| `model.intercept_`, `model.coef_` | The `a` and the `b` values that `LinearRegression` learned (chapter 2, *What does a model learn?*) |
