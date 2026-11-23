# Rules for AI coding agents (yr-pre-ml)

<!-- begin yrProject setup: written by yrProject.sh; "yrProject.sh update" replaces this block -->
## Set up by yrProject.sh

`yrProject.sh` (yrProject v0.9.3; parts: rules, yrIssues, yrRenewals, docs, subjexts) set up this project. yrProject
(https://github.com/y-rosenthal/yrProject) is the templates and the tool that give a project one base for
AI-assisted work: rules for AI agents, skills, hooks, GitHub issues for work to do later, project docs. The tool
installed files here, and `yrProject.sh update` keeps them up to date. Every file that it installed starts with
a comment that names yrProject and its version, and says whether the file belongs to the tool or to the project.

- In the first reply of a session, give one line with the version line `(yrProject v0.9.3 [latest])` (or
  `[latest vA.B.C]` if a newer version exists, or `[latest UNKNOWN]`), the type, the installed parts and the parts
  not installed (`bash .claude/skills/yrProject/scripts/yrProject-notice.sh facts`); then answer. Do not repeat the
  version line in later replies: the Claude Code status line can show it (`yrProject.sh statusline-setup`).
- Before you change a file that the tool installed, read `.yrProject/README.md`. It lists the files, and tells who
  changes each one.
- Do not edit this block, the shared-rules block, the `yrProject` block in `.gitignore`, or the files in
  `.yrProject/`. `yrProject.sh update` writes them again. It does not replace a block that was changed by hand: it
  leaves the block alone and reports it. Put the project's own rules outside the blocks.
- The user does not need to know the tool. To check, update, migrate or remove this setup, or to list or make
  yrProjects, follow the `yrProject` skill (`.claude/skills/yrProject/SKILL.md`).
- "Project" alone does not mean the yrProject setup. Unless the user says yrProject or it is obvious, ask.
<!-- end yrProject setup -->

These rules are for every collaborator and every coding agent. `CLAUDE.md` imports this file. Put new project
rules here, outside the yrProject blocks. The shared rules below come from yrProject.

## This repository

- The source of the book *What is Machine Learning?* (subtitle: *Prerequisite material for getting started*): a
  Jupyter Book v1 in `jb/` with Colab-first notebooks, for the instructor's (Prof. Rosenthal's) business-school
  Python course. It teaches NumPy and pandas before machine learning.
- **The plan, the decisions and the steps are in `docs/PLANNING-v001.qmd`.** Read it before you work on the book.
- The repository is public: `y-rosenthal/yr-pre-ml`. Every push to `main` builds the book and publishes it to
  <https://y-rosenthal.github.io/yr-pre-ml/> (`.github/workflows/deploy-book.yml`).
- The book is the subjexts package `y-rosenthal/pre-ml`. Labels live on subjexts, not in this repository.

## How to work

- Work on a topic branch. Merge into `main` and push only when the instructor says so: the push publishes the
  book.
- Add files to git by path, never `git add -A`.
- Never rename a notebook after it is published: the Colab links and the subjexts marks use its address.
- Write only inside this repository. Other repositories (yrThinkPython, yrS4, yrProject, aiasdSrc) are read-only.
  While yrProject's book-tools work is in progress, do not touch yrProject's repository: run `yrProject.sh update`
  with `--no-register` (`docs/PLANNING-v001.qmd`, "Step 0").
- No dependency on yrThinkPython. A file copied from it is this book's own file, and the list "Files copied from
  other repositories" in `docs/PLANNING-v001.qmd` names it. Nothing here runs yrThinkPython's files or uses its
  environments.
- Older files that are kept, not deleted yet, go into `oldfiles/`. Git does not track that folder.

## The book's content

- No dates, semesters, course sections or lecture numbers in the book. Parts have topic names.
- The writing rules for the notebooks are in `docs/PLANNING-v001.qmd`, "Writing rules for the notebooks".
- No exam questions in this public repository: they go to the private `yrQuestionBank` repository.
- The package versions are Colab's, pinned in `requirements.txt` (`docs/PLANNING-v001.qmd`, D7).

## Build

- The build environment is `.venv` in this folder (git ignores it), made from the system Python 3.12. On the
  instructor's computer, `python3` is linuxbrew's Python 3.14, which pandas 2.2.3 does not support, so give the
  full path: `/usr/bin/python3 -m venv .venv && .venv/bin/pip install --no-cache-dir -r requirements.txt`.
- Build the book: `.venv/bin/jb build jb`. Open `jb/_build/html/index.html`. The build runs every notebook.

<!-- begin shared rules: yrProject v0.9.3, from templates/v0.9.3/AGENTS-shared-rules.md in yrProject; "yrProject.sh update" replaces this block, unless it was changed by hand -->

## Write in plain English

- Write in plain English in replies, docs, commit messages, pull requests, code comments, logs and UI text.
  Follow the main rules of ASD-STE100 (Simplified Technical English) as a guide, not strictly.
- Say directly what a thing does and what it does not do.
- Do not use metaphors or figurative phrasing. Not: "this is a curtain at view time, not a lock". Instead: "the
  overlay hides the text when the page is viewed; the text is still in the page's HTML".
