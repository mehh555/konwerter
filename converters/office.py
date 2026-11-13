import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from core import ConversionError, register

KNOWN_PATHS = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
]


def soffice():
    env = os.environ.get("SOFFICE")
    if env:
        if not Path(env).is_file():
            raise ConversionError(f"Zmienna SOFFICE wskazuje nieistniejący plik: {env}. Popraw ją albo usuń.")
        return env
    for path in [shutil.which("soffice"), shutil.which("libreoffice"), *KNOWN_PATHS]:
        if path and Path(path).is_file():
            return path
    raise ConversionError("Nie znaleziono LibreOffice. Zainstaluj go z libreoffice.org "
                          "albo ustaw zmienną SOFFICE na ścieżkę do soffice.")


@register(".docx", ".pdf")
@register(".odt", ".pdf")
@register(".docx", ".odt")
@register(".odt", ".docx")
def libreoffice(src, dst):
    if not zipfile.is_zipfile(src):
        raise ConversionError(f"{src.name} jest uszkodzony albo to nie jest prawdziwy plik {src.suffix}.")

    fmt = dst.suffix.lstrip(".")
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            soffice(),
            f"-env:UserInstallation={Path(tmp, 'profile').as_uri()}",
            "--headless", "--convert-to", fmt, "--outdir", tmp, str(src),
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            raise ConversionError("LibreOffice nie odpowiada od 120 s. Zamknij jego okna i spróbuj ponownie.")

        out = Path(tmp, src.stem + "." + fmt)
        if res.returncode != 0 or not out.exists():
            raise ConversionError(f"LibreOffice zwrócił kod {res.returncode}: {res.stderr.strip() or 'brak pliku wynikowego'}")
        shutil.copy(out, dst)