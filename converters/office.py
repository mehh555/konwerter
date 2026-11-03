import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from core import ConversionError, register


def soffice():
    path = os.environ.get("SOFFICE") or shutil.which("soffice") or shutil.which("libreoffice")
    if not path:
        raise ConversionError("Nie znaleziono LibreOffice (dodaj do PATH albo ustaw SOFFICE)")
    return path


@register(".docx", ".pdf")
@register(".odt", ".pdf")
def to_pdf(src, dst):
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            soffice(),
            f"-env:UserInstallation={Path(tmp, 'profile').as_uri()}",
            "--headless", "--convert-to", "pdf", "--outdir", tmp, str(src),
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            raise ConversionError("LibreOffice się zawiesił")

        out = Path(tmp, src.stem + ".pdf")
        if res.returncode != 0 or not out.exists():
            raise ConversionError(f"LibreOffice zwrócił kod {res.returncode}: {res.stderr.strip()}")
        shutil.move(out, dst)