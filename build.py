# -*- coding: utf-8 -*-
"""Genera la web de Sea With Jose en inglés (raíz), español (/es/) y ruso (/ru/).

    python build.py

Lee textos.py y fuentes/carta.json (isobatas de EMODnet, ver scripts/carta.py)
y escribe la portada, la página de buceo (la Senda Azul), la de «reserva
recibida», el aviso legal, el 404, sitemap.xml y robots.txt. Las rutas son
relativas, así que la web funciona igual en local, en GitHub Pages y en
seawithjose.es.
"""

import datetime
import html
import json
import math
import os
import sys
import urllib.parse

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from textos import (T, IDIOMAS, WHATSAPP, WHATSAPP_VISIBLE, INSTAGRAM, EMAIL, DOMINIO,  # noqa: E402
                    PRECIO_COMPARTIDA, PRECIO_PRIVADA, PLAZAS, HORARIOS, DIAS_RESERVA, PAGOS, CAMARAS_EMBED,
                    SENDA_AZUL)
CARTA = json.load(open(os.path.join(RAIZ, "fuentes", "carta.json"), encoding="utf-8"))
VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")   # rompe la caché del CSS y el JS


def esc(s):
    return html.escape(str(s), quote=True)


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(texto)}"


def carpeta(lang):
    return "" if lang == IDIOMAS[0] else f"{lang}/"


def prefijo_de(lang):
    return "" if lang == IDIOMAS[0] else "../"


# ─────────────────────────────── símbolos ───────────────────────────────
BANDERAS = {   # Código Internacional de Señales
    "J": '<rect width="18" height="12" fill="#1F4E9A"/><rect y="4" width="18" height="4" fill="#fff"/>',
    "O": '<path d="M0 0H18V12Z" fill="#D2232A"/><path d="M0 0V12H18Z" fill="#F5C400"/>',
    "S": '<rect width="18" height="12" fill="#fff"/><rect x="5.5" y="2.5" width="7" height="7" fill="#1F4E9A"/>',
    "E": '<rect width="18" height="6" fill="#1F4E9A"/><rect y="6" width="18" height="6" fill="#D2232A"/>',
}


def banderas_jose(clase="banderas"):
    return (f'<span class="{clase}" aria-hidden="true">' + "".join(
        f'<svg viewBox="0 0 18 12" width="18" height="12">{BANDERAS[l]}'
        f'<rect width="18" height="12" fill="none" stroke="#10263A" stroke-opacity=".35"/></svg>'
        for l in "JOSE") + "</span>")


SIMBOLOS = {
    "vela": ('<svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true"><path d="M25 4V31H9Z"/>'
             '<path d="M28 9 40 31H28Z"/><path d="M5 35H47L41 41H11Z"/></svg>'),
    # Bandera A del Código: «tengo un buzo sumergido»
    "buceo": ('<svg class="simbolo simbolo-color" viewBox="0 0 52 36" aria-hidden="true">'
              '<rect x="1" y="1" width="24" height="34" fill="#fff" stroke="#10263A" stroke-width="1.4"/>'
              '<path d="M25 1H51L38 18 51 35H25Z" fill="#1F4E9A" stroke="#10263A" stroke-width="1.4" '
              'stroke-linejoin="round"/></svg>'),
    "pesca": ('<svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true">'
              '<path d="M6 22C14 11 31 10 39 22 31 34 14 33 6 22Z"/><path d="M39 22 48 14V30Z"/>'
              '<circle cx="15" cy="20" r="1.6" fill="currentColor" stroke="none"/></svg>'),
    "moto": ('<svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true">'
             '<path d="M6 30H35C39 30 43 28 46 24H38L32 18H23L19 24H8Z"/><path d="M25 18 28 12H33"/>'
             '<path d="M3 37C9 34 15 40 21 37 27 34 33 40 39 37 43 35 46 36 49 37"/></svg>'),
}
# Iconos de la personalización: trazo fino, como los símbolos de la carta
ICONOS_EXTRAS = {
    "buffet": '<path d="M8 34H44M12 34A14 14 0 0 1 40 34M26 20V16M23 16H29"/><path d="M6 38H46"/>',
    "paella": ('<ellipse cx="26" cy="27" rx="17" ry="7"/><path d="M9 27V30C9 34 17 37 26 37S43 34 43 30V27"/>'
               '<path d="M3 26 9 27M49 26 43 27"/><circle cx="20" cy="26" r="1.6"/><circle cx="29" cy="24" r="1.6"/>'
               '<circle cx="33" cy="28.5" r="1.6"/>'),
    "cocteles": '<path d="M12 10H40L26 26Z"/><path d="M26 26V40M18 41H34M34 6 30 16"/><circle cx="21" cy="14" r="2"/>',
    "tarta": ('<path d="M10 40V26H42V40Z"/><path d="M10 31C14 34 18 28 22 31S30 34 34 31 40 28 42 31"/>'
              '<path d="M26 26V18M26 13C24 15 24 17 26 17S28 15 26 13Z"/><path d="M6 40H46"/>'),
    # Empavesado: banderas del Código colgadas, como se engalanan los barcos de fiesta
    "decoracion": ('<path d="M4 12C17 20 35 20 48 12"/><path d="M11 16 13 26 17 17.5M21 18.8 23 29 27 19.2'
                   'M31 19 33 28.6 37 18M41 16.4 43 25 45 14.6"/>'),
    "otra": ('<path d="M26 6 29 20 43 23 29 26 26 40 23 26 9 23 23 20Z"/><path d="M41 7V13M38 10H44M10 35V39M8 37H12"/>'),
}
ICONO_WA = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 '
            '15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1'
            'c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9'
            'c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4 5.2 5.2 0 0 0 3.2.7'
            ' 2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3Z"/></svg>')
ICONO_IG = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" '
            'fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" '
            'stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>')
ICONO_MAIL = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" '
              'fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m4 7 8 6 8-6" fill="none" '
              'stroke="currentColor" stroke-width="1.8"/></svg>')
ICONO_TARJETA = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" '
                 'rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 9.5h19M6 15h4" '
                 'stroke="currentColor" stroke-width="1.8"/></svg>')
FLECHA = '<span class="flecha" aria-hidden="true">→</span>'


# ─────────────────────────────── la carta ───────────────────────────────
def proyectar(lon, lat):
    oeste, sur, este, norte = CARTA["encuadre"]
    return ((lon - oeste) / (este - oeste) * CARTA["ancho"], (norte - lat) / (norte - sur) * CARTA["alto"])


