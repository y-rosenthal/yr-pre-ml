---
name: notebook-conventions
description: The rules for the book's chapter notebooks (jb/chapters/*.ipynb) and pages - audience, style, page structure, the Colab-first but Thonny-portable code, the answer and box formats, pandas 2 and 3. Load before you write, change or review any chapter.
user-invocable: true
argument-hint: "[jb/chapters/NN-name.ipynb]"
---

# The chapter notebooks: the rules

This file is **the one place for the rules of the chapters**. Other files point here. `tools/check_notebooks.py`
checks the rules that a script can check (its `--help` lists them).

## Files

- A chapter is a notebook, `jb/chapters/NN-short-name.ipynb` (`NN` gives the order; Jupyter Book numbers the
  chapters itself). The notebook is the source: Colab opens it from GitHub, and the website is built from it.
  A page with no code (cheat sheet, further reading) is a markdown file, `jb/chapters/NN-short-name.md`.
- **Never rename a published page.** Colab links and subjexts marks use its address.
- Every page is in `jb/_toc.yml`, in a part with a topic name.
- The notebooks have **no stored outputs** (`"outputs": []`, `"execution_count": null`). The build runs them.
- nbformat 4.5; every cell has a unique id of 8 hexadecimal characters; code cells have `"metadata": {"tags": [...]}`.
- To write or rewrite a whole chapter, draft it as a text file outside the repository and convert it:
  `python tools/nbtext.py to-ipynb DRAFT.txt jb/chapters/NN-name.ipynb` (`--help` gives the text format;
  `to-text` goes back). For a small change, edit the cell (Jupyter, or the NotebookEdit tool). Never hand-edit the
  JSON with sed.

## Audience and style

- **Readers:** business students who finished basic Python (*Think Python*): variables, lists, loops, `if`,
  functions, dictionaries. They know no statistics beyond an average, and no NumPy or pandas before this book.
- **The tone of *Think Python*:** short paragraphs, "we", friendly and plain English, concrete business examples
  (customers, stores, sales, prices). Short sentences. Define every new term the first time you use it.
- **One new idea per section.** Show a small example first, then state the general rule.
- Use only what the earlier chapters taught (the outline in `docs/PLANNING-v001.qmd`, "The book's content").
  If a page must use something new, say so ("we explain this in the chapter *Filtering rows*").
- **No timing:** no dates, semesters, course sections or lecture numbers. Not "in Lecture 3", not "this week".
- Write new text. **Never copy text** from McKinney's or VanderPlas's books (NoDerivatives licenses). The NumPy and
  pandas documentation (BSD) and Downey's *Elements of Data Science* (CC BY-NC-SA) may be adapted, with a link.
- Name another chapter by its title in italics: "the chapter *Filtering rows*". A link is welcome; give the full
  website address, so that it also works in Colab:
  `[Filtering rows](https://y-rosenthal.github.io/yr-pre-ml/chapters/10-filtering-rows.html)`
  (`tools/check_notebooks.py` checks that the page exists).

## The structure of a chapter

1. **The first cell** (markdown): the title line `# Title` (no number), a blank line, the Colab badge for this
   notebook, a blank line, one or two sentences that say what the chapter is about, and the learning goals:

   ```markdown
   # Filtering rows

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/y-rosenthal/yr-pre-ml/blob/main/jb/chapters/10-filtering-rows.ipynb)

   A manager rarely wants every row. ...

   **In this chapter, you will learn to:**

   - ...
   ```

2. **The first code cell:** every import of the chapter (`import numpy as np`, `import pandas as pd`,
   `import matplotlib.pyplot as plt`, the scikit-learn imports), and `DATA_URL` if the chapter reads data:

   ```python
   DATA_URL = "https://raw.githubusercontent.com/y-rosenthal/yr-pre-ml/main/data/"
   ```

   Read data in a later cell: `sales = pd.read_csv(DATA_URL + "sales.csv")`.
3. **Sections** (`##`), each with one idea: a short explanation, a small code cell, its output, then what the
   output shows. Keep code cells short (1 to 6 lines, usually). Every cell runs after the cells above it, in order.
4. **Boxes** are block quotes with one of these four labels (they look right on the website and in Colab):

   ```markdown
   > **Try it:** change `0.2` to `0.5` and run the cell again. What changes?

   > **Common mistake:** writing `df["Region"]` when the column is `region`. Column names are case-sensitive.

   > **In Thonny:** the last line of a cell shows its value only in Colab. In Thonny, write `print(sales.head())`.

   > **Note:** ...
   ```

   Do not use MyST directives (`:::{note}`, `{admonition}`) or `<div>` boxes: Colab shows them as raw text.
   The chapters before *Series and DataFrames* have an "In Thonny" box at the first cell whose last line shows a
   value.
