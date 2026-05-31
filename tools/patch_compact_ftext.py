#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from ue_legacy_text import copy_asset_pair, export_for_uexp_offset, parse_package, write_package_offsets


ROOT = Path(__file__).resolve().parents[1]

SWING_ASSETS = [
    "KnightsEnd/Content/KnightsEnd/GameBackend/Systems/InteractionSystem/CoreInteractableChildren/QuestItems/BP_FetchQuest_BloodySword.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_FLAMESWORD.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_Hammer.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_Handaxe.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_Mace.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_MagicStaff.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_PAN.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_PickAxe.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_Quest_Mace.uasset",
    "KnightsEnd/Content/KnightsEnd/Blueprints/Interactables/EquipableItems/BP_Sword.uasset",
]


def patch_raw_text(uasset_path: Path, old_text: str, new_text: str) -> int:
    uexp_path = uasset_path.with_suffix(".uexp")
    uasset = bytearray(uasset_path.read_bytes())
    uexp = bytearray(uexp_path.read_bytes())
    info = parse_package(uasset, uexp)

    old = b"\x1f" + old_text.encode("utf-8") + b"\x00"
    new = b"\x1f" + new_text.encode("utf-8") + b"\x00"
    patched = 0
    cursor = 0

    while True:
        offset = uexp.find(old, cursor)
        if offset < 0:
            break
        target_export = export_for_uexp_offset(info, offset)
        if target_export is None:
            raise ValueError(f"could not resolve export for {uasset_path} at {offset}")

        delta = len(new) - len(old)
        uexp[offset : offset + len(old)] = new
        target_export.serial_size += delta
        absolute_change_point = info.uasset_size + offset
        for export in info.exports:
            if export.serial_offset_abs > absolute_change_point:
                export.serial_offset_abs += delta
        if info.bulk_value is not None:
            info.bulk_value += delta

        patched += 1
        cursor = offset + len(new)

    if patched:
        write_package_offsets(uasset, info)
        uasset_path.write_bytes(uasset)
        uexp_path.write_bytes(uexp)

    return patched


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch compact null-terminated FText payloads missed by FString scanning.")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--src-root", default=ROOT / "legacy_item_original", type=Path)
    args = parser.parse_args()

    total = 0
    for rel_text in SWING_ASSETS:
        rel = Path(rel_text)
        src = args.src_root / rel
        if not src.exists():
            continue

        dst = args.out / rel
        if not dst.exists():
            dst, _ = copy_asset_pair(src, args.out, args.src_root)

        count = patch_raw_text(dst, "Swing", "Удар")
        if count:
            print(f"patched compact FText: {rel_text} ({count})")
            total += count

    print(f"patched {total} compact FText strings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
