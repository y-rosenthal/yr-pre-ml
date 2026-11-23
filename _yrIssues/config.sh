# Added by yrProject v0.9.3 (https://github.com/y-rosenthal/yrProject): the templates and the
# tool that give a project one base for AI-assisted work (rules for AI agents, skills, hooks, GitHub issues for
# work to do later, project docs). A starting point: this project owns it. Edit it as you like; "yrProject.sh
# update" does not change it.
# This repository uses yrProject. What yrProject is, which files come from it and which belong to this repository:
# .yrProject/README.md. The yrProject version and the installed parts, with bash and git only:
#   bash .claude/skills/yrProject/scripts/yrProject-notice.sh facts
#
# Settings of the yrIssues skill for this project. .claude/skills/yrIssues/scripts/yrIssues.sh reads this file.

# The category labels: "name|color|description". Each issue gets one category and one priority.
# After a change, run: bash .claude/skills/yrIssues/scripts/yrIssues.sh setup-labels
CATEGORIES=(
  "fix|D93F0B|Something is wrong and needs fixing"
  "improvement|0E8A16|New or better content or features"
  "decision|5319E7|Needs the owner's decision"
  "recheck|1D76DB|Time-sensitive fact to re-verify"
  "renewal|FBCA04|Something expires or renews (yrRenewals, _yrRenewals/renewals.yml); closing it acknowledges"
)

# Only the open issues with this label count, and only their text reaches the AI agent. "yrIssue" (the default,
# also when empty) is the label of the issues that the yrIssues skill creates. Only people with triage or write
# access to the repository can add a label, so an issue that a stranger opens is never read. To count an issue
# that you opened on GitHub yourself, add the label: gh issue edit NUMBER --add-label yrIssue
# "*" counts every open issue. Use it only in a private repository: in a public one, anyone can open an issue.
# Do not add an issue template (.github/ISSUE_TEMPLATE) that gives the label yrIssue: GitHub applies the labels of
# a template to an issue that anyone opens with it.
LABEL="yrIssue"
