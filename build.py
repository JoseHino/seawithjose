# -*- coding: utf-8 -*-
"""Genera la web de Sea With Jose en inglés (raíz), español (/es/) y ruso (/ru/).

    python build.py

Lee textos.py, fuentes/carta.json (isobatas de EMODnet, ver scripts/carta.py)
y fuentes/mapa_banus.json (plano de OpenStreetMap, ver scripts/mapa.py), y
escribe la portada, la página de buceo (la Senda Azul), la de «reserva
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
                    PARKING_MAPS, SENDA_AZUL, RESENAS, REVISTA_FORMS, BARCO, BARCO_MAPS)
CARTA = json.load(open(os.path.join(RAIZ, "fuentes", "carta.json"), encoding="utf-8"))
MAPA = json.load(open(os.path.join(RAIZ, "fuentes", "mapa_banus.json"), encoding="utf-8"))
VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")   # rompe la caché del CSS y el JS


def esc(s):
    return html.escape(str(s), quote=True)


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(texto)}"


def carpeta(lang):
    return "" if lang == IDIOMAS[0] else f"{lang}/"


def prefijo_de(lang):
    return "" if lang == IDIOMAS[0] else "../"


# ─────────────────────────────── banderas del Código Internacional de Señales ───────────────────────────────
AZUL, ROJO, AMARILLO, NEGRO = "#1F4E9A", "#D2232A", "#F5C400", "#141414"
BANDERAS = {   # en un lienzo de 30 × 20
    "A": f'<rect width="15" height="20" fill="#fff"/><path d="M15 0H30L23 10 30 20H15Z" fill="{AZUL}"/>',
    "E": f'<rect width="30" height="10" fill="{AZUL}"/><rect y="10" width="30" height="10" fill="{ROJO}"/>',
    "H": f'<rect width="15" height="20" fill="#fff"/><rect x="15" width="15" height="20" fill="{ROJO}"/>',
    "I": f'<rect width="30" height="20" fill="{AMARILLO}"/><circle cx="15" cy="10" r="5.2" fill="{NEGRO}"/>',
    "J": f'<rect width="30" height="20" fill="{AZUL}"/><rect y="6.67" width="30" height="6.67" fill="#fff"/>',
    "O": f'<path d="M0 0H30V20Z" fill="{ROJO}"/><path d="M0 0V20H30Z" fill="{AMARILLO}"/>',
    "S": f'<rect width="30" height="20" fill="#fff"/><rect x="10" y="5" width="10" height="10" fill="{AZUL}"/>',
    "T": f'<rect width="10" height="20" fill="{ROJO}"/><rect x="10" width="10" height="20" fill="#fff"/>'
         f'<rect x="20" width="10" height="20" fill="{AZUL}"/>',
    "W": f'<rect width="30" height="20" fill="{AZUL}"/><rect x="3.5" y="3.5" width="23" height="13" fill="#fff"/>'
         f'<rect x="7.5" y="7" width="15" height="6" fill="{ROJO}"/>',
}


def bandera(letra, ancho=30):
    return (f'<svg viewBox="0 0 30 20" width="{ancho}" height="{ancho * 2 // 3}" aria-hidden="true">{BANDERAS[letra]}'
            f'<rect x=".5" y=".5" width="29" height="19" fill="none" stroke="#000" stroke-opacity=".18"/></svg>')


def banderas_jose():
    return '<span class="banderas" aria-hidden="true">' + "".join(bandera(l, 18) for l in "JOSE") + "</span>"


# Iconos de la personalización y de la pesca, con trazo
ICONO_WA = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 '
            '15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1'
            'c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9'
            'c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4 5.2 5.2 0 0 0 3.2.7'
            ' 2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3Z"/></svg>')
ICONO_IG = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" '
            'fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.2" fill="none" '
            'stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>')
ICONO_TARJETA = ('<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" '
                 'rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M2.5 9.5h19M6 15h4" '
                 'stroke="currentColor" stroke-width="1.8"/></svg>')
FLECHA = '<span class="flecha" aria-hidden="true">→</span>'
# Bandera A del Código: «tengo un buzo sumergido»
BANDERA_ALFA = ('<svg class="alfa" viewBox="0 0 52 36" aria-hidden="true">'
                '<rect x="1" y="1" width="24" height="34" fill="#fff" stroke="#10263A" stroke-width="1.4"/>'
                f'<path d="M25 1H51L38 18 51 35H25Z" fill="{AZUL}" stroke="#10263A" stroke-width="1.4" '
                'stroke-linejoin="round"/></svg>')
SIMBOLO_VELA = ('<svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true"><path d="M25 4V31H9Z"/>'
                '<path d="M28 9 40 31H28Z"/><path d="M5 35H47L41 41H11Z"/></svg>')
SIMBOLO_PESCA = ('<svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true">'
                 '<path d="M6 22C14 11 31 10 39 22 31 34 14 33 6 22Z"/><path d="M39 22 48 14V30Z"/>'
                 '<circle cx="15" cy="20" r="1.6" fill="currentColor" stroke="none"/></svg>')


# ─────────────────────────────── la carta náutica ───────────────────────────────
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


# La ruta habitual de la salida: Banús → velas arriba → fondeo frente a San Pedro → mar abierto → vuelta
# Dos vueltas desde Banús: hacia poniente o hacia levante según el viento; el baño, en la parte más alejada de tierra
BANUS = (-4.9530, 36.4846)
VUELTAS = [[(-4.9590, 36.4720), (-4.9680, 36.4600), (-4.9790, 36.4560), (-4.9850, 36.4630), (-4.9780, 36.4730)],
           [(-4.9470, 36.4720), (-4.9380, 36.4600), (-4.9260, 36.4560), (-4.9190, 36.4650), (-4.9270, 36.4750)]]
BANOS = [(-4.9790, 36.4560), (-4.9260, 36.4560)]


def curva(puntos):
    """Catmull-Rom a Bézier: una ruta suave que pasa por todos los puntos."""
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
    ax, ay = W * 0.70, H - 26
    origen = proyectar(*BANUS)
    vueltas = [[origen] + [proyectar(*p) for p in v] + [origen] for v in VUELTAS]
    banos = [proyectar(*p) for p in BANOS]
    rx, ry = origen[0], banos[0][1] + 92          # «según el viento», entre las dos vueltas
    # Cajas que ocupan los rótulos y la ruta: ahí no se pintan sondas
    cajas = [(bx - 16, by - 24, bx + 26 + len(c["banus"]) * 13, by + 40),
             (ax - len(c["alboran"]) * 11, ay - 30, ax + len(c["alboran"]) * 11, ay + 12),
             (rx - len(c["ruta"]) * 7, ry - 30, rx + len(c["ruta"]) * 7, ry + 10)]
    cajas += [(x - 26, y - 26, x + 26, y + 26) for v in vueltas for x, y in v]
    cajas += [(x - 40, y - 26, x + 40, y + 60) for x, y in banos]
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
               f'<g class="simbolo-puerto" transform="translate({bx} {by})"><path d="M0-15V0H-9Z M2-11 9 0H2Z M-12 3H12L8 7H-8Z"/></g>'
               f'<text class="rotulo-puerto" x="{bx + 18}" y="{by - 2}">{esc(c["banus"])}</text>'
               f'<text class="rotulo-mar" x="{ax:.0f}" y="{ay:.0f}" text-anchor="middle">{esc(c["alboran"])}</text>'
               "</g>")
    trazos = "".join(f'<path class="ruta-estela" d="{curva(v)}"/><path class="ruta-linea" pathLength="1" d="{curva(v)}"/>'
                     for v in vueltas)
    # El baño: un círculo con dos olas
    banos_svg = "".join(f'<g class="ruta-punto ruta-bano" transform="translate({x:.0f} {y:.0f})"><circle r="19"/>'
                        '<path d="M-10-3q2.5-4 5 0t5 0 5 0 5 0M-10 5q2.5-4 5 0t5 0 5 0 5 0"/>'
                        f'<text y="50" text-anchor="middle">{esc(c["bano"])}</text></g>' for x, y in banos)
    out.append(f'<g class="derrota">{trazos}{banos_svg}'
               f'<text class="ruta-rotulo" x="{rx:.0f}" y="{ry:.0f}" text-anchor="middle">{esc(c["ruta"])}</text></g>')
    out.append("</g>")                      # fin del recorte
    out.append(borde_graduado(W, H, B, c))
    out.append("</svg>")
    return "".join(out)


# ─────────────────────────────── el plano del parking ───────────────────────────────
# Encuadre del plano (en coordenadas del lienzo de scripts/mapa.py) y el camino andando del parking al puerto
VISTA_MAPA = (250, 40, 590, 600)
# A pie del parking Cristamar al Petit (ruta de OSM, 720 m), en coordenadas del plano
CAMINO = [(556, 190), (567, 193), (555, 209), (579, 238), (594, 250), (645, 308), (542, 455), (520, 490)]
EMBARQUE = (516, 487)


def svg_mapa(t):
    m, a = MAPA, t["mapa"]
    x0, y0, w, h = VISTA_MAPA
    px, py = m["parking"]
    diques = "".join(f'<path class="{"muelle" if tipo == "Polygon" else "pantalan"}" d="{d}"/>'
                     for d, tipo in zip(m["diques"], m["diques_tipo"]))
    calles = "".join(f'<path class="calle calle-{clase}" d="{d}"/>' for clase, d in m["calles"].items())
    camino = "M" + " L".join(f"{x},{y}" for x, y in CAMINO)
    ex, ey = EMBARQUE
    return f"""<svg class="mapa" viewBox="{x0} {y0} {w} {h}" role="img" aria-label="{esc(a["aria"])}">
      <rect class="mapa-tierra" x="{x0}" y="{y0}" width="{w}" height="{h}"/>
      <path class="mapa-mar" d="{m["mar"]}"/>
      <path class="mapa-edificios" d="{m["edificios"]}"/>
      {calles}{diques}
      <path class="mapa-camino" d="{camino}"/>
      <text class="mapa-minutos" x="{CAMINO[5][0] + 14}" y="{CAMINO[5][1] + 6}">{esc(a["minutos"])}</text>
      <g class="mapa-parking" transform="translate({px:.0f} {py:.0f})"><rect x="-15" y="-15" width="30" height="30" rx="3"/>
        <text y="8" text-anchor="middle">P</text></g>
      <text class="mapa-rotulo" x="{px + 22:.0f}" y="{py - 6:.0f}">{esc(a["parking"])}</text>
      <g class="mapa-barco" transform="translate({ex} {ey})"><circle r="16"/>
        <path d="M-1-10V3H-8Z M1-7 7 3H1Z M-10 5H10L7 9H-7Z"/></g>
      <text class="mapa-puerto" x="{ex - 60}" y="{ey + 150}" text-anchor="middle">{esc(a["puerto"])}</text>
    </svg>"""


def imagen(nombre, anchos, alt, prefijo, clase="", sizes="(max-width: 900px) 100vw, 50vw", carga="lazy"):
    srcset = ", ".join(f"{prefijo}assets/fotos/{nombre}-{a}.webp {a}w" for a in anchos)
    clase_attr = f' class="{clase}"' if clase else ""
    return (f'<img{clase_attr} src="{prefijo}assets/fotos/{nombre}-{anchos[0]}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" alt="{esc(alt)}" loading="{carga}" decoding="async">')


# ─────────────────────────────── piezas comunes ───────────────────────────────
def cabeza(t, lang, prefijo, titulo, descripcion, ruta, extra=""):
    alternas = "".join(
        f'<link rel="alternate" hreflang="{l}" href="{DOMINIO}/{carpeta(l)}{ruta}">' for l in IDIOMAS)
    alternas += f'<link rel="alternate" hreflang="x-default" href="{DOMINIO}/{ruta}">'
    sub = "cyrillic" if lang == "ru" else "latin"
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
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{prefijo}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefijo}assets/icono-180.png">
<link rel="preload" href="{prefijo}assets/fuentes/sofia-sans-extra-condensed-normal-700-900-{sub}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefijo}assets/fuentes/sofia-sans-normal-400-800-{sub}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefijo}assets/fuentes.css?v={VERSION}">
<link rel="stylesheet" href="{prefijo}assets/estilo.css?v={VERSION}">
{extra}</head>"""


