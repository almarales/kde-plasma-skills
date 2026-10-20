#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# Copyright the original author of the kde-plasma-design project.
#
# Developed originally in the kde-plasma-design project under
# LGPL-2.0-or-later, and relicensed to Apache-2.0 by the copyright holder
# for this bundle, so that the whole bundle ships under one license.
#
# Derived from the `kde-plasma-design` linter (same project family). The rule
# catalogue was re-keyed to the rules stated in the kde-plasma-skills bundle;
# every check below cites the reference that states the rule it enforces.
"""Static, heuristic checker for KDE Plasma 6 QML and plasmoid metadata.

It enforces the machine-checkable subset of the rules in the kde-plasma-skills
bundle. It is NOT a substitute for review: a clean run proves nothing about
layout, contrast, keyboard flow or RTL, and it cannot tell whether a decision
was the right one.

What it can do is keep a widget on the public, supported surface: no Plasma 5
API, no versioned import, no private module, a correct `metadata.json`, theme
roles instead of literal colors, and Kirigami units instead of pixel literals.
Those are the checks that decide whether a widget still works in a future
Plasma release.

Usage:
  python3 lint_qml.py path/to/plasmoid [more paths] [--json] [--fail-on error|warning|never]
  python3 lint_qml.py --list-checks
"""

import argparse
import json
import os
import re
import sys

