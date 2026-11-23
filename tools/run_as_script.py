"""run_as_script.py: run each chapter as a plain Python script, as Thonny runs it, and run the code of every answer.

Usage: python tools/run_as_script.py [NOTEBOOK ...] [--python PYTHON] [--no-answers] [--keep DIR] [-v]
                                     [-h | --help]

  NOTEBOOK         the notebooks to run (default: every jb/chapters/*.ipynb)
  --python PYTHON  the Python that runs the scripts (default: the Python that runs this script). Give the Python
                   of another environment to check other package versions, for example .venv-newest/bin/python
  --no-answers     do not run the code of the answers
  --keep DIR       write the scripts into DIR (default: jb/_build/scripts, which git ignores; the scripts stay
                   there after the run, for a look at what ran)
  -v               print the output of each script
  -h, --help       show this help and stop

The Thonny check: the book is Colab-first, and the only change for Thonny is "wrap the last line of a cell in
print()". To prove it, the script of a notebook is its code cells, in order, with one change in each cell: when
the last statement is an expression, its value is printed (if it is not None), as Colab shows it. A cell tagged
raises-exception shows an error on purpose: the script catches that error and goes on. No IPython runs: a magic,
display() or any other Jupyter-only code fails here.

The answers check: after the chapter's code, the script runs the Python code blocks (```python) of each answer
(<details class="yr-answer">) in a copy of the chapter's variables, one answer after the other.

The scripts run with MPLBACKEND=Agg (plt.show() opens no window) and with tools/localdata on PYTHONPATH (the
data URLs read data/; see tools/localdata/sitecustomize.py). It prints OK and the counts, or the problems (exit
status 1). Warnings that the code prints (for example FutureWarning) are listed as notes; they do not fail.
"""
import ast
import json
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANSWER = re.compile(r'<details class="yr-answer">(.*?)</details>', re.DOTALL)
CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)

PRELUDE = '''\
import copy as __copy
import warnings as __warnings
__warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive")
def __show(value):
    if value is not None:
        print(value)
'''

ANSWERS_RUNNER = '''
def __copy_value(value):
    if type(value).__module__.split(".")[0] in ("pandas", "numpy") and hasattr(value, "copy"):
        return value.copy()
    if isinstance(value, (list, dict, set)):
        try:
            return __copy.deepcopy(value)
        except Exception:
            return value
    return value

__chapter = {k: v for k, v in globals().items() if not k.startswith("__") or k == "__builtins__"}
__chapter["__show"] = __show
for __label, __code in __ANSWERS:
    __ns = {k: __copy_value(v) for k, v in __chapter.items()}
    print("@@answer " + __label)
    try:
        exec(compile(__code, __label, "exec"), __ns)
    except Exception as __error:
        print("@@answer-failed " + __label + ": " + type(__error).__name__ + ": " + str(__error))
'''


def as_script_code(code, tags, where):
    """CODE with the value of its last expression printed; a cell tagged raises-exception catches its error."""
    try:
        tree = ast.parse(code)
    except SyntaxError as err:
        raise ValueError(f"{where}: not plain Python, so it does not run in Thonny ({err.msg}, line {err.lineno})")
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = tree.body[-1]
        tree.body[-1] = ast.Expr(ast.Call(ast.Name("__show", ast.Load()), [last.value], []))
        ast.fix_missing_locations(tree)
    source = ast.unparse(tree) or "pass"
    if "raises-exception" in tags:
        source = ("try:\n" + textwrap.indent(source, "    ") +
                  "\nexcept Exception as __error:\n    print('(an error, on purpose):', type(__error).__name__)")
    return source


