#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import defaultdict
from pathlib import Path

from ue_legacy_text import copy_asset_pair, parse_package, patch_fstring_at_offset, write_package_offsets


def load_rows(tsv_path: Path) -> list[dict[str, str]]:
    with tsv_path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [row for row in csv.DictReader(fh, dialect="excel-tab")]


def row_translation(row: dict[str, str]) -> str:
    return (row.get("translation") or "").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply TSV translations to legacy UE assets.")
    parser.add_argument("--tsv", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="Output legacy patch directory.")
    parser.add_argument("--new-mode", choices=("utf16", "narrow"), default="utf16")
    parser.add_argument("--copy-extra", action="append", default=[], type=Path, help="Extra file or directory to copy into output.")
    args = parser.parse_args()

    rows = [row for row in load_rows(args.tsv) if row_translation(row)]
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        root = row.get("root", "")
        asset = row.get("asset", "")
        if not root or not asset:
            print(f"bad row without root/asset: {row}", file=sys.stderr)
            return 1
        grouped[(root, asset)].append(row)

    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True)

    patched_assets = 0
    patched_strings = 0
    failures: list[str] = []

    for (root_text, asset_rel), asset_rows in sorted(grouped.items()):
        src_root = Path(root_text)
        src_uasset = src_root / asset_rel
        try:
            dst_uasset, dst_uexp = copy_asset_pair(src_uasset, args.out, src_root)
            uasset = bytearray(dst_uasset.read_bytes())
            uexp = bytearray(dst_uexp.read_bytes())
            info = parse_package(uasset, uexp)
            running_delta = 0
            for row in sorted(asset_rows, key=lambda r: int(r["uexp_offset"])):
                original_offset = int(row["uexp_offset"])
                current_offset = original_offset + running_delta
                delta = patch_fstring_at_offset(
                    uasset=uasset,
                    uexp=uexp,
                    info=info,
                    original_offset=original_offset,
                    current_offset=current_offset,
                    source=row["source"],
                    source_mode=row["mode"],
                    translation=row_translation(row),
                    new_mode=args.new_mode,
                )
                running_delta += delta
                patched_strings += 1
            write_package_offsets(uasset, info)
            dst_uasset.write_bytes(uasset)
            dst_uexp.write_bytes(uexp)
            patched_assets += 1
        except Exception as exc:
            failures.append(f"{asset_rel}: {exc}")

    for extra in args.copy_extra:
        if not extra.exists():
            failures.append(f"extra path missing: {extra}")
            continue
        destination = args.out / extra.name
        if extra.is_dir():
            shutil.copytree(extra, destination, dirs_exist_ok=True)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(extra, destination)

    print(f"patched {patched_strings} strings in {patched_assets} assets into {args.out}")
    if failures:
        print("failures:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
