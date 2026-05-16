#!/usr/bin/env python3

"""
Pretty-print MongoDB CONTROL log entries from piped stdin.

Usage:
    cat control.input | python controlPrint.py
    cat mongodb.log   | python controlPrint.py
"""

from __future__ import annotations

import json
import sys
from typing import Any


SEP = "-" * 72


def fmt(label: str, value: Any) -> str:
    return f"  {label:<30} {value}"


def ts(entry: dict[str, Any]) -> str:
    t = entry.get("t", {})
    if isinstance(t, dict):
        return t.get("$date", "")
    return str(t)


# ── per-message formatters ────────────────────────────────────────────────────

def fmt_process_details(attr: dict) -> list[str]:
    return [
        fmt("PID",          attr.get("pid", "")),
        fmt("Port",         attr.get("port", "")),
        fmt("Architecture", attr.get("architecture", "")),
        fmt("Host",         attr.get("host", "")),
    ]


def fmt_replica_set(attr: dict) -> list[str]:
    cfg = attr.get("config", {})
    members = cfg.get("members", [])
    member_hosts = [m.get("host", "") for m in members]
    return [
        fmt("Replica Set",   cfg.get("_id", "")),
        fmt("Config Version",cfg.get("version", "")),
        fmt("Term",          cfg.get("term", "")),
        fmt("Member State",  attr.get("memberState", "")),
        fmt("Members",       len(member_hosts)),
        *[fmt(f"  [{i}]", h) for i, h in enumerate(member_hosts)],
    ]


def fmt_build_info(attr: dict) -> list[str]:
    bi = attr.get("buildInfo", {})
    env = bi.get("environment", {})
    return [
        fmt("MongoDB Version", bi.get("version", "")),
        fmt("Git Version",     bi.get("gitVersion", "")),
        fmt("OpenSSL",         bi.get("openSSLVersion", "")),
        fmt("Modules",         ", ".join(bi.get("modules", []))),
        fmt("Allocator",       bi.get("allocator", "")),
        fmt("OS / Arch",       f"{env.get('distmod','')} / {env.get('target_arch','')}"),
    ]


def fmt_operating_system(attr: dict) -> list[str]:
    os_ = attr.get("os", {})
    return [
        fmt("OS Name",    os_.get("name", "")),
        fmt("OS Version", os_.get("version", "")),
    ]


def fmt_options(attr: dict) -> list[str]:
    opts = attr.get("options", {})
    net  = opts.get("net", {})
    stor = opts.get("storage", {})
    repl = opts.get("replication", {})
    sec  = opts.get("security", {})
    tls  = net.get("tls", {})
    lines = [
        fmt("Config File",        opts.get("config", "")),
        fmt("Bind IP",            net.get("bindIp", "")),
        fmt("Port",               net.get("port", "")),
        fmt("Max Connections",    net.get("maxIncomingConnections", "")),
        fmt("Compressors",        net.get("compression", {}).get("compressors", "")),
        fmt("TLS Mode",           tls.get("mode", "")),
        fmt("TLS Disabled Proto", tls.get("disabledProtocols", "")),
        fmt("Replica Set Name",   repl.get("replSetName", "")),
        fmt("DB Path",            stor.get("dbPath", "")),
        fmt("Storage Engine",     stor.get("engine", "")),
        fmt("Authorization",      sec.get("authorization", "")),
    ]
    return lines


def fmt_log_rotation(attr: dict) -> list[str]:
    return [
        fmt("Log Type", attr.get("logType", "")),
        fmt("Suffix",   attr.get("suffix", "")),
    ]


def fmt_session_cache_fail(attr: dict) -> list[str]:
    return [
        fmt("Error", attr.get("error", "")),
    ]


def fmt_generic(attr: dict) -> list[str]:
    """Fallback: print attr keys/values one per line."""
    lines = []
    for k, v in attr.items():
        if isinstance(v, (dict, list)):
            v = json.dumps(v)
        lines.append(fmt(k, v))
    return lines


# ── message dispatch ──────────────────────────────────────────────────────────

MSG_DISPATCH: dict[str, Any] = {
    "Process Details":                          fmt_process_details,
    "Node is a member of a replica set":        fmt_replica_set,
    "Build Info":                               fmt_build_info,
    "Operating System":                         fmt_operating_system,
    "Options set by command line":              fmt_options,
    "Log rotation initiated":                   fmt_log_rotation,
    "Failed to refresh session cache, will try again at the next refresh interval":
                                                fmt_session_cache_fail,
}


def render(entry: dict[str, Any]) -> str:
    msg    = entry.get("msg", "<unknown>")
    ctx    = entry.get("ctx", "")
    svc    = entry.get("svc", "")
    eid    = entry.get("id", "")
    sev    = entry.get("s", "")
    attr   = entry.get("attr", {})

    header_parts = [ts(entry), f"[{sev}]", f"ctx={ctx}"]
    if svc and svc != "-":
        header_parts.append(f"svc={svc}")
    header_parts.append(f"id={eid}")

    lines = [SEP, "  " + "  ".join(header_parts), f"  MSG: {msg}"]

    formatter = MSG_DISPATCH.get(msg, fmt_generic)
    if attr:
        lines += formatter(attr)

    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    if sys.stdin.isatty():
        print("ERROR: no piped input. Usage: cat control.input | python controlPrint.py",
              file=sys.stderr)
        return 1

    for raw in sys.stdin:
        line = raw.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(entry, dict):
            continue
        if entry.get("c") != "CONTROL":
            continue

        print(SEP)
        print(f"RAW: {line}")
        print(render(entry))

    print(SEP)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
