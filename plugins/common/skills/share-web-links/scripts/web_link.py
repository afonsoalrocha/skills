#!/usr/bin/env python3
"""Compute a SharePoint web link for a file under a locally synced root.

Standard library only. Configuration comes from environment variables
(SHARE_TENANT, SHARE_SITE, SHARE_LIBRARY, SHARE_LOCAL_ROOT) or arguments.
The URL pattern is an observed convention, not a documented contract.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path, PurePath
from urllib.parse import quote

TYPE_LETTERS = {
    ".pdf": "b",
    ".docx": "w", ".doc": "w",
    ".xlsx": "x", ".xls": "x",
    ".pptx": "p", ".ppt": "p",
    ".png": "i", ".jpg": "i", ".jpeg": "i", ".gif": "i", ".svg": "i",
    ".md": "t", ".txt": "t", ".csv": "t",
}


def type_letter(path: PurePath) -> str:
    return TYPE_LETTERS.get(path.suffix.lower(), "u")


def build_link(tenant: str, site: str, library: str, local_root: str, file_path: str) -> str:
    root = Path(local_root).resolve()
    target = Path(file_path).resolve()
    try:
        rel = target.relative_to(root)
    except ValueError:
        raise ValueError("file is outside the local root") from None
    parts = [p for p in library.replace("\\", "/").split("/") if p] + list(rel.parts)
    encoded = "/".join(quote(p, safe="") for p in parts)
    return (
        f"https://{tenant}.sharepoint.com/:{type_letter(rel)}:/r/sites/"
        f"{quote(site, safe='')}/{encoded}?csf=1&web=1"
    )


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        sub = Path(tmp) / "reports"
        sub.mkdir()
        f = sub / "q1 summary & notes.pdf"
        f.write_text("x")
        got = build_link("my-tenant", "my-site", "Shared Documents/Team", tmp, str(f))
        want = (
            "https://my-tenant.sharepoint.com/:b:/r/sites/my-site/Shared%20Documents/"
            "Team/reports/q1%20summary%20%26%20notes.pdf?csf=1&web=1"
        )
        assert got == want, got
        assert type_letter(PurePath("a.XLSX")) == "x"
        assert type_letter(PurePath("a.zip")) == "u"
        try:
            build_link("t", "s", "L", tmp, str(Path(tmp).parent / "other.pdf"))
        except ValueError:
            pass
        else:
            raise AssertionError("outside root must fail")
    print("OK self-test")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", help="full local path of the file")
    ap.add_argument("--tenant", default=os.environ.get("SHARE_TENANT"))
    ap.add_argument("--site", default=os.environ.get("SHARE_SITE"))
    ap.add_argument("--library", default=os.environ.get("SHARE_LIBRARY"))
    ap.add_argument("--local-root", default=os.environ.get("SHARE_LOCAL_ROOT"))
    ap.add_argument("--self-test", action="store_true", help="run the built-in test")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.path:
        ap.error("path is required")
    missing = [n for n, v in (("tenant", a.tenant), ("site", a.site),
                              ("library", a.library), ("local-root", a.local_root)) if not v]
    if missing:
        print(f"ERRO missing setting: {', '.join(missing)}", file=sys.stderr)
        return 2
    try:
        print(build_link(a.tenant, a.site, a.library, a.local_root, a.path))
    except ValueError as e:
        print(f"ERRO {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
