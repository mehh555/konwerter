import sys
from pathlib import Path

import converters
from core import ConversionError, convert

if len(sys.argv) != 4:
    sys.exit("python cli.py <plik> <format> <katalog>")

try:
    print("Zapisano:", convert(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])))
except ConversionError as e:
    sys.exit(f"Błąd: {e}")