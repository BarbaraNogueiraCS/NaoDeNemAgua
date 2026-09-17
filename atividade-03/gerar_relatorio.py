from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

base = Path(__file__).resolve().parent / "barbara-nogueira"
font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdfmetrics.registerFont(TTFont("Projeto", str(font)))
styles = getSampleStyleSheet()
for name in ["Normal", "Title", "Heading2", "Heading3"]:
    styles[name].fontName = "Projeto"
styles["Normal"].fontSize = 10
styles["Normal"].leading = 15
story = []
for block in (base / "relatorio.md").read_text().split("\n\n"):
    block = block.strip()
    if not block:
        continue
    style = "Title" if block.startswith("# ") else "Heading2" if block.startswith("## ") else "Heading3" if block.startswith("### ") else "Normal"
    text = block[2:] if style == "Title" else block[3:] if style == "Heading2" else block[4:] if style == "Heading3" else block
    story.append(Paragraph(escape(text).replace("\n", "<br/>"), styles[style]))
    story.append(Spacer(1, 8))
capturas = [
    ("teste-normal.png", "Estado normal: leitura de 60,02%, dados válidos e autorização desligada."),
    ("teste-decisao.png", "Decisão: leitura de 20,73%, AUTORIZADO e LED verde aceso."),
    ("adversarial-antes-expiracao.png", "Adversarial: último valor retido, com autorização ainda válida antes de expirar."),
    ("teste-adversarial.png", "Adversarial: transição em ageMs=5000 para DADO_OBSOLETO e bloqueio da autorização."),
    ("teste-recuperacao.png", "Recuperação: primeiras novas amostras em AGUARDANDO. O monitor mostra registros anteriores ao estado atual dos LEDs."),
    ("recuperacao-autorizada.png", "Recuperação: novas leituras válidas e retorno a AUTORIZADO."),
]
for filename, caption in capturas:
    image_path = base / "evidencias" / filename
    if not image_path.exists():
        continue
    story.append(PageBreak())
    story.append(Paragraph("Evidência — " + escape(filename), styles["Heading2"]))
    story.append(Paragraph(escape(caption), styles["Normal"]))
    story.append(Spacer(1, 12))
    img = Image(str(image_path))
    ratio = min((A4[0] - 84) / img.imageWidth, 620 / img.imageHeight)
    img.drawWidth = img.imageWidth * ratio
    img.drawHeight = img.imageHeight * ratio
    story.append(img)

def rodape(canvas, doc):
    canvas.setFont("Projeto", 8)
    canvas.drawString(42, 24, "Bárbara Nogueira — 202004744 — Atividade 03")
    canvas.drawRightString(A4[0] - 42, 24, str(doc.page))
SimpleDocTemplate(str(base / "relatorio.pdf"), pagesize=A4, rightMargin=42,
                  leftMargin=42, topMargin=42, bottomMargin=42).build(
                  story, onFirstPage=rodape, onLaterPages=rodape)
print(base / "relatorio.pdf")
