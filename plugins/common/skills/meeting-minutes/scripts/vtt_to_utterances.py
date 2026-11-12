#!/usr/bin/env python3
"""Convert a WebVTT transcript with voice tags into '[Speaker] text' lines.

Standard library only. Consecutive cues from the same speaker are merged, empty
speech is dropped, output is written atomically, and the script exits 1 with
ERRO when no speech is found.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

CUE = re.compile(r"<v(?:\.[^\s>]+)?\s+([^>]*)>(.*?)(?:</v>|$)", re.DOTALL)
TAG = re.compile(r"<[^>]+>")


def parse(text: str) -> list[tuple[str, str]]:
    utterances: list[tuple[str, str]] = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n")):
        for speaker, body in CUE.findall(block):
            body = " ".join(TAG.sub("", body).split())
            speaker = speaker.strip()
            if not body or not speaker:
                continue
            if utterances and utterances[-1][0] == speaker:
                utterances[-1] = (speaker, utterances[-1][1] + " " + body)
            else:
                utterances.append((speaker, body))
    return utterances


def write_atomic(path: Path, content: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".part")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def self_test() -> int:
    sample = (
        "WEBVTT\n\n00:00:01.000 --> 00:00:03.000\n<v Ana>Hello team.</v>\n\n"
        "00:00:03.000 --> 00:00:05.000\n<v Ana>Let us start.</v>\n\n"
        "00:00:05.000 --> 00:00:06.000\n<v Bob>   </v>\n\n"
        "00:00:06.000 --> 00:00:08.000\n<v Bob>Ready.</v>\n\n"
        "00:00:08.000 --> 00:00:09.000\n<v Ana>Done.</v>\n"
    )
    got = parse(sample)
    assert got == [("Ana", "Hello team. Let us start."), ("Bob", "Ready."), ("Ana", "Done.")], got
    assert parse("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nplain text\n") == []
    print("OK self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", nargs="?", help="path to the .vtt file")
    ap.add_argument("output", nargs="?", help="path of the text file to write")
    ap.add_argument("--self-test", action="store_true", help="run the built-in test")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.input or not a.output:
        ap.error("input and output are required")
    src = Path(a.input)
    if not src.is_file():
        print(f"ERRO input not found: {src}", file=sys.stderr)
        return 1
    utterances = parse(src.read_text(encoding="utf-8-sig", errors="replace"))
    if not utterances:
        print("ERRO no speech found in the expected <v Speaker> format; "
              "check the transcript format before concluding anything", file=sys.stderr)
        return 1
    write_atomic(Path(a.output), "\n".join(f"[{s}] {t}" for s, t in utterances) + "\n")
    print(f"OK {len(utterances)} utterances -> {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