def borde_graduado(W, H, B, c):
    """Borde de carta náutica: barras alternas de un minuto de latitud y de longitud,
    rotuladas como en las cartas (grados en la primera marca, solo minutos en el resto)."""
    oeste, sur, este, norte = CARTA["encuadre"]
    out = ['<g class="borde" aria-hidden="true">']

    def barras(marcas, total, eje):
        cortes = [0.0] + [p for _, p in marcas] + [total]
        piezas = []
        for i in range(len(cortes) - 1):
            a, b = cortes[i], cortes[i + 1]
            clase = "barra-llena" if i % 2 == 0 else "barra-vacia"
            for fijo in ((-B, H) if eje == "x" else (-B, W)):
                if eje == "x":
                    piezas.append(f'<rect class="{clase}" x="{a:.1f}" y="{fijo}" width="{b - a:.1f}" height="{B}"/>')
                else:
                    piezas.append(f'<rect class="{clase}" x="{fijo}" y="{a:.1f}" width="{B}" height="{b - a:.1f}"/>')
        return piezas

    m_lon = [(m, (m / 60 - oeste) / (este - oeste) * W)
             for m in range(math.ceil(oeste * 60), math.floor(este * 60) + 1)]
    m_lat = [(m, (norte - m / 60) / (norte - sur) * H)
             for m in range(math.floor(norte * 60), math.ceil(sur * 60) - 1, -1)]
    out += barras(m_lon, W, "x") + barras(m_lat, H, "y")
    out.append(f'<rect class="filete" x="{-B}" y="{-B}" width="{W + 2 * B}" height="{H + 2 * B}"/>')
    out.append(f'<rect class="filete" width="{W}" height="{H}"/>')
    for n, (m, x) in enumerate(m_lon):
        g, mi = divmod(abs(m), 60)
        rotulo = f"{g}°{mi:02d}′{c['oeste']}" if n == 0 or mi == 0 else f"{mi:02d}′"
        out.append(f'<text class="rotulo-borde" x="{x:.1f}" y="{-B - 9}" text-anchor="middle">{rotulo}</text>')
    for n, (m, y) in enumerate(m_lat):
        g, mi = divmod(m, 60)
        rotulo = f"{g}°{mi:02d}′{c['norte']}" if n == 0 or mi == 0 else f"{mi:02d}′"
        out.append(f'<text class="rotulo-borde" x="{-B - 9}" y="{y:.1f}" text-anchor="end" '
                   f'dominant-baseline="middle">{rotulo}</text>')
    out.append("</g>")
    return "".join(out)


# La derrota habitual de la salida: Banús → velas arriba → fondeo frente a San Pedro → mar abierto → vuelta
WAYPOINTS = [(-4.9530, 36.4846), (-4.9480, 36.4700), (-4.9850, 36.4700), (-4.9650, 36.4480), (-4.9300, 36.4650)]


def curva(puntos):
    """Catmull-Rom a Bézier: una derrota suave que pasa por todos los puntos."""
    d = f"M{puntos[0][0]:.0f},{puntos[0][1]:.0f}"
    for i in range(len(puntos) - 1):
        p0 = puntos[i - 1] if i > 0 else puntos[i]
        p1, p2 = puntos[i], puntos[i + 1]
        p3 = puntos[i + 2] if i + 2 < len(puntos) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.0f},{c1[1]:.0f} {c2[0]:.0f},{c2[1]:.0f} {p2[0]:.0f},{p2[1]:.0f}"
    return d


def svg_carta(t):
    W, H = CARTA["ancho"], CARTA["alto"]
    L, c = CARTA["lugares"], t["carta"]
    M, B = 98, 9      # margen para los rótulos del borde · grosor de las barras
    out = [f'<svg class="carta" viewBox="{-M} -42 {W + M + B + 4} {H + 42 + B + 4}" role="img" '
           f'aria-label="{esc(t["carta_aria"])}">',
           f'<clipPath id="recorte-carta"><rect width="{W}" height="{H}"/></clipPath>',
           '<g clip-path="url(#recorte-carta)">',
           f'<rect class="carta-mar" width="{W}" height="{H}"/>']
    profundidades = sorted({i["m"] for i in CARTA["isobatas"]})
    out.append('<g class="carta-isobatas">' + "".join(
        f'<path class="iso{" iso-principal" if i["m"] in (10, 20, 50, 100) else ""}" pathLength="1" '
        f'style="--i:{profundidades.index(i["m"])}" d="{i["d"]}"/>' for i in CARTA["isobatas"]) + "</g>")
    out.append('<g class="carta-tierra">' + "".join(f'<path d="{d}"/>' for d in CARTA["tierra"]) + "</g>")
    bx, by = L["banus"]
    gx, gy = L["galeon"]
    ax, ay = W * 0.70, H - 26
    pts = [proyectar(*p) for p in WAYPOINTS]
    # Cajas que ocupan los rótulos y la derrota: ahí no se pintan sondas
    cajas = [(bx - 16, by - 24, bx + 26 + len(c["banus"]) * 13, by + 40),
             (gx - 20, gy - 22, gx + 30 + len(c["galeon"]) * 11.5, gy + 16),
             (ax - len(c["alboran"]) * 11, ay - 30, ax + len(c["alboran"]) * 11, ay + 12)]
    cajas += [(x - 26, y - 26, x + 26, y + 26) for x, y in pts]
    cajas.append((pts[3][0] - 30 - len(c["ruta"]) * 12, pts[3][1] + 20, pts[3][0] - 20, pts[3][1] + 56))
    libres = [s for s in CARTA["sondas"]
              if not any(x0 <= s["x"] <= x1 and y0 <= s["y"] <= y1 for x0, y0, x1, y1 in cajas)]
    out.append('<g class="carta-sondas" aria-hidden="true">' + "".join(
        f'<text class="sonda" x="{s["x"]}" y="{s["y"]}" style="--j:{n}">{s["m"]}</text>'
        for n, s in enumerate(libres)) + "</g>")
    out.append('<g class="carta-rotulos" aria-hidden="true">'
               f'<text class="rotulo-tierra" x="22" y="{L["sanpedro"][1] - 46}">{esc(c["sanpedro"])}</text>'
               f'<text class="rotulo-tierra" x="{W - 20}" y="32" text-anchor="end">{esc(c["marbella"])}</text>'
               f'<text class="rotulo-tierra rotulo-rio" x="{L["rioverde"][0]}" y="{L["rioverde"][1] - 30}" '
               f'text-anchor="middle">{esc(c["rioverde"])}</text>'
               # Puerto deportivo: símbolo de la carta (velero) en magenta
               f'<g class="simbolo-puerto" transform="translate({bx} {by})"><path d="M0-15V0H-9Z M2-11 9 0H2Z M-12 3H12L8 7H-8Z"/></g>'
               f'<text class="rotulo-puerto" x="{bx + 18}" y="{by - 2}">{esc(c["banus"])}</text>'
               # Pecio no peligroso (INT1 K29): línea con tres trazos
               f'<g class="simbolo-pecio" transform="translate({gx} {gy})"><path d="M-14 0H14 M-7-6V6 M0-6V6 M7-6V6"/></g>'
               f'<text class="rotulo-pecio" x="{gx + 22}" y="{gy + 6}">{esc(c["galeon"])}</text>'
               f'<text class="rotulo-mar" x="{ax:.0f}" y="{ay:.0f}" text-anchor="middle">{esc(c["alboran"])}</text>'
               "</g>")
    # La derrota, en magenta como las rutas que se trazan a lápiz sobre la carta
    ida = curva(pts + [pts[0]])
    out.append(f'<g class="derrota"><path class="ruta-estela" d="{ida}"/><path class="ruta-linea" pathLength="1" d="{ida}"/>'
               + "".join(f'<g class="ruta-punto" transform="translate({x:.0f} {y:.0f})" style="--k:{n}">'
                         f'<circle r="17"/><text dy="6" text-anchor="middle">{n + 1}</text></g>'
                         for n, (x, y) in enumerate(pts))
               + f'<text class="ruta-rotulo" x="{pts[3][0] - 24:.0f}" y="{pts[3][1] + 46:.0f}" text-anchor="end">{esc(c["ruta"])}</text>'
               + "</g>")
    out.append("</g>")                      # fin del recorte
    out.append(borde_graduado(W, H, B, c))
    out.append("</svg>")
    return "".join(out)