5. `## Summary`: a short list of what the chapter taught, with the code forms.
6. `## Further reading` (optional): one to three links, never needed for the chapter.
7. `## Practice questions`: about six to ten questions, in this order: Easy, Medium, Hard, and at most one
   Challenge. Each question is one markdown cell with its answer, followed by an empty code cell for the student:

   ````markdown
   ### Question 3 (Medium)

   Which stores sold more than 100 units on one day? ...

   <details class="yr-answer">
   <summary>Answer</summary>

   One or two sentences that explain the answer.

   ```python
   big = sales[sales["units"] > 100]
   big["store"].unique()
   ```

   </details>
   ````

   The code cell after it holds only `# Write your answer here`. Keep the blank lines exactly as shown: they let
   the website and Colab format the text inside. On the website and in Colab the answer stays closed until the
   student clicks "Answer". The subjexts tutor does not see the answers.
   `tools/run_as_script.py` runs the code of every answer after the chapter's code, in a copy of the chapter's
   variables: an answer may use the chapter's variables, and must define everything else that it uses. An answer
   must not need the output of another answer.

## Code that runs in Colab and in Thonny

The book is Colab-first. The only change a Thonny user makes is "wrap the last line in `print()`". So:

- A bare expression on the last line of a cell, to show its value, is fine (Colab shows it). Do not end a line
  with `;` to hide a value.
- No `%` or `!` lines (no `!pip install`: Colab has numpy, pandas, scikit-learn and matplotlib), no
  `google.colab`, no `files.upload()`, no `display()`, no `input()`.
- Data comes only from `DATA_URL + "NAME.csv"` (the files in `data/`, described in
  `jb/chapters/18-datasets.md`), never from a local or Google Drive path. A local path may appear in a markdown
  code block (not run), for example in the chapter about Thonny.
- **Charts:** end every chart cell with `plt.show()`. In Thonny, the chart opens in a window, and the program
  waits until the window is closed.
- **An error on purpose:** give the code cell the tag `raises-exception` (in a draft: `%% code
  tags=raises-exception`). Without it, the build stops. Then explain the last line of the error message. Keep such
  cells few.
- **Randomness:** give every random step a seed (`random_state=42`, `np.random.default_rng(42)`), so the output on
  the website is the output students get.
- **What the reader sees** is the notebook form of a value, not its `print()` form: an array shows as
  `array([20. ,  8.5])`, a NumPy number as `np.int64(9012)` or `np.float64(12.0)` (also a pandas result such as
  `sales["units"].sum()`), a dtype as `dtype('float64')`. `tools/run_as_script.py -v` prints the `print()` form
  (what Thonny shows). Text that quotes an output must match the notebook form: look at the built page.
- **Small outputs:** show at most about 10 rows (`head()`), and tables of about six columns, so they fit in 80
  characters (Thonny's Shell).

## pandas 2 and pandas 3

Colab has pandas 2.2. A student who installs the newest pandas in Thonny gets pandas 3. The code must work in both
(the build checks both versions):

- Change values only with `df.loc[mask, "col"] = value` or `df["col"] = ...`. Never chained assignment
  (`df[mask]["col"] = value`): it changes nothing in pandas 3.
- No `inplace=True`. Write `df["col"] = df["col"].fillna(value)` and `df = df.dropna()`.
- Text columns have the dtype `object` in pandas 2 and `str` in pandas 3. When the text names the dtype, name
  both: "`object` (or `str` in pandas 3)". Do not write code that tests the dtype name.
- Before `mean()` or `sum()` over a whole DataFrame or a `groupby`, select the number columns
  (`sales.groupby("store")["units"].sum()`), or pass `numeric_only=True`.
- Do not use removed or deprecated features: `append`, `applymap`, `fillna(method=...)`, `swapaxes`.

## After you write or change a chapter

1. `python tools/check_notebooks.py` must print `OK`.
2. `.venv/bin/python tools/run_as_script.py jb/chapters/NN-name.ipynb` must print `OK` (the Thonny check and the
   answers check).
3. `tools/build_book.sh` must build the book with no warning. Look at the page in `jb/_build/html/chapters/`.
