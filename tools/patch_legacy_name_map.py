#!/usr/bin/env python3
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path


def read_i32(buf: bytes | bytearray, off: int) -> int:
    return struct.unpack_from("<i", buf, off)[0]


def read_i64(buf: bytes | bytearray, off: int) -> int:
    return struct.unpack_from("<q", buf, off)[0]


def write_i32(buf: bytearray, off: int, value: int) -> None:
    struct.pack_into("<i", buf, off, value)


def write_i64(buf: bytearray, off: int, value: int) -> None:
    struct.pack_into("<q", buf, off, value)


def parse_pairs(values: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError("Expected OLD=NEW")
        old_text, new_text = value.split("=", 1)
        pairs.append((old_text, new_text))
    return pairs


def parse_import_object_pairs(values: list[str]) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError("Expected IMPORT_INDEX=NAME")
        import_index, name = value.split("=", 1)
        pairs.append((int(import_index), name))
    return pairs


def parse_name_map(uasset: bytes, name_count: int, name_offset: int) -> tuple[list[str], int]:
    names: list[str] = []
    cursor = name_offset
    for _ in range(name_count):
        raw_len = read_i32(uasset, cursor)
        cursor += 4
        if raw_len < 0:
            char_count = -raw_len
            raw = uasset[cursor : cursor + char_count * 2]
            text = raw[:-2].decode("utf-16le", errors="replace")
            cursor += char_count * 2
        else:
            raw = uasset[cursor : cursor + raw_len]
            text = raw[:-1].decode("utf-8", errors="replace")
            cursor += raw_len
        cursor += 4
        names.append(text)
    return names, cursor


def encode_name(text: str) -> bytes:
    raw = text.encode("utf-8") + b"\x00"
    return struct.pack("<i", len(raw)) + raw + b"\x00\x00\x00\x00"


def find_bulk_data_field(uasset: bytes, total_size: int, scan_limit: int = 512) -> int | None:
    hits: list[int] = []
    limit = min(scan_limit, len(uasset) - 8)
    for offset in range(0, limit + 1, 4):
        value = read_i64(uasset, offset)
        if total_size - 64 <= value <= total_size + 64:
            hits.append(offset)
    if len(hits) == 1:
        return hits[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Patch legacy uasset name-map strings and shift summary/export offsets."
    )
    parser.add_argument("--uasset", required=True, type=Path)
    parser.add_argument("--uexp", required=True, type=Path)
    parser.add_argument("--replace-name", action="append", default=[], help="OLD=NEW")
    parser.add_argument("--append-name", action="append", default=[], help="Append a new name-map string if missing")
    parser.add_argument(
        "--set-import-object-name",
        action="append",
        default=[],
        help="Set import entry object_name by import index: IMPORT_INDEX=NAME",
    )
    parser.add_argument(
        "--preserve-export-serial-offsets",
        action="store_true",
        help="Keep cooked export serial offsets unchanged after name-map size changes.",
    )
    args = parser.parse_args()

    replacements = parse_pairs(args.replace_name)
    import_object_patches = parse_import_object_pairs(args.set_import_object_name)
    uasset = bytearray(args.uasset.read_bytes())
    uexp = args.uexp.read_bytes()

    if read_i32(uasset, 0) != -1641380927:
        print("Unexpected package tag.", file=sys.stderr)
        return 1

    folder_len = read_i32(uasset, 0x20)
    summary_base = 0x24 + folder_len
    name_count = read_i32(uasset, summary_base + 4)
    name_offset = read_i32(uasset, summary_base + 8)
    export_count = read_i32(uasset, summary_base + 28)
    export_offset = read_i32(uasset, summary_base + 32)
    depends_offset = read_i32(uasset, summary_base + 44)
    entry_size = (depends_offset - export_offset) // export_count

    names, old_name_map_end = parse_name_map(uasset, name_count, name_offset)
    patched_names: list[str] = []
    changed = False
    for current in names:
        updated = current
        for old_text, new_text in replacements:
            if current == old_text:
                updated = new_text
                changed = True
                print(f'name "{old_text}" -> "{new_text}"')
                break
        patched_names.append(updated)

    for appended_name in args.append_name:
        if appended_name not in patched_names:
            patched_names.append(appended_name)
            changed = True
            print(f'append name "{appended_name}"')

    if not changed and not import_object_patches:
        print("No name-map strings matched.", file=sys.stderr)
        return 1

    new_name_map = b"".join(encode_name(name) for name in patched_names)
    old_name_map = bytes(uasset[name_offset:old_name_map_end])
    delta = len(new_name_map) - len(old_name_map)
    old_uasset_size = len(uasset)
    old_total_size = len(uasset) + len(uexp)

    rebuilt = bytearray()
    rebuilt += uasset[:name_offset]
    rebuilt += new_name_map
    rebuilt += uasset[old_name_map_end:]

    write_i32(rebuilt, summary_base + 4, len(patched_names))

    # Shift 32-bit summary offsets that point past the old name map.
    for off in range(summary_base, name_offset, 4):
        value = read_i32(rebuilt, off)
        if old_name_map_end <= value <= old_uasset_size:
            write_i32(rebuilt, off, value + delta)

    # Shift export serial offsets for tools that expect a physically contiguous
    # uasset+uexp pair. Cooked UE5 IoStore packages can instead expect the
    # original cooked offsets, so keep the old values for those targeted tests.
    if not args.preserve_export_serial_offsets:
        new_export_offset = read_i32(rebuilt, summary_base + 32)
        for index in range(export_count):
            entry_off = new_export_offset + index * entry_size
            serial_offset = read_i64(rebuilt, entry_off + 36)
            if serial_offset >= old_uasset_size:
                write_i64(rebuilt, entry_off + 36, serial_offset + delta)

    import_offset = read_i32(rebuilt, summary_base + 40)

    if import_object_patches:
        name_lookup = {name: idx for idx, name in enumerate(patched_names)}
        import_count = read_i32(rebuilt, summary_base + 36)
        import_entry_size = 32
        for import_index, target_name in import_object_patches:
            if target_name not in name_lookup:
                print(f'Import patch target name "{target_name}" is not present in the name map.', file=sys.stderr)
                return 1
            if not (0 <= import_index < import_count):
                print(f"Import index {import_index} is out of range.", file=sys.stderr)
                return 1
            entry_off = import_offset + import_index * import_entry_size
            write_i32(rebuilt, entry_off + 20, name_lookup[target_name])
            write_i32(rebuilt, entry_off + 24, 0)
            print(f'import {import_index} object_name -> "{target_name}"')

    bulk_field = None if args.preserve_export_serial_offsets else find_bulk_data_field(rebuilt, old_total_size)
    if bulk_field is not None:
        write_i64(rebuilt, bulk_field, read_i64(rebuilt, bulk_field) + delta)

    args.uasset.write_bytes(rebuilt)
    print(
        f"Wrote {args.uasset.name}: name map delta {delta:+d}, "
        f"uasset size {old_uasset_size}->{len(rebuilt)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