def simbolo_isobatas():
    """Las isobatas de la carta, una sola vez por página, para usarlas de textura de fondo."""
    W, H = CARTA["ancho"], CARTA["alto"]
    return (f'<svg class="oculto-svg" aria-hidden="true"><symbol id="isobatas" viewBox="0 0 {W} {H}">'
            + "".join(f'<path d="{i["d"]}"/>' for i in CARTA["isobatas"]) + "</symbol></svg>")


def fondo_isobatas():
    W, H = CARTA["ancho"], CARTA["alto"]
    return (f'<svg class="fondo-isobatas" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<use href="#isobatas" width="{W}" height="{H}"/></svg>')


def imagen(nombre, anchos, alt, prefijo, clase="", sizes="(max-width: 900px) 100vw, 50vw", carga="lazy"):
    srcset = ", ".join(f"{prefijo}assets/fotos/{nombre}-{a}.webp {a}w" for a in anchos)
    clase_attr = f' class="{clase}"' if clase else ""
    return (f'<img{clase_attr} src="{prefijo}assets/fotos/{nombre}-{anchos[0]}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" alt="{esc(alt)}" loading="{carga}" decoding="async">')


def vela_hero(t, prefijo):
    """La foto del atardecer recortada con la forma de una mayor, con su mástil y su botavara."""
    return f"""<svg class="vela" viewBox="0 0 520 640" role="img" aria-label="{esc(t["hero_foto_alt"])}">
        <defs><clipPath id="forma-vela"><path d="M46 12 L206 12 C 330 196 452 418 500 596 L46 596 Z"/></clipPath></defs>
        <image href="{prefijo}assets/fotos/petit-atardecer-1047.webp" x="46" y="12" width="454" height="584"
               preserveAspectRatio="xMidYMin slice" clip-path="url(#forma-vela)"/>
        <path class="vela-relinga" d="M206 12 C 330 196 452 418 500 596"/>
        <line class="vela-mastil" x1="40" y1="0" x2="40" y2="640"/>
        <line class="vela-botavara" x1="34" y1="603" x2="508" y2="603"/>
      </svg>"""


# ─────────────────────────────── piezas comunes ───────────────────────────────
def cabeza(t, lang, prefijo, titulo, descripcion, ruta, extra=""):
    alternas = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}/{carpeta(l)}{ruta}">' for l in IDIOMAS)
    alternas += f'<link rel="alternate" hreflang="x-default" href="{DOMINIO}/{ruta}">'
    precarga = "cyrillic" if lang == "ru" else "latin"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
<link rel="canonical" href="{DOMINIO}/{carpeta(lang)}{ruta}">
{alternas}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sea With Jose">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{DOMINIO}/{carpeta(lang)}{ruta}">
<meta property="og:image" content="{DOMINIO}/assets/compartir.jpg">
<meta property="og:locale" content="{t['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E3B5C">
<link rel="icon" href="{prefijo}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefijo}assets/icono-180.png">
<link rel="preload" href="{prefijo}assets/fuentes/spectral-normal-600-{precarga}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefijo}assets/fuentes/onest-normal-400-700-{precarga}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefijo}assets/fuentes.css?v={VERSION}">
<link rel="stylesheet" href="{prefijo}assets/estilo.css?v={VERSION}">
{extra}</head>"""


def cabecera(t, lang, prefijo, pagina="index.html"):
    """En la portada, los enlaces son anclas; en el resto de páginas apuntan a la portada (salvo Buceo)."""
    inicio = "" if pagina == "index.html" else f"{prefijo}{carpeta(lang)}"
    destino = {k: f"{inicio}#{k}" for k in t["nav"]}
    destino["buceo"] = f"{prefijo}{carpeta(lang)}buceo.html"
    actual = {"buceo.html": "buceo"}.get(pagina)
    enlaces = "".join(f'<li><a href="{destino[k]}"' + (' aria-current="page"' if k == actual else "")
                      + f'>{esc(v)}</a></li>' for k, v in t["nav"].items())
    ruta = "" if pagina == "index.html" else pagina
    idiomas = "".join(
        (f'<a href="{prefijo}{carpeta(l)}{ruta}" lang="{l}" hreflang="{l}"'
         + (' aria-current="true"' if l == lang else "") + f' title="{esc(T[l]["nombre_idioma"])}">{T[l]["corto"]}</a>')
        for l in IDIOMAS)
    return f"""<a class="saltar" href="#contenido">{esc(t["saltar"])}</a>
<header class="cabecera">
  <div class="contenedor cabecera-fila">
    <a class="marca" href="{prefijo}{carpeta(lang)}">{banderas_jose()}<span>Sea With Jose</span></a>
    <button class="menu-boton" type="button" aria-expanded="false" aria-controls="navegacion">
      <span class="menu-raya" aria-hidden="true"></span><span class="visualmente-oculto">{esc(t["menu"])}</span>
    </button>
    <nav id="navegacion" class="navegacion" aria-label="{esc(t["menu"])}">
      <ul>{enlaces}</ul>
      <div class="idiomas">{idiomas}</div>
      <a class="boton boton-principal boton-pequeno" href="{inicio}#reservar">{esc(t["reservar_corto"])}</a>
    </nav>
  </div>
