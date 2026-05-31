#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


BASE = Path("localization/map_texts.tsv")
TARGET = Path("localization/ru_rescue_with_signs.tsv")

TRANSLATIONS = {
    "outer gates": "Ворота",
    "outergates": "Ворота",
    "graveyard": "Погост",
    "greaveyard": "Погост",
    "lumbermill": "Лесопилка",
    "lumber mill": "Лесопилка",
    "village": "Деревня",
    "farm": "Ферма",
    "forest": "Лес",
    "ye olde farm": "Старая ферма",
    "keep off the wildlife": "Зверьё не трогать",
    "tower beacon": "Огонь башни",
    "for the\nlost knights": "Заблудшим\nрыцарям",
    "big billy": "Герась",
    "tis' dangerous outside\ntake this": "Снаружи опасно\nВозьми это",
    "notes": "Записки",
    "merchant": "Торговец",
    "castle walls": "Стены замка",
    "castle wall": "Стена замка",
    "garden": "Сад",
    "abandoned village": "Покинутая деревня",
    "cave": "Пещера",
    "pond": "Пруд",
    "lake": "Озеро",
    "forest ruins": "Лесные руины",
    "no swimming": "Не купаться",
    "beware the water": "Бойся воды",
    "cave ahead": "Впереди пещера",
    "stay on ye paths!": "Не сходи с троп!",
    "castle": "Замок",
    "2x - bluemushroom\n1x - rat tail\n2x - fangs of a beast": "2 Синегриба\n1 Хвост крысы\n2 Клыка зверя",
    "apothacary\nbeacon": "Огонь\nаптекаря",
    "inn": "Трактир",
    "pond beacon": "Огонь пруда",
    "tavern beacon": "Огонь таверны",
    "tavern": "Таверна",
    "closed": "Закрыто",
    "church": "Церковь",
    "blacksmith": "Кузница",
    "market": "Рынок",
    "butcher": "Мясник",
    "one way\n--------->": "Только\nтуда --->",
}


def sign_key(text: str) -> str:
    lines = [line.strip() for line in text.replace("\r\n", "\n").split("\n")]
    return "\n".join(lines).strip().lower()


def is_service_name(text: str) -> bool:
    stripped = text.strip()
    return not stripped or stripped.startswith("BP_")


def main() -> int:
    with TARGET.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, dialect="excel-tab")
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise SystemExit("target TSV has no header")
        target_rows = list(reader)

    by_id = {row["id"]: row for row in target_rows}
    missing: list[str] = []
    added = 0
    updated = 0

    with BASE.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, dialect="excel-tab"):
            if not row["export"].startswith("BP_Sign"):
                continue
            source = row["source"]
            if is_service_name(source):
                continue
            key = sign_key(source)
            translation = TRANSLATIONS.get(key)
            if not translation:
                missing.append(source.replace("\n", "\\n"))
                continue
            if row["id"] in by_id:
                target = by_id[row["id"]]
                if target.get("translation") != translation:
                    target["translation"] = translation
                    updated += 1
                target["comment"] = "world sign text"
                continue
            target_rows.append(
                {
                    "id": row["id"],
                    "root": row["root"],
                    "asset": row["asset"],
                    "uexp_offset": row["uexp_offset"],
                    "mode": row["mode"],
                    "export": row["export"],
                    "source": source,
                    "translation": translation,
                    "comment": "world sign text",
                }
            )
            added += 1

    with TARGET.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, dialect="excel-tab", lineterminator="\n")
        writer.writeheader()
        writer.writerows(target_rows)

    print(f"added {added}, updated {updated}")
    if missing:
        print("missing translations:")
        for source in sorted(set(missing)):
            print(f"  {source}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