def cabecera(t, lang, prefijo, pagina="index.html"):
    """En la portada, los enlaces son anclas; en el resto de páginas apuntan a la portada (salvo Buceo)."""
    portada = f"{prefijo}{carpeta(lang)}" or "./"     # en inglés (raíz) quedaría vacío y apuntaría a la propia página
    inicio = "" if pagina == "index.html" else portada
    destino = {k: f"{inicio}#{k}" for k in t["nav"]}
    destino["revista"] = f"{prefijo}{carpeta(lang)}revista.html"
    actual = {"revista.html": "revista"}.get(pagina)
    enlaces = "".join(f'<li><a href="{destino[k]}"' + (' aria-current="page"' if k == actual else "")
                      + f'>{esc(v)}</a></li>' for k, v in t["nav"].items())
    ruta = "" if pagina in ("index.html", "404.html") else pagina
    idiomas = "".join(
        (f'<a href="{prefijo}{carpeta(l)}{ruta}" lang="{l}" hreflang="{l}"'
         + (' aria-current="true"' if l == lang else "") + f' title="{esc(T[l]["nombre_idioma"])}">{T[l]["corto"]}</a>')
        for l in IDIOMAS)
    return f"""<a class="saltar" href="#contenido">{esc(t["saltar"])}</a>
<header class="cabecera">
  <div class="contenedor cabecera-fila">
    <a class="marca" href="{portada}"><span>Sea With Jose</span></a>
    <button class="menu-boton" type="button" aria-expanded="false" aria-controls="navegacion">
      <span class="menu-raya" aria-hidden="true"></span><span class="visualmente-oculto">{esc(t["menu"])}</span>
    </button>
    <nav id="navegacion" class="navegacion" aria-label="{esc(t["menu"])}">
      <ul>{enlaces}</ul>
      <div class="idiomas">{idiomas}</div>
      <a class="boton boton-amarillo boton-pequeno" href="{inicio}#reservar">{esc(t["reservar_corto"])}</a>
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
        "geo": {"@type": "GeoCoordinates", "latitude": BARCO[0], "longitude": BARCO[1]},
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


def ficha_sitio(sitio, n, s, lang, mini=False):
    acceso = " · ".join(s["accesos"][a] for a in sitio["acceso"])
    cerca = f'<span class="cerca">{esc(s["cerca"])}</span>' if sitio["banus"] else ""
    niveles = "".join(f'<span class="nivel nivel-{x}">{esc(s["niveles"][x])}</span>' for x in sitio["nivel"])
    datos = (f'<dl class="sitio-datos"><div><dt>{esc(s["campos"]["acceso"])}</dt><dd>{esc(acceso)}</dd></div>'
             f'<div><dt>{esc(s["campos"]["vis"])}</dt><dd>{esc(s["visibilidades"][sitio["vis"]])}</dd></div></dl>')
    enlace = (f'<a class="sitio-enlace" href="{wa(s["msg"].format(sitio=sitio["nombre"]))}">{ICONO_WA}'
              f'{esc(s["quiero"])}</a>')
    return f"""
      <article class="sitio" id="sitio-{sitio["id"]}" data-nivel="{" ".join(sitio["nivel"])}" data-banus="{str(sitio["banus"]).lower()}">
        <p class="sitio-num">{n:02d} · {esc(sitio["lugar"])}{cerca}</p>
        <h3>{esc(sitio["nombre"])}</h3>
        <p class="sitio-prof"><span>{esc(sitio["prof"])}</span> m</p>
        <p class="sitio-niveles">{niveles}</p>
        <p class="sitio-que">{esc(sitio["que"][lang])}</p>
        {"" if mini else datos}
        {"" if mini else enlace}
      </article>"""


# ─────────────────────────────── el mar, ahora ───────────────────────────────
# Lo que solo se pinta en el HTML; el resto de t["mar"] va al JS, que rellena las notas con datos/mar.json
SOLO_HTML = ("eyebrow", "h2", "intro", "camaras_h", "en_directo", "ver", "camaras_nota", "camaras", "notas_h",
             "dias_aria", "como_h", "como", "aviso_legal", "cargando")


def seccion_mar(t):
    m = t["mar"]

    def camara(c, embed):
        if embed:          # cámara autorizada: se ve aquí mismo
            return f"""
      <li class="camara-aqui">
        <iframe src="{esc(embed)}" title="{esc(c["nombre"])}" loading="lazy" allow="fullscreen"></iframe>
        <a href="{esc(c["url"])}" target="_blank" rel="noopener">{esc(c["nombre"])} · {esc(c["fuente"])} ↗</a>
      </li>"""
        return f"""
      <li><a class="camara" href="{esc(c["url"])}" target="_blank" rel="noopener">
        <span class="camara-directo"><span class="camara-punto" aria-hidden="true"></span>{esc(m["en_directo"])}</span>
        <span class="camara-nombre">{esc(c["nombre"])}</span>
        <span class="camara-que">{esc(c["que"])}</span>
        <span class="camara-fuente">{esc(m["ver"])} · {esc(c["fuente"])} <span aria-hidden="true">↗</span></span>
      </a></li>"""

    camaras = "".join(camara(c, e) for c, e in zip(m["camaras"], CAMARAS_EMBED))
    simbolos = {"navegar": SIMBOLO_VELA, "bucear": BANDERA_ALFA, "pescar": SIMBOLO_PESCA}
    indices = "".join(f"""
        <article class="indice" data-act="{a}">
          <h4 class="indice-cabeza">{simbolos[a]}<span>{esc(m["actividades"][a])}</span></h4>
          <p class="indice-cifra"><span class="indice-n">–</span><span class="indice-de">/10</span></p>
          <p class="indice-banda"></p>
          <div class="indice-escala" aria-hidden="true">{"<i></i>" * 10}</div>
          <p class="indice-frase"></p>
          <ul class="indice-tramos"></ul>
        </article>""" for a in ("navegar", "bucear", "pescar"))
    como = "".join(f"<li><strong>{esc(a)}:</strong> {esc(b)}</li>" for a, b in m["como"])
    return f"""
