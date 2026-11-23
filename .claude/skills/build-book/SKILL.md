---
name: build-book
description: Build the book's website locally (the same build as the GitHub Action) and look at a page. Use when asked to build, preview or render the book, to see how a page looks, or to reproduce a failed build of the GitHub Action.
user-invocable: true
argument-hint: "[--clean] [--open]"
---

# Build the book locally

```bash
tools/build_book.sh            # add --clean after a change to jb/_toc.yml or jb/_config.yml; --open opens the browser
```

- It runs `jb build jb -W -n --keep-going` with the `.venv` (README.md, "Build the book on your computer"), and
  with `tools/localdata` on `PYTHONPATH`, so the data URLs read the files in `data/`: a new or changed CSV file
  works before it is pushed.
- The build runs every notebook (`execute_notebooks: force`). A cell that raises an error, without the tag
  `raises-exception`, stops the build; the log of the failed notebook is in `jb/_build/html/reports/`.
- **A warning fails the build** (`-W`). Fix it. The usual causes: a page that is not in `jb/_toc.yml`, a file in
  `jb/_toc.yml` that does not exist, a broken link to a section, a markdown cell with an unclosed code block.
- The result is `jb/_build/html/index.html`; a chapter is `jb/_build/html/chapters/NN-name.html`. To check that a
  change is there: `grep -c "a phrase" jb/_build/html/chapters/NN-name.html`.
- A full build takes about a minute. Never commit `jb/_build/` (git ignores it).

Run the checks first (`check-notebooks` skill). Publishing is the `deploy-book` skill.
