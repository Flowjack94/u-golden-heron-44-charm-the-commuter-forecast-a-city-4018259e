#!/usr/bin/env python3
"""Charm the Commuter: Forecast a City That Isn't.

Writes one line of weather forecast, at most 140 characters, for a city
that does not exist, to /output/entry.txt.

The entry is a single literal line written by hand in this file: a
broadcast-style forecast for Quillwater, an invented city, with one
concrete commuter detail (the number 12 tram finally running on time)
to make a bored commuter smile on the way to work.

Deterministic: no network, no randomness, no environment secrets, no
input files. The same line is written on every run.
"""

import os
import sys

# The forecast line, written by hand. 118 characters.
ENTRY = (
    "Quillwater: light rain until ten, then sunshine and the number 12 "
    "tram finally on time \u2014 brolly up, chin up, home dry."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 140


def validate_entry(text):
    """Check the entry against the sealed gate's rules.

    Returns True only when the text is:
      * a str of 1-140 characters,
      * not only whitespace,
      * free of control characters (other than none expected here),
    and encodes cleanly as UTF-8.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    # Reject control characters (C0 and DEL); a forecast line has none.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return False
    # Reject C1 control characters (U+0080-U+009F): invisible formatting
    # controls (e.g. padding, next-line) that never belong in a
    # one-line forecast and would render inconsistently across viewers.
    if any(0x80 <= ord(ch) <= 0x9F for ch in text):
        return False
    # Reject U+FFFD, the Unicode replacement character: it only appears
    # when bytes failed to decode, so its presence means the text is
    # already corrupted; a clean hand-written line never contains it.
    if "\ufffd" in text:
        return False
    # Reject lone surrogates (U+D800-U+DFFF): they are not valid Unicode
    # scalar values and cannot encode to UTF-8, so the text could not
    # be written out byte-for-byte.
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in text):
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    if not validate_entry(ENTRY):
        print("error: entry failed validation", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")

    print(f"wrote {len(ENTRY)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
