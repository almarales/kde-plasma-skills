#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Install, update, check or remove the KDE Plasma skills bundle.
#
#   ./install.sh                    install or update, user scope
#   ./install.sh --scope project    install or update, inside this repository
#   ./install.sh --root DIR         install into DIR instead of the default
#   ./install.sh check              report drift, duplicates and resolution
#   ./install.sh uninstall          remove the bundle from the target root
#
# An update replaces the installed copy completely: a file removed or renamed
# upstream does not survive in the installation, and a copy of the same skill
# left in another scanned root is reported instead of silently shadowing it.

set -euo pipefail

BUNDLE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILLS=(kde-plasma-ui-ux kde-plasma-best-practices kde-plasma-builder)

ACTION=install
SCOPE=user
ROOT=""
REFRESH=1

info()  { printf '  %s\n' "$*"; }
warn()  { printf '  warning: %s\n' "$*" >&2; }
fail()  { printf '  error: %s\n' "$*" >&2; exit 1; }

usage() {
    sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit "${1:-0}"
}

while [ $# -gt 0 ]; do
    case "$1" in
        check|install|uninstall) ACTION="$1"; shift ;;
        --scope) SCOPE="${2:-}"; shift 2 ;;
        --root)  ROOT="${2:-}"; shift 2 ;;
        --no-registry) REFRESH=0; shift ;;
        -h|--help) usage 0 ;;
        *) fail "unknown argument: $1" ;;
    esac
done

case "$SCOPE" in
    user)    DEFAULT_ROOT="$HOME/.agents/skills" ;;
    project) DEFAULT_ROOT="$BUNDLE/.agents/skills" ;;
    *) fail "--scope must be 'user' or 'project'" ;;
esac
TARGET_ROOT="${ROOT:-$DEFAULT_ROOT}"

# --- registry helpers -------------------------------------------------------

registry_list() {
    command -v gentle-ai >/dev/null 2>&1 || return 1
    gentle-ai skill-registry list 2>/dev/null || return 1
}

registry_refresh() {
    [ "$REFRESH" -eq 1 ] || { info "registry refresh skipped (--no-registry)"; return 0; }
    command -v gentle-ai >/dev/null 2>&1 || {
        warn "gentle-ai not found: the skill registry was not refreshed"
        return 0
    }
    gentle-ai skill-registry refresh >/dev/null 2>&1 \
        && info "skill registry refreshed" \
        || warn "skill registry refresh failed; run 'gentle-ai skill-registry refresh' by hand"
}

# Where the registry currently resolves a skill, if it knows it.
resolved_path() {
    registry_list | awk -v n="$1" -F'\t' '$1 == n { print $3; exit }'
}

# --- actions -----------------------------------------------------------------

sync_skill() {
    local name="$1"
    local src="$BUNDLE/$name"
    local dst="$TARGET_ROOT/$name"
    mkdir -p "$dst"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "$src/" "$dst/"
    else
        rm -rf "$dst"; mkdir -p "$dst"; cp -a "$src/." "$dst/"
    fi
}

do_install() {
    printf 'Installing into %s\n' "$TARGET_ROOT"
    for skill in "${SKILLS[@]}"; do
        [ -d "$BUNDLE/$skill" ] || fail "missing skill directory: $skill"
        sync_skill "$skill"
        info "updated  $skill"
    done
    registry_refresh

    # The registry keeps one entry per skill name. If it still resolves one of
    # ours to a different path, a stale copy in another scanned root wins.
    local resolved resolved_dir resolved_root
    for skill in "${SKILLS[@]}"; do
        resolved="$(resolved_path "$skill" || true)"
        [ -n "$resolved" ] || continue
        resolved_dir="${resolved%/*}"
        resolved_root="${resolved_dir%/*}"
        if [ ! -f "$resolved" ]; then
            warn "$skill resolves to $resolved, which no longer exists"
        elif [ "$resolved_root" != "$TARGET_ROOT" ]; then
            warn "$skill resolves to $resolved, not to $TARGET_ROOT: a copy in another root shadows this one"
        fi
    done
    printf 'Done. %s skill(s) in %s\n' "${#SKILLS[@]}" "$TARGET_ROOT"
}

do_uninstall() {
    printf 'Removing from %s\n' "$TARGET_ROOT"
    for skill in "${SKILLS[@]}"; do
        if [ -d "$TARGET_ROOT/$skill" ]; then
            rm -rf "$TARGET_ROOT/$skill"
            info "removed   $skill"
        else
            info "absent    $skill"
        fi
    done
    registry_refresh
}

do_check() {
    local problems=0
    local installed resolved resolved_dir resolved_root
    printf 'Bundle:  %s\n' "$BUNDLE"
    printf 'Target:  %s\n\n' "$TARGET_ROOT"

    for skill in "${SKILLS[@]}"; do
        installed="$TARGET_ROOT/$skill"
        if [ ! -d "$installed" ]; then
            warn "$skill is not installed in $TARGET_ROOT"
            problems=$((problems + 1))
            continue
        fi
        if diff -rq "$BUNDLE/$skill" "$installed" >/dev/null 2>&1; then
            info "ok        $skill matches the bundle"
        else
            warn "$skill differs from the bundle:"
            diff -rq "$BUNDLE/$skill" "$installed" 2>&1 | sed 's/^/            /' >&2
            problems=$((problems + 1))
        fi
        resolved="$(resolved_path "$skill" || true)"
        if [ -n "$resolved" ]; then
            resolved_dir="${resolved%/*}"
            resolved_root="${resolved_dir%/*}"
            if [ ! -f "$resolved" ]; then
                warn "$skill resolves to $resolved, which no longer exists"
                problems=$((problems + 1))
            elif [ "$resolved_root" != "$TARGET_ROOT" ]; then
                warn "$skill resolves to $resolved: another root shadows this installation"
                problems=$((problems + 1))
            fi
        fi
    done

    if [ "$problems" -eq 0 ]; then
        printf '\nNo problems found.\n'
    else
        printf '\n%s problem(s) found.\n' "$problems" >&2
    fi
    return "$problems"
}

case "$ACTION" in
    install)   do_install ;;
    uninstall) do_uninstall ;;
    check)     do_check ;;
esac