- Use short sentences, 20 words or fewer when you can. Put one instruction or one idea in each sentence.
- Use the active voice: "the script deletes the file", not "the file is deleted".
- Use one word for one meaning. After you give a thing a name, use that same name every time.
- Do not start with filler such as "Sure, I can help with that". Do not hedge without a reason. Say what you
  know, and say clearly what you do not know.
- Do not change code, names (of variables, files, commands, APIs) or technical terms to make the text simpler.

## Scripts have --help

Every script you write or change (for a skill, a tool, or a one-off script that stays in the project) has `-h`
and `--help`. The help states the general purpose of the script, its usage line, and every option with its
default. With `-h` or `--help`, the script prints the help, exits with status 0, and does no work: it changes no
files and installs nothing.

- Python: the docstring at the top holds the help. At the start of `main`, before any work:
  `if '-h' in argv or '--help' in argv: print(__doc__); return 0` (or use `argparse` with a description).
- Bash: the header comment holds the help. Right after `set -euo pipefail`, before any setup:
  `case "${1:-}" in -h|--help) sed -n '2,/^[^#]/{/^#/s/^# \{0,1\}//p}' "$0"; exit 0 ;; esac`
- Other languages: the same behavior, in the usual way for that language.
- When you add, remove or change an option, update the help in the same change.
- Do not add `--help` to files that are only imported or sourced, or to third-party files that the project
  keeps unchanged (for example files from an upstream repository).

## Rules for every AI tool are in AGENTS.md

- Put a project's rules in its `AGENTS.md`, so that every collaborator's coding agent reads them. Most agents read
  `AGENTS.md` (Codex, Cursor, GitHub Copilot, Claude Code). Keep `CLAUDE.md` as one import line, `@AGENTS.md`, plus
  rules that apply only to Claude Code. Do not use a symlink for `CLAUDE.md` (Windows clones and Dropbox can break it).
- If a project's `AGENTS.md` does not have the block `<!-- begin shared rules -->`, tell the user and offer to set
  it up as a yrProject with `yrProject.sh update`. `yrProject.sh status` shows the project's state,
  `yrProject.sh check` whether it is set up correctly, `yrProject.sh remove` takes the setup out again, and
  `yrProject.sh --help` explains them. An agent has no
  terminal to answer `update`'s question in: run `yrProject.sh update --dry-run`, show the user the plan, and run
  `yrProject.sh update -y` only after the user approves it. In a yrProject, the `yrProject` skill does all this.

## "Project" does not mean yrProject

- A yrProject is a project that `yrProject.sh` set up: its shared rules, skills and hooks, and its record in
  `.yrProject/`. Do not assume that the word "project" means a yrProject, or its yrProject setup. Unless the user
  says yrProject (or the yrProject setup, the tool, its shared rules or its skills), or it is otherwise obvious,
  ask what they mean before you act. For example, "update the project" or "make a new project" may mean the code,
  the book, or something else.

## The docs, skills and rules reflect the chat

- Before a push, and when the user says they are done or is about to clear or leave the chat, do what a careful
  developer does before handing work over: bring everything in the repository that describes or depends on the
  changes into line with them (the docs, the skills, a script's `--help`, a comment, a test, whatever the change
  touched; what that is depends on the change), and put what the user decided or asked for from now on into
  the project's rules (`AGENTS.md`, `CLAUDE.md`): a chat is cleared, a rule stays. If the project has the
  `yrUpdateDocsSkillsRulesEtc` skill (`.claude/skills/yrUpdateDocsSkillsRulesEtc/`), follow it; its hook refuses
  `git push` until the skill recorded its review, and after `/clear` a hook names the chat to read.

## Work to do later is GitHub issues

- Record work to do later as GitHub issues in the project's own repository, not in a to-do file, a task board or a
  TODO document. Call them "issues", as GitHub does. If the project has the `yrIssues` skill
  (`.claude/skills/yrIssues/`), use it: a SessionStart hook shows the user how many issues are open, and the issues
  that it creates get the label `yrIssue`. (Projects set up before yrProject v0.5.0 have the `pending-work` skill
  instead; `yrProject.sh update` replaces it.)
- If a project keeps such a list in a file, tell the user and offer to move it into issues.
- Things that expire or renew on a date (API keys, access tokens, domains, certificates, subscriptions, periodic
  checks) go in `_yrRenewals/renewals.yml` if the project has the `yrRenewals` skill
  (`.claude/skills/yrRenewals/`): a daily GitHub workflow opens a reminder issue before each date, and closing
  it is the acknowledgement. Never write a key, a token or a password there, or in an issue.
- `_yrIssues/issues.md` (the saved copy of the open issues) and `_yrIssues/queue.md` (issues written while GitHub
  could not be reached) are written by the yrIssues skill, and git ignores them (yrProject v0.6.0 and later). Do
  not edit, commit or restore them. In a project from before v0.6.0, a staged deletion of `issues.md` is the
  migration (`git rm --cached`: the file stays on disk), not an accident: leave it, and commit it with a plain
  `git commit`, not one limited to paths. A path-limited commit rebuilds those paths from the working tree, where
  the ignored file still exists, and silently drops the untracking.

<!-- end shared rules -->
