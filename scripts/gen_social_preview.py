# -*- coding: utf-8 -*-
"""Gera a imagem de social preview do repositório (1280x640).

Uso:
  pip install Pillow
  python scripts/gen_social_preview.py   # gera assets/social_preview.png
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG = (13, 17, 23)        # GitHub dark
FG = (230, 237, 243)
MUTED = (139, 148, 158)
AMBER = (210, 153, 34)
BLUE = (56, 139, 253)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def bold(s):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans-Bold.ttf", s)


def sans(s):
    return ImageFont.truetype(f"{FONT_DIR}/DejaVuSans.ttf", s)

RESULTS = [
    ("BM25 (1994, sem IA)", 0.771, AMBER),
    ("bge-m3 (SOTA multilíngue)", 0.441, BLUE),
    ("serafim-335m (SOTA PT)", 0.170, BLUE),
    ("MiniLM (mais baixado do mundo)", 0.040, BLUE),
]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.text((70, 52), "JurisBench-BR", font=bold(58), fill=FG)
d.text((70, 130), "O 1º benchmark aberto de busca semântica jurídica em PT-BR",
       font=sans(28), fill=MUTED)

d.text((70, 196), "Um algoritmo de 1994 vence todos os embeddings de IA",
       font=bold(34), fill=AMBER)
d.text((70, 242), "na jurisprudência brasileira — por margens enormes.",
       font=bold(34), fill=AMBER)

# gráfico de barras (nDCG@10)
x0, x1 = 470, 1180
y, bar_h, gap = 330, 40, 22
d.text((x0, y - 36), "nDCG@10 (maior = melhor)", font=sans(20), fill=MUTED)
for nome, valor, cor in RESULTS:
    w = int((x1 - x0) * valor)
    d.text((70, y + 8), nome, font=sans(24), fill=FG)
    d.rounded_rectangle([x0, y, x0 + max(w, 6), y + bar_h], radius=6, fill=cor)
    d.text((x0 + max(w, 6) + 14, y + 7), f"{valor:.3f}".replace(".", ","),
           font=bold(24), fill=FG)
    y += bar_h + gap

d.text((70, 592), "github.com/ThalesAndrades/JurisBench-BR  ·  reproduza em 3 comandos  ·  Apache 2.0",
       font=sans(22), fill=MUTED)

img.save("assets/social_preview.png", optimize=True)
print("ok: assets/social_preview.png")
