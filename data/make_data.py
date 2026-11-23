"""make_data.py: write the book's datasets (CSV files), made up but realistic, with fixed random seeds.

Usage: python data/make_data.py [--out DIR] [--check] [-h | --help]

  --out DIR   the folder for the CSV files (default: the folder of this script, data/)
  --check     write the files into a temporary folder (in jb/_build/) and compare them with the files in data/. Print OK, or
              the names of the files that differ (exit status 1). Changes nothing in data/.
  -h, --help  show this help and stop

The files (jb/chapters/18-datasets.md describes each column):
  customers.csv    500 customers of a store chain; the target is annual_spend; some values are missing
  sales.csv        2,000 sales of eight stores in one year; no missing values
  deliveries.csv   500 food deliveries; the target is minutes; some values are missing (numbers and text)
  marketing.csv    520 weeks of sales in four regions; the target is units_sold; some values are missing

Each file has its own seed, so a change to one file does not change the others. The script uses
numpy.random.RandomState, whose numbers stay the same in every NumPy version, and it rounds every number before
it writes it. So the files are the same on every computer.
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def add_missing(rs, df, column, count):
    """Set COUNT values of COLUMN to missing (NaN), in rows chosen at random."""
    rows = rs.choice(len(df), size=count, replace=False)
    df.loc[rows, column] = np.nan


def customers():
    rs = np.random.RandomState(101)
    n = 500
    region = rs.choice(["North", "South", "East", "West"], size=n, p=[0.3, 0.25, 0.25, 0.2])
    age = rs.randint(18, 76, size=n)
    months = rs.randint(1, 121, size=n)
    visits = np.round(np.clip(rs.gamma(2.0, 1.6, size=n) + 0.5, 0.5, 12.0), 1)
    basket = np.round(np.clip(rs.normal(42, 14, size=n), 8, None) + (age - 18) * 0.35, 2)
    region_factor = pd.Series(region).map({"North": 1.05, "South": 0.95, "East": 1.0, "West": 1.1}).to_numpy()
    spend = 12 * visits * basket * region_factor * (1 + months / 300) * rs.normal(1.0, 0.08, size=n)
    df = pd.DataFrame({
        "age": age.astype(float),
        "region": region,
        "months_as_customer": months,
        "visits_per_month": visits,
        "avg_basket": basket,
        "annual_spend": np.round(spend, 2),
    })
    add_missing(rs, df, "age", 14)
    add_missing(rs, df, "avg_basket", 11)
    return df


def sales():
    rs = np.random.RandomState(202)
    n = 2000
    stores = {"S1": "North", "S2": "North", "S3": "South", "S4": "South",
              "S5": "East", "S6": "East", "S7": "West", "S8": "West"}
    categories = {  # category: (lowest price, highest price, average units)
        "Grocery": (2, 15, 6), "Clothing": (10, 80, 2.5), "Home": (5, 120, 1.8), "Electronics": (25, 600, 0.6)}
    days = pd.date_range("2025-01-01", "2025-12-31", freq="D").strftime("%Y-%m-%d")
    date = np.sort(rs.choice(days, size=n))
    store = rs.choice(list(stores), size=n)
    category = rs.choice(list(categories), size=n, p=[0.4, 0.25, 0.2, 0.15])
    low = np.array([categories[c][0] for c in category])
    high = np.array([categories[c][1] for c in category])
    mean_units = np.array([categories[c][2] for c in category])
    price = np.round(np.round(low + rs.random_sample(n) * (high - low)) - 0.01, 2)
    units = rs.poisson(mean_units) + 1
    discount = rs.choice([0.0, 0.0, 0.0, 0.05, 0.1, 0.2], size=n)
    return pd.DataFrame({
        "date": date,
        "store": store,
        "region": [stores[s] for s in store],
        "category": category,
        "units": units,
        "price": price,
        "discount": discount,
    })


def deliveries():
    rs = np.random.RandomState(303)
    n = 500
    distance = np.round(rs.gamma(2.0, 2.4, size=n) + 0.3, 1)
    items = rs.randint(1, 13, size=n)
    time_of_day = rs.choice(["Morning", "Afternoon", "Evening"], size=n, p=[0.25, 0.35, 0.4])
    weather = rs.choice(["Clear", "Rain", "Snow"], size=n, p=[0.6, 0.3, 0.1])
    driver_years = rs.randint(0, 16, size=n).astype(float)
    time_extra = pd.Series(time_of_day).map({"Morning": 0, "Afternoon": 3, "Evening": 6}).to_numpy()
    weather_extra = pd.Series(weather).map({"Clear": 0, "Rain": 5, "Snow": 12}).to_numpy()
    minutes = (10 + 3.2 * distance + 0.8 * items + time_extra + weather_extra
               - 0.5 * np.minimum(driver_years, 10) + rs.normal(0, 4, size=n))
    df = pd.DataFrame({
        "distance_km": distance,
        "items": items,
        "time_of_day": time_of_day,
        "weather": weather,
        "driver_years": driver_years,
        "minutes": np.round(np.clip(minutes, 5, None), 1),
    })
    add_missing(rs, df, "driver_years", 30)
    add_missing(rs, df, "weather", 18)
    return df


def marketing():
    rs = np.random.RandomState(404)
    regions = ["North", "South", "East", "West"]
    weeks = 130
    n = weeks * len(regions)
    region = np.repeat(regions, weeks)
    tv = np.round(rs.uniform(0, 50, size=n), 1)
    online = np.round(rs.uniform(0, 20, size=n), 1)
    price = np.round(rs.uniform(8, 15, size=n), 2)
    promotion = rs.choice(["Yes", "No"], size=n, p=[0.3, 0.7])
    region_extra = pd.Series(region).map({"North": 40, "South": 0, "East": 20, "West": 60}).to_numpy()
    units = (300 + 6 * tv + 14 * online - 18 * price + np.where(promotion == "Yes", 70, 0)
             + region_extra + rs.normal(0, 35, size=n))
    df = pd.DataFrame({
        "region": region,
        "tv_spend": tv,
        "online_spend": online,
        "price": price,
        "promotion": promotion,
        "units_sold": np.round(np.clip(units, 0, None)).astype(int),
    })
    add_missing(rs, df, "online_spend", 26)
    add_missing(rs, df, "promotion", 12)
    return df


MAKERS = {"customers.csv": customers, "sales.csv": sales, "deliveries.csv": deliveries, "marketing.csv": marketing}


def write_all(folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    for name, make in MAKERS.items():
        make().to_csv(folder / name, index=False)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if "--check" in argv:
        scratch = HERE.parent / "jb" / "_build"     # inside the repository; git ignores it
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as tmp:
            write_all(tmp)
            differ = [name for name in MAKERS
                      if not (HERE / name).is_file() or (Path(tmp) / name).read_bytes() != (HERE / name).read_bytes()]
        if differ:
            print("make_data.py --check: these files differ from what the script writes (run "
                  "python data/make_data.py): " + ", ".join(differ))
            return 1
        print("OK")
        return 0
    out = HERE
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            print("make_data.py: --out needs a folder", file=sys.stderr)
            return 2
        out = Path(argv[i + 1])
    write_all(out)
    print(f"wrote {', '.join(MAKERS)} in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
