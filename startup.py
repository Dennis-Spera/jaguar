#!/usr/bin/env python3

"""
Detect mongod startup/shutdown occurrences and print JSON around them.

Usage:
  cat mongodb.log | python startup.py
  python startup.py --input mongodb.log
  python startup.py --input mongodb.log --context 5
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, TextIO


STARTUP_MESSAGES = {
    "Process Details",
    "Build Info",
    "Operating System",
    "Options set by command line",
}

STOP_PATTERNS = [
    re.compile(r"\bshutting down\b", re.IGNORECASE),
    re.compile(r"\bshutdown\b", re.IGNORECASE),
    re.compile(r"\bmongod shutdown complete\b", re.IGNORECASE),
    re.compile(r"\bdbexit\b", re.IGNORECASE),
    re.compile(r"\bterminating\b", re.IGNORECASE),
    re.compile(r"\bkill\b", re.IGNORECASE),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect mongod startup/shutdown events and show JSON context."
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help="Path to mongodb log file when stdin is not piped.",
    )
    parser.add_argument(
        "-c",
        "--context",
        type=int,
        default=3,
        help="Number of JSON records before/after each match (default: 3).",
    )
    return parser.parse_args()


def read_json_records(handle: TextIO) -> tuple[list[dict[str, Any]], int, int]:
    records: list[dict[str, Any]] = []
    total_lines = 0
    parse_errors = 0

    for raw_line in handle:
        total_lines += 1
        line = raw_line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            doc = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue
        if not isinstance(doc, dict):
            continue

        doc["__raw"] = line
        doc["__line"] = total_lines
        records.append(doc)

    return records, total_lines, parse_errors


def is_startup_event(doc: dict[str, Any]) -> bool:
    if doc.get("c") != "CONTROL":
        return False
    msg = doc.get("msg")
    return isinstance(msg, str) and msg in STARTUP_MESSAGES


def is_shutdown_event(doc: dict[str, Any]) -> bool:
    if doc.get("c") != "CONTROL":
        return False
    msg = doc.get("msg")
    if not isinstance(msg, str):
        return False
    for pattern in STOP_PATTERNS:
        if pattern.search(msg):
            return True
    return False


def ts(doc: dict[str, Any]) -> str:
    t = doc.get("t")
    if isinstance(t, dict):
        d = t.get("$date")
        if isinstance(d, str):
            return d
    return "<no-timestamp>"


def print_occurrence(
    title: str,
    docs: list[dict[str, Any]],
    idx: int,
    context: int,
    occurrence_no: int,
) -> None:
    start = max(0, idx - context)
    end = min(len(docs), idx + context + 1)

    center = docs[idx]
    print(f"[{title} #{occurrence_no}] line={center['__line']} ts={ts(center)} msg={center.get('msg', '<missing>')}")
    print("-" * 88)

    for i in range(start, end):
        mark = ">>>" if i == idx else "   "
        rec = docs[i]
        print(f"{mark} line={rec['__line']} {rec['__raw']}")
    print()


def main() -> int:
    args = parse_args()

    if args.context < 0:
        print("ERROR: --context must be >= 0")
        return 1

    if sys.stdin.isatty():
        if not args.input:
            print("ERROR: no piped input detected. Pipe mongodb.log or use --input.")
            return 1

        path = Path(args.input)
        if not path.exists():
            print(f"ERROR: input file not found: {path}")
            return 1

        with path.open("r", encoding="utf-8", errors="replace") as handle:
            docs, total_lines, parse_errors = read_json_records(handle)
        source = str(path)
    else:
        docs, total_lines, parse_errors = read_json_records(sys.stdin)
        source = "stdin"

    startup_idx: list[int] = []
    shutdown_idx: list[int] = []

    for i, doc in enumerate(docs):
        if is_startup_event(doc):
            startup_idx.append(i)
        if is_shutdown_event(doc):
            shutdown_idx.append(i)

    print("MongoDB Startup/Shutdown Detector")
    print("================================")
    print("DISCLAIMER: These results are estimates and should be verified.")
    print()
    print(f"Input source         : {source}")
    print(f"Total lines          : {total_lines}")
    print(f"JSON parse errors    : {parse_errors}")
    print(f"JSON records parsed  : {len(docs)}")
    print(f"Startup markers      : {len(startup_idx)}")
    print(f"Shutdown markers     : {len(shutdown_idx)}")
    print()

    if not startup_idx and not shutdown_idx:
        print("No startup/shutdown markers found.")
        return 0

    for n, idx in enumerate(startup_idx, start=1):
        print_occurrence("STARTUP", docs, idx, args.context, n)

    for n, idx in enumerate(shutdown_idx, start=1):
        print_occurrence("SHUTDOWN", docs, idx, args.context, n)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