</header>"""


def pie(t, lang, prefijo, ruta=""):
    idiomas = " · ".join(f'<a href="{prefijo}{carpeta(l)}{ruta}" lang="{l}">{T[l]["nombre_idioma"]}</a>'
                         for l in IDIOMAS)
    return f"""<footer class="pie">
  <div class="contenedor pie-rejilla">
    <div>
      <p class="pie-marca">{banderas_jose()}<span>Sea With Jose</span></p>
      <p>{esc(t["pie_lugar"])}</p>
    </div>
    <div>
      <p><a href="{wa(t["wa_hola"])}">WhatsApp {WHATSAPP_VISIBLE}</a><br>
      <a href="https://www.instagram.com/{INSTAGRAM}/">Instagram @{INSTAGRAM}</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <p>{idiomas}</p>
      <p><a href="{prefijo}{carpeta(lang)}legal.html">{esc(t["pie_legal"])}</a></p>
      <p class="pie-creditos">{esc(t["pie_creditos"])} · © {datetime.date.today().year} Sea With Jose</p>
    </div>
  </div>
</footer>"""


def json_ld(t, lang):
    datos = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Sea With Jose",
        "url": f"{DOMINIO}/{carpeta(lang)}", "image": f"{DOMINIO}/assets/compartir.jpg",
        "description": t["description"], "telephone": "+" + WHATSAPP, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": "Puerto José Banús", "postalCode": "29660",
                    "addressLocality": "Marbella", "addressRegion": "Málaga", "addressCountry": "ES"},
        "geo": {"@type": "GeoCoordinates", "latitude": 36.4846, "longitude": -4.953},
        "areaServed": "Marbella", "sameAs": [f"https://www.instagram.com/{INSTAGRAM}/"],
        "knowsLanguage": IDIOMAS,
        "makesOffer": [
            {"@type": "Offer", "name": t["opciones"]["compartida"]["titulo"], "price": str(PRECIO_COMPARTIDA),
             "priceCurrency": "EUR", "url": f"{DOMINIO}/{carpeta(lang)}#reservar"},
            {"@type": "Offer", "name": t["opciones"]["privada"]["titulo"], "price": str(PRECIO_PRIVADA),
             "priceCurrency": "EUR", "url": f"{DOMINIO}/{carpeta(lang)}#reservar"},
        ],
        "founder": {"@type": "Person", "name": "José María Hinojosa Figueira",
                    "jobTitle": "Yacht captain, oceanographer and diving instructor"},
    }
    return f'<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False)}</script>\n'


def datos_pagina(datos):
    return f'<script type="application/json" id="datos-pagina">{json.dumps(datos, ensure_ascii=False)}</script>'


def nivel_badges(nivel, s):
    return "".join(f'<span class="nivel nivel-{n}">{esc(s["niveles"][n])}</span>' for n in nivel)


def ficha_sitio(sitio, n, s, lang, mini=False):
    acceso = " · ".join(s["accesos"][a] for a in sitio["acceso"])
    cerca = f'<span class="cerca">{esc(s["cerca"])}</span>' if sitio["banus"] else ""
    datos = (f'<dl class="sitio-datos"><div><dt>{esc(s["campos"]["acceso"])}</dt><dd>{esc(acceso)}</dd></div>'
             f'<div><dt>{esc(s["campos"]["vis"])}</dt><dd>{esc(s["visibilidades"][sitio["vis"]])}</dd></div></dl>')
    enlace = (f'<a class="sitio-enlace" href="{wa(s["msg"].format(sitio=sitio["nombre"]))}">{ICONO_WA}'
              f'{esc(s["quiero"])}</a>')
    return f"""
      <article class="sitio" id="sitio-{sitio["id"]}" data-nivel="{" ".join(sitio["nivel"])}" data-banus="{str(sitio["banus"]).lower()}">
        <p class="sitio-num">{n:02d} · {esc(sitio["lugar"])}{cerca}</p>
        <h3>{esc(sitio["nombre"])}</h3>
        <p class="sitio-prof"><span>{esc(sitio["prof"])}</span> m</p>
        <p class="sitio-niveles">{nivel_badges(sitio["nivel"], s)}</p>
        <p class="sitio-que">{esc(sitio["que"][lang])}</p>
        {"" if mini else datos}
        {"" if mini else enlace}
      </article>"""


# ─────────────────────────────── portada ───────────────────────────────
def portada(lang):
    t = T[lang]
    prefijo = prefijo_de(lang)
    f, b, s = t["form"], t["billete"], t["senda"]
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "pagina": "portada",
                "precios": {"compartida": PRECIO_COMPARTIDA, "privada": PRECIO_PRIVADA}, "plazas": PLAZAS,
                "dias": DIAS_RESERVA, "pagos": PAGOS, "form": f, "billete": b,
                "extras": {e["id"]: e["titulo"] for e in t["extras"]},
                "chip": [t["hero_chip"], t["hero_chip_agua"], t["hero_chip_sol"]],
                "mar": {k: v for k, v in t["mar"].items() if k not in SOLO_HTML}}

    precios = "".join(f'<li class="precio"><span class="precio-tipo">{esc(a)}</span>'
                      f'<span class="precio-cifra">{esc(p)}</span><span class="precio-unidad">{esc(u)}</span></li>'
                      for a, p, u in t["hero_precios"])
    credenciales = "".join(f'<li><strong>{esc(a)}</strong><span>{esc(c)}</span></li>' for a, c in t["credenciales"])

    def tarjeta_salida(tipo, foto, anchos):
        o = t["opciones"][tipo]
        return f"""
      <article class="salida salida-{tipo}">
        <figure class="salida-foto">{imagen(foto, anchos, o["foto_alt"], prefijo, "", "(max-width: 900px) 100vw, 50vw")}</figure>
        <div class="salida-cuerpo">
          <h3>{esc(o["titulo"])}</h3>
          <p class="salida-precio"><span>{esc(o["precio"])}</span> {esc(o["unidad"])}</p>
          <ul>{"".join(f"<li>{esc(x)}</li>" for x in o["puntos"])}</ul>
          <a class="boton boton-principal" href="#reservar" data-tipo="{tipo}">{esc(o["cta"])}{FLECHA}</a>
        </div>
      </article>"""

    pasos = "".join(f'<li><span class="paso-num" aria-hidden="true">{i}</span><p class="paso-hora">{esc(h)}</p>'
                    f'<h3>{esc(a)}</h3><p>{esc(x)}</p></li>' for i, (h, a, x) in enumerate(t["ruta_pasos"], 1))

    horas = "".join(f'<label class="chip"><input type="radio" name="hora" value="{h}">'
                    + (f'<span>{esc(f["atardecer"])} <b class="hora-atardecer"></b></span>' if h == "atardecer"
                       else f"<span>{h}</span>") + "</label>" for h in HORARIOS)
    extras_form = "".join(f'<label class="extra-check"><input type="checkbox" name="extras" value="{e["id"]}">'
                          f'<span>{esc(e["titulo"])}</span></label>' for e in t["extras"] if e["id"] != "otra")
    hay_pago = bool(PAGOS.get("privada") or PAGOS.get("compartida"))
    boton_pago = (f'<button class="boton boton-principal boton-pagar" type="submit" form="reserva">{ICONO_TARJETA}'
                  f'<span class="pagar-texto">{esc(f["pagar"].format(total="—"))}</span></button>'
                  if hay_pago else
                  f'<button class="boton boton-principal boton-pagar" type="submit" form="reserva" data-modo="whatsapp">'
                  f'{ICONO_WA}<span>{esc(f["whatsapp"])}</span></button>')
    extras_tiles = "".join(f"""
        <li class="extra extra-{e["id"]}">
          <svg class="extra-icono" viewBox="0 0 52 46" aria-hidden="true">{ICONOS_EXTRAS[e["id"]]}</svg>
          <h3>{esc(e["titulo"])}</h3>
          <p>{esc(e["texto"])}</p>
        </li>""" for e in t["extras"])
    galeria_fotos = {"petit-azul": (800, 1600), "petit-proa": (800, 1600), "petit-pantalan": (640, 1024),
                     "petit-cubierta": (800, 1600), "petit-bimini": (800, 1600), "petit-fondeado": (634,)}
    galeria = "".join(
        f'<figure class="foto-carrete">{imagen(n, anchos, t["galeria"][n], prefijo, "", "(max-width: 900px) 80vw, 34vw")}'
        f'<figcaption>{esc(t["galeria"][n])}</figcaption></figure>' for n, anchos in galeria_fotos.items())
    datos_petit = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(c)}</dd></div>" for a, c in t["petit_datos"])
    cerca = [x for x in SENDA_AZUL if x["banus"]]
    sitios_cerca = "".join(ficha_sitio(x, SENDA_AZUL.index(x) + 1, s, lang, mini=True) for x in cerca)
    tambien = "".join(f"""
      <article class="exp" id="exp-{e["id"]}">
        {SIMBOLOS[e["id"]]}
        <h3>{esc(e["titulo"])}</h3>
        <p class="exp-frase">{esc(e["frase"])}</p>
        <ul>{"".join(f"<li>{esc(x)}</li>" for x in e["puntos"])}</ul>
        <a class="exp-enlace" href="{wa(e["wa"])}">{ICONO_WA}{esc(e["cta"])}{FLECHA}</a>
      </article>""" for e in t["tambien"])
    bitacora = "".join(f'<li><time>{a}</time><span>{esc(x)}</span></li>' for a, x in t["bitacora"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"])
    precarga = f'<link rel="preload" as="image" href="{prefijo}assets/fotos/petit-atardecer-1047.webp">\n'

    cuerpo = f"""
