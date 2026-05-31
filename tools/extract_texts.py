#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from ue_legacy_text import scan_fstrings


def iter_assets(root: Path) -> list[Path]:
    suffixes = {".uasset", ".umap"}
    return sorted(
        path
        for path in root.rglob("*")
        if path.suffix.lower() in suffixes and path.with_suffix(".uexp").exists()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract likely translatable UE legacy FString/FText payloads to TSV.")
    parser.add_argument("roots", nargs="+", type=Path, help="Legacy extraction roots to scan.")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Output TSV path.")
    parser.add_argument("--include-short", action="store_true", help="Keep 2-3 character strings.")
    parser.add_argument("--max-chars", type=int, default=4096)
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, int, str]] = set()
    for root in args.roots:
        if not root.exists():
            print(f"missing root: {root}", file=sys.stderr)
            continue
        for uasset_path in iter_assets(root):
            uexp_path = uasset_path.with_suffix(".uexp")
            try:
                hits = scan_fstrings(
                    uasset_path.read_bytes(),
                    uexp_path.read_bytes(),
                    include_short=args.include_short,
                    max_chars=args.max_chars,
                )
            except Exception as exc:
                print(f"skip {uasset_path}: {exc}", file=sys.stderr)
                continue

            rel = uasset_path.relative_to(root).as_posix()
            for hit in hits:
                key = (rel, hit.offset, hit.source)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "id": hit.stable_id,
                        "root": root.as_posix(),
                        "asset": rel,
                        "uexp_offset": str(hit.offset),
                        "mode": hit.mode,
                        "export": hit.export_name,
                        "source": hit.source.replace("\r\n", "\n"),
                        "translation": "",
                        "comment": "",
                    }
                )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["id", "root", "asset", "uexp_offset", "mode", "export", "source", "translation", "comment"],
            dialect="excel-tab",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