<section class="seccion mar" id="mar" aria-labelledby="mar-titulo">
  <div class="contenedor">
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


# ─────────────────────────────── portada ───────────────────────────────
def portada(lang):
    t = T[lang]
    prefijo = prefijo_de(lang)
    f, r, s = t["form"], t["resumen"], t["senda"]
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "pagina": "portada",
                "precios": {"compartida": PRECIO_COMPARTIDA, "privada": PRECIO_PRIVADA}, "plazas": PLAZAS,
                "dias": DIAS_RESERVA, "pagos": PAGOS, "form": f, "resumen": r,
                "extras": {e["id"]: e["titulo"] for e in t["extras"]},
                "mar": {k: v for k, v in t["mar"].items() if k not in SOLO_HTML}}

    hero_precios = "".join(f'<div><dt>{esc(a)}</dt><dd><b>{esc(p)}</b> {esc(u)}</dd></div>'
                           for a, p, u in t["hero_precios"])

    def panel(tipo):
        o = t["opciones"][tipo]
        return f"""
      <article class="panel panel-{tipo}">
        <h3>{esc(o["titulo"])}</h3>
        <p class="panel-precio">{esc(o["precio"])}</p>
        <p class="panel-unidad">{esc(o["unidad"])}</p>
        <p class="panel-incluye-titulo">{esc(t["incluye_titulo"])}</p>
        <ul class="panel-incluye">{"".join(f"<li>{esc(x)}</li>" for x in o["incluye"])}</ul>
        <a class="panel-parking" href="#llegar"><span class="letra-p" aria-hidden="true">P</span>{esc(o["parking"])}</a>
        <ul class="panel-letra">{"".join(f"<li>{esc(x)}</li>" for x in o["letra"])}</ul>
        <a class="boton {"boton-azul" if tipo == "privada" else "boton-amarillo"}" href="#reservar" data-tipo="{tipo}">{esc(o["cta"])}{FLECHA}</a>
      </article>"""

    tira = "".join(f'<figure>{imagen(n, anchos, t["fotos_alt"][n], prefijo, "", "(max-width: 700px) 100vw, 34vw")}</figure>'
                   for n, anchos in (("petit-delfines", (640, 1136)), ("petit-banera", (800, 1600)),
                                     ("petit-proa", (800, 1600))))
    horas = "".join(f'<label class="chip"><input type="radio" name="hora" value="{h}">'
                    + (f'<span>{esc(f["atardecer"])} <b class="hora-atardecer"></b></span>' if h == "atardecer"
                       else f"<span>{h}</span>") + "</label>" for h in HORARIOS)
    extras_form = "".join(f'<label class="chip"><input type="checkbox" name="extras" value="{e["id"]}">'
                          f'<span>{esc(e["titulo"])}</span></label>' for e in t["extras"] if e["id"] != "otra")
    hay_pago = bool(PAGOS.get("privada") or PAGOS.get("compartida"))
    boton_pago = (f'<button class="boton boton-azul boton-pagar" type="submit" form="reserva">{ICONO_TARJETA}'
                  f'<span class="pagar-texto">{esc(f["pagar"].format(total="—"))}</span></button>'
                  if hay_pago else
                  f'<button class="boton boton-azul boton-pagar" type="submit" form="reserva">{ICONO_WA}'
                  f'<span>{esc(f["whatsapp"])}</span></button>')
    carta_extras = "".join(f"""
        <li><p class="extra-linea"><span class="extra-nombre">{esc(e["titulo"])}</span><span class="extra-puntos" aria-hidden="true"></span><span class="extra-precio">{esc(t["extras_precio"])}</span></p>
          <p class="extra-texto">{esc(e["texto"])}</p></li>""" for e in t["extras"])
    mosaico = "".join(f'<figure class="m{i}">{imagen(n, anchos, t["galeria"][n], prefijo, "", "(max-width: 700px) 100vw, 40vw")}</figure>'
                      for i, (n, anchos) in enumerate((("petit-azul", (800, 1600)), ("petit-concha", (600, 1200)),
                                                        ("petit-ocaso", (800, 1200)), ("petit-pantalan", (640, 1024)),
                                                        ("petit-torre", (800, 1200)))))
    datos_barco = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(c)}</dd></div>" for a, c in t["barco_datos"])
    bitacora = "".join(f'<li><time>{a}</time><span>{esc(x)}</span></li>' for a, x in t["bitacora"])
    cerca = [x for x in SENDA_AZUL if x["banus"]]
    sitios_cerca = "".join(ficha_sitio(x, SENDA_AZUL.index(x) + 1, s, lang, mini=True) for x in cerca)
    resenas = "" if not RESENAS else f"""
<section class="seccion resenas" aria-labelledby="resenas-titulo">
  <div class="contenedor">
    <h2 id="resenas-titulo">{esc(t["resenas_h2"])}</h2>
    <ul class="resenas-lista">{"".join(
        f'<li><blockquote><p>{esc(x["texto"])}</p></blockquote><p class="resena-autor">{esc(x["nombre"])}'
        f'{", " + esc(x["origen"]) if x.get("origen") else ""}<span>{esc(x.get("fuente", ""))}</span></p></li>'
        for x in RESENAS)}</ul>
  </div>
</section>
"""
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"])
    precarga = (f'<link rel="preload" as="image" imagesrcset="{prefijo}assets/fotos/petit-puerto-600.webp 600w, '
                f'{prefijo}assets/fotos/petit-puerto-1086.webp 1086w" imagesizes="(max-width: 900px) 100vw, 44vw">\n')

    cuerpo = f"""
<body class="portada">
{cabecera(t, lang, prefijo)}
<main id="contenido">

<section class="hero" aria-labelledby="titulo">
  <div class="hero-texto">
    <h1 id="titulo">{esc(t["hero_h1"])}</h1>
    <p class="entradilla">{esc(t["hero_lead"])}</p>
    <p class="hero-idiomas">{esc(t["hero_idiomas"])}</p>
    <dl class="hero-precios">{hero_precios}</dl>
    <a class="hero-parking" href="#llegar"><span class="letra-p" aria-hidden="true">P</span>{esc(t["hero_parking"])}</a>
    <div class="botones">
      <a class="boton boton-amarillo boton-grande" href="#reservar">{esc(t["hero_cta"])}{FLECHA}</a>
      <a class="boton boton-borde" href="{wa(t["wa_hola"])}">{ICONO_WA}{esc(t["hero_cta2"])}</a>
    </div>
  </div>
  <figure class="hero-foto">
    {imagen("petit-puerto", (600, 1086), t["hero_foto_alt"], prefijo, "", "(max-width: 900px) 100vw, 44vw", "eager")}
  </figure>
</section>

<section class="seccion precios" id="precios" aria-labelledby="precios-titulo">
  <div class="contenedor">
    <h2 id="precios-titulo">{esc(t["precios_h2"])}</h2>
    <div class="paneles">{panel("compartida")}{panel("privada")}
    </div>
    <p class="precios-nota">{esc(t["precios_nota"])}</p>
    <div class="parking-gratis">
      <span class="letra-p" aria-hidden="true">P</span>
      <div>
        <p class="parking-titulo">{esc(t["parking"]["titulo"])}</p>
        <p>{esc(t["parking"]["texto"])}</p>
        <a class="parking-enlace" href="#llegar">{esc(t["parking"]["enlace"])}{FLECHA}</a>
      </div>
    </div>
  </div>
</section>
{resenas}
<div class="tira">{tira}</div>

<section class="seccion reservar" id="reservar" aria-labelledby="reservar-titulo">
  <div class="contenedor">
    <h2 id="reservar-titulo">{esc(t["reserva_h2"])}</h2>
    <p class="intro">{esc(t["reserva_intro"])}</p>
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
        <label class="campo">{esc(f["nombre"])}<input type="text" name="nombre" autocomplete="name"></label>
        <p class="prevision" hidden></p>
        <p class="error" role="alert" hidden></p>
      </form>
      <aside class="resumen-zona" aria-labelledby="resumen-titulo">
        <div class="resumen">
          <h3 id="resumen-titulo">{esc(r["titulo"])}</h3>
          <dl>
            <div><dt>{esc(r["salida"])}</dt><dd data-campo="tipo">{esc(f["tipos"]["compartida"])}</dd></div>
            <div><dt>{esc(r["fecha"])}</dt><dd data-campo="fecha">—</dd></div>
            <div><dt>{esc(r["hora"])}</dt><dd data-campo="hora">—</dd></div>
            <div><dt>{esc(r["pax"])}</dt><dd data-campo="pax">2</dd></div>
            <div class="resumen-extras" hidden><dt>{esc(r["extras"])}</dt><dd data-campo="extras">—</dd></div>
          </dl>
          <p class="resumen-total"><span>{esc(r["total"])}</span><strong data-campo="total">{PRECIO_COMPARTIDA * 2} €</strong></p>
          <p class="resumen-detalle" data-campo="detalle">{esc(f["detalle_compartida"].format(n=2))}</p>
        </div>
        {boton_pago}
        {"" if hay_pago else f'<p class="nota">{esc(f["sin_pago"])}</p>'}
        {f'<a class="enlace-wa" href="{wa(f["msg_inicio"])}">{ICONO_WA}{esc(f["whatsapp"])}</a>' if hay_pago else ""}
        <p class="nota">{esc(f["politica"])}</p>
        {f'<p class="nota">{esc(f["seguro"])}</p>' if hay_pago else ""}
      </aside>
    </div>
  </div>
</section>

<section class="seccion extras" id="extras" aria-labelledby="extras-titulo">
  <div class="contenedor">
    <h2 id="extras-titulo">{esc(t["extras_h2"])}</h2>
    <p class="intro">{esc(t["extras_intro"])}</p>
    <ul class="carta-extras">{carta_extras}
    </ul>
    <a class="boton boton-amarillo" href="#reservar" data-tipo="privada">{esc(t["extras_cta"])}{FLECHA}</a>
  </div>
</section>

<section class="seccion barco" id="barco" aria-labelledby="barco-titulo">
  <div class="contenedor barco-rejilla">
    <figure class="barco-video">
      <video muted loop playsinline preload="none" poster="{prefijo}assets/video/petit-navegando.webp" aria-label="{esc(t["video_alt"])}">
        <source src="{prefijo}assets/video/petit-navegando.mp4" type="video/mp4">
      </video>
      <button class="video-boton" type="button" aria-pressed="false" data-play="{esc(t["video_play"])}" data-pausa="{esc(t["video_pausa"])}">
        <span class="visualmente-oculto">{esc(t["video_play"])}</span>
      </button>
    </figure>
    <div class="barco-texto">
      <h2 id="barco-titulo">{esc(t["barco_h2"])}</h2>
      <p class="barco-sub">{esc(t["barco_sub"])}</p>
      {"".join(f"<p>{esc(x)}</p>" for x in t["barco_p"])}
      <dl class="barco-datos">{datos_barco}</dl>
    </div>
  </div>
  <div class="contenedor mosaico">{mosaico}</div>
</section>

<section class="seccion llegar" id="llegar" aria-labelledby="llegar-titulo">
  <div class="contenedor llegar-rejilla">
    <figure class="llegar-mapa">{svg_mapa(t)}<figcaption>{esc(t["mapa"]["fuente"])}</figcaption></figure>
    <div>
      <h2 id="llegar-titulo">{esc(t["llegar_h2"])}</h2>
      {"".join(f"<p>{esc(x)}</p>" for x in t["llegar_p"])}
      <div class="botones">
        <a class="boton boton-azul" href="{BARCO_MAPS}" target="_blank" rel="noopener">{esc(t["llegar_barco"])} ↗</a>
        <a class="boton boton-borde-azul" href="{PARKING_MAPS}" target="_blank" rel="noopener">{esc(t["llegar_enlace"])} ↗</a>
      </div>
    </div>
  </div>
</section>


<section class="pesca" aria-labelledby="pesca-titulo">
  <div class="contenedor pesca-fila">
    {SIMBOLO_PESCA}
    <div>
      <h2 id="pesca-titulo">{esc(t["pesca_h2"])}</h2>
      <p>{esc(t["pesca_p"])}</p>
    </div>
    <a class="boton boton-borde-azul" href="{wa(t["pesca_wa"])}">{ICONO_WA}{esc(t["pesca_cta"])}</a>
  </div>
</section>

<section class="seccion faq" id="faq" aria-labelledby="faq-titulo">
  <div class="contenedor faq-rejilla">
    <h2 id="faq-titulo">{esc(t["faq_h2"])}</h2>
    <div>{faq}</div>
  </div>
</section>

<section class="final" aria-labelledby="final-titulo">
  <div class="contenedor final-fila">
    <div>
      <h2 id="final-titulo">{esc(t["final_h2"])}</h2>
      <p>{esc(t["final_p"])}</p>
    </div>
    <div class="botones">
      <a class="boton boton-azul boton-grande" href="#reservar">{esc(t["hero_cta"])}{FLECHA}</a>
      <a class="boton boton-borde-azul" href="{wa(t["wa_hola"])}">{ICONO_WA}WhatsApp</a>
      <a class="boton boton-borde-azul" href="https://www.instagram.com/{INSTAGRAM}/">{ICONO_IG}@{INSTAGRAM}</a>
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
<section class="seccion buceo-cabeza" aria-labelledby="senda-titulo">
  <div class="contenedor">
    <h1 id="senda-titulo">{BANDERA_ALFA}{esc(s["h1"])}</h1>
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

<section class="seccion buceo-oscuro" aria-labelledby="pecio-titulo">
  <div class="contenedor">
    <article class="pecio">
      <p class="sonda-grande" aria-hidden="true">−8<span> m</span></p>
      <div>
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
        <a class="boton boton-amarillo" href="{wa(t["buceo_wa"])}">{ICONO_WA}{esc(t["buceo_wa_cta"])}</a>
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


# ─────────────────────────────── la Bitácora del mar (revista quincenal) ───────────────────────────────
# Iconos de los ejes, con el mismo trazo que el resto de la web
ICONOS_EJE = {
    "mar": '<path d="M4 30c4-3 8-3 12 0s8 3 12 0 8-3 12 0 8 3 8 3"/><path d="M4 22c4-3 8-3 12 0s8 3 12 0 8-3 12 0 8 3 8 3"/><path d="M34 6v10M30 10h8"/>',
    "buceo": '<path d="M8 14h36v12a6 6 0 0 1-6 6h-6l-4-5-4 5h-6a6 6 0 0 1-6-6z"/><path d="M44 18h4v18"/>',
    "vela": '<path d="M26 4v30"/><path d="M26 6 10 30h16z"/><path d="M28 10l12 20H28z"/><path d="M6 36h40l-4 5H10z"/>',
    "pesca": '<path d="M10 22c6-8 18-8 26 0-8 8-20 8-26 0z"/><path d="M36 22l8-6v12z"/><circle cx="17" cy="20" r="1.5"/>',
    "viajes": '<circle cx="26" cy="22" r="16"/><path d="M10 22h32M26 6c-6 6-6 26 0 32M26 6c6 6 6 26 0 32"/>',
    "ciencia": '<path d="M6 26c6-10 22-14 34-6l6-6v20l-6-6c-12 8-28 4-34-2z"/><circle cx="16" cy="24" r="1.5"/>',
}
INDICE_REVISTA = os.path.join(RAIZ, "revista", "index.json")


def numeros_revista():
    """Los números publicados, del más reciente al más antiguo (los escribe scripts/revista.py)."""
    try:
        lista = json.load(open(INDICE_REVISTA, encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return sorted(lista, key=lambda x: x.get("numero", ""), reverse=True)


def pagina_revista(lang):
    t = T[lang]
    prefijo = prefijo_de(lang)
    r = t["revista"]
    ejes = "".join(
        f'<article class="revista-eje"><svg class="simbolo" viewBox="0 0 52 44" aria-hidden="true">{ICONOS_EJE[k]}</svg>'
        f'<h3>{esc(a)}</h3><p>{esc(b)}</p></article>' for k, a, b in r["ejes"])
    orden = ["es", "en"] if lang == "es" else ["en", "es"]
    if any(REVISTA_FORMS.values()):
        botones = "".join(f'<a href="{esc(REVISTA_FORMS[l])}" target="_blank" rel="noopener" lang="{l}">'
                          f'{esc(T[l]["nombre_idioma"])}</a>' for l in orden if REVISTA_FORMS[l])
    else:
        botones = f'<a href="{wa(r["susc_wa"])}">WhatsApp</a>'
    numeros = numeros_revista()
    if numeros:
        filas = []
        for n in numeros:
            enlaces = " · ".join(
                f'<a href="{prefijo}revista/{esc(n["archivos"][l])}" lang="{l}">{esc(r["archivo_idioma"][l])}</a>'
                for l in ("es", "en") if n.get("archivos", {}).get(l))
            titulo = n.get("titulos", {}).get(lang if lang in ("es", "en") else "en") or n.get("titulos", {}).get("es", "")
            filas.append(f'<li><span class="revista-num">{esc(n["fecha"].get(lang, n["fecha"].get("en", "")))}</span>'
                         f'<span class="revista-tit">{esc(titulo)}</span><span class="revista-idiomas">{enlaces}</span></li>')
        archivo = f'<ol class="revista-archivo">{"".join(filas)}</ol>'
    else:
        archivo = f'<p class="nota">{esc(r["archivo_vacio"])}</p>'
    estados = json.dumps({k: list(v) for k, v in r["estado"].items()}, ensure_ascii=False)
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "pagina": "revista"}
    cuerpo = f"""
