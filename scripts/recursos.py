# -*- coding: utf-8 -*-
"""Prepara tipografías y fotos de la web (se ejecuta a mano, una vez o al cambiar fotos).

    python scripts/recursos.py

- Tipografías: se descargan de Google Fonts y se sirven desde la propia web
  (sin peticiones a Google al visitarla: sin cookies ni transferencias de datos
  fuera de la UE, y por tanto sin banner). Las dos llevan alfabeto cirílico.
    Sofia Sans Extra Condensed  (titulares, en mayúsculas, como los carteles de regata)
    Sofia Sans                  (texto, datos y rótulos de la carta)
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

FUENTES_CSS = ("https://fonts.googleapis.com/css2?family=Sofia+Sans:ital,wght@0,400..800;1,400..600"
               "&family=Sofia+Sans+Extra+Condensed:wght@700..900&display=swap")
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
    # El Petit (fotos de la carpeta del chárter; las de bandera francesa a la vista no se usan)
    "petit-delfines": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.44.17.jpeg"), None, (640, 1136)),
    "petit-banera": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.42.25.jpeg"), None, (800, 1600)),
    "petit-pantalan": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.41.51.jpeg"), None, (640, 1024)),
    "petit-proa": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.44.45.jpeg"), None, (800, 1600)),
    "petit-azul": (os.path.join(BARCO, "WhatsApp Image 2026-07-03 at 16.44.53.jpeg"), None, (800, 1600)),
    # Fotos del 26-10-2026 en Banús (subcarpeta 261026): sustituyen a las que no dejaban ver bien el barco
    # editada por el usuario; el editor cambió el rótulo del casco y se le devolvió el «42CC» de la foto original
    "petit-banus": (os.path.join(BARCO, "261026", "Velero Jeanneau al atardecer en el puerto (editada, rotulo 42CC).png"), None, (600, 1086)),
    "petit-concha": (os.path.join(BARCO, "261026", "WhatsApp Image 2026-10-26 at 09.25.27 (3).jpeg"), None, (600, 1200)),
    "petit-ocaso": (os.path.join(BARCO, "261026", "WhatsApp Image 2026-10-26 at 09.25.28.jpeg"), (0.0, 0.33, 1.0, 1.0), (800, 1200)),
    "petit-torre": (os.path.join(BARCO, "261026", "WhatsApp Image 2026-10-26 at 09.25.28 (2).jpeg"), (0.0, 0.22, 1.0, 1.0), (800, 1200)),
}
VIDEO = os.path.join(BARCO, "WhatsApp Video 2026-07-03 at 16.43.47.mp4")


def descargar(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fuentes():
    destino = os.path.join(RAIZ, "assets", "fuentes")
    os.makedirs(destino, exist_ok=True)
    for viejo in os.listdir(destino):                 # fuera las tipografías de antes
        os.remove(os.path.join(destino, viejo))
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
        f.write("/* Generado por scripts/recursos.py · Sofia Sans y Sofia Sans Extra Condensed (SIL OFL 1.1) */\n")
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
    # Imagen para compartir en redes (1200x630): el Petit con los delfines
    img = ImageOps.exif_transpose(Image.open(FOTOS["petit-delfines"][0])).convert("RGB")
    img = ImageOps.fit(img, (1200, 630), Image.LANCZOS, centering=(0.5, 0.55))
    img.save(os.path.join(RAIZ, "assets", "compartir.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
    print("  [ok] compartir.jpg")


def video():
    """El Petit navegando: MP4 sin sonido, ligero y con arranque rápido, más su fotograma de portada."""
    import subprocess
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ffmpeg = "ffmpeg"
    destino = os.path.join(RAIZ, "assets", "video")
    os.makedirs(destino, exist_ok=True)
    mp4 = os.path.join(destino, "petit-navegando.mp4")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", VIDEO, "-an", "-vf", "scale=848:-2,fps=30",
                    "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p", "-crf", "27",
                    "-preset", "slow", "-movflags", "+faststart", mp4], check=True)
    poster = os.path.join(destino, "petit-navegando.jpg")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-ss", "3", "-i", VIDEO, "-frames:v", "1",
                    "-vf", "scale=848:-2", "-strict", "unofficial", "-q:v", "4", poster], check=True)
    Image.open(poster).convert("RGB").save(poster.replace(".jpg", ".webp"), "WEBP", quality=78, method=6)
    os.remove(poster)
    print(f"  [ok] vídeo: {os.path.getsize(mp4) // 1024} KB")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                             # noqa: BLE001
        pass
    pasos = sys.argv[1:] or ["fuentes", "fotos", "video"]       # p. ej. «python scripts/recursos.py fotos»
    for paso in pasos:
        {"fuentes": fuentes, "fotos": fotos, "video": video}[paso]()