<body class="portada">
{simbolo_isobatas()}
{cabecera(t, lang, prefijo)}
<main id="contenido">

<section class="hero" aria-labelledby="titulo">
  {fondo_isobatas()}
  <div class="contenedor hero-rejilla">
    <div class="hero-texto">
      <p class="eyebrow">{banderas_jose("banderas banderas-hero")}{esc(t["hero_eyebrow"])}</p>
      <h1 id="titulo">{t["hero_h1"]}</h1>
      <p class="entradilla">{esc(t["hero_lead"])}</p>
      <ul class="precios">{precios}</ul>
      <div class="botones">
        <a class="boton boton-principal boton-grande" href="#reservar">{esc(t["hero_cta"])}{FLECHA}</a>
        <a class="boton boton-claro" href="{wa(t["wa_hola"])}">{ICONO_WA}{esc(t["hero_cta2"])}</a>
      </div>
    </div>
    <div class="hero-foto">
      {vela_hero(t, prefijo)}
      <figure class="ojo-de-buey">{imagen("petit-delfines", (640, 1136), t["hero_delfines_alt"], prefijo, "", "(max-width: 900px) 46vw, 260px", "eager")}</figure>
      <a class="chip-mar" href="#mar"><span class="chip-punto" aria-hidden="true"></span><span class="chip-texto">{esc(t["hero_chip"])}</span></a>
    </div>
  </div>
</section>

<section class="credenciales" aria-label="{esc(t["jose_eyebrow"])}">
  <ul class="contenedor">{credenciales}</ul>
</section>

<section class="seccion" id="salidas" aria-labelledby="salidas-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["salidas_eyebrow"])}</p>
    <h2 id="salidas-titulo">{esc(t["salidas_h2"])}</h2>
    <p class="intro">{esc(t["salidas_intro"])}</p>
    <div class="salidas">{tarjeta_salida("compartida", "petit-banera", (800, 1600))}{tarjeta_salida("privada", "petit-fondeado", (634,))}
    </div>
  </div>
</section>

<section class="seccion seccion-blanca ruta-seccion" id="ruta" aria-labelledby="ruta-titulo">
  <div class="contenedor ruta">
    <div class="ruta-carta">{svg_carta(t)}</div>
    <div class="ruta-texto">
      <p class="eyebrow">{esc(t["ruta_eyebrow"])}</p>
      <h2 id="ruta-titulo">{esc(t["ruta_h2"])}</h2>
      <ol class="pasos">{pasos}</ol>
      <p class="nota">{esc(t["ruta_nota"])}</p>
    </div>
  </div>
</section>

