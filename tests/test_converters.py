import csv
import json

import pytest
from docx import Document

from converters import office
from core import ConversionError, convert


@pytest.fixture
def docx_file(tmp_path):
    src = tmp_path / "raport.docx"
    doc = Document()
    doc.add_paragraph("Zażółć gęślą jaźń")
    doc.add_paragraph("Drugi akapit")
    doc.save(src)
    return src


def test_csv_do_json(tmp_path):
    src = tmp_path / "dane.csv"
    src.write_text("imię;miasto;wiek\nŁukasz;Gdańsk;30\nZofia;;\n", encoding="utf-8")

    data = json.loads(convert(src, "json", tmp_path).read_text(encoding="utf-8"))

    assert data == [
        {"imię": "Łukasz", "miasto": "Gdańsk", "wiek": "30"},
        {"imię": "Zofia", "miasto": "", "wiek": ""},
    ]
    assert list(data[0]) == ["imię", "miasto", "wiek"]


def test_json_do_csv(tmp_path):
    src = tmp_path / "dane.json"
    src.write_text('[{"produkt": "Jabłka", "cena": 3.5}, {"produkt": "Śliwki", "kraj": "Polska"}]', encoding="utf-8")

    with open(convert(src, "csv", tmp_path), encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    assert rows == [
        {"produkt": "Jabłka", "cena": "3.5", "kraj": ""},
        {"produkt": "Śliwki", "cena": "", "kraj": "Polska"},
    ]


def test_zly_json(tmp_path):
    src = tmp_path / "dane.json"
    src.write_text('[{"a": }]', encoding="utf-8")
    with pytest.raises(ConversionError, match="Zły JSON"):
        convert(src, "csv", tmp_path)


def test_csv_z_inna_liczba_pol(tmp_path):
    src = tmp_path / "dane.csv"
    src.write_text("a,b\n1,2,3\n", encoding="utf-8")
    with pytest.raises(ConversionError, match="liczbę pól"):
        convert(src, "json", tmp_path)


def test_txt_do_docx(tmp_path):
    src = tmp_path / "notatka.txt"
    src.write_text("Tytuł\n\nZażółć gęślą jaźń.\n", encoding="utf-8")

    doc = Document(convert(src, "docx", tmp_path))

    assert [p.text for p in doc.paragraphs] == ["Tytuł", "", "Zażółć gęślą jaźń."]


def test_docx_do_txt(docx_file, tmp_path):
    out = convert(docx_file, "txt", tmp_path)

    assert out.read_text(encoding="utf-8") == "Zażółć gęślą jaźń\nDrugi akapit\n"


@pytest.mark.parametrize("fmt", ["txt", "pdf"])
def test_uszkodzony_docx(tmp_path, fmt):
    src = tmp_path / "zepsuty.docx"
    src.write_text("to nie jest docx", encoding="utf-8")
    with pytest.raises(ConversionError, match="uszkodzony"):
        convert(src, fmt, tmp_path)


def test_brak_libreoffice(monkeypatch, docx_file, tmp_path):
    monkeypatch.delenv("SOFFICE", raising=False)
    monkeypatch.setattr(office.shutil, "which", lambda name: None)
    monkeypatch.setattr(office, "KNOWN_PATHS", [])

    with pytest.raises(ConversionError, match="Nie znaleziono LibreOffice"):
        convert(docx_file, "pdf", tmp_path)


def test_docx_do_pdf(docx_file, tmp_path):
    try:
        office.soffice()
    except ConversionError:
        pytest.skip("LibreOffice nie jest zainstalowany")

    out = convert(docx_file, "pdf", tmp_path)

    assert out.read_bytes().startswith(b"%PDF")