from docx import Document

from core import ConversionError, register


@register(".txt", ".docx")
def txt_to_docx(src, dst):
    doc = Document()
    try:
        for line in src.read_text(encoding="utf-8-sig").splitlines():
            doc.add_paragraph(line)
    except ValueError:
        raise ConversionError(f"{src.name} zawiera znaki sterujące - to nie jest zwykły plik tekstowy.")
    doc.save(dst)


@register(".docx", ".txt")
def docx_to_txt(src, dst):
    try:
        doc = Document(src)
    except Exception:
        raise ConversionError(f"{src.name} jest uszkodzony albo to nie jest prawdziwy plik DOCX.")
    text = "\n".join(p.text for p in doc.paragraphs)
    dst.write_text(text + "\n", encoding="utf-8")