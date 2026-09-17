from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

base = Path(__file__).resolve().parent / "barbara-nogueira"
font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("Projeto", str(font)))
styles = getSampleStyleSheet()
for name in ["Normal", "Title", "Heading2"]:
    styles[name].fontName = "Projeto"
styles["Normal"].fontSize = 10
styles["Normal"].leading = 15
story = []
for block in (base / "relatorio.md").read_text().split("\n\n"):
    block = block.strip()
    if not block:
        continue
    style = "Title" if block.startswith("# ") else "Heading2" if block.startswith("## ") else "Normal"
    text = block[2:] if style == "Title" else block[3:] if style == "Heading2" else block
    story.append(Paragraph(escape(text).replace("\n", "<br/>"), styles[style]))
    story.append(Spacer(1, 8))
def rodape(canvas, doc):
    canvas.setFont("Projeto", 8)
    canvas.drawString(42, 24, "Bárbara Nogueira — 202004744 — Atividade 03")
    canvas.drawRightString(A4[0] - 42, 24, str(doc.page))
SimpleDocTemplate(str(base / "relatorio.pdf"), pagesize=A4, rightMargin=42,
                  leftMargin=42, topMargin=42, bottomMargin=42).build(
                  story, onFirstPage=rodape, onLaterPages=rodape)
print(base / "relatorio.pdf")
