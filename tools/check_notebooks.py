"""check_notebooks.py: the static checks of the book (fast; the standard library only; runs no notebook).

Usage: python tools/check_notebooks.py [NOTEBOOK ...] [-h | --help]

Without arguments it checks every page in jb/chapters/ and the table of contents. It prints OK, or one line for
each problem (exit status 1). The rules are in .claude/skills/notebook-conventions/SKILL.md.

For each notebook (jb/chapters/*.ipynb):
  - valid JSON, nbformat 4.5 or later, a kernelspec;
  - every cell has an id of 8 hexadecimal characters, and the ids are different;
  - no stored outputs: every code cell has "outputs": [] and "execution_count": null;
  - the first cell is markdown; its first line is "# TITLE"; it has the "Open in Colab" badge with the link to
    this notebook on main (BADGE below);
  - portability (Colab-first, but the code also runs in Thonny): no line that starts with % or !, no
    google.colab, no display(, no files.upload, no input(); read_csv reads only DATA_URL + "NAME.csv" or the
    full data URL; DATA_URL is DATA_PREFIX; each data file that a notebook reads exists in data/ (except in a cell tagged raises-exception, which may
    misspell a file name on purpose);
  - every <details> block is an answer: <details class="yr-answer"> with <summary>Answer</summary>, and a
    closing </details>;
  - a cell tagged raises-exception is a code cell.
For every page (notebooks and .md files in jb/chapters/, and jb/intro.md): no timing in the book (the words
"lecture" and "semester", or a season with a year); a link into the book's website (SITE + "chapters/NAME.html")
names a page that exists; the page is in jb/_toc.yml.
For jb/_toc.yml: every file that it names exists.
For the scripts in tools/ and data/: each has --help (it runs them with --help), except the files that are only
imported (NO_HELP).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "jb" / "chapters"
TOC = ROOT / "jb" / "_toc.yml"
DATA_PREFIX = "https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/"
SITE = "https://y-rosenthal.github.io/yr-pre-ml/"
SITE_LINK = re.compile(re.escape(SITE) + r"chapters/([\w.-]+?)\.html")
COLAB = "https://colab.research.google.com/github/y-rosenthal/yr-pre-ml/blob/main/jb/chapters/"
BADGE = "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](" + COLAB + "{name})"
NO_HELP = {"tools/localdata/sitecustomize.py"}
TIMING = re.compile(r"\b(lectures?|semesters?|(fall|spring|summer|winter)\s+(term\s+)?20\d\d)\b", re.IGNORECASE)
READ_CSV = re.compile(r"read_csv\(\s*([^,)]*)")
DATA_FILE = re.compile(r"""DATA_URL\s*\+\s*["']([^"']+)["']""")
NOT_PORTABLE = [(re.compile(r"google\.colab"), "google.colab"), (re.compile(r"\bdisplay\("), "display("),
                (re.compile(r"files\.upload"), "files.upload"), (re.compile(r"\binput\("), "input(")]


def check_notebook(path, problems):
    rel = path.relative_to(ROOT).as_posix()
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        problems.append(f"{rel}: not valid JSON ({err})")
        return
    if nb.get("nbformat") != 4 or nb.get("nbformat_minor", 0) < 5:
        problems.append(f"{rel}: nbformat must be 4.5 or later")
    if "kernelspec" not in nb.get("metadata", {}):
        problems.append(f"{rel}: no kernelspec in the notebook metadata")
    cells = nb.get("cells", [])
    if not cells:
        problems.append(f"{rel}: no cells")
        return
    ids = [c.get("id", "") for c in cells]
    for i, cid in enumerate(ids):
        if not re.fullmatch(r"[0-9a-f]{8}", cid or ""):
            problems.append(f"{rel}: cell {i}: the id {cid!r} is not 8 hexadecimal characters")
    if len(set(ids)) != len(ids):
        problems.append(f"{rel}: two cells have the same id")
    first = cells[0]
    first_src = "".join(first.get("source", []))
    if first.get("cell_type") != "markdown" or not re.match(r"# \S", first_src):
        problems.append(f'{rel}: the first cell must be markdown and start with "# TITLE"')
    if BADGE.format(name=path.name) not in first_src:
        problems.append(f"{rel}: the first cell has no Colab badge for this notebook: {BADGE.format(name=path.name)}")
    for i, cell in enumerate(cells):
        src = "".join(cell.get("source", []))
        tags = cell.get("metadata", {}).get("tags", [])
        if cell.get("cell_type") == "code":
            if cell.get("outputs") or cell.get("execution_count") is not None:
                problems.append(f"{rel}: cell {i}: stored outputs or an execution count (clear them)")
            for line in src.split("\n"):
                if line.lstrip().startswith(("%", "!")):
                    problems.append(f"{rel}: cell {i}: a magic or shell line does not run in Thonny: {line.strip()}")
            for pattern, what in NOT_PORTABLE:
                if pattern.search(src):
                    problems.append(f"{rel}: cell {i}: {what} does not run in Thonny, or not in the build")
            for arg in READ_CSV.findall(src):
                arg = arg.strip()
                if not (arg.startswith("DATA_URL") or arg.strip("\"'").startswith(DATA_PREFIX)):
                    problems.append(f'{rel}: cell {i}: read_csv must read DATA_URL + "NAME.csv": read_csv({arg}')
            for match in re.finditer(r"""DATA_URL\s*=\s*["']([^"']*)["']""", src):
                if match.group(1) != DATA_PREFIX:
                    problems.append(f'{rel}: cell {i}: DATA_URL must be "{DATA_PREFIX}"')
            for name in DATA_FILE.findall(src) + re.findall(re.escape(DATA_PREFIX) + r"([\w.-]+)", src):
                if not (ROOT / "data" / name).is_file() and "raises-exception" not in tags:
                    problems.append(f"{rel}: cell {i}: data/{name} does not exist")
        else:
            if "raises-exception" in tags:
                problems.append(f"{rel}: cell {i}: the tag raises-exception is for code cells only")
            opened = re.findall(r"<details\b[^>]*>", src)
            for tag in opened:
                if tag != '<details class="yr-answer">':
                    problems.append(f'{rel}: cell {i}: an answer starts with <details class="yr-answer">, not {tag}')
            if len(opened) != src.count("</details>"):
                problems.append(f"{rel}: cell {i}: each <details> needs one </details>")
            if len(opened) != src.count("<summary>Answer</summary>"):
                problems.append(f"{rel}: cell {i}: each answer needs <summary>Answer</summary>")
            check_timing(rel, f"cell {i}: ", src, problems)


def check_timing(rel, where, text, problems):
    """No timing words (D4), and every link into the book's website names a page that exists."""
    for match in TIMING.finditer(text):
        problems.append(f"{rel}: {where}no timing in the book (D4): {match.group(0)!r}")
    for name in SITE_LINK.findall(text):
        if not any((CHAPTERS / (name + ext)).is_file() for ext in (".ipynb", ".md")):
            problems.append(f"{rel}: {where}the link to {SITE}chapters/{name}.html names no page in jb/chapters/")


