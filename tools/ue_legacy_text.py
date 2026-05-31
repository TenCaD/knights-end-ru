from __future__ import annotations

import hashlib
import re
import shutil
import struct
from dataclasses import dataclass
from pathlib import Path


PACKAGE_TAG = -1641380927


@dataclass
class ExportEntry:
    index: int
    object_name: str
    serial_size: int
    serial_offset_abs: int
    entry_offset: int


@dataclass
class PackageInfo:
    uasset_size: int
    summary_base: int
    exports: list[ExportEntry]
    bulk_field_offset: int | None
    bulk_value: int | None


def read_i32(buf: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<i", buf, offset)[0]


def read_i64(buf: bytes | bytearray, offset: int) -> int:
    return struct.unpack_from("<q", buf, offset)[0]


def write_i64(buf: bytearray, offset: int, value: int) -> None:
    struct.pack_into("<q", buf, offset, value)


def parse_name_map(uasset: bytes, name_count: int, name_offset: int) -> list[str]:
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
    return names


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


def parse_package(uasset: bytes, uexp: bytes) -> PackageInfo:
    if read_i32(uasset, 0) != PACKAGE_TAG:
        raise ValueError("not a legacy Unreal uasset")

    folder_len = read_i32(uasset, 0x20)
    folder_bytes = (-folder_len * 2) if folder_len < 0 else folder_len
    summary_base = 0x24 + folder_bytes

    name_count = read_i32(uasset, summary_base + 4)
    name_offset = read_i32(uasset, summary_base + 8)
    export_count = read_i32(uasset, summary_base + 28)
    export_offset = read_i32(uasset, summary_base + 32)
    depends_offset = read_i32(uasset, summary_base + 44)

    if export_count <= 0 or export_offset <= 0 or depends_offset <= export_offset:
        raise ValueError("package has no parseable export map")

    entry_size = (depends_offset - export_offset) // export_count
    if entry_size <= 0:
        raise ValueError("invalid export map entry size")

    names = parse_name_map(uasset, name_count, name_offset)
    exports: list[ExportEntry] = []
    for index in range(export_count):
        entry_offset = export_offset + index * entry_size
        object_name_index = read_i32(uasset, entry_offset + 16)
        object_name = names[object_name_index] if 0 <= object_name_index < len(names) else f"<name:{object_name_index}>"
        exports.append(
            ExportEntry(
                index=index,
                object_name=object_name,
                serial_size=read_i64(uasset, entry_offset + 28),
                serial_offset_abs=read_i64(uasset, entry_offset + 36),
                entry_offset=entry_offset,
            )
        )

    total_size = len(uasset) + len(uexp)
    bulk_field_offset = find_bulk_data_field(uasset, total_size)
    bulk_value = read_i64(uasset, bulk_field_offset) if bulk_field_offset is not None else None
    return PackageInfo(
        uasset_size=len(uasset),
        summary_base=summary_base,
        exports=exports,
        bulk_field_offset=bulk_field_offset,
        bulk_value=bulk_value,
    )


def encode_fstring(text: str, mode: str) -> bytes:
    if mode == "narrow":
        payload = text.encode("utf-8")
        return struct.pack("<i", len(payload) + 1) + payload + b"\x00"
    if mode == "utf16":
        payload = text.encode("utf-16le")
        return struct.pack("<i", -(len(text) + 1)) + payload + b"\x00\x00"
    raise ValueError(f"unsupported FString mode: {mode}")


def export_for_uexp_offset(info: PackageInfo, uexp_offset: int) -> ExportEntry | None:
    abs_offset = info.uasset_size + uexp_offset
    for export in info.exports:
        start = export.serial_offset_abs
        end = start + export.serial_size
        if start <= abs_offset < end:
            return export
    return None


def write_package_offsets(uasset: bytearray, info: PackageInfo) -> None:
    for export in info.exports:
        write_i64(uasset, export.entry_offset + 28, export.serial_size)
        write_i64(uasset, export.entry_offset + 36, export.serial_offset_abs)
    if info.bulk_field_offset is not None and info.bulk_value is not None:
        write_i64(uasset, info.bulk_field_offset, info.bulk_value)


def patch_fstring_at_offset(
    uasset: bytearray,
    uexp: bytearray,
    info: PackageInfo,
    original_offset: int,
    current_offset: int,
    source: str,
    source_mode: str,
    translation: str,
    new_mode: str = "utf16",
) -> int:
    source_variants = [source]
    if "\n" in source:
        source_variants.append(source.replace("\n", "\r\n"))
    old_bytes_options = [encode_fstring(candidate, source_mode) for candidate in source_variants]
    old_bytes = old_bytes_options[0]
    new_bytes = encode_fstring(translation, new_mode)
    matched = next((candidate for candidate in old_bytes_options if uexp[current_offset : current_offset + len(candidate)] == candidate), None)
    if matched is None:
        nearby = -1
        for candidate in old_bytes_options:
            nearby = uexp.find(candidate, max(0, current_offset - 64), min(len(uexp), current_offset + 64 + len(candidate)))
            if nearby >= 0:
                old_bytes = candidate
                break
        if nearby < 0:
            matches: list[int] = []
            for candidate in old_bytes_options:
                cursor = uexp.find(candidate)
                while cursor >= 0:
                    matches.append(cursor)
                    cursor = uexp.find(candidate, cursor + 1)
                if matches:
                    old_bytes = candidate
                    break
            if not matches:
                raise ValueError(f"source bytes not found near original offset {original_offset}: {source!r}")
            nearby = min(matches, key=lambda match: abs(match - current_offset))
        current_offset = nearby
    else:
        old_bytes = matched

    target_export = export_for_uexp_offset(info, current_offset)
    if target_export is None:
        raise ValueError(f"could not resolve export for offset {original_offset}: {source!r}")

    delta = len(new_bytes) - len(old_bytes)
    uexp[current_offset : current_offset + len(old_bytes)] = new_bytes
    target_export.serial_size += delta

    absolute_change_point = info.uasset_size + current_offset
    for export in info.exports:
        if export.serial_offset_abs > absolute_change_point:
            export.serial_offset_abs += delta
    if info.bulk_value is not None:
        info.bulk_value += delta
    return delta


GUIDISH_RE = re.compile(r"^[0-9A-F]{20,}$")
PATHISH_RE = re.compile(r"^/(Game|Script|Engine)/")
DEVISH_PREFIXES = (
    "BPTYPE_",
    "CallFunc_",
    "K2Node_",
    "Default__",
    "EQuest",
    "Class ",
)


def is_probably_translatable(text: str, include_short: bool = False) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if "\x00" in stripped:
        return False
    if any((ord(ch) < 32 and ch not in "\r\n\t") for ch in stripped):
        return False
    if len(stripped) < (2 if include_short else 4):
        return False
    if "\ufffd" in stripped:
        return False
    if GUIDISH_RE.match(stripped):
        return False
    if PATHISH_RE.match(stripped):
        return False
    if any(stripped.startswith(prefix) for prefix in DEVISH_PREFIXES):
        return False
    if stripped.startswith("Engine.") or stripped.startswith("Script."):
        return False
    if not any(ch.isalpha() for ch in stripped):
        return False
    return True


@dataclass
class FStringHit:
    offset: int
    mode: str
    source: str
    export_name: str

    @property
    def stable_id(self) -> str:
        raw = f"{self.offset}:{self.mode}:{self.source}".encode("utf-8", "surrogatepass")
        return hashlib.sha1(raw).hexdigest()[:12]


def scan_fstrings(uasset: bytes, uexp: bytes, include_short: bool = False, max_chars: int = 4096) -> list[FStringHit]:
    info = parse_package(uasset, uexp)
    hits: list[FStringHit] = []
    offset = 0
    while offset <= len(uexp) - 6:
        raw_len = read_i32(uexp, offset)
        consumed = 1
        mode: str | None = None
        text: str | None = None
        byte_len = 0

        if 1 < raw_len <= max_chars and offset + 4 + raw_len <= len(uexp):
            payload = uexp[offset + 4 : offset + 4 + raw_len]
            if payload.endswith(b"\x00"):
                try:
                    decoded = payload[:-1].decode("utf-8")
                except UnicodeDecodeError:
                    decoded = None
                if decoded is not None and is_probably_translatable(decoded, include_short):
                    mode = "narrow"
                    text = decoded
                    byte_len = 4 + raw_len

        if mode is None and -max_chars <= raw_len < -1:
            char_count = -raw_len
            byte_count = char_count * 2
            if offset + 4 + byte_count <= len(uexp):
                payload = uexp[offset + 4 : offset + 4 + byte_count]
                if payload.endswith(b"\x00\x00"):
                    try:
                        decoded = payload[:-2].decode("utf-16le")
                    except UnicodeDecodeError:
                        decoded = None
                    if decoded is not None and is_probably_translatable(decoded, include_short):
                        mode = "utf16"
                        text = decoded
                        byte_len = 4 + byte_count

        if mode is not None and text is not None:
            export = export_for_uexp_offset(info, offset)
            if export is not None:
                hits.append(FStringHit(offset=offset, mode=mode, source=text, export_name=export.object_name))
                consumed = max(byte_len, 1)

        offset += consumed
    return hits


def copy_asset_pair(src_uasset: Path, out_root: Path, src_root: Path) -> tuple[Path, Path]:
    src_uexp = src_uasset.with_suffix(".uexp")
    if not src_uexp.exists():
        raise FileNotFoundError(src_uexp)
    rel_uasset = src_uasset.relative_to(src_root)
    dst_uasset = out_root / rel_uasset
    dst_uexp = dst_uasset.with_suffix(".uexp")
    dst_uasset.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_uasset, dst_uasset)
    shutil.copy2(src_uexp, dst_uexp)
    return dst_uasset, dst_uexp
