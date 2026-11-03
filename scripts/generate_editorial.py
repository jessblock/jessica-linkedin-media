import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/produto-problema-cliente.json").read_text(encoding="utf-8"))
OUT = ROOT / "posts" / DATA["slug"]
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1080, 1350
BG, GOLD, WHITE, TEAL = "#102F3C", "#D5BE94", "#F1EDE5", "#2B6770"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")), size)
def lines(draw, text, f, width):
    words, result, line = text.split(), [], ""
    for word in words:
        candidate = (line + " " + word).strip()
        if draw.textbbox((0,0),candidate,font=f)[2] > width and line:
            result.append(line); line=word
        else: line=candidate
    if line: result.append(line)
    return result
pages=[]
for index, slide in enumerate(DATA["slides"]):
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)
    d.rectangle((62,62,W-62,H-62),outline=GOLD,width=3)
    d.line((112,180,968,180),fill=GOLD,width=2)
    d.text((114,119),"JESSICA BLOCK  /  PRODUCT & STRATEGY",font=font(24,True),fill=GOLD)
    d.text((114,242),slide["eyebrow"],font=font(29,True),fill=GOLD)
    title_font=font(65,True)
    y=342
    for line in lines(d,slide["title"],title_font,830):
        d.text((110,y),line,font=title_font,fill=WHITE);y+=92
    d.line((112,y+55,300,y+55),fill=GOLD,width=4)
    y+=115
    body_font=font(37)
    for line in lines(d,slide["body"],body_font,835):
        d.text((112,y),line,font=body_font,fill=WHITE);y+=64
    d.text((114,1190),"JESSICA BLOCK",font=font(25,True),fill=GOLD)
    d.text((890,1190),f"{index+1:02d} / {len(DATA['slides']):02d}",font=font(23),fill=GOLD)
    pages.append(img)
    if index==0: img.save(OUT/"cover.jpg",quality=94)
pdf=canvas.Canvas(str(OUT/"carousel.pdf"),pagesize=(W,H),pageCompression=1)
for img in pages:
    from io import BytesIO
    from reportlab.lib.utils import ImageReader
    buf=BytesIO()
    img.save(buf,format="PNG")
    buf.seek(0)
    pdf.drawImage(ImageReader(buf),0,0,width=W,height=H)
    pdf.showPage()
pdf.save()
print("Generated",OUT/"carousel.pdf","and",OUT/"cover.jpg")
