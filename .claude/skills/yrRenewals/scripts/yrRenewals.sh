#!/usr/bin/env bash
# Installed by yrProject v0.9.3 (https://github.com/y-rosenthal/yrProject): the templates and
# the tool that give a project one base for AI-assisted work (rules for AI agents, skills, hooks, GitHub issues
# for work to do later, project docs). This file belongs to the tool: do not edit it by hand, and do not change
# it without the tool. "yrProject.sh update" replaces it with each new version (if you change it, update leaves
# it alone, and it gets no newer versions); "yrProject.sh remove" removes it.
# This repository uses yrProject. What yrProject is, which files come from it and which belong to this repository:
# .yrProject/README.md. The yrProject version and the installed parts, with bash and git only:
#   bash .claude/skills/yrProject/scripts/yrProject-notice.sh facts
#
# yrRenewals.sh - helper for the yrRenewals skill of yrProject: reminders for the things that expire or renew
# (API keys, access tokens, domains, subscriptions, periodic checks), opened as GitHub issues before the date.
#
# The items are in _yrRenewals/renewals.yml (the project owns that file): what expires, the date, what to do,
# and whether it repeats. "check" opens a GitHub issue for an item 60, 30, 7 and 1 days before its date, and
# when it is overdue: one issue per item and milestone, never twice (the title identifies it: an open or closed
# issue with that title is not opened again). GitHub emails the people who watch the repository, and closing
# the issue is the acknowledgement. The workflow .github/workflows/yrRenewals.yml runs "check" every day.
#
# Usage: bash yrRenewals.sh [COMMAND] [OPTIONS]
#   list            (the default) every item with its next date and the days left, soonest first, and the
#                   reminders that "check" would open today. Needs no network
#   check           open the reminder issues that are due today (needs gh, logged in; in GitHub Actions,
#                   GH_TOKEN). Makes the labels first, if a reminder is to be opened
#   add             add an item to the list, or replace the item with the same id: --id, --what, --date,
#                   --action, and --repeat if it repeats. It checks the values, writes the item (quoted), and
#                   prints its line as "list" shows it. It makes the list if there is none
#   remove          remove the item --id ID from the list
#   setup-labels    create or update the labels of the reminders on GitHub: renewal, yrIssue and the three
#                   priorities (safe to repeat). It says if _yrIssues/config.sh lacks the category renewal
#   -h, --help      show this help and stop
# Options:
#   --id ID         add, remove: the item's id (letters, digits and hyphens)
#   --what TEXT     add: what expires or renews, and what stops working
#   --date DATE     add: the date, YYYY-MM-DD
#   --repeat R      add: monthly or yearly (default: the item does not repeat)
#   --action TEXT   add: what to do when the date comes
#   --dry-run       check: print the reminders that would be opened; open nothing, and never go to GitHub
#   --today DATE    pretend that today is DATE (YYYY-MM-DD), for testing (default: today, UTC)
#   --repo OWNER/NAME  the GitHub repository of the issues (default: GITHUB_REPOSITORY in Actions, else the
#                   "origin" remote of the project)
#   --file FILE     the list of items (default: _yrRenewals/renewals.yml in the project folder)
#
# The list, _yrRenewals/renewals.yml, is a small subset of YAML: one value per line, optionally in double quotes,
# comments after "#". Each item:
#   items:
#     - id: tutor-key                     a short name, unique in the file (letters, digits, hyphens)
#       what: Anthropic API key "tutor" expires (the tutor stops answering)
#       date: 2027-06-02                  YYYY-MM-DD; for a repeating item, any occurrence, past or future
#       repeat: yearly                    optional: monthly or yearly (the date rolls forward by itself, keeping
#                                         the day: the 31st falls on the last day of a shorter month)
#       action: Make a new key at ..., paste it into .env, then run ...
# A reminder issue gets the labels renewal, yrIssue (so that the yrIssues skill counts it) and a priority: low
# at 60 days, medium at 30, high at 7 and 1 days and when overdue. If _yrIssues/config.sh sets LABEL, the
# issue gets that label too. An item that does not repeat and is past its date gets one "overdue" issue.
#
# Needs bash and GNU date (Linux, Git Bash on Windows, GitHub Actions); check and setup-labels also need gh.
# Exit status: 0 OK; 1 an item is wrong (a bad date, a missing field) or GitHub could not be used; 2 bad usage.