<section class="seccion reservar" id="reservar" aria-labelledby="reservar-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["reservar_eyebrow"])}</p>
    <h2 id="reservar-titulo">{esc(t["reservar_h2"])}</h2>
    <p class="intro">{esc(t["reservar_intro"])}</p>
    <div class="reservar-rejilla">
      <form id="reserva" class="reserva" novalidate>
        <fieldset class="tipos">
          <legend>{esc(f["tipo"])}</legend>
          <div class="tipos-opciones">
          <label class="tipo"><input type="radio" name="tipo" value="compartida" checked>
            <span><strong>{esc(f["tipos"]["compartida"])}</strong><small>{esc(f["tipos_sub"]["compartida"])}</small></span></label>
          <label class="tipo"><input type="radio" name="tipo" value="privada">
            <span><strong>{esc(f["tipos"]["privada"])}</strong><small>{esc(f["tipos_sub"]["privada"])}</small></span></label>
          </div>
        </fieldset>
        <div class="fila-2">
          <label class="campo">{esc(f["fecha"])}<input type="date" name="fecha" required></label>
          <div class="campo">
            <span id="etiqueta-personas">{esc(f["personas"])}</span>
            <div class="contador" role="group" aria-labelledby="etiqueta-personas">
              <button type="button" class="contador-menos" aria-label="{esc(f["menos"])}">−</button>
              <input type="number" name="personas" value="2" min="1" max="{PLAZAS}" inputmode="numeric" aria-labelledby="etiqueta-personas">
              <button type="button" class="contador-mas" aria-label="{esc(f["mas"])}">+</button>
            </div>
            <small class="nota">{esc(f["max"])}</small>
          </div>
        </div>
        <fieldset class="horas">
          <legend>{esc(f["hora"])}</legend>
          <div class="chips">{horas}</div>
        </fieldset>
        <fieldset class="extras-form" hidden>
          <legend>{esc(f["extras"])}</legend>
          <div class="chips">{extras_form}</div>
          <label class="campo">{esc(f["otra"])}<textarea name="otra" rows="2"></textarea></label>
          <p class="nota">{esc(f["extras_nota"])}</p>
        </fieldset>
        <label class="campo">{esc(f["nombre"])}<input type="text" name="nombre" autocomplete="name" placeholder="{esc(f["nombre_ph"])}"></label>
        <p class="prevision" hidden></p>
        <p class="error" role="alert" hidden></p>
      </form>
      <aside class="billete-zona" aria-labelledby="billete-titulo">
        <div class="billete">
          <div class="billete-cabeza"><p id="billete-titulo">{esc(b["titulo"])}</p>{banderas_jose()}</div>
          <dl class="billete-datos">
            <div><dt>{esc(b["barco"])}</dt><dd>{esc(b["barco_v"])}</dd></div>
            <div><dt>{esc(b["puerto"])}</dt><dd>{esc(b["puerto_v"])}</dd></div>
            <div><dt>{esc(b["tipo"])}</dt><dd data-campo="tipo">{esc(f["tipos"]["compartida"])}</dd></div>
            <div><dt>{esc(b["fecha"])}</dt><dd data-campo="fecha">—</dd></div>
            <div><dt>{esc(b["hora"])}</dt><dd data-campo="hora">—</dd></div>
            <div><dt>{esc(b["pax"])}</dt><dd data-campo="pax">2</dd></div>
            <div class="billete-extras" hidden><dt>{esc(b["extras"])}</dt><dd data-campo="extras">—</dd></div>
            <div><dt>{esc(b["capitan"])}</dt><dd>{esc(b["capitan_v"])}</dd></div>
          </dl>
          <div class="billete-pie">
            <p class="billete-total"><span>{esc(b["total"])}</span><strong data-campo="total">{PRECIO_COMPARTIDA * 2} €</strong></p>
            <p class="billete-detalle" data-campo="detalle">{esc(f["detalle_compartida"].format(n=2))}</p>
          </div>
        </div>
        {boton_pago}
        {"" if hay_pago else f'<p class="nota">{esc(f["sin_pago"])}</p>'}
        {f'<a class="enlace-wa" href="{wa(f["msg_inicio"])}">{ICONO_WA}{esc(f["whatsapp"])}</a>' if hay_pago else ""}
        <p class="nota">{esc(f["politica"])}</p>
        {f'<p class="nota nota-segura">{esc(f["seguro"])}</p>' if hay_pago else ""}
      </aside>
    </div>
  </div>
</section>

<section class="seccion personaliza" id="personaliza" aria-labelledby="pers-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["pers_eyebrow"])}</p>
    <h2 id="pers-titulo">{esc(t["pers_h2"])}</h2>
    <p class="intro">{esc(t["pers_intro"])}</p>
    <ul class="extras">{extras_tiles}
    </ul>
    <div class="botones">
      <a class="boton boton-principal" href="#reservar" data-tipo="privada">{esc(t["pers_cta"])}{FLECHA}</a>
      <p class="nota">{esc(t["pers_nota"])}</p>
    </div>
  </div>
</section>

<section class="seccion seccion-blanca" id="petit" aria-labelledby="petit-titulo">
  <div class="contenedor petit">
    <div class="petit-texto">
      <p class="eyebrow">{esc(t["petit_eyebrow"])}</p>
      <h2 id="petit-titulo">{esc(t["petit_h2"])}</h2>
      <p class="petit-sub">{esc(t["petit_sub"])}</p>
      {"".join(f"<p>{esc(x)}</p>" for x in t["petit_p"])}
      <dl class="petit-datos">{datos_petit}</dl>
    </div>
    <figure class="petit-video">
      <video muted loop playsinline preload="none" poster="{prefijo}assets/video/petit-navegando.webp" aria-label="{esc(t["video_alt"])}">
        <source src="{prefijo}assets/video/petit-navegando.mp4" type="video/mp4">
      </video>
      <button class="video-boton" type="button" aria-pressed="false" data-play="{esc(t["video_play"])}" data-pausa="{esc(t["video_pausa"])}">
        <span class="visualmente-oculto">{esc(t["video_play"])}</span>
      </button>
    </figure>
  </div>
  <div class="carrete" tabindex="0" aria-label="{esc(t["petit_h2"])}">{galeria}</div>
</section>
{seccion_mar(t)}
<section class="seccion buceo" id="buceo" aria-labelledby="buceo-titulo">
  <div class="contenedor">
    <p class="eyebrow">{SIMBOLOS["buceo"]}{esc(t["buceo_eyebrow"])}</p>
    <h2 id="buceo-titulo">{esc(t["buceo_h2"])}</h2>
    <p class="intro">{esc(t["buceo_lead"])}</p>
    <div class="sitios sitios-mini">{sitios_cerca}
    </div>
    <div class="botones">
      <a class="boton boton-principal" href="buceo.html">{esc(t["buceo_cta"])}{FLECHA}</a>
      <a class="boton boton-claro" href="{wa(t["buceo_wa"])}">{ICONO_WA}{esc(t["buceo_wa_cta"])}</a>
    </div>
  </div>
</section>

<section class="seccion seccion-blanca" id="jose" aria-labelledby="jose-titulo">
  <div class="contenedor jose">
    <figure class="jose-fotos">
      {imagen("jose-buceo", (520, 1040), t["jose_foto"], prefijo, "jose-foto", "(max-width: 900px) 100vw, 40vw")}
      {imagen("jose-lancha", (520, 1040), "", prefijo, "jose-foto-2", "(max-width: 900px) 50vw, 18vw")}
    </figure>
    <div class="jose-texto">
      <p class="eyebrow">{esc(t["jose_eyebrow"])}</p>
      <h2 id="jose-titulo">{esc(t["jose_h2"])}</h2>
      {"".join(f"<p>{esc(x)}</p>" for x in t["jose_p"])}
      <div class="bitacora">
        <h3>{esc(t["cuaderno"])}</h3>
        <ol>{bitacora}</ol>
      </div>
    </div>
  </div>
</section>

<section class="seccion" id="tambien" aria-labelledby="tambien-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["tambien_eyebrow"])}</p>
    <h2 id="tambien-titulo">{esc(t["tambien_h2"])}</h2>
    <div class="experiencias">{tambien}
    </div>
  </div>
</section>

