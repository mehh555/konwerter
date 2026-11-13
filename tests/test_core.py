from pathlib import Path

import pytest

import converters
from core import ConversionError, available_targets, convert, validate


@pytest.fixture
def csv_file(tmp_path):
    src = tmp_path / "dane.csv"
    src.write_text("a,b\n1,2\n", encoding="utf-8")
    return src


def test_available_targets():
    assert available_targets(Path("dane.csv")) == [".json"]
    assert available_targets(Path("raport.DOCX")) == [".odt", ".pdf", ".txt"]
    assert available_targets(Path("obraz.png")) == []


def test_validate_brak_pliku(tmp_path):
    with pytest.raises(ConversionError, match="Nie ma pliku"):
        validate(tmp_path / "brak.csv", "json", tmp_path)


def test_validate_nieobslugiwana_para(csv_file, tmp_path):
    with pytest.raises(ConversionError, match="Nie obsługuję"):
        validate(csv_file, "pdf", tmp_path)


def test_validate_brak_katalogu(csv_file, tmp_path):
    with pytest.raises(ConversionError, match="Nie ma katalogu"):
        validate(csv_file, "json", tmp_path / "nie_ma")


def test_istniejacy_plik_nie_jest_nadpisywany(csv_file, tmp_path):
    (tmp_path / "dane.json").write_text("stary", encoding="utf-8")

    out = convert(csv_file, "json", tmp_path)

    assert out.name == "dane (1).json"
    assert (tmp_path / "dane.json").read_text(encoding="utf-8") == "stary"


def test_nadpisanie_na_zyczenie(csv_file, tmp_path):
    (tmp_path / "dane.json").write_text("stary", encoding="utf-8")

    out = convert(csv_file, "json", tmp_path, overwrite=True)

    assert out.name == "dane.json"
    assert "stary" not in out.read_text(encoding="utf-8")