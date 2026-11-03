"""Generate PUBLIC test assets. These are not approved for posting."""
from pathlib import Path
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

out = Path("posts/technical-test")
out.mkdir(parents=True, exist_ok=True)
w, h = 1080, 1350
bg = (17, 44, 55)
gold = (215, 193, 151)
cream = (241, 237, 226)
img = Image.new("RGB", (w, h), bg)
draw = ImageDraw.Draw(img)
draw.rectangle((55, 55, w-55, h-55), outline=gold, width=4)
draw.text((100, 185), "JESSICA BLOCK", fill=gold)
draw.text((100, 380), "TESTE TECNICO", fill=cream)
draw.text((100, 450), "NAO PUBLICAR", fill=cream)
draw.text((100, 1150), "Validacao de hospedagem de arquivos", fill=gold)
img.save(out / "cover.jpg", quality=88)
pdf = canvas.Canvas(str(out / "carousel.pdf"), pagesize=(w, h))
pdf.setFillColorRGB(17/255,44/255,55/255)
pdf.rect(0,0,w,h,fill=1,stroke=0)
pdf.setStrokeColorRGB(215/255,193/255,151/255)
pdf.rect(55,55,w-110,h-110,fill=0,stroke=1)
pdf.setFillColorRGB(241/255,237/255,226/255)
pdf.setFont("Helvetica-Bold",50)
pdf.drawString(100,900,"TESTE TECNICO")
pdf.drawString(100,825,"NAO PUBLICAR")
pdf.setFont("Helvetica",24)
pdf.drawString(100,160,"Validacao de hospedagem de arquivos")
pdf.save()
print("Created test PDF and cover; not for publication")
