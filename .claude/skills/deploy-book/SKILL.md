---
name: deploy-book
description: Publish the book to https://y-rosenthal.github.io/yr-pre-ml/ by merging into main and pushing (the GitHub Action checks, builds and publishes), watch the run, and check the live site. Use when asked to publish, deploy or redeploy the book, or to see whether the last publish worked.
user-invocable: true
argument-hint: "[status | push | rerun]"
---

# Publish the book

A push to `main` runs `.github/workflows/deploy-book.yml`: the checks, the build, and the push of
`jb/_build/html` to the `gh-pages` branch, which GitHub Pages serves. Nothing is built or published from this
computer. **Publish only when the instructor asks.**

## Before the push

1. The checks print `OK` (`check-notebooks` skill), and the book builds with no warning (`build-book` skill).
2. Update the docs, skills and rules (the `yrUpdateDocsSkillsRulesEtc` skill; its hook refuses `git push` until it
   ran).
3. Merge the topic branch into `main`: `git switch main && git merge --no-ff BRANCH`.

## Push and watch

```bash
git push origin main      # use the system git: the snap gh cannot push (gh repo create --push fails)
gh run list -R y-rosenthal/yr-pre-ml --workflow deploy-book.yml --limit 3
gh run watch -R y-rosenthal/yr-pre-ml --exit-status $(gh run list -R y-rosenthal/yr-pre-ml --workflow deploy-book.yml --limit 1 --json databaseId -q '.[0].databaseId')
```

To publish again without a new commit: `gh workflow run deploy-book.yml -R y-rosenthal/yr-pre-ml --ref main`.
On a failure: `gh run view -R y-rosenthal/yr-pre-ml RUN_ID --log-failed`. The job `newest-versions` does not stop
the publish; when it fails, a chapter does not work with the newest package versions: fix it.

## Check the live site

GitHub Pages serves the new version a minute or two after the run.

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://y-rosenthal.github.io/yr-pre-ml/
curl -s https://y-rosenthal.github.io/yr-pre-ml/chapters/NN-name.html | grep -c "a phrase you changed"
```

After each publish, the subjexts scan learns the new pages and reports orphaned marks (the `subjexts` skill;
**the instructor runs** `node cli/bin/yrS4.mjs scan y-rosenthal/pre-ml` in yrS4).
