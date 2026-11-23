---
name: add-page
description: Add a new chapter (a notebook) or a markdown page to the book - its file name, its place in jb/_toc.yml, the first cell with the Colab badge, and the checks. Use when asked to add a chapter, a page, an appendix or a project to the book.
user-invocable: true
argument-hint: "[NN-short-name] [title]"
---

# Add a page to the book

1. **Choose the file name** `jb/chapters/NN-short-name.ipynb` (or `.md` for a page without code): `NN` puts it
   in order; the short name is a few words with hyphens. **The name is permanent once it is published** (Colab
   links and subjexts marks use it). Do not renumber the pages after it: a number may be skipped or reused with
   a letter (`11b-...`) instead.
2. **Write the page** by the rules of the `notebook-conventions` skill: draft it as a text file outside the
   repository and convert it with `python tools/nbtext.py to-ipynb DRAFT.txt jb/chapters/NN-short-name.ipynb`. The
   first cell holds the title, the Colab badge for this file name, the introduction and the learning goals. Copy the
   structure of a chapter in the same part.
3. **List it in `jb/_toc.yml`**, in the part of its topic (a part's caption names a topic, never a lecture or a
   date). A data file that it needs goes into `data/make_data.py` (then `python data/make_data.py`), and its
   columns into `jb/chapters/18-datasets.md`.
4. **Check it** (`check-notebooks` skill), and **build** the book (`build-book` skill). Look at the page.
5. If the page changes the outline of the book, update "The book's content" in `docs/PLANNING-v001.qmd`, and the
   cheat sheet (`jb/chapters/17-cheat-sheet.md`) if it teaches new forms.
