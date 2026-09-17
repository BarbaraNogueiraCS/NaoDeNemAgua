from pathlib import Path
import subprocess
import sys
import zipfile

base = Path(__file__).resolve().parent
folder = base / "barbara-nogueira"
report = (folder / "relatorio.md").read_text()
images = [folder / "evidencias" / name for name in
          ["teste-normal.png", "teste-decisao.png", "teste-adversarial.png"]]
missing = [str(p.name) for p in images if not p.exists()]
if missing or "pendente" in report.lower() or "https://wokwi.com/projects/" not in report:
    sys.exit("Entrega incompleta: registrar resultados reais, inserir link Wokwi e adicionar as três capturas. "
             + "Capturas ausentes: " + ", ".join(missing))
subprocess.run([sys.executable, str(base / "gerar_relatorio.py")], check=True)
target = base / "atividade-03-barbara-nogueira-202004744.zip"
with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
    for name in ["sketch.ino", "controle.h", "diagram.json", "relatorio.pdf"]:
        archive.write(folder / name, name)
    for image in images:
        archive.write(image, "evidencias/" + image.name)
print(target)
