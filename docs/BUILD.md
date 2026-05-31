# Сборка патча

Эта инструкция для тех, кто хочет вести перевод, менять TSV и пересобирать локальный `.pak/.ucas/.utoc` патч.

## Требования

- Windows.
- Python 3.11+.
- PowerShell.
- Легальная установленная копия Knights End.
- `retoc.exe` для сборки UE5 IoStore-контейнера.

`retoc.exe` не хранится в git. Положи его сюда:

```text
tools/retoc/retoc.exe
```

Если нужен Oodle DLL для твоей версии `retoc`, положи его рядом с `retoc.exe`. Не коммить эти файлы.

## Подготовка исходных ассетов

Скрипт применяет перевод к уже распакованным legacy `.uasset/.uexp` ассетам. Для текущей таблицы ожидаются такие корневые папки рядом с репозиторием или внутри рабочей копии:

```text
legacy_full_original/KnightsEnd/Content/KnightsEnd/Maps/Levels
legacy_horrornotes_original
legacy_item_original
legacy_notes
legacy_quests
legacy_ui_original
```

Эти папки получаются извлечением ассетов из установленной игры. Оригинальные ассеты не добавляются в git.

## Проверка таблицы

Перед сборкой желательно проверить, что в переводах нет битой кодировки:

```powershell
python - <<'PY'
import csv
from pathlib import Path
p = Path('translations/knights_end_ru.tsv')
bad = []
with p.open('r', encoding='utf-8-sig', newline='') as f:
    for i, r in enumerate(csv.DictReader(f, dialect='excel-tab'), 2):
        text = r.get('translation', '')
        if '????' in text or '\ufffd' in text or any(0x80 <= ord(ch) <= 0xFF for ch in text):
            bad.append((i, r.get('source', ''), text))
print('bad rows:', len(bad))
for row in bad[:20]:
    print(row)
PY
```

## Сборка

Обычная сборка с установкой в текущую папку игры:

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_translation_patch.ps1 `
  -Tsv translations\knights_end_ru.tsv `
  -WorkDir work_ru_final `
  -PatchDir patch_ru_final `
  -PatchName translation_ru_final `
  -PatchWorldSignFont `
  -Install
```

Без `-Install` скрипт только соберет файлы в `patch_ru_final`.

## Шрифты табличек

Для кириллицы на деревянных табличках использовался отдельный override `WBP_SignWriting`, где шрифт табличек переключён на шрифт с поддержкой кириллицы. Эти cooked-ассеты не лежат в git.

Рабочее правило: при изменении name-map для `WBP_SignWriting` не сдвигать cooked export serial offsets. Для этого в `tools/patch_legacy_name_map.py` есть флаг:

```powershell
python tools\patch_legacy_name_map.py `
  --uasset path\to\WBP_SignWriting.uasset `
  --uexp path\to\WBP_SignWriting.uexp `
  --replace-name OLD_FONT_NAME=Quest_Journal_Font `
  --preserve-export-serial-offsets
```

После генерации override положи его в:

```text
world_sign_font_patch_assets_noshift/KnightsEnd/Content/KnightsEnd/Blueprints/Landscape/
```

`tools/build_translation_patch.ps1` автоматически подхватит эту папку при `-PatchWorldSignFont`.

## Архив для релиза

После успешной сборки сделай zip со структурой для игроков:

```powershell
$stage = 'dist\KnightsEnd_RU_patch'
New-Item -ItemType Directory -Force "$stage\KnightsEnd\Content\Paks" | Out-Null
Copy-Item KnightsEnd\Content\Paks\KnightsEnd-Windows_P.* "$stage\KnightsEnd\Content\Paks" -Force
Copy-Item docs\INSTALL_RU.txt "$stage\README_RU.txt" -Force
Compress-Archive -Path "$stage\*" -DestinationPath "dist\KnightsEnd_RU_patch.zip" -Force
```

