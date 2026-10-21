import csv
import json
from pathlib import Path

from core.errors import ConversionError
from core.registry import register


@register(".csv", ".json")
def csv_to_json(source: Path, target: Path) -> None:
    try:
        with source.open(encoding="utf-8-sig", newline="") as f:
            first_line = f.readline()
            f.seek(0)
            delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
            rows = list(csv.DictReader(f, delimiter=delimiter))
    except UnicodeDecodeError:
        raise ConversionError("Plik nie jest w UTF-8. Zapisz go jako CSV UTF-8.")
    except csv.Error as e:
        raise ConversionError(f"Błędny plik CSV: {e}")

    if not first_line.strip():
        raise ConversionError("Plik CSV jest pusty.")

    with target.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)