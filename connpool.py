#!/usr/bin/env python3

"""
Summarize MongoDB CONNPOOL events from log input.

Usage:
  cat mongodb.log | python connpool.py
  python connpool.py --input mongodb.log
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, TextIO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize details from MongoDB CONNPOOL log events."
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help="Path to log file when stdin is not piped.",
    )
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=25,
        help="Max rows to print per section (default: 25).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Print all rows for each section.",
    )
    return parser.parse_args()


def extract_ts(event: dict[str, Any]) -> str | None:
    t = event.get("t")
    if isinstance(t, dict):
        d = t.get("$date")
        if isinstance(d, str):
            return d
    return None


def print_counter(title: str, counter: Counter[Any], limit: int | None) -> None:
    print(title)
    if not counter:
        print("  (none)")
        print()
        return

    items = counter.most_common() if limit is None else counter.most_common(limit)
    width = max(len(str(k)) for k, _ in items)
    for key, count in items:
        print(f"  {str(key):<{width}}  {count}")
    print()


def summarize(handle: TextIO) -> dict[str, Any]:
    total_lines = 0
    parse_errors = 0
    connpool_entries = 0

    severity_counts: Counter[str] = Counter()
    context_counts: Counter[str] = Counter()
    id_counts: Counter[str] = Counter()
    msg_counts: Counter[str] = Counter()
    host_counts: Counter[str] = Counter()
    error_counts: Counter[str] = Counter()
    attr_key_counts: Counter[str] = Counter()
    error_json_events: list[str] = []

    # host -> msg -> count
    host_msg_counts: dict[str, Counter[str]] = defaultdict(Counter)

    num_open_values: list[int] = []
    num_open_by_host: dict[str, list[int]] = defaultdict(list)

    first_ts: str | None = None
    last_ts: str | None = None

    for raw_line in handle:
        total_lines += 1
        line = raw_line.strip()
        if not line or not line.startswith("{"):
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue

        if not isinstance(event, dict):
            continue
        if event.get("c") != "CONNPOOL":
            continue

        connpool_entries += 1

        ts = extract_ts(event)
        if ts:
            if first_ts is None or ts < first_ts:
                first_ts = ts
            if last_ts is None or ts > last_ts:
                last_ts = ts

        severity = str(event.get("s", "<missing>"))
        ctx = str(event.get("ctx", "<missing>"))
        eid = str(event.get("id", "<missing>"))
        msg = str(event.get("msg", "<missing>"))

        severity_counts[severity] += 1
        context_counts[ctx] += 1
        id_counts[eid] += 1
        msg_counts[msg] += 1

        attr = event.get("attr", {})
        if not isinstance(attr, dict):
            attr = {}

        for key in attr.keys():
            attr_key_counts[str(key)] += 1

        host = str(attr.get("hostAndPort", "<missing>"))
        host_counts[host] += 1
        host_msg_counts[host][msg] += 1

        if "error" in attr:
            error_counts[str(attr.get("error"))] += 1
            error_json_events.append(line)

        noc = attr.get("numOpenConns")
        if isinstance(noc, int):
            num_open_values.append(noc)
            num_open_by_host[host].append(noc)

    return {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "connpool_entries": connpool_entries,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "severity_counts": severity_counts,
        "context_counts": context_counts,
        "id_counts": id_counts,
        "msg_counts": msg_counts,
        "host_counts": host_counts,
        "error_counts": error_counts,
        "error_json_events": error_json_events,
        "attr_key_counts": attr_key_counts,
        "host_msg_counts": host_msg_counts,
        "num_open_values": num_open_values,
        "num_open_by_host": num_open_by_host,
    }


def print_num_open_summary(values: list[int], by_host: dict[str, list[int]]) -> None:
    print("numOpenConns summary")
    if not values:
        print("  (none)")
        print()
        return

    total = sum(values)
    avg = total / len(values)
    print(f"  samples: {len(values)}")
    print(f"  min   : {min(values)}")
    print(f"  max   : {max(values)}")
    print(f"  avg   : {avg:.2f}")
    print()

    print("numOpenConns by host")
    for host in sorted(by_host.keys()):
        vals = by_host[host]
        host_avg = sum(vals) / len(vals)
        print(
            f"  {host}: samples={len(vals)} min={min(vals)} "
            f"max={max(vals)} avg={host_avg:.2f}"
        )
    print()


def print_host_message_matrix(
    host_msg_counts: dict[str, Counter[str]],
    max_rows: int | None,
) -> None:
    print("Host + message counts")
    rows: list[tuple[str, str, int]] = []
    for host, msg_counter in host_msg_counts.items():
        for msg, count in msg_counter.items():
            rows.append((host, msg, count))

    if not rows:
        print("  (none)")
        print()
        return

    rows.sort(key=lambda row: row[2], reverse=True)
    if max_rows is not None:
        rows = rows[:max_rows]

    host_w = max(len(r[0]) for r in rows)
    msg_w = max(len(r[1]) for r in rows)
    for host, msg, count in rows:
        print(f"  {host:<{host_w}}  {msg:<{msg_w}}  {count}")
    print()


def print_error_json_events(events: list[str]) -> None:
    print("Full JSON for events with attr.error")
    if not events:
        print("  (none)")
        print()
        return

    for i, event_json in enumerate(events, start=1):
        print(f"[{i}] {event_json}")
    print()


def main() -> int:
    args = parse_args()
    max_rows = None if args.all else args.top

    if sys.stdin.isatty():
        if not args.input:
            print("ERROR: no piped input detected. Pipe log input or use --input.")
            return 1
        in_path = Path(args.input)
        if not in_path.exists():
            print(f"ERROR: input file not found: {in_path}")
            return 1
        with in_path.open("r", encoding="utf-8", errors="replace") as handle:
            data = summarize(handle)
        source = str(in_path)
    else:
        data = summarize(sys.stdin)
        source = "stdin"

    print("MongoDB CONNPOOL Summary")
    print("========================")
    print(f"Input source      : {source}")
    print(f"Total lines       : {data['total_lines']}")
    print(f"JSON parse errors : {data['parse_errors']}")
    print(f"CONNPOOL entries  : {data['connpool_entries']}")
    print(f"First timestamp   : {data['first_ts'] or '<not available>'}")
    print(f"Last timestamp    : {data['last_ts'] or '<not available>'}")
    print()

    print_counter("By severity", data["severity_counts"], max_rows)
    print_counter("By context", data["context_counts"], max_rows)
    print_counter("By event id", data["id_counts"], max_rows)
    print_counter("By message", data["msg_counts"], max_rows)
    print_counter("By hostAndPort", data["host_counts"], max_rows)
    print_counter("Error values", data["error_counts"], max_rows)
    print_counter("Attribute key presence", data["attr_key_counts"], max_rows)

    print_num_open_summary(data["num_open_values"], data["num_open_by_host"])
    print_host_message_matrix(data["host_msg_counts"], max_rows)
    print_error_json_events(data["error_json_events"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