set -uo pipefail
case "${1:-}" in -h|--help) sed -n '2,/^[^#]/{/^#/s/^# \{0,1\}//p}' "$0"; exit 0 ;; esac

LIST="_yrRenewals/renewals.yml"
CONFIG="_yrIssues/config.sh"
MARK="yrIssue"                  # the label of the issues of the yrIssues skill: the reminders get it too
RENEWAL="renewal"               # the category label of the reminders
MILESTONES="60 30 7 1"          # days before the date on which a reminder is opened

here="$(cd "$(dirname "$0")" && pwd)"
root="${CLAUDE_PROJECT_DIR:-}"
[ -n "$root" ] && [ -d "$root" ] || root="$(git -C "$here" rev-parse --show-toplevel 2>/dev/null || pwd)"

cmd=list
dry=0
today=""
repo="${GITHUB_REPOSITORY:-}"
file=""
o_id=""; o_what=""; o_date=""; o_repeat=""; o_action=""
while [ $# -gt 0 ]; do
  case "$1" in
    list|check|add|remove|setup-labels) cmd="$1" ;;
    --dry-run) dry=1 ;;
    --today) today="${2:-}"; shift ;;
    --repo) repo="${2:-}"; shift ;;
    --file) file="${2:-}"; shift ;;
    --id) o_id="${2:-}"; shift ;;
    --what) o_what="${2:-}"; shift ;;
    --date) o_date="${2:-}"; shift ;;
    --repeat) o_repeat="${2:-}"; shift ;;
    --action) o_action="${2:-}"; shift ;;
    *) echo "yrRenewals.sh: unknown argument '$1' (see --help)" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$file" ] || file="$root/$LIST"
if [ ! -f "$file" ] && [ "$cmd" = add ]; then
  mkdir -p "$(dirname "$file")"
  printf '# The things that expire or renew (the yrRenewals skill of yrProject; "yrRenewals.sh --help" gives the format).\nitems:\n' > "$file"
fi
if [ ! -f "$file" ]; then
  echo "yrRenewals.sh: $file not found (the list of things that expire or renew; see --help for its format)" >&2
  exit 1
fi

# Dates: midnight UTC, as seconds, so that the days between two dates are exact.
epoch() { date -u -d "$1" +%s 2>/dev/null; }
valid_date() { [[ "$1" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] && [ "$(date -u -d "$1" +%Y-%m-%d 2>/dev/null)" = "$1" ]; }
[ -n "$today" ] || today="$(date -u +%Y-%m-%d)"
if ! valid_date "$today"; then echo "yrRenewals.sh: --today needs a date YYYY-MM-DD, not '$today'" >&2; exit 2; fi
today_s="$(epoch "$today")"

# The labels of the reminders. LABEL and CATEGORIES come from the yrIssues settings, if the project has them.
LABEL=""
CATEGORIES=()
# shellcheck source=/dev/null
[ -f "$root/$CONFIG" ] && . "$root/$CONFIG"
[ "$LABEL" = "*" ] && LABEL=""   # "*": the yrIssues skill counts every issue; no extra label for the reminders
renewal_desc="Something expires or renews (yrRenewals, $LIST); closing it acknowledges"
renewal_color="FBCA04"
has_category=0
for c in "${CATEGORIES[@]:-}"; do
  case "$c" in "$RENEWAL|"*) IFS='|' read -r _ renewal_color renewal_desc <<< "$c"; has_category=1 ;; esac
done

