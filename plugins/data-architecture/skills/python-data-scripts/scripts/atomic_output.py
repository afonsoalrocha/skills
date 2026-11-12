"""Write a DataFrame atomically and drop a manifest next to it.

    from atomic_output import write_atomic
    write_atomic(df, Path("out/result.parquet"), source="<catalog>.<schema>.<table>",
                 window=("2026-10-01", "2026-11-01"))

Requires pandas, which is not in the Python standard library.
Parquet output also requires pyarrow or fastparquet.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_atomic(df: pd.DataFrame, target: Path, *, source: str, window: tuple[str, str]) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".partial")
    try:
        if target.suffix == ".parquet":
            df.to_parquet(partial, index=False)
        elif target.suffix == ".csv":
            df.to_csv(partial, index=False, encoding="utf-8-sig")
        else:
            raise ValueError(f"unsupported suffix {target.suffix}")
        os.replace(partial, target)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    manifest = {
        "output": target.name,
        "source": source,
        "window": {"start": window[0], "end_exclusive": window[1]},
        "rows": int(len(df)),
        "sha256": _sha256(target),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    mpath = target.with_name(target.name + ".manifest.json")
    mpath.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return mpath
