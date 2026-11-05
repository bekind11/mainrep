"""Собирает PDF для печати: одна картинка-раскраска на страницу A4.

Ориентация листа подбирается под картинку, поля 1 см.
Запуск: python3 scripts/make_coloring_pdf.py <папка с картинками> <выходной.pdf> [файлы-исключения...]
"""
import io
import sys
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
MARGIN = 1 * cm


def main(src: str, out: str, skip: list[str]) -> None:
    files = sorted(p for p in Path(src).iterdir() if p.suffix.lower() in EXTS and p.name not in skip)
    c = canvas.Canvas(out)
    c.setTitle("Раскраска")
    for p in files:
        im = Image.open(p).convert("RGB")
        w, h = im.size
        page = landscape(A4) if w > h else portrait(A4)
        c.setPageSize(page)
        pw, ph = page
        scale = min((pw - 2 * MARGIN) / w, (ph - 2 * MARGIN) / h)
        dw, dh = w * scale, h * scale
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=95)
        c.drawImage(ImageReader(buf), (pw - dw) / 2, (ph - dh) / 2, dw, dh)
        c.showPage()
        print(f"{p.name}: {'альбомная' if w > h else 'книжная'}")
    c.save()
    print(f"Готово: {out}, страниц: {len(files)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