# owner/repo from the git remote, unless given (no network needed)
if [ -z "$repo" ]; then
  remote_url="$(git -C "$root" remote get-url origin 2>/dev/null || true)"
  case "$remote_url" in *github.com*) repo="$(printf '%s' "$remote_url" | sed -E 's#(\.git)?/*$##; s#^.*github\.com[:/]##')" ;; esac
fi
gh_bin="$(command -v gh || true)"
[ -z "$gh_bin" ] && [ -x /snap/bin/gh ] && gh_bin=/snap/bin/gh

run_gh() {
  if command -v timeout >/dev/null 2>&1; then timeout 30 "$gh_bin" "$@"; else "$gh_bin" "$@"; fi
}

need_gh() {
  if [ -z "$gh_bin" ]; then echo "yrRenewals.sh: gh (the GitHub command) is not installed" >&2; exit 1; fi
  if [ -z "$repo" ]; then echo "yrRenewals.sh: no GitHub repository (git remote origin); give --repo OWNER/NAME" >&2; exit 1; fi
}

# The items of the list, one per line: id, what, date, repeat, action, separated by the character US (\037;
# a tab would be collapsed by "read" when a field is empty).
parse_items() {
  awk '
    function val(s) {        # the value: in double quotes (\" and \\ inside), or up to a " #" comment
      sub(/^[ \t]+/, "", s)
      if (s ~ /^"/) { s = substr(s, 2); sub(/"[ \t]*(#.*)?$/, "", s); gsub(/\\"/, "\"", s); gsub(/\\\\/, "\\", s) }
      else { sub(/[ \t]#.*$/, "", s); sub(/[ \t]+$/, "", s) }
      gsub(/\t/, " ", s)
      return s
    }
    function flush() { if (n) print id "\037" what "\037" date "\037" repeat "\037" action; id = what = date = repeat = action = ""; n = 0 }
    /^[ \t]*#/ || /^[ \t]*$/ { next }
    /^[ \t]*-([ \t]|$)/ { flush(); n = 1; sub(/^[ \t]*-[ \t]*/, "") }
    n && match($0, /^[ \t]*[A-Za-z_][A-Za-z0-9_-]*[ \t]*:([ \t]|$)/) {
      key = substr($0, RSTART, RLENGTH); sub(/^[ \t]+/, "", key); sub(/[ \t]*:.*$/, "", key)
      v = val(substr($0, RSTART + RLENGTH))
      if (key == "id") id = v; else if (key == "what") what = v; else if (key == "date") date = v
      else if (key == "repeat") repeat = v; else if (key == "action") action = v
    }
    END { flush() }
  ' "$file"
}

# The next occurrence of an item's date, on or after today. A repeating item keeps its day of the month (the
# 31st falls on the last day of a shorter month; February 29 on the 28th in other years): no drift.
next_due() {   # $1 date, $2 repeat
  local y="${1:0:4}" m="${1:5:2}" d="${1:8:2}" k ym last cand
  [ -n "$2" ] || { printf '%s\n' "$1"; return; }
  if [ "$2" = monthly ]; then k=$(( (10#${today:0:4} - 10#$y) * 12 + (10#${today:5:2} - 10#$m) ))
  else k=$(( 10#${today:0:4} - 10#$y )); fi
  [ "$k" -gt 0 ] || k=0
  while :; do
    ym="$(date -u -d "$y-$m-01 +$k $([ "$2" = monthly ] && echo month || echo year)" +%Y-%m)"
    last="$(date -u -d "$ym-01 +1 month -1 day" +%d)"
    cand="$ym-$([ $(( 10#$d <= 10#$last )) -eq 1 ] && echo "$d" || echo "$last")"
    if [ "$(epoch "$cand")" -ge "$today_s" ]; then printf '%s\n' "$cand"; return; fi
    k=$((k + 1))
  done
}

milestone_of() {   # $1 days left: "overdue", "60 days", ..., "1 day", or "" (no reminder today)
  local days="$1" m
  if [ "$days" -lt 0 ]; then echo overdue; return; fi
  for m in $MILESTONES; do
    if [ "$days" -eq "$m" ]; then echo "$m day$([ "$m" -eq 1 ] || echo s)"; return; fi
  done
  echo ""
}

priority_of() {   # $1 milestone
  case "$1" in "60 days") echo low ;; "30 days") echo medium ;; *) echo high ;; esac
}

days_text() {     # $1 days left
  if [ "$1" -lt 0 ]; then echo "$(( -$1 )) day$([ "$1" -eq -1 ] || echo s) overdue"
  elif [ "$1" -eq 0 ]; then echo "today"
  else echo "in $1 day$([ "$1" -eq 1 ] || echo s)"; fi
}

# Read the items, check them, and compute each one's next date. Fills the arrays below; bad items are reported.
ids=(); whats=(); dues=(); dayss=(); actions=(); repeats=(); mss=()
bad=0
load_items() {
  local id what date repeat action due days ms
  while IFS=$'\037' read -r id what date repeat action; do
    [ -n "$id$what$date$action" ] || continue
    if [ -z "$id" ] || [ -z "$what" ] || [ -z "$date" ] || [ -z "$action" ]; then
      echo "! item '${id:-?}': id, what, date and action are all needed ($LIST)" >&2; bad=1; continue
    fi
    if ! valid_date "$date"; then echo "! item '$id': the date must be YYYY-MM-DD, not '$date'" >&2; bad=1; continue; fi
    case "$repeat" in ""|monthly|yearly) ;; *) echo "! item '$id': repeat must be monthly or yearly, not '$repeat'" >&2; bad=1; continue ;; esac
    due="$(next_due "$date" "$repeat")"
    days=$(( ($(epoch "$due") - today_s) / 86400 ))
    ms="$(milestone_of "$days")"
    ids+=("$id"); whats+=("$what"); dues+=("$due"); dayss+=("$days"); actions+=("$action"); repeats+=("$repeat"); mss+=("$ms")
  done < <(parse_items)
}

title_of() {      # $1 index
  local short="${whats[$1]%% (*}"
  printf 'Renewal: %s (due %s, %s)\n' "$short" "${dues[$1]}" "${mss[$1]}"
}

body_of() {       # $1 index
  local extra="change or delete the item in the file when it does not come back"
  [ -n "${repeats[$1]}" ] && extra="it repeats ${repeats[$1]}, so the date rolls forward by itself"
  printf '**%s**\n\nDue: **%s** (%s).\n\nWhat to do: %s\n\nFrom `%s` (item `%s`), opened by the yrRenewals skill of yrProject. Close this issue when it is done; %s.\n' \
    "${whats[$1]}" "${dues[$1]}" "$(days_text "${dayss[$1]}")" "${actions[$1]}" "$LIST" "${ids[$1]}" "$extra"
}

setup_labels() {
  need_gh
  run_gh label create "$RENEWAL" --repo "$repo" --color "$renewal_color" --description "$renewal_desc" --force || return 1
  run_gh label create "$MARK" --repo "$repo" --color "FBCA04" --description "Made by the yrIssues skill (yrProject)" --force || return 1
  if [ -n "$LABEL" ] && [ "$LABEL" != "$MARK" ]; then
    run_gh label create "$LABEL" --repo "$repo" --color "FBCA04" --description "Counted at the start of each Claude Code session" --force || return 1
  fi
  run_gh label create "priority: high"   --repo "$repo" --color "B60205" --description "Do soon" --force || return 1
  run_gh label create "priority: medium" --repo "$repo" --color "FBCA04" --description "Normal priority" --force || return 1
  run_gh label create "priority: low"    --repo "$repo" --color "C2E0C6" --description "When there's time" --force || return 1
}

# The line numbers (first and last) of the item with id $1 in the list, or "0 0": an item runs from its "- "
# line to the line before the next one (or the end of the file).
item_lines() {
  TID="$1" awk '
    BEGIN { tid = ENVIRON["TID"]; start = 0; found = 0; fstart = 0 }
    function close_item() { if (found && !fstart) { fstart = start; fend = NR - 1 } found = 0 }
    /^[ \t]*-([ \t]|$)/ { close_item(); start = NR; sub(/^[ \t]*-[ \t]*/, "") }
    start && !fstart && match($0, /^[ \t]*id[ \t]*:([ \t]|$)/) {
      v = substr($0, RSTART + RLENGTH); sub(/^[ \t]+/, "", v); sub(/[ \t]#.*$/, "", v); sub(/[ \t]+$/, "", v)
      if (v ~ /^".*"$/) v = substr(v, 2, length(v) - 2)
      if (v == tid) found = 1
    }
    END { if (found && !fstart) { fstart = start; fend = NR } print fstart + 0, fend + 0 }
  ' "$file"
}

quoted() { printf '"%s"' "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"; }

# Write the list again with the item $1 replaced by the block $2 (or removed, with an empty block), or the block
# appended after the last line (after an "items:" line, which is added if the file has none).
rewrite_list() {
  local first last tmp
  read -r first last <<< "$(item_lines "$1")"
  tmp="$(mktemp)"
  if [ "$first" -gt 0 ]; then
    FIRST="$first" LAST="$last" BLK="$2" awk '
      NR == ENVIRON["FIRST"] + 0 { if (ENVIRON["BLK"] != "") printf "%s", ENVIRON["BLK"] }
      NR >= ENVIRON["FIRST"] + 0 && NR <= ENVIRON["LAST"] + 0 { next }
      { print }' "$file" > "$tmp"
  else
    [ -z "$2" ] && { rm -f "$tmp"; return 1; }
    cp "$file" "$tmp"
    [ -z "$(tail -c 1 "$tmp")" ] || printf '\n' >> "$tmp"
    grep -q '^items:' "$tmp" || printf 'items:\n' >> "$tmp"
    printf '%s' "$2" >> "$tmp"
  fi
  cat "$tmp" > "$file" && rm -f "$tmp"
}

case "$cmd" in

  add)
    bad_args=0
    [ -n "$o_id" ] && [ -n "$o_what" ] && [ -n "$o_date" ] && [ -n "$o_action" ] || {
      echo "yrRenewals.sh add: --id, --what, --date and --action are all needed (see --help)" >&2; bad_args=1; }
    [[ "$o_id" =~ ^[A-Za-z0-9-]+$ ]] || { echo "yrRenewals.sh add: the id must be letters, digits and hyphens, not '$o_id'" >&2; bad_args=1; }
    valid_date "$o_date" || { echo "yrRenewals.sh add: --date needs a date YYYY-MM-DD, not '$o_date'" >&2; bad_args=1; }
    case "$o_repeat" in ""|monthly|yearly) ;; *) echo "yrRenewals.sh add: --repeat must be monthly or yearly, not '$o_repeat'" >&2; bad_args=1 ;; esac
    [ "$bad_args" -eq 0 ] || exit 2
    block="  - id: $o_id
    what: $(quoted "$o_what")
    date: $o_date
"
    [ -n "$o_repeat" ] && block="${block}    repeat: $o_repeat
"
    block="${block}    action: $(quoted "$o_action")
"
    read -r first _ <<< "$(item_lines "$o_id")"
    rewrite_list "$o_id" "$block" || { echo "yrRenewals.sh add: could not write $file" >&2; exit 1; }
    load_items
    for i in "${!ids[@]}"; do
      [ "${ids[$i]}" = "$o_id" ] || continue
      printf '%s: %s  %s  %s: %s%s\n' "$([ "$first" -gt 0 ] && echo replaced || echo added)" "${dues[$i]}" "$(days_text "${dayss[$i]}")" "${ids[$i]}" "${whats[$i]}" "${repeats[$i]:+ [${repeats[$i]}]}"
    done
    echo "Push the list: the workflow on GitHub reads the pushed copy."
    exit $bad
    ;;

  remove)
    [ -n "$o_id" ] || { echo "yrRenewals.sh remove: give --id ID" >&2; exit 2; }
    rewrite_list "$o_id" "" || { echo "yrRenewals.sh remove: no item with the id '$o_id' in $file" >&2; exit 1; }
    echo "removed: $o_id"
    ;;

  list)
    load_items
    if [ ${#ids[@]} -eq 0 ]; then
      echo "No items in $LIST (today: $today). Add one: see the file, or bash $(basename "$0") --help."
      exit $bad
    fi
    echo "Things that expire or renew ($LIST; today: $today), the soonest first:"
    for i in "${!ids[@]}"; do
      printf '%s\037%s\037%s\037%s\037%s\037%s\n' "${dues[$i]}" "${dayss[$i]}" "${ids[$i]}" "${whats[$i]}" "${repeats[$i]}" "${mss[$i]}"
    done | sort | while IFS=$'\037' read -r due days id what repeat ms; do
      printf '  %s  %-16s %s: %s%s%s\n' "$due" "$(days_text "$days")" "$id" "$what" "${repeat:+ [$repeat]}" \
        "${ms:+  <- reminder today: $ms}"
    done
    echo "Reminders are opened as issues 60, 30, 7 and 1 days before the date, and when it is overdue."
    exit $bad
    ;;

  check)
    load_items
    due_now=()
    for i in "${!ids[@]}"; do [ -n "${mss[$i]}" ] && due_now+=("$i"); done
    if [ ${#due_now[@]} -eq 0 ]; then
      echo "No reminder is due today ($today): ${#ids[@]} item(s) in $LIST."
      exit $bad
    fi
    if [ "$dry" -eq 1 ]; then
      for i in "${due_now[@]}"; do echo "would open: $(title_of "$i")  [priority: $(priority_of "${mss[$i]}")]"; done
      echo "--dry-run: ${#due_now[@]} reminder(s) would be opened (if not open or closed already); nothing was changed."
      exit $bad
    fi
    need_gh
    existing="$(run_gh issue list --repo "$repo" --state all --label "$RENEWAL" --limit 500 --json title --jq '.[].title' 2>&1)" || {
      # no such label yet: no reminder exists either
      if printf '%s' "$existing" | grep -qi 'label'; then existing=""; else
        echo "yrRenewals.sh: could not read the issues of $repo: $existing" >&2; exit 1; fi
    }
    opened=0; skipped=0; labels_done=0
    for i in "${due_now[@]}"; do
      title="$(title_of "$i")"
      if grep -qxF "$title" <<< "$existing"; then skipped=$((skipped + 1)); continue; fi
      if [ "$labels_done" -eq 0 ]; then setup_labels >/dev/null || { echo "yrRenewals.sh: could not make the labels" >&2; exit 1; }; labels_done=1; fi
      labels=(--label "$RENEWAL" --label "$MARK" --label "priority: $(priority_of "${mss[$i]}")")
      [ -n "$LABEL" ] && [ "$LABEL" != "$MARK" ] && labels+=(--label "$LABEL")
      url="$(run_gh issue create --repo "$repo" --title "$title" --body "$(body_of "$i")" "${labels[@]}")" || {
        echo "yrRenewals.sh: could not open '$title'" >&2; exit 1; }
      echo "opened: $title  $url"
      opened=$((opened + 1))
    done
    echo "$opened reminder(s) opened, $skipped already open or closed (today: $today)."
    exit $bad
    ;;

  setup-labels)
    setup_labels && echo "the labels of the reminders are on GitHub ($repo): $RENEWAL, $MARK, the priorities"
    if [ -f "$root/$CONFIG" ] && [ "$has_category" -eq 0 ]; then
      echo "note: $CONFIG has no category $RENEWAL, so the yrIssues skill does not know it. Add this line to CATEGORIES there:" >&2
      echo "  \"$RENEWAL|$renewal_color|$renewal_desc\"" >&2
    fi
    ;;
esac