<body class="pagina-revista">
{cabecera(t, lang, prefijo, "revista.html")}
<main id="contenido">
<section class="seccion revista-cabeza" aria-labelledby="revista-titulo">
  <div class="contenedor">
    <p class="revista-eyebrow">{esc(r["eyebrow"])}</p>
    <h1 id="revista-titulo">{esc(r["h1"])}</h1>
    <p class="intro">{esc(r["lead"])}</p>
    <div class="revista-estado" role="status" hidden></div>
    <p class="susc-mini" id="suscribirse"><span>{esc(r["susc_corto"])}</span>{botones}</p>
    <p class="nota revista-privacidad">{esc(r["privacidad"])}</p>
  </div>
</section>

<section class="seccion revista-ejes-seccion" aria-labelledby="ejes-titulo">
  <div class="contenedor">
    <h2 id="ejes-titulo">{esc(r["ejes_h"])}</h2>
    <div class="revista-ejes">{ejes}</div>
    <h3 class="revista-archivo-h">{esc(r["archivo_h"])}</h3>
    {archivo}
    <p class="revista-datos"><a href="{prefijo}{carpeta(lang)}datos.html">{esc(t["datos"]["h1"])}</a></p>
  </div>
</section>
</main>
{pie(t, lang, prefijo, "revista.html")}
{datos_pagina(datos_js)}
<script>
(function () {{
  var e = {estados}[new URLSearchParams(location.search).get("suscripcion")];
  if (!e) return;
  var c = document.querySelector(".revista-estado");
  var b = document.createElement("strong"); b.textContent = e[0];
  var p = document.createElement("span"); p.textContent = e[1];
  c.appendChild(b); c.appendChild(p); c.hidden = false;
}})();
</script>
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
"""
    return cabeza(t, lang, prefijo, r["title"], r["description"], "revista.html") + cuerpo


# ─────────────────────────────── datos oficiales de Marbella (AEMET) ───────────────────────────────
def pagina_datos(lang):
    t = T[lang]
    prefijo = prefijo_de(lang)
    d = t["datos"]
    opciones = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in d["js"]["vars"].items())

    def selector(id_, etiqueta, valor, ninguna=False):
        ops = (f'<option value="">{esc(d["ninguna"])}</option>' if ninguna else "") + opciones
        ops = ops.replace(f'value="{valor}"', f'value="{valor}" selected', 1)
        return f'<label class="campo"><span>{esc(etiqueta)}</span><select id="{id_}">{ops}</select></label>'

    estaciones = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in d["estaciones"].items())
    rangos = "".join(f'<button type="button" class="filtro" data-rango="{k}" aria-pressed="{str(k == "7").lower()}">'
                     f'{esc(v)}</button>' for k, v in d["rangos"].items())
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "pagina": "datos", "datos": d["js"]}
    cuerpo = f"""
