#!/usr/bin/env python3
"""

 File: jsonFetcher.py
 Author: Dennis Spera
 
"""

import sys
import json as j
from commandlines import Command as cmd

b = ""
e = ""
max_input_length = 14
min_input_length = 8

def validate_input(func) -> callable:
    def wrapper(*args, **kwargs):
        if not b or not e:
            sys.stderr.write("Both beginning and ending timestamps must be provided.\n")
            printHelp()
            sys.exit(0)
        return func(*args, **kwargs)

    return wrapper


@validate_input
def is_json(text) -> bool:
    try:
        j.loads(text)
    except ValueError:
        return False
    return True


def printHelp() -> None:
    sys.stderr.write(
        'enter a valid beginning {b} date and end {e} to extract from logs' + "\n"
    )
    sys.stderr.write(
        'jsonFetcher -b YYYYMMDD[24HRMISS] -e YYYYMMDD[24HRMISS]' + "\n"
    )


def normalize_bound(label: str, value: str) -> str:
    if len(value) > max_input_length:
        sys.stderr.write(
            f'{label} timestamp exceeds timestamp length of {max_input_length}'
        )
        printHelp()
        sys.exit(0)

    if len(value) < min_input_length:
        sys.stderr.write(
            f'{label} timestamp less than timestamp length of {min_input_length}'
        )
        printHelp()
        sys.exit(0)

    try:
        int(value)
    except ValueError:
        sys.stderr.write(f'{label} timestamp is an invalid data format')
        printHelp()
        sys.exit(0)

    # Pad missing HHMMSS tail with zeros.
    return value + ("0" * (max_input_length - len(value)))


def iso_to_compact_14(iso_text: str) -> str | None:
    # Expected examples:
    # 2025-04-29T00:12:58.262+00:00
    # 2026-03-24T11:07:47.233-04:00
    if len(iso_text) < 19:
        return None

    # Fast positional extraction; avoids regex/datetime in hot path.
    try:
        return (
            iso_text[0:4]
            + iso_text[5:7]
            + iso_text[8:10]
            + iso_text[11:13]
            + iso_text[14:16]
            + iso_text[17:19]
        )
    except Exception:
        return None


try:
    c = cmd()

    try:
        b = c.get_definition('b')
        e = c.get_definition('e')
        b = normalize_bound("beginning", b)
        e = normalize_bound("ending", e)
    except Exception:
        sys.stderr.write('error parsing input parameters')
        printHelp()
        sys.exit(0)

    if b > e:
        sys.stderr.write('beginning timestamp must be <= ending timestamp\n')
        printHelp()
        sys.exit(0)

    for line in sys.stdin:
        text = line.strip()
        if not text or not text.startswith("{"):
            continue

        try:
            d = j.loads(text)
        except ValueError:
            continue

        try:
            date_t = d["t"]["$date"]
        except Exception:
            continue

        compact = iso_to_compact_14(date_t)
        if compact is None:
            continue

        if b <= compact <= e:
            print(line, end="")

    sys.stdin.close()

except OSError as err:
    sys.stderr.write(err)
