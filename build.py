# -*- coding: utf-8 -*-
"""Genera la web de Sea With Jose en inglés (raíz), español (/es/) y ruso (/ru/).

    python build.py

Lee textos.py y fuentes/carta.json (isobatas de EMODnet, ver scripts/carta.py)
y escribe index.html, es/, ru/, legal, 404, sitemap.xml y robots.txt. Las rutas
son relativas, así que la web funciona igual en local, en GitHub Pages y en
seawithjose.es.
"""

import datetime
import html
import json
import os
import sys
import urllib.parse

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from textos import T, IDIOMAS, WHATSAPP, WHATSAPP_VISIBLE, INSTAGRAM, EMAIL, DOMINIO  # noqa: E402
CARTA = json.load(open(os.path.join(RAIZ, "fuentes", "carta.json"), encoding="utf-8"))
VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M")   # rompe la caché del CSS y el JS


def esc(s):
    return html.escape(str(s), quote=True)


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={urllib.parse.quote(texto)}"


def carpeta(lang):
    return "" if lang == IDIOMAS[0] else f"{lang}/"


# ─────────────────────────────── símbolos ───────────────────────────────
BANDERAS = {   # Código Internacional de Señales
    "J": '<rect width="18" height="12" fill="#1F4E9A"/><rect y="4" width="18" height="4" fill="#fff"/>',
    "O": '<path d="M0 0H18V12Z" fill="#D2232A"/><path d="M0 0V12H18Z" fill="#F5C400"/>',
    "S": '<rect width="18" height="12" fill="#fff"/><rect x="5.5" y="2.5" width="7" height="7" fill="#1F4E9A"/>',
    "E": '<rect width="18" height="6" fill="#1F4E9A"/><rect y="6" width="18" height="6" fill="#D2232A"/>',
}


def banderas_jose():
    return ('<span class="banderas" aria-hidden="true">' + "".join(
        f'<svg viewBox="0 0 18 12" width="18" height="12">{BANDERAS[l]}'
        f'<rect width="18" height="12" fill="none" stroke="#10263A" stroke-opacity=".35"/></svg>'
        for l in "JOSE") + "</span>")