<body class="pagina-datos">
{cabecera(t, lang, prefijo, "datos.html")}
<main id="contenido">
<section class="seccion revista-cabeza" aria-labelledby="datos-titulo">
  <div class="contenedor">
    <p class="revista-eyebrow">{esc(d["eyebrow"])}</p>
    <h1 id="datos-titulo">{esc(d["h1"])}</h1>
    <p class="intro">{esc(d["lead"])}</p>
    <label class="campo campo-estacion"><span>{esc(d["estacion"])}</span><select id="sel-est">{estaciones}</select></label>
  </div>
</section>

<section class="seccion datos-seccion" aria-labelledby="ahora-titulo">
  <div class="contenedor">
    <div class="datos-cabeza"><h2 id="ahora-titulo">{esc(d["ahora_h"])}</h2><p class="nota" id="datos-hora"></p></div>
    <div class="datos-ahora" id="datos-ahora"></div>
    <p class="nota" id="datos-error" hidden>{esc(d["error"])}</p>

    <h2 class="datos-h2">{esc(d["serie_h"])}</h2>
    <div class="datos-controles">
      {selector("sel-v1", d["var1"], "viento")}
      {selector("sel-v2", d["var2"], "racha", True)}
      <div class="filtros datos-rangos" role="group">{rangos}</div>
    </div>
    <div class="datos-grafica"><canvas id="grafica-serie" aria-label="{esc(d["serie_h"])}"></canvas></div>
    <div class="datos-pie">
      <p class="nota">{esc(d["zoom_ayuda"])}</p>
      <div class="datos-botones">
        <button type="button" class="boton boton-borde-azul boton-pequeno" id="boton-zoom">{esc(d["zoom"])}</button>
        <button type="button" class="boton boton-borde-azul boton-pequeno" id="boton-csv">{esc(d["csv"])}</button>
      </div>
    </div>

    <h2 class="datos-h2">{esc(d["cruce_h"])}</h2>
    <p class="intro">{esc(d["cruce_p"])}</p>
    <div class="datos-controles">
      {selector("sel-x", d["eje_x"], "dir")}
      {selector("sel-y", d["eje_y"], "viento")}
    </div>
    <div class="datos-grafica"><canvas id="grafica-cruce" aria-label="{esc(d["cruce_h"])}"></canvas></div>
    <p class="datos-lectura" id="cruce-texto" aria-live="polite"></p>

    <p class="nota datos-nota">{esc(d["nota"])}</p>
    <p class="nota datos-nota"><strong>{esc(d["fuente"])}</strong></p>
  </div>