<section class="seccion seccion-blanca" id="faq" aria-labelledby="faq-titulo">
  <div class="contenedor faq">
    <h2 id="faq-titulo">{esc(t["faq_h2"])}</h2>
    <div>{faq}</div>
  </div>
</section>

<section class="seccion final" aria-labelledby="final-titulo">
  {fondo_isobatas()}
  <div class="contenedor">
    <h2 id="final-titulo">{esc(t["final_h2"])}</h2>
    <p class="intro">{esc(t["final_p"])}</p>
    <div class="botones botones-centro">
      <a class="boton boton-principal boton-grande" href="#reservar">{esc(t["hero_cta"])}{FLECHA}</a>
      <a class="boton boton-claro" href="{wa(t["wa_hola"])}">{ICONO_WA}WhatsApp {WHATSAPP_VISIBLE}</a>
      <a class="boton boton-claro" href="https://www.instagram.com/{INSTAGRAM}/">{ICONO_IG}@{INSTAGRAM}</a>
    </div>
  </div>
</section>

</main>
{pie(t, lang, prefijo)}
{datos_pagina(datos_js)}
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
"""
    return cabeza(t, lang, prefijo, t["title"], t["description"], "", precarga + json_ld(t, lang)) + cuerpo


# ─────────────────────────────── el mar, ahora ───────────────────────────────
# Lo que solo se pinta en el HTML; el resto de t["mar"] va al JS, que rellena las notas con datos/mar.json
SOLO_HTML = ("eyebrow", "h2", "intro", "camaras_h", "en_directo", "ver", "camaras_nota", "camaras", "notas_h",
             "dias_aria", "como_h", "como", "aviso_legal", "cargando")


def seccion_mar(t):
    m = t["mar"]

    def camara(c, embed):
        if embed:          # cámara autorizada: se ve aquí mismo
            return f"""
      <li class="camara camara-directo-aqui">
        <iframe src="{esc(embed)}" title="{esc(c["nombre"])}" loading="lazy" allow="fullscreen"></iframe>
        <a class="camara-pie" href="{esc(c["url"])}" target="_blank" rel="noopener">{esc(c["nombre"])} · {esc(c["fuente"])} ↗</a>
      </li>"""
        return f"""
      <li><a class="camara" href="{esc(c["url"])}" target="_blank" rel="noopener">
        <span class="camara-directo"><span class="camara-punto" aria-hidden="true"></span>{esc(m["en_directo"])}</span>
        <span class="camara-nombre">{esc(c["nombre"])}</span>
        <span class="camara-que">{esc(c["que"])}</span>
        <span class="camara-fuente">{esc(m["ver"])} · {esc(c["fuente"])} <span aria-hidden="true">↗</span></span>
      </a></li>"""

    camaras = "".join(camara(c, e) for c, e in zip(m["camaras"], CAMARAS_EMBED))
    indices = "".join(f"""
        <article class="indice" data-act="{a}">
          <h4 class="indice-cabeza">{SIMBOLOS[s]}<span>{esc(m["actividades"][a])}</span></h4>
          <p class="indice-cifra"><span class="indice-n">–</span><span class="indice-de">/10</span></p>
          <p class="indice-banda"></p>
          <div class="indice-escala" aria-hidden="true">{"<i></i>" * 10}</div>
          <p class="indice-frase"></p>
          <ul class="indice-tramos"></ul>
        </article>""" for a, s in (("navegar", "vela"), ("bucear", "buceo"), ("pescar", "pesca")))
    como = "".join(f"<li><strong>{esc(a)}:</strong> {esc(b)}</li>" for a, b in m["como"])
    return f"""
<section class="seccion mar" id="mar" aria-labelledby="mar-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(m["eyebrow"])}</p>
    <h2 id="mar-titulo">{esc(m["h2"])}</h2>
    <p class="intro">{esc(m["intro"])}</p>

    <h3 class="mar-sub">{esc(m["camaras_h"])}</h3>
    <ul class="camaras">{camaras}
    </ul>
    <p class="nota mar-nota">{esc(m["camaras_nota"])}</p>

    <div class="notas">
      <div class="notas-cabeza">
        <h3 class="mar-sub">{esc(m["notas_h"])}</h3>
        <div class="dias" role="group" aria-label="{esc(m["dias_aria"])}"></div>
      </div>
      <p class="notas-estado">{esc(m["cargando"])}</p>
      <div class="aviso-mar" role="alert" hidden></div>
      <div class="indices" hidden>{indices}
      </div>
      <div class="notas-detalle" hidden>
        <table class="bitacora-mar"></table>
        <div class="costera" hidden></div>
      </div>
      <details class="notas-como">
        <summary>{esc(m["como_h"])}</summary>
        <ul>{como}</ul>
      </details>
      <p class="nota notas-legal">{esc(m["aviso_legal"])}</p>
      <p class="nota notas-fuente"></p>
    </div>
  </div>
</section>
"""


# ─────────────────────────────── buceo: la Senda Azul ───────────────────────────────
def linea_senda(s):
    """La Senda Azul como una línea de costa esquemática, de oeste a este, con Puerto Banús marcado."""
    paradas, anterior = [], None
    for n, x in enumerate(SENDA_AZUL, 1):
        municipio = x["lugar"].split(" · ")[0]
        rotulo = municipio if municipio != anterior else ""
        anterior = municipio
        paradas.append(f'<li><a class="parada parada-{x["nivel"][0]}" href="#sitio-{x["id"]}" title="{esc(x["nombre"])}">'
                       f'<span aria-hidden="true">{n}</span><span class="visualmente-oculto">{esc(x["nombre"])}</span></a>'
                       f'<span class="parada-lugar" aria-hidden="true">{esc(rotulo)}</span></li>')
        if x["id"] == "botones":
            paradas.append('<li class="parada-banus-li"><span class="parada parada-banus" aria-hidden="true">'
                           '<svg viewBox="-13 -16 26 24"><path d="M0-15V0H-9Z M2-11 9 0H2Z M-12 3H12L8 7H-8Z"/></svg>'
                           f'</span><span class="parada-lugar">{esc(s["salida"])}</span></li>')
    return f'<ol class="linea" aria-label="{esc(s["linea_aria"])}">{"".join(paradas)}</ol>'


def pagina_buceo(lang):
    t = T[lang]
    prefijo = prefijo_de(lang)
    s = t["senda"]
    filtros = "".join(f'<button type="button" class="filtro" data-filtro="{k}" aria-pressed="{str(k == "todos").lower()}">'
                      f'{esc(v)}</button>' for k, v in s["filtros"].items())
    leyenda = "".join(f'<span class="nivel nivel-{k}">{esc(v)}</span>' for k, v in s["niveles"].items())
    fichas = "".join(ficha_sitio(x, n, s, lang) for n, x in enumerate(SENDA_AZUL, 1))
    bloques = "".join(f'<div class="buceo-bloque"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in t["buceo_bloques"])
    pecio_datos = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in t["pecio_datos"])
    fb = t["fotos_buceo"]
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "pagina": "buceo"}
    cuerpo = f"""
