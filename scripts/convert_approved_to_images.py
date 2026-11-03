from pathlib import Path
import fitz
from PIL import Image

root = Path(__file__).resolve().parents[1]
folder = root / "posts" / "post-01"
source = folder / "carousel.pdf"
if not source.is_file():
    raise SystemExit("Approved PDF not found")
doc = fitz.open(source)
if len(doc) != 4:
    raise SystemExit(f"Expected four approved pages, found {len(doc)}")
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.thumbnail((1080, 1350), Image.Resampling.LANCZOS)
    if img.size != (1080, 1350):
        img = img.resize((1080, 1350), Image.Resampling.LANCZOS)
    dest = folder / f"slide-{i:02d}.jpg"
    img.save(dest, "JPEG", quality=94, optimize=True)
    print(f"Saved {dest.relative_to(root)}: {img.size}")