def toc_files():
    return re.findall(r"^\s*-?\s*file:\s*(\S+)\s*$", TOC.read_text(encoding="utf-8"), flags=re.MULTILINE)


def check_toc(pages, problems):
    listed = toc_files()
    for name in listed:
        if not any((ROOT / "jb" / (name + ext)).is_file() for ext in ("", ".md", ".ipynb")):
            problems.append(f"jb/_toc.yml: the file {name} does not exist")
    for page in pages:
        name = page.relative_to(ROOT / "jb").with_suffix("").as_posix()
        if name not in listed:
            problems.append(f"{page.relative_to(ROOT).as_posix()}: not in jb/_toc.yml")


def check_help(problems):
    scripts = sorted(list((ROOT / "tools").rglob("*.py")) + list((ROOT / "tools").rglob("*.sh"))
                     + list((ROOT / "data").glob("*.py")))
    for script in scripts:
        rel = script.relative_to(ROOT).as_posix()
        if rel in NO_HELP:
            continue
        command = (["bash", str(script)] if script.suffix == ".sh" else [sys.executable, str(script)]) + ["--help"]
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=60, cwd=ROOT)
        except subprocess.TimeoutExpired:
            problems.append(f"{rel}: --help did not finish in 60 seconds")
            continue
        if run.returncode != 0 or not run.stdout.strip():
            problems.append(f"{rel}: --help must print the help and exit with status 0")


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    problems = []
    if argv:
        notebooks = [Path(a).resolve() for a in argv]
    else:
        notebooks = sorted(CHAPTERS.glob("*.ipynb"))
        pages = notebooks + sorted(CHAPTERS.glob("*.md"))
        for page in sorted(CHAPTERS.glob("*.md")):
            check_timing(page.relative_to(ROOT).as_posix(), "", page.read_text(encoding="utf-8"), problems)
        check_toc(pages, problems)
        check_help(problems)
        check_timing("jb/intro.md", "", (ROOT / "jb" / "intro.md").read_text(encoding="utf-8"), problems)
    for nb in notebooks:
        check_notebook(nb, problems)
    for problem in problems:
        print(problem)
    if problems:
        print(f"{len(problems)} problem(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
