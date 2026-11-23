"""Make the book's data URLs read the CSV files in this repository's data/ folder, when the book is built or checked.

The chapters read their data from GitHub, for example
pd.read_csv("https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/customers.csv"). A new or changed
CSV file is not at that address until it is pushed to main, and GitHub caches the old file for some minutes.

tools/build_book.sh and tools/run_as_script.py put this folder on PYTHONPATH. Python then imports this file when
it starts. It replaces urllib.request.urlopen, which pandas.read_csv uses for a URL: a URL that starts with
DATA_PREFIX opens the file of the same name in data/ instead. Other URLs do not change. Students never use this
file. It is only imported (no --help).
"""
import pathlib
import urllib.error
import urllib.request

DATA_PREFIX = "https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/"
DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / "data"

_original_urlopen = urllib.request.urlopen


def _urlopen(url, *args, **kwargs):
    address = url.full_url if isinstance(url, urllib.request.Request) else url
    if isinstance(address, str) and address.startswith(DATA_PREFIX):
        path = DATA_DIR / address[len(DATA_PREFIX):]
        if not path.is_file():
            # The same error that GitHub gives for a file that does not exist, so the book shows what students see.
            raise urllib.error.HTTPError(address, 404, "Not Found", None, None)
        return _original_urlopen(path.as_uri())
    return _original_urlopen(url, *args, **kwargs)


urllib.request.urlopen = _urlopen