<body class="pagina-buceo">
{cabecera(t, lang, prefijo, "buceo.html")}
<main id="contenido">
<section class="seccion buceo buceo-cabeza" aria-labelledby="senda-titulo">
  <div class="contenedor">
    <p class="eyebrow">{SIMBOLOS["buceo"]}{esc(s["eyebrow"])}</p>
    <h1 id="senda-titulo">{esc(s["h1"])}</h1>
    <p class="intro">{esc(s["lead"])}</p>
    {linea_senda(s)}
    <p class="leyenda">{leyenda}</p>
  </div>
</section>

<section class="seccion senda" aria-label="{esc(s["h1"])}">
  <div class="contenedor">
    <div class="filtros" role="group" aria-label="{esc(s["campos"]["nivel"])}">{filtros}</div>
    <div class="sitios">{fichas}
    </div>
    <p class="senda-vacio" hidden>{esc(s["vacio"])}</p>
    <p class="nota">{esc(s["aviso"])}</p>
    <p class="nota">{esc(s["fuente"])}</p>
  </div>
</section>

<section class="seccion buceo" aria-labelledby="pecio-titulo">
  <div class="contenedor">
    <article class="pecio">
      <p class="sonda-grande" aria-hidden="true">−8<span> m</span></p>
      <div>
        <p class="eyebrow">{esc(t["pecio_eyebrow"])}</p>
        <h2 id="pecio-titulo">{t["pecio_h"]}</h2>
        {"".join(f"<p>{x}</p>" for x in t["pecio_p"])}
        <dl class="pecio-datos">{pecio_datos}</dl>
      </div>
    </article>
    <div class="buceo-rejilla">
      {bloques}
      <figure class="buceo-foto">{imagen("senal-ok", (640, 1150), fb["ok"], prefijo, "", "(max-width: 900px) 100vw, 50vw")}</figure>
      <figure class="buceo-foto">{imagen("pulpo", (640, 1170), fb["pulpo"], prefijo, "", "(max-width: 900px) 100vw, 50vw")}</figure>
    </div>
    <div class="buceo-mas">
      <div>
        <h3>{esc(t["habichuelas_h"])}</h3>
        <p>{t["habichuelas_p"]}</p>
        <h3>{esc(t["viajes_h"])}</h3>
        <p>{esc(t["viajes_p"])}</p>
        <a class="boton boton-principal" href="{wa(t["buceo_wa"])}">{ICONO_WA}{esc(t["buceo_wa_cta"])}</a>
      </div>
      <figure class="buceo-foto">{imagen("tortuga", (520, 1040), fb["tortuga"], prefijo, "", "(max-width: 900px) 50vw, 22vw")}</figure>
      <figure class="buceo-foto">{imagen("tiburon", (520, 1040), fb["tiburon"], prefijo, "", "(max-width: 900px) 50vw, 22vw")}</figure>
    </div>
  </div>
</section>
</main>
{pie(t, lang, prefijo, "buceo.html")}
{datos_pagina(datos_js)}
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
"""
    return cabeza(t, lang, prefijo, t["buceo_title"], t["buceo_description"], "buceo.html") + cuerpo


# ─────────────────────────────── páginas sencillas ───────────────────────────────
def pagina_simple(lang, titulo, h1, contenido, ruta, datos=None, indexable=False, prefijo=None):
    t = T[lang]
    prefijo = prefijo_de(lang) if prefijo is None else prefijo
    datos = datos or {}
    datos.update({"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP})
    return (cabeza(t, lang, prefijo, titulo, t["description"], ruta,
                   "" if indexable else '<meta name="robots" content="noindex">\n')
            + f"""
<body>
{cabecera(t, lang, prefijo, ruta)}
<main id="contenido" class="seccion">
  <article class="contenedor texto-legal">
    <h1>{esc(h1)}</h1>
    {contenido}
    <p><a class="boton boton-secundario" href="{prefijo}{carpeta(lang)}">{esc(t["volver"])}</a></p>
  </article>
</main>
{pie(t, lang, prefijo, ruta)}
{datos_pagina(datos)}
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
""")


def legal(lang):
    t = T[lang]
    contenido = "".join(
        f"<h2>{esc(a)}</h2><p>{esc(b).format(email=EMAIL, tel=WHATSAPP_VISIBLE)}</p>" for a, b in t["legal"])
    return pagina_simple(lang, t["legal_title"], t["legal_h1"], contenido, "legal.html")


def gracias(lang):
    t = T[lang]
    g, b = t["gracias"], t["billete"]
    contenido = f"""
    <p class="intro">{esc(g["p"])}</p>
    <div class="gracias-billete" hidden>
      <h2>{esc(g["resumen"])}</h2>
      <dl class="billete-datos"></dl>
    </div>
    <p class="gracias-sin" hidden>{esc(g["sin"])}</p>
    <p><a class="boton boton-principal" href="{wa(t["form"]["msg_pagado"])}" data-wa-gracias>{ICONO_WA}{esc(g["wa"])}</a></p>"""
    datos = {"pagina": "gracias", "billete": b, "form": t["form"],
             "extras": {e["id"]: e["titulo"] for e in t["extras"]}}
    return pagina_simple(lang, g["title"], g["h1"], contenido, "gracias.html", datos)


def escribir(ruta, texto):
    ruta = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def main():
    for lang in IDIOMAS:
        escribir(f"{carpeta(lang)}index.html", portada(lang))
        escribir(f"{carpeta(lang)}buceo.html", pagina_buceo(lang))
        escribir(f"{carpeta(lang)}legal.html", legal(lang))
        escribir(f"{carpeta(lang)}gracias.html", gracias(lang))
    t = T[IDIOMAS[0]]
    # El 404 se sirve en cualquier dirección: sus enlaces van desde la raíz del dominio
    escribir("404.html", pagina_simple(IDIOMAS[0], t["e404_h1"] + " — Sea With Jose", t["e404_h1"],
                                       f'<p>{esc(t["e404_p"])}</p>', "404.html", prefijo="/"))
    hoy = datetime.date.today().isoformat()
    urls = []
    for ruta in ("", "buceo.html"):
        for lang in IDIOMAS:
            alternas = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{DOMINIO}/{carpeta(l)}{ruta}"/>'
                               for l in IDIOMAS)
            urls.append(f"<url><loc>{DOMINIO}/{carpeta(lang)}{ruta}</loc><lastmod>{hoy}</lastmod>{alternas}</url>")
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("Web generada:", ", ".join(f"/{carpeta(l)}" for l in IDIOMAS), "· portada, buceo, legal, gracias")


if __name__ == "__main__":
    main()
