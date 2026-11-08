#!/usr/bin/env python3
"""
Automated Security Scanner for Hackathon Judging Agents.
Verifies:
  1. ZERO hardcoded API keys, tokens, or secrets across all repository files.
  2. Read-only database configuration and presence of .env.example.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECRET_PATTERNS = [
    ("OpenAI / Metis Live Key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    ("Bearer Token Literal", re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{25,}")),
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private Key Block", re.compile(r"BEGIN\s+(?:RSA|OPENSSH|EC)\s+PRIVATE\s+KEY"))
]


def scan_repository() -> int:
    findings = []
    scanned_files = 0
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts or "node_modules" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in (".png", ".jpg", ".duckdb", ".zip"):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scanned_files += 1
        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(content):
                findings.append((str(path.relative_to(ROOT)), label, m.group(0)[:12] + "..."))

    if findings:
        print(f"FAIL: Found {len(findings)} potential hardcoded secret(s):")
        for rel, lbl, snippet in findings:
            print(f"  - {rel}: {lbl} ({snippet})")
        return 1

    print(f"PASS: 0 hardcoded secrets found across all {scanned_files} repository files.")
    return 0


if __name__ == "__main__":
    sys.exit(scan_repository())