SIMBOLOS = {
    "vela": ('<svg class="exp-simbolo" viewBox="0 0 52 44" aria-hidden="true"><path d="M25 4V31H9Z"/>'
             '<path d="M28 9 40 31H28Z"/><path d="M5 35H47L41 41H11Z"/></svg>'),
    # Bandera A del Código: «tengo un buzo sumergido»
    "buceo": ('<svg class="exp-simbolo" viewBox="0 0 52 36" aria-hidden="true">'
              '<rect x="1" y="1" width="24" height="34" fill="#fff" stroke="#10263A" stroke-width="1.4"/>'
              '<path d="M25 1H51L38 18 51 35H25Z" fill="#1F4E9A" stroke="#10263A" stroke-width="1.4" '
              'stroke-linejoin="round"/></svg>'),
    "pesca": ('<svg class="exp-simbolo" viewBox="0 0 52 44" aria-hidden="true">'
              '<path d="M6 22C14 11 31 10 39 22 31 34 14 33 6 22Z"/><path d="M39 22 48 14V30Z"/>'
              '<circle cx="15" cy="20" r="1.6" fill="currentColor" stroke="none"/></svg>'),
    "moto": ('<svg class="exp-simbolo" viewBox="0 0 52 44" aria-hidden="true">'
             '<path d="M6 30H35C39 30 43 28 46 24H38L32 18H23L19 24H8Z"/><path d="M25 18 28 12H33"/>'
             '<path d="M3 37C9 34 15 40 21 37 27 34 33 40 39 37 43 35 46 36 49 37"/></svg>'),
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
FLECHA = '<span class="flecha" aria-hidden="true">→</span>'


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

    import math
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
    ax, ay = W * 0.21, H - 26
    # Cajas que ocupan los rótulos del mar: ahí no se pintan sondas
    cajas = [(bx - 16, by - 24, bx + 26 + len(c["banus"]) * 13, by + 40),
             (gx - 20, gy - 22, gx + 30 + len(c["galeon"]) * 11.5, gy + 16),
             (ax - len(c["alboran"]) * 11, ay - 30, ax + len(c["alboran"]) * 11, ay + 12)]
    libres = [s for s in CARTA["sondas"]
              if not any(x0 <= s["x"] <= x1 and y0 <= s["y"] <= y1 for x0, y0, x1, y1 in cajas)]
    out.append('<g class="carta-sondas" aria-hidden="true">' + "".join(
        f'<text class="sonda" x="{s["x"]}" y="{s["y"]}" style="--j:{n}">{s["m"]}</text>'
        for n, s in enumerate(libres)) + "</g>")
    out.append('<g class="carta-rotulos" aria-hidden="true">'
               f'<text class="rotulo-tierra" x="22" y="{L["sanpedro"][1] - 46}">{esc(c["sanpedro"])}</text>'
               f'<text class="rotulo-tierra" x="{W - 20}" y="32" text-anchor="end">{esc(c["marbella"])}</text>'
               f'<text class="rotulo-tierra rotulo-rio" x="{L["rioverde"][0]}" y="{L["rioverde"][1] - 30}" text-anchor="middle">{esc(c["rioverde"])}</text>'
               # Puerto deportivo: símbolo de la carta (velero) en magenta
               f'<g class="simbolo-puerto" transform="translate({bx} {by})"><path d="M0-15V0H-9Z M2-11 9 0H2Z M-12 3H12L8 7H-8Z"/></g>'
               f'<text class="rotulo-puerto" x="{bx + 18}" y="{by + 30}">{esc(c["banus"])}</text>'
               # Pecio no peligroso (INT1 K29): línea con tres trazos
               f'<g class="simbolo-pecio" transform="translate({gx} {gy})"><path d="M-14 0H14 M-7-6V6 M0-6V6 M7-6V6"/></g>'
               f'<text class="rotulo-pecio" x="{gx + 22}" y="{gy + 6}">{esc(c["galeon"])}</text>'
               f'<text class="rotulo-mar" x="{ax:.0f}" y="{ay:.0f}" text-anchor="middle">{esc(c["alboran"])}</text>'
               "</g>")
    out.append("</g>")                      # fin del recorte
    out.append(borde_graduado(W, H, B, c))
    out.append("</svg>")
    return "".join(out)


def imagen(nombre, anchos, alt, prefijo, clase="", sizes="(max-width: 900px) 100vw, 50vw", carga="lazy"):
    srcset = ", ".join(f"{prefijo}assets/fotos/{nombre}-{a}.webp {a}w" for a in anchos)
    return (f'<img class="{clase}" src="{prefijo}assets/fotos/{nombre}-{anchos[0]}.webp" srcset="{srcset}" '
            f'sizes="{sizes}" alt="{esc(alt)}" loading="{carga}" decoding="async">')


# ─────────────────────────────── piezas ───────────────────────────────
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
<meta name="theme-color" content="#10263A">
<link rel="icon" href="{prefijo}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefijo}assets/icono-180.png">
<link rel="preload" href="{prefijo}assets/fuentes/spectral-normal-600-{precarga}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefijo}assets/fuentes/onest-normal-400-700-{precarga}.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefijo}assets/fuentes.css?v={VERSION}">
<link rel="stylesheet" href="{prefijo}assets/estilo.css?v={VERSION}">
{extra}</head>"""


def cabecera(t, lang, prefijo, ancla_base=""):
    n = t["nav"]
    enlaces = "".join(f'<li><a href="{ancla_base}#{k}">{esc(v)}</a></li>' for k, v in n.items())
    idiomas = "".join(
        (f'<a href="{prefijo}{carpeta(l)}" lang="{l}" hreflang="{l}"'
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
      <a class="boton boton-principal boton-pequeno" href="{wa(t["plan"]["msg_inicio"])}">{ICONO_WA}{esc(t["whatsapp_corto"])}</a>
    </nav>
  </div>
</header>"""


def pie(t, lang, prefijo):
    idiomas = " · ".join(f'<a href="{prefijo}{carpeta(l)}" lang="{l}">{T[l]["nombre_idioma"]}</a>' for l in IDIOMAS)
    return f"""<footer class="pie">
  <div class="contenedor pie-rejilla">
    <div>
      <p class="pie-marca">{banderas_jose()}<span>Sea With Jose</span></p>
      <p>{esc(t["pie_lugar"])}</p>
    </div>
    <div>
      <p><a href="{wa(t["plan"]["msg_inicio"])}">WhatsApp {WHATSAPP_VISIBLE}</a><br>
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
        "founder": {"@type": "Person", "name": "José María Hinojosa Figueira",
                    "jobTitle": "Yacht captain, oceanographer and diving instructor"},
    }
    return f'<script type="application/ld+json">{json.dumps(datos, ensure_ascii=False)}</script>\n'


# ─────────────────────────────── el mar, ahora ───────────────────────────────
# Lo que solo se pinta en el HTML; el resto de t["mar"] va al JS, que rellena las notas con datos/mar.json
SOLO_HTML = ("eyebrow", "h2", "intro", "camaras_h", "en_directo", "ver", "camaras_nota", "camaras", "notas_h",
             "dias_aria", "como_h", "como", "aviso_legal", "cargando")


def seccion_mar(t):
    m = t["mar"]
    camaras = "".join(f"""
      <li><a class="camara" href="{esc(c["url"])}" target="_blank" rel="noopener">
        <span class="camara-directo"><span class="camara-punto" aria-hidden="true"></span>{esc(m["en_directo"])}</span>
        <span class="camara-nombre">{esc(c["nombre"])}</span>
        <span class="camara-que">{esc(c["que"])}</span>
        <span class="camara-fuente">{esc(m["ver"])} · {esc(c["fuente"])} <span aria-hidden="true">↗</span></span>
      </a></li>""" for c in m["camaras"])
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


# ─────────────────────────────── portada ───────────────────────────────
def portada(lang):
    t = T[lang]
    prefijo = "" if lang == IDIOMAS[0] else "../"
    p = t["parte"]
    datos_js = {"lang": lang, "prefijo": prefijo, "whatsapp": WHATSAPP, "parte": p, "plan": t["plan"],
                "mar": {k: v for k, v in t["mar"].items() if k not in SOLO_HTML}}

    credenciales = "".join(f'<li><strong>{esc(a)}</strong><span>{esc(b)}</span></li>' for a, b in t["credenciales"])
    experiencias = "".join(f"""
      <article class="exp" id="exp-{e["id"]}">
        {SIMBOLOS[e["id"]]}
        <h3>{esc(e["titulo"])}</h3>
        <p class="exp-frase">{esc(e["frase"])}</p>
        <ul>{"".join(f"<li>{esc(x)}</li>" for x in e["puntos"])}</ul>
        <a class="exp-enlace" href="{wa(e["wa"])}">{ICONO_WA}{esc(e["cta"])}{FLECHA}</a>
      </article>""" for e in t["experiencias"])
    bitacora = "".join(f'<li><time>{a}</time><span>{esc(b)}</span></li>' for a, b in t["bitacora"])
    bloques = "".join(f'<div class="buceo-bloque"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in t["buceo_bloques"])
    pecio_datos = "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>" for a, b in t["pecio_datos"])
    pasos = "".join(f'<li><span class="paso-num" aria-hidden="true">{i}</span><h3>{esc(a)}</h3><p>{esc(b)}</p></li>'
                    for i, (a, b) in enumerate(t["pasos"], 1))
    pl = t["plan"]
    opciones = "".join(f"<option>{esc(o)}</option>" for o in pl["opciones"])
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faq"])
    fb = t["fotos_buceo"]
    buceo_wa = wa(t["experiencias"][1]["wa"])

    cuerpo = f"""
<body>
{cabecera(t, lang, prefijo)}
<main id="contenido">

<section class="hero" aria-labelledby="titulo">
  <div class="contenedor hero-rejilla">
    <div class="hero-texto">
      <p class="eyebrow">{esc(t["hero_eyebrow"])}</p>
      <h1 id="titulo">{t["hero_h1"]}</h1>
      <p class="entradilla">{esc(t["hero_lead"])}</p>
      <div class="botones">
        <a class="boton boton-principal" href="{wa(t["plan"]["msg_inicio"])}">{ICONO_WA}{esc(t["hero_cta"])}</a>
        <a class="boton boton-secundario" href="#experiencias">{esc(t["hero_cta2"])}</a>
      </div>
    </div>
    <div class="hero-carta">
      {svg_carta(t)}
      <aside class="parte" aria-labelledby="parte-titulo" aria-live="polite">
        <p class="parte-titulo" id="parte-titulo">{esc(p["titulo"])}</p>
        <p class="parte-lugar">{esc(p["lugar"])}</p>
        <dl class="parte-datos"></dl>
        <p class="parte-lectura"></p>
        <p class="parte-fuente">{esc(p["sin_datos"])}</p>
        <a class="parte-enlace" href="#mar">{esc(p["enlace"])} <span aria-hidden="true">↓</span></a>
      </aside>
    </div>
  </div>
</section>

<section class="credenciales" aria-label="{esc(t["jose_eyebrow"])}">
  <ul class="contenedor">{credenciales}</ul>
</section>

<section class="seccion" id="experiencias" aria-labelledby="exp-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["exp_eyebrow"])}</p>
    <h2 id="exp-titulo">{esc(t["exp_h2"])}</h2>
    <p class="intro">{esc(t["exp_intro"])}</p>
    <div class="experiencias">{experiencias}
    </div>
  </div>
</section>
{seccion_mar(t)}
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

<section class="seccion buceo" id="buceo" aria-labelledby="buceo-titulo">
  <div class="contenedor">
    <p class="eyebrow">{esc(t["buceo_eyebrow"])}</p>
    <h2 id="buceo-titulo">{esc(t["buceo_h2"])}</h2>
    <p class="intro">{esc(t["buceo_lead"])}</p>
    <div class="buceo-rejilla">
      {bloques}
      <figure class="buceo-foto">{imagen("senal-ok", (640, 1150), fb["ok"], prefijo, "", "(max-width: 900px) 100vw, 50vw")}</figure>
      <figure class="buceo-foto">{imagen("pulpo", (640, 1170), fb["pulpo"], prefijo, "", "(max-width: 900px) 100vw, 50vw")}</figure>
    </div>
    <article class="pecio">
      <p class="sonda-grande" aria-hidden="true">−6<span> m</span></p>
      <div>
        <p class="eyebrow">{esc(t["pecio_eyebrow"])}</p>
        <h3>{t["pecio_h"]}</h3>
        {"".join(f"<p>{x}</p>" for x in t["pecio_p"])}
        <dl class="pecio-datos">{pecio_datos}</dl>
      </div>
    </article>
    <div class="buceo-mas">
      <div>
        <h3>{esc(t["habichuelas_h"])}</h3>
        <p>{t["habichuelas_p"]}</p>
        <h3>{esc(t["viajes_h"])}</h3>
        <p>{esc(t["viajes_p"])}</p>
        <a class="boton boton-principal" href="{buceo_wa}">{ICONO_WA}{esc(t["buceo_cta"])}</a>
      </div>
      <figure class="buceo-foto">{imagen("tortuga", (520, 1040), fb["tortuga"], prefijo, "", "(max-width: 900px) 50vw, 22vw")}</figure>
      <figure class="buceo-foto">{imagen("tiburon", (520, 1040), fb["tiburon"], prefijo, "", "(max-width: 900px) 50vw, 22vw")}</figure>
    </div>
  </div>
</section>

<section class="seccion" id="como" aria-labelledby="como-titulo">
  <div class="contenedor">
    <h2 id="como-titulo">{esc(t["como_h2"])}</h2>
    <ol class="pasos">{pasos}</ol>
  </div>
</section>

<section class="seccion seccion-blanca" id="plan" aria-labelledby="plan-titulo">
  <div class="contenedor plan">
    <div>
      <h2 id="plan-titulo">{esc(t["plan_h2"])}</h2>
      <p class="intro">{esc(t["plan_intro"])}</p>
    </div>
    <form id="planificador" class="plan-form">
      <label class="campo campo-ancho">{esc(pl["que"])}
        <select name="actividad">{opciones}</select></label>
      <label class="campo">{esc(pl["fecha"])}<input type="date" name="fecha"></label>
      <label class="campo">{esc(pl["personas"])}<input type="number" name="personas" min="1" max="30" inputmode="numeric"></label>
      <label class="campo campo-ancho">{esc(pl["nombre"])}<input type="text" name="nombre" autocomplete="given-name"></label>
      <label class="campo campo-ancho">{esc(pl["notas"])}<textarea name="notas" rows="3"></textarea></label>
      <div class="campo-ancho plan-enviar">
        <button class="boton boton-principal" type="submit">{ICONO_WA}{esc(pl["boton"])}</button>
        <p class="nota">{esc(pl["nota"])}</p>
      </div>
    </form>
  </div>
</section>

<section class="seccion" id="faq" aria-labelledby="faq-titulo">
  <div class="contenedor faq">
    <h2 id="faq-titulo">{esc(t["faq_h2"])}</h2>
    <div>{faq}</div>
  </div>
</section>

<section class="seccion final" aria-labelledby="final-titulo">
  <div class="contenedor">
    <h2 id="final-titulo">{esc(t["final_h2"])}</h2>
    <p class="intro">{esc(t["final_p"])}</p>
    <div class="botones botones-centro">
      <a class="boton boton-principal" href="{wa(t["plan"]["msg_inicio"])}">{ICONO_WA}WhatsApp {WHATSAPP_VISIBLE}</a>
      <a class="boton boton-secundario" href="https://www.instagram.com/{INSTAGRAM}/">{ICONO_IG}@{INSTAGRAM}</a>
      <a class="boton boton-secundario" href="mailto:{EMAIL}">{ICONO_MAIL}Email</a>
    </div>
  </div>
</section>

</main>
{pie(t, lang, prefijo)}
<script type="application/json" id="datos-pagina">{json.dumps(datos_js, ensure_ascii=False)}</script>
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
"""
    return cabeza(t, lang, prefijo, t["title"], t["description"], "", json_ld(t, lang)) + cuerpo


def pagina_simple(lang, titulo, h1, contenido, ruta):
    t = T[lang]
    prefijo = "" if lang == IDIOMAS[0] else "../"
    return (cabeza(t, lang, prefijo, titulo, t["description"], ruta, '<meta name="robots" content="noindex">\n')
            + f"""
<body>
{cabecera(t, lang, prefijo, prefijo + carpeta(lang))}
<main id="contenido" class="seccion">
  <article class="contenedor texto-legal">
    <h1>{esc(h1)}</h1>
    {contenido}
    <p><a class="boton boton-secundario" href="{prefijo}{carpeta(lang)}">{esc(t["volver"])}</a></p>
  </article>
</main>
{pie(t, lang, prefijo)}
<script type="application/json" id="datos-pagina">{json.dumps({"lang": lang, "prefijo": prefijo}, ensure_ascii=False)}</script>
<script src="{prefijo}assets/web.js?v={VERSION}" defer></script>
</body>
</html>
""")


def legal(lang):
    t = T[lang]
    contenido = "".join(
        f"<h2>{esc(a)}</h2><p>{esc(b).format(email=EMAIL, tel=WHATSAPP_VISIBLE)}</p>" for a, b in t["legal"])
    return pagina_simple(lang, t["legal_title"], t["legal_h1"], contenido, "legal.html")


def escribir(ruta, texto):
    ruta = os.path.join(RAIZ, ruta)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def main():
    for lang in IDIOMAS:
        escribir(f"{carpeta(lang)}index.html", portada(lang))
        escribir(f"{carpeta(lang)}legal.html", legal(lang))
    t = T[IDIOMAS[0]]
    escribir("404.html", pagina_simple(IDIOMAS[0], t["e404_h1"] + " — Sea With Jose", t["e404_h1"],
                                       f'<p>{esc(t["e404_p"])}</p>', "404.html"))
    hoy = datetime.date.today().isoformat()
    urls = []
    for lang in IDIOMAS:
        alternas = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{DOMINIO}/{carpeta(l)}"/>' for l in IDIOMAS)
        urls.append(f"<url><loc>{DOMINIO}/{carpeta(lang)}</loc><lastmod>{hoy}</lastmod>{alternas}</url>")
    escribir("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    escribir("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("Web generada:", ", ".join(f"/{carpeta(l)}" for l in IDIOMAS))


if __name__ == "__main__":
    main()
