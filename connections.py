#!/usr/bin/env python3

"""
Create a connection report from MongoDB logs.

Report includes:
- Total connections opened and closed
- Per-IP open/close counts
- Per-user authentication counts and IP usage

Usage:
  cat mongodb.log | python connections.py
  python connections.py --input mongodb.log
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, TextIO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Report MongoDB connection open/close activity by IP and user."
    )
    parser.add_argument(
        "-i",
        "--input",
        default=None,
        help="Path to mongodb.log (used only if stdin is not piped).",
    )
    return parser.parse_args()


def extract_ip(remote: str) -> str:
    if not remote:
        return "<unknown>"

    # IPv6 in bracket form: [::1]:27017
    if remote.startswith("[") and "]" in remote:
        return remote[1 : remote.index("]")]

    # IPv4/host with port: host:port
    if ":" in remote:
        return remote.rsplit(":", 1)[0]

    return remote


def ctx_to_connection_id(ctx: str) -> int | None:
    match = re.fullmatch(r"conn(\d+)", ctx or "")
    if not match:
        return None
    return int(match.group(1))


def process_log(handle: TextIO) -> dict[str, Any]:
    opened_total = 0
    closed_total = 0
    parse_errors = 0
    total_lines = 0

    opened_by_ip: Counter[str] = Counter()
    closed_by_ip: Counter[str] = Counter()
    auth_by_user: Counter[str] = Counter()
    ips_by_user: dict[str, set[str]] = defaultdict(set)

    # Keep connection state for correlation between open/auth/close.
    conn_ip: dict[int, str] = {}
    conn_users: dict[int, set[str]] = defaultdict(set)

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

        component = event.get("c")
        message = event.get("msg", "")
        attr = event.get("attr", {})
        if not isinstance(attr, dict):
            attr = {}

        # Connection accepted
        if component == "NETWORK" and message == "Connection accepted":
            conn_id = attr.get("connectionId")
            remote = str(attr.get("remote", ""))
            ip = extract_ip(remote)

            opened_total += 1
            opened_by_ip[ip] += 1

            if isinstance(conn_id, int):
                conn_ip[conn_id] = ip
            continue

        # Connection ended
        if component == "NETWORK" and message == "Connection ended":
            conn_id = attr.get("connectionId")
            remote = str(attr.get("remote", ""))
            ip = extract_ip(remote)

            closed_total += 1
            closed_by_ip[ip] += 1

            if isinstance(conn_id, int):
                # Prefer current event's ip, but keep mapping coherent.
                conn_ip.setdefault(conn_id, ip)
            continue

        # Successful authentication
        if component == "ACCESS" and message == "Successfully authenticated":
            user = str(attr.get("user", "<unknown>"))
            client = str(attr.get("client", ""))
            ip = extract_ip(client)

            auth_by_user[user] += 1
            ips_by_user[user].add(ip)

            ctx = str(event.get("ctx", ""))
            conn_id = ctx_to_connection_id(ctx)
            if conn_id is not None:
                conn_users[conn_id].add(user)
                # Backfill user->ip if we only know conn id from NETWORK open event.
                if conn_id in conn_ip:
                    ips_by_user[user].add(conn_ip[conn_id])

    # Derived metrics
    currently_open_estimate = opened_total - closed_total

    return {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "opened_total": opened_total,
        "closed_total": closed_total,
        "currently_open_estimate": currently_open_estimate,
        "opened_by_ip": opened_by_ip,
        "closed_by_ip": closed_by_ip,
        "auth_by_user": auth_by_user,
        "ips_by_user": ips_by_user,
    }


def print_counter_table(title: str, left: Counter[str], right: Counter[str]) -> None:
    print(title)
    all_ips = sorted(set(left.keys()) | set(right.keys()))
    if not all_ips:
        print("  (none)")
        return

    header = f"{'IP Address':<24} {'Opened':>8} {'Closed':>8} {'Delta':>8}"
    print(header)
    print("-" * len(header))
    for ip in all_ips:
        opened = left.get(ip, 0)
        closed = right.get(ip, 0)
        delta = opened - closed
        print(f"{ip:<24} {opened:>8} {closed:>8} {delta:>8}")


def print_user_table(auth_by_user: Counter[str], ips_by_user: dict[str, set[str]]) -> None:
    print("By user (successful authentication)")
    users = sorted(auth_by_user.keys())
    if not users:
        print("  (none)")
        return

    header = f"{'User':<24} {'Auths':>8} {'Unique IPs':>12}  IP List"
    print(header)
    print("-" * len(header))
    for user in users:
        ips = sorted(ips_by_user.get(user, set()))
        ip_list = ", ".join(ips)
        print(f"{user:<24} {auth_by_user[user]:>8} {len(ips):>12}  {ip_list}")


def main() -> int:
    args = parse_args()

    if sys.stdin.isatty():
        if not args.input:
            print("ERROR: no piped input detected. Pipe mongodb.log or use --input.")
            return 1

        input_path = Path(args.input)
        if not input_path.exists():
            print(f"ERROR: input file not found: {input_path}")
            return 1

        with input_path.open("r", encoding="utf-8", errors="replace") as handle:
            report = process_log(handle)
        input_source = str(input_path)
    else:
        report = process_log(sys.stdin)
        input_source = "stdin"

    print("MongoDB Connection Report")
    print("=========================")
    print(f"Input source             : {input_source}")
    print(f"Total lines              : {report['total_lines']}")
    print(f"JSON parse errors        : {report['parse_errors']}")
    print(f"Connections opened       : {report['opened_total']}")
    print(f"Connections closed       : {report['closed_total']}")
    print(f"Current open (estimate)  : {report['currently_open_estimate']}")
    print()

    print_counter_table(
        "By IP",
        report["opened_by_ip"],
        report["closed_by_ip"],
    )
    print()
    print_user_table(report["auth_by_user"], report["ips_by_user"])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
