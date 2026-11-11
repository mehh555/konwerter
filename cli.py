import sys
from pathlib import Path

import converters
from core import ConversionError, convert, setup_logging

setup_logging()

args = [a for a in sys.argv[1:] if a != "--nadpisz"]
if len(args) != 3:
    sys.exit("python cli.py <plik> <format> <katalog> [--nadpisz]")

try:
    print("Zapisano:", convert(Path(args[0]), args[1], Path(args[2]), overwrite="--nadpisz" in sys.argv))
except ConversionError as e:
    sys.exit(f"Błąd: {e}")