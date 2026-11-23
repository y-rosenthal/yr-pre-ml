---
name: check-notebooks
description: Check the book's chapters - the static checks (format, Colab badge, portability, answers, no timing, table of contents, scripts' --help), the Thonny and answers check with Colab's versions and with the newest versions, and the data check. Use after any change to a chapter, the data or the tools, before a commit, and when asked to test or validate the book.
user-invocable: true
argument-hint: "[jb/chapters/NN-name.ipynb ...]"
---

# Check the book

Run from the repository folder. Each check prints `OK`, or the problems (exit status 1). What each check does is
in its `--help`; the rules it checks are in the `notebook-conventions` skill.

```bash
.venv/bin/python tools/check_notebooks.py                       # static checks of everything (seconds)
.venv/bin/python tools/run_as_script.py                         # every chapter as a Thonny script, and every answer (Colab's versions)
.venv/bin/python tools/run_as_script.py --python .venv-newest/bin/python   # the same with the newest versions (pandas 3)
.venv/bin/python data/make_data.py --check                      # the CSV files are what the script writes
```

- Give notebook paths to check only those: `tools/run_as_script.py jb/chapters/10-filtering-rows.ipynb -v`
  (`-v` prints what each script printed: the `print()` form, which Thonny shows. Colab and the website show the
  notebook form of the last expression, for example `np.int64(9012)` for `9012`: look at the built page, or at the
  executed notebook in `jb/_build/jupyter_execute/chapters/`).
- `.venv-newest` is the environment with the newest numpy, pandas, scikit-learn and matplotlib. Make it once,
  and again when new versions come out:
  `/usr/bin/python3 -m venv .venv-newest && .venv-newest/bin/pip install --no-cache-dir --upgrade numpy pandas scikit-learn matplotlib`.
- A `note:` line names a warning that a chapter's code printed. Change the code so that it prints no warning.
- Then build the book (`build-book` skill): the build runs every notebook again, as Jupyter does.

The GitHub Action runs the same checks before it publishes (`.github/workflows/deploy-book.yml`).
