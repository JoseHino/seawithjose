# -*- coding: utf-8 -*-
"""Prepara tipografías y fotos de la web (se ejecuta a mano, una vez o al cambiar fotos).

    python scripts/recursos.py

- Tipografías: se descargan de Google Fonts y se sirven desde la propia web
  (sin peticiones a Google al visitarla: sin cookies ni transferencias de datos
  fuera de la UE, y por tanto sin banner). Las tres llevan alfabeto cirílico.
    Spectral   (titulares; la cursiva rotula la carta, como en las cartas náuticas)
    Onest      (texto)
    PT Mono    (coordenadas, sondas y el parte del mar)
- Fotos: recorte y WebP en dos anchos. Las de origen viven fuera del repositorio.
"""

import os
import re
import sys
import urllib.request

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESCRITORIO = os.path.join(os.path.expanduser("~"), "OneDrive", "Escritorio")
BUCEO = os.path.join(ESCRITORIO, "buceo-marbella", "img")
BARCO = os.path.join(ESCRITORIO, "Proyectos", "Petit", "Charter", "Fotos")

FUENTES_CSS = ("https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,500;0,600;1,400;1,500"
               "&family=Onest:wght@400..700&family=PT+Mono&display=swap")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
SUBCONJUNTOS = {"latin", "latin-ext", "cyrillic", "cyrillic-ext"}

# nombre: (archivo de origen, recorte relativo (izq, arriba, der, abajo) o None, anchos)
FOTOS = {
    "jose-buceo": (os.path.join(BUCEO, "jose-barco.jpg"), (0.0, 0.18, 1.0, 0.92), (520, 1040)),
    "jose-lancha": (os.path.join(BUCEO, "salida-barco.jpg"), (0.0, 0.04, 1.0, 0.80), (520, 1040)),
    "pulpo": (os.path.join(BUCEO, "pulpo.jpg"), (0.0, 0.01, 0.99, 0.985), (640, 1170)),
    "senal-ok": (os.path.join(BUCEO, "senal-ok.jpg"), (0.012, 0.0, 0.985, 0.985), (640, 1150)),
    "tortuga": (os.path.join(BUCEO, "tortuga.jpg"), (0.015, 0.008, 0.985, 0.99), (520, 1040)),
    "tiburon": (os.path.join(BUCEO, "grupo-tiburon.jpg"), None, (520, 1040)),
    "timon": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.42.25.jpeg"), (0.40, 0.0, 1.0, 1.0), (640, 960)),
}


def descargar(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fuentes():
    destino = os.path.join(RAIZ, "assets", "fuentes")
    os.makedirs(destino, exist_ok=True)
    css = descargar(FUENTES_CSS).decode("utf-8")
    bloques = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css)
    salida, n = [], 0
    for subconjunto, bloque in bloques:
        if subconjunto not in SUBCONJUNTOS:
            continue
        familia = re.search(r"font-family:\s*'([^']+)'", bloque).group(1)
        estilo = re.search(r"font-style:\s*(\w+)", bloque).group(1)
        peso = re.search(r"font-weight:\s*([\d ]+);", bloque).group(1).replace(" ", "-")
        url = re.search(r"url\((https://[^)]+\.woff2)\)", bloque).group(1)
        nombre = f"{familia.lower().replace(' ', '-')}-{estilo}-{peso}-{subconjunto}.woff2"
        open(os.path.join(destino, nombre), "wb").write(descargar(url))
        salida.append(bloque.replace(url, f"fuentes/{nombre}"))
        n += 1
    with open(os.path.join(RAIZ, "assets", "fuentes.css"), "w", encoding="utf-8") as f:
        f.write("/* Generado por scripts/recursos.py · Spectral, Onest y PT Mono (SIL OFL 1.1) */\n")
        f.write("\n".join(salida) + "\n")
    print(f"  [ok] {n} archivos de tipografía")


def fotos():
    destino = os.path.join(RAIZ, "assets", "fotos")
    os.makedirs(destino, exist_ok=True)
    for nombre, (origen, recorte, anchos) in FOTOS.items():
        img = ImageOps.exif_transpose(Image.open(origen)).convert("RGB")
        if recorte:
            w, h = img.size
            img = img.crop((int(recorte[0] * w), int(recorte[1] * h), int(recorte[2] * w), int(recorte[3] * h)))
        for ancho in anchos:
            copia = img.copy()
            if copia.width > ancho:
                copia = copia.resize((ancho, round(copia.height * ancho / copia.width)), Image.LANCZOS)
            copia.save(os.path.join(destino, f"{nombre}-{ancho}.webp"), "WEBP", quality=80, method=6)
        print(f"  [ok] {nombre}: {img.width}x{img.height} → {', '.join(map(str, anchos))}")
    # Imagen para compartir en redes (1200x630), a partir de la foto del timón
    img = ImageOps.exif_transpose(Image.open(FOTOS["timon"][0])).convert("RGB")
    w, h = img.size
    img = ImageOps.fit(img.crop((int(0.30 * w), 0, w, h)), (1200, 630), Image.LANCZOS, centering=(0.5, 0.45))
    img.save(os.path.join(RAIZ, "assets", "compartir.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("  [ok] compartir.jpg")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                             # noqa: BLE001
        pass
    fuentes()
    fotos()
