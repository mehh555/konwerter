import csv
import json

from core import ConversionError, register


@register(".csv", ".json")
def csv_to_json(src, dst):
    with open(src, encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        if not first.strip():
            raise ConversionError("Pusty plik CSV")
        f.seek(0)
        sep = ";" if first.count(";") > first.count(",") else ","
        try:
            rows = list(csv.DictReader(f, delimiter=sep))
        except csv.Error as e:
            raise ConversionError(f"Zły CSV: {e}")

    if any(None in row or None in row.values() for row in rows):
        raise ConversionError("Wiersz ma inną liczbę pól niż nagłówek")

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


@register(".json", ".csv")
def json_to_csv(src, dst):
    try:
        data = json.loads(src.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        raise ConversionError(f"Zły JSON: {e}")

    if isinstance(data, dict):
        data = [data]
    if not data or not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
        raise ConversionError("JSON ma być listą obiektów")

    cols = list(dict.fromkeys(k for row in data for k in row))
    fix = lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list, bool)) else v

    with open(dst, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows({k: fix(v) for k, v in row.items()} for row in data)