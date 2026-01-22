#!/usr/bin/env python3
"""Validate requirements files for CI.

Checks performed:
- No triple-backtick fences
- No non-package markdown content
- Lines are either comments, pip options (starting with - or --), or package specs

Exit code 0 on success, 1 on failure.
"""
import re
import sys

REQ_FILES = ["requirements.txt", "requirements-dev.txt"]
PACKAGE_RE = re.compile(r"^[A-Za-z0-9_.+\-]+(?:\[.*\])?(?:==|~=|!=|>=|<=|@).+")
SIMPLE_PKG_RE = re.compile(r"^[A-Za-z0-9_.+\-]+(?:\[.*\])?$")

errors = []

for path in REQ_FILES:
    try:
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                s = line.rstrip("\n")
                if "```" in s:
                    errors.append(f"{path}:{i}: contains triple-backtick fence")
                    continue
                s_strip = s.strip()
                if not s_strip or s_strip.startswith("#"):
                    continue
                if s_strip.startswith("-r") or s_strip.startswith("-e") or s_strip.startswith("--"):
                    continue
                # allow editable refs and git urls containing @
                if PACKAGE_RE.match(s_strip) or SIMPLE_PKG_RE.match(s_strip):
                    continue
                errors.append(f"{path}:{i}: invalid line: {s_strip}")
    except FileNotFoundError:
        errors.append(f"{path}: file not found")

if errors:
    print("Requirements validation failed:")
    for e in errors:
        print(" - ", e)
    print("\nFix the files or update the validator logic. Failing CI to prevent regressions.")
    sys.exit(1)

print("Requirements validation passed ✅")
sys.exit(0)
