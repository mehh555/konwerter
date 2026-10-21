import sys
from pathlib import Path

import converters  
from core.errors import ConversionError
from core.registry import convert

if len(sys.argv) != 4:
    print("Użycie: python cli.py <plik> <format> <katalog>")
    print("Przykład: python cli.py dane.csv .json .")
    sys.exit(1)

try:
    result = convert(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
    print(f"Zapisano: {result}")
except ConversionError as e:
    print(f"Błąd: {e}")
    sys.exit(1)