def build_script(notebook, with_answers):
    nb = json.loads(notebook.read_text(encoding="utf-8"))
    parts, answers = [PRELUDE], []
    for i, cell in enumerate(nb["cells"]):
        src = "".join(cell.get("source", []))
        if cell["cell_type"] == "code":
            parts.append(f"# --- cell {i}\n" + as_script_code(src, cell.get("metadata", {}).get("tags", []),
                                                             f"cell {i}"))
        elif with_answers:
            for n, answer in enumerate(ANSWER.findall(src), start=1):
                for code in CODE_BLOCK.findall(answer):
                    label = f"cell {i}, answer {n}"
                    answers.append((label, as_script_code(code, [], label)))
    if with_answers:
        parts.append("__ANSWERS = " + repr(answers) + "\n" + ANSWERS_RUNNER)
    return "\n\n".join(parts) + "\n", len(answers)


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    python, keep, verbose, with_answers, notebooks = sys.executable, None, False, True, []
    args = iter(argv)
    for arg in args:
        if arg == "--python":
            python = next(args, None)
        elif arg == "--keep":
            keep = next(args, None)
        elif arg == "--no-answers":
            with_answers = False
        elif arg == "-v":
            verbose = True
        elif arg.startswith("-"):
            print(f"run_as_script.py: unknown option {arg} (--help)", file=sys.stderr)
            return 2
        else:
            notebooks.append(Path(arg).resolve())
    if python is None or (keep is None and "--keep" in argv):
        print("run_as_script.py: --python and --keep need a value", file=sys.stderr)
        return 2
    if os.sep in python:
        python = os.path.abspath(python)    # the scripts run in another folder; abspath keeps a venv's symlink
    notebooks = notebooks or sorted((ROOT / "jb" / "chapters").glob("*.ipynb"))
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONPATH=str(ROOT / "tools" / "localdata"))
    versions = subprocess.run([python, "-c", "import sys, numpy, pandas, sklearn, matplotlib; print("
                               "'Python', sys.version.split()[0], 'numpy', numpy.__version__, 'pandas', "
                               "pandas.__version__, 'scikit-learn', sklearn.__version__, 'matplotlib', "
                               "matplotlib.__version__)"], capture_output=True, text=True, env=env)
    print("run_as_script.py with " + (versions.stdout.strip() or versions.stderr.strip()))
    problems, notes, answer_count = [], [], 0
    folder = Path(keep) if keep else ROOT / "jb" / "_build" / "scripts"
    folder.mkdir(parents=True, exist_ok=True)
    for notebook in notebooks:
        rel = notebook.relative_to(ROOT).as_posix() if notebook.is_relative_to(ROOT) else str(notebook)
        try:
            script, count = build_script(notebook, with_answers)
        except ValueError as err:
            problems.append(f"{rel}: {err}")
            continue
        answer_count += count
        path = folder / (notebook.stem + ".py")
        path.write_text(script, encoding="utf-8")
        try:
            run = subprocess.run([python, str(path)], capture_output=True, text=True, cwd=folder, env=env,
                                 timeout=600)
        except subprocess.TimeoutExpired:
            problems.append(f"{rel}: the script did not finish in 600 seconds")
            continue
        if verbose:
            print(f"===== {rel}\n{run.stdout}{run.stderr}")
        if run.returncode != 0:
            tail = "\n    ".join(run.stderr.strip().split("\n")[-6:])
            problems.append(f"{rel}: the script failed (as in Thonny):\n    {tail}")
        for line in run.stdout.split("\n"):
            if line.startswith("@@answer-failed "):
                problems.append(f"{rel}: {line[len('@@answer-failed '):]}")
        for line in run.stderr.split("\n"):
            if re.search(r"\w*Warning:", line):
                notes.append(f"{rel}: {line.strip()}")
    for note in dict.fromkeys(notes):
        print("note:", note)
    for problem in problems:
        print(problem)
    if problems:
        print(f"{len(problems)} problem(s)")
        return 1
    print(f"OK: {len(notebooks)} notebook(s) ran as scripts" + (f", {answer_count} answer(s) ran" if with_answers
                                                                  else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
