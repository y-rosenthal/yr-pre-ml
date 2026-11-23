# What is Machine Learning?

*Prerequisite material for getting started*

The source of a free online book, a Jupyter Book. It teaches business students the NumPy and pandas that they
need before machine learning. Each chapter is a notebook that opens in Google Colab. One chapter shows how to run
the same code in Thonny and in other Python editors.

- The book: <https://y-rosenthal.github.io/yr-pre-ml/>
- License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Layout

| Path | What it holds |
|---|---|
| `jb/_config.yml`, `jb/_toc.yml`, `jb/intro.md` | The Jupyter Book (v1) |
| `jb/chapters/NN-short-name.ipynb` | The chapters, one notebook each, with no stored outputs; `.md` pages for the appendices without code |
| `data/` | The datasets (CSV files) and `make_data.py`, which makes them |
| `tools/` | The checks (`check_notebooks.py`, `run_as_script.py`), the build (`build_book.sh`), and `nbtext.py` for drafting a chapter |
| `.claude/skills/` | The procedures, for people and AI agents: `notebook-conventions` (the rules of the chapters), `check-notebooks`, `build-book`, `add-page`, `deploy-book`, and the yrProject skills |
| `requirements.txt` | The Python packages: Colab's versions of the packages that the chapters use, and the tools that build the book |
| `.github/workflows/deploy-book.yml` | Checks, builds and publishes the book to GitHub Pages on every push to `main` |
| `docs/` | The project documents (a Quarto book: `quarto preview docs`). The plan for the book: `docs/PLANNING-v001.qmd` |

## Build and check the book on your computer

Use Python 3.11, 3.12 or 3.13 (Colab has 3.13; pandas 2.2.3 does not support 3.14).

```bash
python3 -m venv .venv && .venv/bin/pip install --no-cache-dir -r requirements.txt   # once
.venv/bin/python tools/check_notebooks.py       # static checks
.venv/bin/python tools/run_as_script.py         # every chapter as a Thonny script, and every answer
tools/build_book.sh                             # the website, in jb/_build/html/index.html
```

The `check-notebooks` and `build-book` skills give the details.

<!-- begin yrProject setup: written by yrProject.sh; "yrProject.sh update" replaces this block -->
**This repository uses yrProject** (yrProject v0.9.3; parts: rules, yrIssues, yrRenewals, docs, subjexts). yrProject is the templates and the tool that give a project one base for AI-assisted work (rules for AI agents, skills, hooks, GitHub issues for work to do later, project docs).
Its repository: https://github.com/y-rosenthal/yrProject (if the link does not open, the repository is private: ask the owner of this project).

- What yrProject is, which files come from it and which belong to this repository: `.yrProject/README.md`. Every
  file that yrProject installed starts with a comment that names yrProject. The tool `yrProject.sh` runs on the
  owner's computer; without it, all these files are ordinary files.
- The yrProject version and the installed parts (bash and git only): `bash .claude/skills/yrProject/scripts/yrProject-notice.sh facts`
<!-- end yrProject setup -->
