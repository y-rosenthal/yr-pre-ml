# The datasets

The chapters use four data files. They are made up, but realistic: a script makes them with fixed random numbers,
so they are the same for everyone. Some values are missing on purpose, because real data has missing values too.

Each chapter reads a file from the book's GitHub repository:

```python
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/"
customers = pd.read_csv(DATA_URL + "customers.csv")
```

To use a file without internet (for example in Thonny), open its link below, save it next to your script, and read
it by its name: `pd.read_csv("customers.csv")`.

## customers.csv

[customers.csv](https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/customers.csv): 500 members of a
store chain's loyalty program, one row for each member.

| Column | Meaning | Values |
|---|---|---|
| `age` | The member's age, in years | 18 to 75; 14 values are missing |
| `region` | The region of the member's store (text) | `North`, `South`, `East`, `West` |
| `months_as_customer` | How long the person has been a member, in months | 1 to 120 |
| `visits_per_month` | The average number of store visits per month | 0.6 to 12.0 |
| `avg_basket` | The average amount spent per visit, in dollars | about 12 to 97; 11 values are missing |
| `annual_spend` | The amount spent last year, in dollars: **the target** | about 260 to 11,500 |

## sales.csv

[sales.csv](https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/sales.csv): 2,000 sales in the eight
stores of a chain during one year, one row for each sale, in date order. No values are missing.

| Column | Meaning | Values |
|---|---|---|
| `date` | The day of the sale (text, `YYYY-MM-DD`) | `2025-01-01` to `2025-12-31` |
| `store` | The store (text) | `S1` to `S8` |
| `region` | The region of the store (text) | `North` (S1, S2), `South` (S3, S4), `East` (S5, S6), `West` (S7, S8) |
| `category` | The product category (text) | `Grocery`, `Clothing`, `Home`, `Electronics` |
| `units` | The number of units sold | 1 to 16 |
| `price` | The price of one unit before the discount, in dollars | 1.99 to 597.99 |
| `discount` | The discount, as a fraction of the price | `0.0`, `0.05`, `0.1`, `0.2` |

The revenue of a sale is `units * price * (1 - discount)`.

## deliveries.csv

[deliveries.csv](https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/deliveries.csv): 500 deliveries
of a food-delivery company, one row for each delivery.

| Column | Meaning | Values |
|---|---|---|
| `distance_km` | The distance from the restaurant to the customer, in kilometers | 0.4 to 17.5 |
| `items` | The number of items in the order | 1 to 12 |
| `time_of_day` | When the order was placed (text) | `Morning`, `Afternoon`, `Evening` |
| `weather` | The weather during the delivery (text) | `Clear`, `Rain`, `Snow`; 18 values are missing |
| `driver_years` | The driver's experience, in years | 0 to 15; 30 values are missing |
| `minutes` | How long the delivery took, in minutes: **the target** | about 6 to 75 |

## marketing.csv

[marketing.csv](https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/marketing.csv): the weekly sales of
one product in four regions, for 130 weeks (520 rows), with the advertising of each week.

| Column | Meaning | Values |
|---|---|---|
| `region` | The sales region (text) | `North`, `South`, `East`, `West` (130 rows each) |
| `tv_spend` | Money spent on TV advertising that week, in thousands of dollars | 0.1 to 50.0 |
| `online_spend` | Money spent on online advertising that week, in thousands of dollars | 0.0 to 19.9; 26 values are missing |
| `price` | The product's price that week, in dollars | 8.00 to 15.00 |
| `promotion` | Whether a store promotion ran that week (text) | `Yes`, `No`; 12 values are missing |
| `units_sold` | The number of units sold that week: **the target** | about 100 to 810 |

## How the files are made

The script [`data/make_data.py`](https://github.com/y-rosenthal/yr-pre-ml/blob/main/data/make_data.py) in the book's
repository makes all four files. It is a good example of NumPy and pandas at work, once you have read the book.