# id: (severity, message, fix, basis)
# basis names the reference in the bundle that states the rule.
CHECKS = {
    # --- Forward compatibility: the public, supported Plasma surface -------
    "FC01": ("error", "Plasma 5 API in use",
             "Use the Plasma 6 replacement: Kirigami.Theme / Kirigami.Units / Kirigami.Icon.",
             "FWD-01 references/forward-compatibility.md#plasma-5-apis-removed"),
    "FC02": ("error", "Versioned QML import",
             "Qt 6 imports are unversioned: `import QtQuick`, `import org.kde.kirigami as Kirigami`.",
             "FWD-02 references/forward-compatibility.md#imports-are-unversioned"),
    "FC03": ("warning", "Private Plasma module import",
             "Private modules are not public API and can change without notice. Use the public module.",
             "FWD-03 references/forward-compatibility.md#private-modules-are-not-api"),
    "FC04": ("error", "metadata.json: X-Plasma-API-Minimum-Version missing or below 6.0",
             'Set "X-Plasma-API-Minimum-Version": "6.0", or the widget is treated as Plasma 5 only.',
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
    "FC05": ("error", "metadata.json: KPackageStructure is not Plasma/Applet",
             'Set "KPackageStructure": "Plasma/Applet" at the top level.',
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
    "FC06": ("error", "metadata.json: removed Plasma 5 key present",
             "Remove X-Plasma-MainScript and X-Plasma-API; ui/main.qml is always the entry point.",
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
    "FC07": ("error", "metadata.json: KPlugin.Id under org.kde.*",
             "org.kde.* is reserved for KDE contributions. Use a reverse-DNS id you own.",
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
    "FC08": ("warning", "metadata.json: no KPlugin.License",
             "Declare an SPDX license id so packagers and users can see it.",
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
    "FC09": ("info", "Plasma5Support import",
             "The compatibility layer is a migration aid, not a destination. Isolate it behind one component.",
             "FWD-05 references/plasma-development.md#qml-api-surface-in-plasma-6"),
    # --- Native surface: theme roles, units and platform material ----------
    "NS01": ("error", "Hex color literal",
             "Bind to a Kirigami.Theme role. Colors must survive every scheme the user picks.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 1"),
    "NS02": ("error", "Named CSS color literal",
             "Named colors are forbidden in Plasma UI chrome; use a theme role.",
             "kde-plasma-ui-ux visual-consistency.md"),
    "NS03": ("error", "Qt.rgba with literal channels",
             "Literal channels freeze one palette. Derive the tint from a theme role instead.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 1"),
    "NS04": ("info", "Qt.rgba derived from theme role channels",
             "Role plus alpha follows the scheme. Record it in the documented allowlist.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 1"),
    "NS05": ("error", "Custom material",
             "Do not paint your own surface: no Gradient, MultiEffect, DropShadow, FastBlur or layer.effect.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 2"),
    "NS06": ("warning", "glowEnabled used",
             "Use MultiEffect shadowEnabled with a theme role, in an optional layer.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 2"),
    "NS07": ("warning", "Literal spacing, margin, padding or radius",
             "Use Kirigami.Units.smallSpacing / largeSpacing / cornerRadius so it scales.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 4"),
    "NS08": ("warning", "Literal font size",
             "Use the typography ladder: Kirigami.Theme fonts and Kirigami.Heading levels.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 6"),
    "NS09": ("warning", "Literal animation duration",
             "Use Kirigami.Units.*Duration so the animation follows the system setting.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 8"),
    "NS10": ("error", "Infinite animation loop",
             "Official applets never loop an animation. Progress is a BusyIndicator.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 8"),
    "NS11": ("warning", "Literal fixed size in pixels",
             "Use Kirigami.Units.gridUnit * N so the size follows the scale factor.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 4"),
    "NS12": ("warning", "No Plasmoid.backgroundHints in the root file",
             "Request the theme frame: DefaultBackground | ConfigurableBackground.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 3"),
    "NS13": ("warning", "compactRepresentation without Accessible.name",
             "Give the compact view an Accessible.name and role so it is reachable without a pointer.",
             "kde-plasma-ui-ux official-applet-anatomy.md#testable-rules 10"),
    # --- Engineering rules owned by this skill ------------------------------
    "EN01": ("warning", "Timer runs without visibility gating",
             "Gate periodic work on expanded or visible, so a collapsed widget costs nothing.",
             "BP-QML-06 references/rules/qml/timer-lifecycle.md"),
    "EN02": ("error", "metadata.json is not valid JSON",
             "Fix the JSON syntax; the package cannot be parsed otherwise.",
             "FWD-04 references/forward-compatibility.md#metadata-json-requirements"),
}

NAMED = ("white black red green blue gray grey yellow orange purple cyan magenta pink brown "
         "silver gold navy teal lime maroon olive aqua fuchsia").split()

RE_HEX = re.compile(r"[\"']#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})[\"']")
RE_NAMED = re.compile(r"\b(?:\w+\.)?[cC]olor\s*:\s*[\"'](%s)[\"']" % "|".join(NAMED))
RE_RGBA = re.compile(r"Qt\.rgba\(([^)]*)\)")
RE_PIXEL = re.compile(r"\bpixelSize\s*:\s*\d")
RE_POINTSIZE = re.compile(r"\bpointSize\s*:\s*\d")
RE_IMPORT_VER = re.compile(r"^\s*import\s+(?:QtQuick[\w.]*|org\.kde\.[\w.]+)\s+\d+(?:\.\d+)?\b")
RE_REMOVED = re.compile(r"\bPlasmaCore\.(?:Units|Theme|IconItem|ColorScope)\b")
RE_DURATION = re.compile(r"\bduration\s*:\s*\d")
RE_METRIC = re.compile(r"\b(spacing|radius|margins|leftMargin|rightMargin|topMargin|bottomMargin|padding|"
                       r"leftPadding|rightPadding|topPadding|bottomPadding|rowSpacing|columnSpacing)"
                       r"\s*:\s*(\d+(?:\.\d+)?)\s*(?:;|\}|$)")
RE_SIZE = re.compile(r"\b(?:Layout\.(?:preferred|minimum|maximum)(?:Width|Height)|implicitWidth|implicitHeight|"
                     r"width|height)\s*:\s*(\d+(?:\.\d+)?)\s*(?:;|\}|$)")
RE_MATERIAL = re.compile(r"\b(Gradient|MultiEffect|DropShadow|FastBlur)\b|layer\.effect")
RE_GLOW = re.compile(r"\bglowEnabled\b")
RE_INFINITE = re.compile(r"loops\s*:\s*Animation\.Infinite")
RE_PRIVATE = re.compile(r"^\s*import\s+org\.kde\.plasma\.private\b")
RE_P5S = re.compile(r"^\s*import\s+org\.kde\.plasma\.plasma5support\b")


def blank_comments(text):
    """Replace comment bodies with spaces, keeping line numbers intact."""
    out, i, n, q = [], 0, len(text), None
    while i < n:
        c = text[i]
        if q:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == q:
                q = None
            i += 1
            continue
        if c in "\"'`":
            q = c
            out.append(c)
            i += 1
            continue
        if text.startswith("//", i):
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if text.startswith("/*", i):
            while i < n and not text.startswith("*/", i):
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
            out.append("  ")
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def lint_qml(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = blank_comments(fh.read())
    lines = text.split("\n")
    found = []

    def hit(code, ln, extra=""):
        severity, message, fix, basis = CHECKS[code]
        found.append({"file": path, "line": ln, "check": code, "severity": severity,
                      "message": message + (f": {extra}" if extra else ""), "fix": fix, "basis": basis})

    for i, line in enumerate(lines, 1):
        m = RE_HEX.search(line)
        if m:
            hit("NS01", i, m.group(0))
        m = RE_NAMED.search(line)
        if m:
            hit("NS02", i, m.group(0).strip())
        m = RE_RGBA.search(line)
        if m:
            args = m.group(1)
            literal = re.match(r"\s*[\d.]+\s*,", args)
            hit("NS03" if literal else "NS04", i, args.strip())
        if RE_PIXEL.search(line) or RE_POINTSIZE.search(line):
            hit("NS08", i, line.strip())
        m = RE_IMPORT_VER.search(line)
        if m:
            hit("FC02", i, line.strip())
        m = RE_REMOVED.search(line)
        if m:
            hit("FC01", i, m.group(0))
        m = RE_PRIVATE.search(line)
        if m:
            hit("FC03", i, line.strip())
        if RE_P5S.search(line):
            hit("FC09", i)
        if RE_DURATION.search(line):
            hit("NS09", i, line.strip())
        m = RE_METRIC.search(line)
        if m and float(m.group(2)) >= 2:
            hit("NS07", i, f"{m.group(1)}: {m.group(2)}")
        m = RE_SIZE.search(line)
        if m and float(m.group(1)) >= 40:
            hit("NS11", i, line.strip())
        m = RE_MATERIAL.search(line)
        if m:
            hit("NS05", i, m.group(0))
        if RE_GLOW.search(line):
            hit("NS06", i)
        if RE_INFINITE.search(line):
            hit("NS10", i)

    if "compactRepresentation" in text and "Accessible.name" not in text:
        ln = next((i for i, l in enumerate(lines, 1) if "compactRepresentation" in l), 1)
        hit("NS13", ln)
    if os.path.basename(path) == "main.qml" and "backgroundHints" not in text:
        hit("NS12", 1)

    for m in re.finditer(r"\bTimer\s*\{([^{}]*)\}", text):
        body = m.group(1)
        if re.search(r"\brunning\s*:\s*true\b", body) and not re.search(r"\b(expanded|visible)\b", body):
            hit("EN01", text.count("\n", 0, m.start()) + 1)
    return found


def lint_metadata(path):
    found = []

    def hit(code, extra=""):
        severity, message, fix, basis = CHECKS[code]
        found.append({"file": path, "line": 1, "check": code, "severity": severity,
                      "message": message + (f": {extra}" if extra else ""), "fix": fix, "basis": basis})

    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        hit("EN02", str(exc))
        return found

    plugin = data.get("KPlugin", {})
    pid = plugin.get("Id", "")
    if pid.startswith("org.kde."):
        hit("FC07", pid)
    try:
        ok = float(str(data.get("X-Plasma-API-Minimum-Version", "0")).split(".")[0]) >= 6
    except ValueError:
        ok = False
    if not ok:
        hit("FC04")
    if data.get("KPackageStructure") != "Plasma/Applet":
        hit("FC05", str(data.get("KPackageStructure")))
    for removed in ("X-Plasma-MainScript", "X-Plasma-API"):
        if removed in data:
            hit("FC06", removed)
    if not plugin.get("License"):
        hit("FC08")
    return found


def collect(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "dist", "build")]
            for f in files:
                if f.endswith(".qml") or f == "metadata.json":
                    yield os.path.join(root, f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-checks", action="store_true", help="print the check catalogue and exit")
    ap.add_argument("--fail-on", choices=["error", "warning", "never"], default="error")
    a = ap.parse_args()

    if a.list_checks:
        for cid, (severity, message, fix, basis) in CHECKS.items():
            print(f"{cid}  {severity:<7}  {message}\n      basis: {basis}\n      fix:   {fix}")
        return 0

    if not a.paths:
        ap.error("at least one path is required")

    res = []
    for f in collect(a.paths):
        res += lint_metadata(f) if f.endswith("metadata.json") else lint_qml(f)

    if a.json:
        print(json.dumps(res, indent=2))
    else:
        for r in sorted(res, key=lambda r: (r["file"], r["line"])):
            print(f"{r['file']}:{r['line']}: {r['severity']} [{r['check']}] {r['message']}\n"
                  f"    basis: {r['basis']}\n    fix:   {r['fix']}")
        c = {s: sum(1 for r in res if r["severity"] == s) for s in ("error", "warning", "info")}
        print(f"\n{len(res)} finding(s): {c['error']} error, {c['warning']} warning, {c['info']} info.")
        print("Heuristic only: layout, contrast, keyboard flow and RTL still need review.")

    if a.fail_on == "never":
        return 0
    bad = any(r["severity"] == "error" for r in res) or (
        a.fail_on == "warning" and any(r["severity"] == "warning" for r in res))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
