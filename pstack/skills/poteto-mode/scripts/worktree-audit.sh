#!/usr/bin/env bash
# Local, read-only worktree audit. Reports size, age, local merge/ref state,
# and tracked, untracked, and ignored content. PR and session state are unknown.
# No bucket establishes deletion safety. Never fetches, queries services, or
# deletes worktrees. Temporary audit files are the only files it writes.
#
# Usage: worktree-audit.sh [-b|--base <ref>] [repo-path]
#   repo-path defaults to the current repo.
#   -b selects a local ref for the MERGED column (e.g. origin/integration).
#   Otherwise use origin/HEAD, then origin/main, then origin/master.
#   Remote-tracking refs are local snapshots and can be stale.
#   Exit 1 means an inspection failed; affected facts remain unknown.
set -u

export GIT_OPTIONAL_LOCKS=0
base=""
while [ $# -gt 0 ]; do
	case "$1" in
	-b|--base) [ $# -ge 2 ] || { echo "error: $1 needs a ref" >&2; exit 2; }; base="$2"; shift 2 ;;
	-h|--help) sed -n '2,/^set -u/p' "$0" | sed '$d; s/^# \{0,1\}//'; exit 0 ;;
	--) shift; break ;;
	-*) echo "error: unknown option: $1" >&2; exit 2 ;;
	*) break ;;
	esac
done
[ $# -le 1 ] || { echo "error: give at most one repo path" >&2; exit 2; }
repo="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$repo" ] || { echo "not in a git repo; pass a repo path" >&2; exit 1; }
cd -- "$repo" || exit 1
git rev-parse --git-dir >/dev/null 2>&1 || { echo "error: not a git repo: $repo" >&2; exit 1; }

if [ -z "$base" ]; then
	for cand in "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null)" origin/main origin/master; do
		[ -n "$cand" ] && git rev-parse --verify --quiet --end-of-options "$cand^{commit}" >/dev/null && { base="$cand"; break; }
	done
	[ -n "$base" ] || { echo "error: no local base ref; pass -b <ref>" >&2; exit 1; }
fi
base_oid=$(git rev-parse --verify --quiet --end-of-options "$base^{commit}") || { echo "error: base ref not found locally: $base" >&2; exit 1; }
scratch=$(mktemp -d) || exit 1
trap 'rm -f -- "$scratch/worktrees" "$scratch/status" "$scratch/rows"; rmdir -- "$scratch"' EXIT
if ! git worktree list --porcelain -z > "$scratch/worktrees"; then
	echo "error: cannot list worktrees" >&2
	exit 1
fi

# Escape table separators only after Git receives each complete NUL-delimited path.
cell() {
	local value=$1
	value=${value//\\/\\\\}
	value=${value//$'\t'/\\t}
	value=${value//$'\r'/\\r}
	value=${value//$'\n'/\\n}
	printf '%s' "$value"
}
failed=0
inspection_failed() {
	printf 'warn: cannot inspect %s for %s\n' "$1" "$(cell "$wt")" >&2
	row_failed=1
	failed=1
}
now=$(date +%s) || exit 1
main_seen=0
: > "$scratch/rows"
while IFS= read -r -d '' field; do
	case "$field" in 'worktree '*) wt=${field#worktree } ;; *) continue ;; esac
	if [ "$main_seen" = 0 ]; then main_seen=1; continue; fi
	row_failed=0
	size=unknown; age=unknown; merged=unknown; dirty=unknown; remote=unknown
	if usage=$(du -sh -- "$wt" 2>/dev/null); then
		size=${usage%%$'\t'*}
	else inspection_failed size; fi
	if head=$(git -C "$wt" rev-parse --verify HEAD 2>/dev/null); then
		git merge-base --is-ancestor "$head" "$base_oid" 2>/dev/null
		case $? in 0) merged=YES ;; 1) merged=no ;; *) inspection_failed merge-base ;; esac
	else inspection_failed HEAD; fi
	if head_ts=$(git -C "$wt" log -1 --format='%ct' HEAD 2>/dev/null) && [[ "$head_ts" =~ ^[0-9]+$ ]]; then
		age="$(( (now - head_ts) / 86400 ))d"
	else inspection_failed age; fi

	# Disable index refresh and override user settings that hide local content.
	if git -C "$wt" status --porcelain=v1 -z --untracked-files=all --ignored --ignore-submodules=none > "$scratch/status" 2>/dev/null; then
		tracked=0; untracked=0; ignored=0; status_failed=0
		while IFS= read -r -d '' entry; do
			xy=${entry:0:2}
			case "$xy" in
			'??') untracked=$((untracked + 1)) ;;
			'!!') ignored=$((ignored + 1)) ;;
			*) tracked=$((tracked + 1)) ;;
			esac
			case "$xy" in
			*R*|*C*) IFS= read -r -d '' original || { status_failed=1; break; } ;;
			esac
		done < "$scratch/status"
		if [ "$status_failed" = 1 ]; then inspection_failed status
		elif [ "$tracked" = 0 ] && [ "$untracked" = 0 ] && [ "$ignored" = 0 ]; then dirty=clean
		else dirty="tracked:$tracked,untracked:$untracked,ignored:$ignored"; fi
	else inspection_failed status; fi

	branch=$(git -C "$wt" symbolic-ref --quiet --short HEAD 2>/dev/null)
	branch_status=$?
	if [ "$branch_status" = 0 ]; then
		ref="refs/remotes/origin/$branch"
		git -C "$wt" show-ref --verify --quiet "$ref" 2>/dev/null
		ref_status=$?
		if [ "$ref_status" = 1 ]; then remote=no-local-ref
		elif [ "$ref_status" != 0 ]; then inspection_failed local-ref
		elif counts=$(git -C "$wt" rev-list --left-right --count "$ref...HEAD" 2>/dev/null); then
			read -r behind ahead <<< "$counts"
			if [[ "$ahead" =~ ^[0-9]+$ && "$behind" =~ ^[0-9]+$ ]]; then
				remote="local-ref:ahead$ahead,behind$behind"
			else inspection_failed local-ref; fi
		else inspection_failed local-ref; fi
	elif [ "$branch_status" = 1 ]; then remote=detached
	else inspection_failed branch; fi

	bucket=review
	if [ "$row_failed" = 1 ]; then bucket=review-unknown
	elif [ "$tracked" -gt 0 ]; then bucket=hold-wip
	elif [ "$untracked" -gt 0 ] || [ "$ignored" -gt 0 ]; then bucket=hold-local-content; fi
	printf '%s\t%s\t%s\t%s\t%s\tunknown\tunknown\t%s\t%s\n' \
		"$size" "$age" "$merged" "$dirty" "$remote" "$bucket" "$(cell "$wt")" >> "$scratch/rows"
done < "$scratch/worktrees"
[ "$main_seen" = 1 ] || { echo "error: worktree list has no primary entry" >&2; exit 1; }
printf '# base: %s (local snapshot)\n' "$(cell "$base")"
printf 'SIZE\tAGE\tMERGED\tDIRTY\tREMOTE\tPR\tLAST_CHAT\tBUCKET\tWORKTREE\n'
sort -t$'\t' -k1,1 -rh "$scratch/rows" || exit 1
exit "$failed"
