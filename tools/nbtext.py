"""nbtext.py: convert a chapter between a notebook (.ipynb) and a plain-text cell file, for drafting and editing.

Usage:
  python tools/nbtext.py to-ipynb TEXT_FILE NOTEBOOK     make NOTEBOOK (nbformat 4.5, no outputs) from TEXT_FILE
  python tools/nbtext.py to-text NOTEBOOK TEXT_FILE      write the cells of NOTEBOOK into TEXT_FILE
  python tools/nbtext.py -h | --help                     show this help and stop

The notebook in jb/chapters/ is the source of the book. A text file is only a working copy: write it, convert
it, and do not commit it.

The text format: a line that starts with "%% " begins a new cell. The rest of the file, up to the next such
line, is the cell's source.
  %% md                                 a markdown cell
  %% code                               a code cell
  %% code tags=raises-exception         a code cell with tags (comma-separated, no spaces)
Blank lines at the start and the end of a cell are removed. A line in a cell cannot start with "%% ".

Cell ids: the cell's position, hashed with the notebook's file name (8 hexadecimal characters), so the same
text file always gives the same notebook. Stdlib only.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HEADER = re.compile(r"^%% (md|code)(?: tags=([\w,-]+))?\s*$")

METADATA = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}


def cell_id(name, index):
    return hashlib.sha1(f"{name}:{index}".encode()).hexdigest()[:8]


def source_lines(text):
    lines = text.split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]] if text else []


def to_ipynb(text_file, notebook):
    cells, current = [], None
    for number, line in enumerate(Path(text_file).read_text(encoding="utf-8").split("\n"), start=1):
        match = HEADER.match(line)
        if match:
            current = {"kind": match.group(1), "tags": match.group(2).split(",") if match.group(2) else [],
                       "lines": []}
            cells.append(current)
        elif line.startswith("%% "):
            raise SystemExit(f"nbtext.py: {text_file}:{number}: unknown cell header: {line}")
        elif current is None:
            if line.strip():
                raise SystemExit(f"nbtext.py: {text_file}:{number}: text before the first cell header")
        else:
            current["lines"].append(line)
    name = Path(notebook).name
    out = []
    for index, cell in enumerate(cells):
        text = "\n".join(cell["lines"]).strip("\n")
        if cell["kind"] == "md":
            out.append({"cell_type": "markdown", "id": cell_id(name, index), "metadata": {},
                        "source": source_lines(text)})
        else:
            out.append({"cell_type": "code", "execution_count": None, "id": cell_id(name, index),
                        "metadata": {"tags": cell["tags"]}, "outputs": [], "source": source_lines(text)})
    nb = {"cells": out, "metadata": METADATA, "nbformat": 4, "nbformat_minor": 5}
    Path(notebook).write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {notebook} ({len(out)} cells)")


def to_text(notebook, text_file):
    nb = json.loads(Path(notebook).read_text(encoding="utf-8"))
    parts = []
    for cell in nb["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            parts.append("%% md\n" + source)
        else:
            tags = cell.get("metadata", {}).get("tags", [])
            parts.append("%% code" + (" tags=" + ",".join(tags) if tags else "") + "\n" + source)
    Path(text_file).write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {text_file} ({len(parts)} cells)")


def main(argv):
    if not argv or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if len(argv) != 3 or argv[0] not in ("to-ipynb", "to-text"):
        print("nbtext.py: give to-ipynb TEXT_FILE NOTEBOOK, or to-text NOTEBOOK TEXT_FILE (--help)", file=sys.stderr)
        return 2
    (to_ipynb if argv[0] == "to-ipynb" else to_text)(argv[1], argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
