---
name: yrRenewals
description: Reminders for the things that expire or renew (the yrRenewals skill of yrProject) - API keys, access tokens, domains, certificates, subscriptions, periodic checks. They are listed in _yrRenewals/renewals.yml with a date and the action to take; a daily GitHub workflow opens a reminder issue 60, 30, 7 and 1 days before each date and when it is overdue, and closing the issue is the acknowledgement. Covers adding, changing and listing items, what to do with a reminder issue, and the one-time setup.
when_to_use: Use when the user mentions something that expires, renews or must be redone on a date - "the API key expires in June", "remind me before the domain renews", "add a renewal", "what expires next?", "list renewals" - and when an issue titled "Renewal: ..." comes up (the yrIssues list, or "let's do the renewal"). Also when a project gets a new key, token, domain or subscription with an end date: offer to list it.
allowed-tools:
  - Bash(bash ${CLAUDE_SKILL_DIR}/scripts/yrRenewals.sh *)
  - Bash(gh issue list *)
  - Bash(gh issue view *)
  - Bash(gh issue close *)
---

<!-- Installed by yrProject v0.9.3 (https://github.com/y-rosenthal/yrProject): the templates
     and the tool that give a project one base for AI-assisted work (rules for AI agents, skills, hooks, GitHub
     issues for work to do later, project docs). This file belongs to the tool: do not edit it by hand, and do
     not change it without the tool. "yrProject.sh update" replaces it with each new version (if you change it,
     update leaves it alone, and it gets no newer versions); "yrProject.sh remove" removes it.
     This repository uses yrProject. What yrProject is, which files come from it and which belong to this repository:
     .yrProject/README.md. The yrProject version and the installed parts, with bash and git only:
       bash .claude/skills/yrProject/scripts/yrProject-notice.sh facts -->

# Renewals and expiries (yrRenewals)

## What it is for

- Things that expire or renew on a date must not be forgotten: an API key, an access token, a domain, a
  certificate, a paid plan, a monthly restore check, a yearly review. The user lists them once, with the date
  and the action, and gets a reminder in time, by email, without a calendar.
- The list is `_yrRenewals/renewals.yml` in the project (the project owns it). The workflow
  `.github/workflows/yrRenewals.yml` runs every day on GitHub and opens a **reminder issue** for each item that
  is 60, 30, 7 or 1 days away, or overdue: one issue per item and milestone, never twice. GitHub emails the
  people who watch the repository. **Closing the issue is the acknowledgement.**
- The reminders are ordinary issues of the project, with the labels `renewal`, `yrIssue` and a priority (`low`
  at 60 days, `medium` at 30, `high` at 7 and 1 days and when overdue), so the yrIssues skill counts and lists
  them like any other issue.

## The list

`_yrRenewals/renewals.yml` is a small subset of YAML: one value per line, in double quotes if needed. Each item:

```yaml
items:
  - id: tutor-key                 # a short name, unique in the file (letters, digits, hyphens)
    what: Anthropic API key "tutor" expires (the tutor stops answering)
    date: 2027-06-02              # YYYY-MM-DD; for a repeating item, any occurrence
    repeat: yearly                # optional: monthly or yearly (the date rolls forward by itself)
    action: Make a new key at platform.claude.com/settings/keys, paste it into .env as ANTHROPIC_API_KEY, then run `supabase secrets set ANTHROPIC_API_KEY=...` (the agent can do the last two steps).
```

- `what` names the thing and says what stops working. The issue's title is the text before the first ` (`.
- `action` says what to do: where to go, what to paste where, which command to run, and what the agent can do.
- **Never put a key, a token or a password in the file** (the repository may be public, or become public): say
  where it is kept (`.env`, a secret, a password manager).
- `bash ${CLAUDE_SKILL_DIR}/scripts/yrRenewals.sh list` shows every item with its next date and the days left,
  and reports a wrong item (a bad date, a missing field). `check --dry-run --today 2027-05-03` shows what the
  workflow would open on a day. `--help` shows every command.

## Adding or changing an item

When the user mentions something that expires, renews or must be redone on a date:

1. Ask for what is missing: the date (or how it repeats), and what to do when it comes (the action).
2. Add the item with the script, which checks the values and writes the file (the same `id` replaces an item;
   keep the ids stable, the reminders name them):

   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/yrRenewals.sh add --id tutor-key --what 'Anthropic API key "tutor" expires (the tutor stops answering)' \
     --date 2027-06-02 [--repeat monthly|yearly] --action 'Make a new key at ..., paste it into .env as ...'
   ```

   It prints the item's line as `list` shows it; show it to the user. `remove --id ID` takes an item out. Edit
   the file by hand only for what the script cannot do (a comment, the order).
3. Commit and push when the user agrees: **the workflow reads the pushed file.** An item that is not pushed
   gets no reminder.

For a date that nobody knows yet (a renewal date not recorded anywhere), put the best guess and an action that
says to check the real date first.

## When a reminder issue comes

An issue titled `Renewal: ... (due DATE, 60 days)` (or 30 days, 7 days, 1 day, overdue) is a reminder. Its body
has the item, the date and the action.

1. Show the user the issue (`gh issue view <N>`) and offer to do the parts of the action that an agent can do
   (for example paste a new key into `.env`, run a command). Never fetch or invent a secret yourself: the user
   makes the new key or token and gives it to you, or pastes it themselves.
2. When it is done, close the issue: `gh issue close <N> --comment "Done: ..."`. That is the acknowledgement; the
   later milestones of the same date are still opened as they come, so for a one-time item that was renewed to a
   **new date**, change `date` in the file (and push), or delete the item if it does not come back. A repeating
   item rolls forward by itself.
3. An "overdue" issue means that the date passed with the item still in the file: do the action, then fix the
   date or delete the item.

## The one-time setup

- The workflow runs on GitHub, so the project needs a GitHub repository with Actions enabled; it needs no
  secret (it uses the workflow's own token, with permission to write issues).
- The labels: `bash ${CLAUDE_SKILL_DIR}/scripts/yrRenewals.sh setup-labels` makes `renewal`, `yrIssue` and the
  three priorities (safe to repeat; `check` makes them too when it opens the first reminder). If
  `_yrIssues/config.sh` has no category `renewal`, `setup-labels` and `yrProject.sh check` print the exact line
  to add to its `CATEGORIES` (the template of a new project has it): add that line, so that the yrIssues skill
  knows the category.
- To run the check by hand: on GitHub, Actions, "yrRenewals", "Run workflow"; or locally,
  `bash ${CLAUDE_SKILL_DIR}/scripts/yrRenewals.sh check` with `gh` logged in (it opens the same issues).
- Without a GitHub repository, the list still works (`list`), but nothing opens reminders.