</section>
</main>
{pie(t, lang, prefijo, "datos.html")}
{datos_pagina(datos_js)}
<script src="{prefijo}assets/vendor/chart.umd.js"></script>
<script src="{prefijo}assets/vendor/chartjs-adapter-date-fns.bundle.min.js"></script>
<script src="{prefijo}assets/vendor/hammer.min.js"></script>
<script src="{prefijo}assets/vendor/chartjs-plugin-zoom.min.js"></script>
<script src="{prefijo}assets/datos.js?v={VERSION}" defer></script>
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
"""
    return cabeza(t, lang, prefijo, d["title"], d["description"], "datos.html") + cuerpo


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
    <p><a class="boton boton-borde-azul" href="{prefijo}{carpeta(lang) or './'}">{esc(t["volver"])}</a></p>
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
    g = t["gracias"]
    contenido = f"""
    <p class="intro">{esc(g["p"])}</p>
    <div class="gracias-resumen" hidden>
      <h2>{esc(g["resumen"])}</h2>
      <dl></dl>
    </div>
    <p class="gracias-sin" hidden>{esc(g["sin"])}</p>
    <p><a class="boton boton-amarillo" href="{wa(t["form"]["msg_pagado"])}" data-wa-gracias>{ICONO_WA}{esc(g["wa"])}</a></p>"""
    datos = {"pagina": "gracias", "resumen": t["resumen"], "form": t["form"],
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
        escribir(f"{carpeta(lang)}revista.html", pagina_revista(lang))
        escribir(f"{carpeta(lang)}datos.html", pagina_datos(lang))
        escribir(f"{carpeta(lang)}legal.html", legal(lang))
        escribir(f"{carpeta(lang)}gracias.html", gracias(lang))
    t = T[IDIOMAS[0]]
    # El 404 se sirve en cualquier dirección: sus enlaces van desde la raíz del dominio
    escribir("404.html", pagina_simple(IDIOMAS[0], t["e404_h1"] + " · Sea With Jose", t["e404_h1"],
                                       f'<p>{esc(t["e404_p"])}</p>', "404.html", prefijo="/"))
    hoy = datetime.date.today().isoformat()
    urls = []
    for ruta in ("", "revista.html", "datos.html"):
        for lang in IDIOMAS:
            alternas = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{DOMINIO}/{carpeta(l)}{ruta}"/>'
                               for l in IDIOMAS)
            urls.append(f"<url><loc>{DOMINIO}/{carpeta(lang)}{ruta}</loc><lastmod>{hoy}</lastmod>{alternas}</url>")
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("Web generada:", ", ".join(f"/{carpeta(l)}" for l in IDIOMAS), "· portada, revista, legal, gracias")


if __name__ == "__main__":
    main()
