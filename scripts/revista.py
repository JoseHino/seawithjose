# -*- coding: utf-8 -*-
"""Bitácora del mar: la revista quincenal de Sea With Jose, en español y en inglés.

    python scripts/revista.py borrador [AAAA-MM-Q]   prepara el número (Q = 1 o 2, por quincena) y su versión 1
    python scripts/revista.py abrir                  abre la incidencia de GitHub para aprobarlo (tras subir los ficheros)
    python scripts/revista.py revisar                lee la respuesta de Jose: OK publica y envía; si no, nueva versión
    python scripts/revista.py comentar               contesta en la incidencia (tras subir los ficheros)

El circuito, todo en GitHub Actions y sin servidor:

  1. `revista-borrador.yml` (días 1 y 16, o a mano) ejecuta `borrador`: junta los
     datos del mar de la quincena (Open-Meteo y AEMET), las noticias guardadas por
     `revista_noticias.py`, y la IA redacta los dos idiomas. El HTML lo monta este
     script con la plantilla de abajo: la IA no escribe ninguna cifra.
  2. `abrir` crea una incidencia con la etiqueta «revista» que menciona a Jose:
     GitHub se la manda por correo con los enlaces a la vista previa.
  3. Jose responde a ese correo (o comenta en la incidencia). `revista-revision.yml`
     ejecuta `revisar`: «OK» → se publica en seawithjose.es/revista/ y se envía con
     Brevo a la lista de cada idioma; cualquier otra cosa → la IA aplica los cambios
     y sale la versión siguiente.

Variables de entorno (secretos y variables del repositorio):
  OPENAI_API_KEY, REVISTA_MODELO (por defecto gpt-5.6-terra)
  BREVO_API_KEY, BREVO_LISTA_ES, BREVO_LISTA_EN, REVISTA_REMITENTE (por defecto boletin@seawithjose.es)
  GITHUB_TOKEN, GITHUB_REPOSITORY, REVISTA_EDITOR (por defecto el dueño del repositorio)
  ISSUE_NUMBER, ISSUE_TITLE, COMMENT_BODY   (los pone `revista-revision.yml`)
"""

import datetime
import html
import json
import math
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "revista")
BORRADORES = os.path.join(CARPETA, "borradores")
INDICE = os.path.join(CARPETA, "index.json")
NOTICIAS = os.path.join(RAIZ, "datos", "revista", "noticias.json")
PARTE = os.path.join(RAIZ, "datos", "mar.json")
SALIDA_TMP = os.path.join(RAIZ, ".revista_salida.json")
DOMINIO = "https://seawithjose.es"
LAT, LON = 36.47, -4.95                       # frente a Puerto Banús
IDIOMAS = ("es", "en")
EJES = ("local", "buceo", "vela", "pesca", "viajes", "ciencia")

MODELO = os.environ.get("REVISTA_MODELO") or "gpt-5.6-terra"
REMITENTE = os.environ.get("REVISTA_REMITENTE") or "boletin@seawithjose.es"

COLOR = {"marino": "#0B2D52", "azul": "#1F4E9A", "amarillo": "#FFC20E", "rojo": "#D2232A", "tinta": "#0D1B2A",
         "gris": "#4E5F70", "cielo": "#E7F1F7", "linea": "#CFDCE5"}

TXT = {
    "es": {"nombre": "Bitácora del mar", "de": "Sea With Jose", "num": "Nº", "quincena": ["1.ª quincena", "2.ª quincena"],
           "meses": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split(),
           "mar_h": "El mar en la quincena", "agua": "Agua (media)", "rango": "mín. {a} · máx. {b} °C",
           "vs": "{d} °C {s} que hace un año", "mas": "más", "menos": "menos", "igual": "igual que hace un año",
           "ola": "Ola más alta", "viento": "Racha más fuerte", "luna": "Luna", "hoy": "Agua hoy (AEMET)",
           "fases": {"nueva": "Luna nueva", "llena": "Luna llena", "creciente": "Cuarto creciente", "menguante": "Cuarto menguante"},
           "fuentes": "Datos: Open-Meteo (Copernicus Marine, ERA5) y AEMET, frente a Puerto Banús.",
           "leer": "Leer en", "web": "Ver en la web", "baja": "Darse de baja",
           "pie": "Recibes la Bitácora porque te suscribiste en seawithjose.es.", "salidas": "Salir a navegar, bucear o pescar conmigo",
           "aviso": "Borrador para tu aprobación · versión {v}",
           "aviso_p": "Responde «OK» al correo de GitHub (o comenta en la incidencia) y se publica y se envía. Si quieres cambios, escríbelos en tu respuesta."},
    "en": {"nombre": "The Sea Logbook", "de": "Sea With Jose", "num": "No.", "quincena": ["First half of", "Second half of"],
           "meses": "January February March April May June July August September October November December".split(),
           "mar_h": "The sea this fortnight", "agua": "Water (average)", "rango": "min {a} · max {b} °C",
           "vs": "{d} °C {s} than a year ago", "mas": "warmer", "menos": "cooler", "igual": "same as a year ago",
           "ola": "Highest wave", "viento": "Strongest gust", "luna": "Moon", "hoy": "Water today (AEMET)",
           "fases": {"nueva": "New moon", "llena": "Full moon", "creciente": "First quarter", "menguante": "Last quarter"},
           "fuentes": "Data: Open-Meteo (Copernicus Marine, ERA5) and AEMET, off Puerto Banús.",
           "leer": "Read on", "web": "View on the website", "baja": "Unsubscribe",
           "pie": "You get the Logbook because you subscribed at seawithjose.es.", "salidas": "Come sailing, diving or fishing with me",
           "aviso": "Draft for your approval · version {v}",
           "aviso_p": "Reply “OK” to the GitHub email (or comment on the issue) and it will be published and sent."},
}


# ─────────────────────────────── utilidades ───────────────────────────────
def esc(s):
    return html.escape(str(s or ""), quote=True)


def pedir_json(url, datos=None, cabeceras=None, metodo=None, timeout=60):
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    req = urllib.request.Request(url, data=cuerpo, method=metodo or ("POST" if cuerpo else "GET"),
                                 headers={"User-Agent": "seawithjose-revista", "Content-Type": "application/json",
                                          **(cabeceras or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            texto = r.read().decode("utf-8")
            return json.loads(texto) if texto.strip() else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{metodo or 'GET'} {url} -> {e.code}: {e.read().decode('utf-8', 'replace')[:600]}") from e


def numero_de(fecha):
    return f"{fecha.year}-{fecha.month:02d}-{1 if fecha.day < 16 else 2}"


def periodo(numero):
    """Días que cubre un número: la quincena ANTERIOR a su salida (sale el 1 y el 16)."""
    a, m, q = (int(x) for x in numero.split("-"))
    salida = datetime.date(a, m, 1 if q == 1 else 16)
    fin = salida - datetime.timedelta(days=1)
    ini = fin.replace(day=16) if fin.day > 15 else fin.replace(day=1)
    return ini, fin


def titulo_fecha(numero, lang):
    a, m, q = (int(x) for x in numero.split("-"))
    t = TXT[lang]
    mes = t["meses"][m - 1]
    return f"{t['quincena'][q - 1]} de {mes} de {a}" if lang == "es" else f"{t['quincena'][q - 1]} {mes} {a}"


def num_es(x, dec=1):
    return f"{x:.{dec}f}".replace(".", ",")


def fmt(x, lang, dec=1):
    return num_es(x, dec) if lang == "es" else f"{x:.{dec}f}"


# ─────────────────────────────── datos del mar ───────────────────────────────
def serie_mar(ini, fin):
    url = ("https://marine-api.open-meteo.com/v1/marine?"
           + urllib.parse.urlencode({"latitude": LAT, "longitude": LON, "hourly": "sea_surface_temperature",
                                     "daily": "wave_height_max", "start_date": ini.isoformat(),
                                     "end_date": fin.isoformat(), "timezone": "Europe/Madrid"}))
    d = pedir_json(url)
    sst = [x for x in d.get("hourly", {}).get("sea_surface_temperature", []) if x is not None]
    olas = [x for x in d.get("daily", {}).get("wave_height_max", []) if x is not None]
    return sst, olas


def fases_luna(ini, fin):
    """Fases principales entre dos fechas (mes sinódico desde la luna nueva del 6-1-2000 18:14 UTC)."""
    base = datetime.datetime(2000, 1, 6, 18, 14)
    sinodico = 29.530588853
    salida, d = [], ini
    while d <= fin:
        edad = ((datetime.datetime(d.year, d.month, d.day, 12) - base).total_seconds() / 86400) % sinodico
        for nombre, objetivo in (("nueva", 0), ("creciente", sinodico / 4), ("llena", sinodico / 2),
                                 ("menguante", 3 * sinodico / 4)):
            if (edad - objetivo) % sinodico < 1:      # la edad avanza un día por día: solo un día cae en esa ventana
                salida.append((d, nombre))
        d += datetime.timedelta(days=1)
    return salida


def datos_mar(numero):
    ini, fin = periodo(numero)
    out = {"desde": ini.isoformat(), "hasta": fin.isoformat()}
    try:
        sst, olas = serie_mar(ini, fin)
        if sst:
            out.update(agua=round(sum(sst) / len(sst), 1), agua_min=round(min(sst), 1), agua_max=round(max(sst), 1))
        if olas:
            out["ola_max"] = round(max(olas), 1)
        sst_ant, _ = serie_mar(ini.replace(year=ini.year - 1), fin.replace(year=fin.year - 1))
        if sst and sst_ant:
            out["agua_dif"] = round(out["agua"] - sum(sst_ant) / len(sst_ant), 1)
    except Exception as e:  # noqa: BLE001
        print("  Open-Meteo marino:", e)
    try:
        url = ("https://api.open-meteo.com/v1/forecast?"
               + urllib.parse.urlencode({"latitude": 36.48, "longitude": LON, "daily": "wind_gusts_10m_max",
                                         "start_date": ini.isoformat(), "end_date": fin.isoformat(),
                                         "timezone": "Europe/Madrid"}))
        rachas = [x for x in pedir_json(url).get("daily", {}).get("wind_gusts_10m_max", []) if x is not None]
        if rachas:
            out["racha_max"] = round(max(rachas))
    except Exception as e:  # noqa: BLE001
        print("  Open-Meteo viento:", e)
    try:
        parte = json.load(open(PARTE, encoding="utf-8"))
        hoy = parte["dias"][0]
        if hoy.get("agua") is not None:
            out["agua_hoy"] = hoy["agua"]
    except Exception:  # noqa: BLE001
        pass
    # la luna de la quincena que empieza ahora, que es la que le sirve a quien sale a pescar
    a, m, q = (int(x) for x in numero.split("-"))
    salida = datetime.date(a, m, 1 if q == 1 else 16)
    out["luna"] = [(d.isoformat(), f) for d, f in fases_luna(salida, salida + datetime.timedelta(days=15))]
    return out


def texto_mar(mar, lang):
    """Las cifras en una línea, para que la IA comente sin inventarlas."""
    t = TXT[lang]
    partes = []
    if "agua" in mar:
        partes.append(f"agua media {mar['agua']} °C (mín {mar['agua_min']}, máx {mar['agua_max']})")
    if "agua_dif" in mar:
        partes.append(f"diferencia con hace un año {mar['agua_dif']:+} °C")
    if "ola_max" in mar:
        partes.append(f"ola máxima {mar['ola_max']} m")
    if "racha_max" in mar:
        partes.append(f"racha máxima {mar['racha_max']} km/h")
    if mar.get("luna"):
        partes.append("luna: " + ", ".join(f"{t['fases'][f]} {d}" for d, f in mar["luna"]))
    return "; ".join(partes)


# ─────────────────────────────── noticias de la quincena ───────────────────────────────
def noticias(numero, lang, por_eje=14):
    ini, fin = periodo(numero)
    ini = ini - datetime.timedelta(days=3)
    try:
        todas = json.load(open(NOTICIAS, encoding="utf-8"))["noticias"]
    except (OSError, ValueError, KeyError):
        return ""
    lineas = []
    for eje in EJES:
        sel = [n for n in todas if n["lang"] == lang and n["eje"] == eje and ini.isoformat() <= n["fecha"] <= fin.isoformat()]
        for i, n in enumerate(sel[:por_eje]):
            lineas.append(f"[{eje}] {n['fecha']} · {n['fuente']} · {n['titular']} · {n['url']}")
    return "\n".join(lineas)


# ─────────────────────────────── la IA ───────────────────────────────
def ia(sistema, usuario):
    clave = os.environ.get("OPENAI_API_KEY")
    if not clave:
        sys.exit("Falta el secreto OPENAI_API_KEY en el repositorio (Settings → Secrets and variables → Actions).")
    r = pedir_json("https://api.openai.com/v1/chat/completions", {
        "model": MODELO, "reasoning_effort": "low", "max_completion_tokens": 16000,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": usuario}]},
        {"Authorization": f"Bearer {clave}"}, timeout=300)
    return json.loads(r["choices"][0]["message"]["content"])


def instrucciones(nombre):
    return open(os.path.join(CARPETA, f"instrucciones_{nombre}.md"), encoding="utf-8").read()


def redactar(numero, mar, notas=""):
    usuario = [f"NÚMERO: {numero}", f"NOTAS DE JOSE: {notas or '(ninguna)'}"]
    for lang in IDIOMAS:
        usuario += [f"\n=== IDIOMA {lang} ===", f"CIFRAS DEL MAR ({mar['desde']} a {mar['hasta']}): {texto_mar(mar, lang)}",
                    f"NOTICIAS ({lang}; formato: [eje] fecha · fuente · titular · enlace):", noticias(numero, lang)]
    return ia(instrucciones("redaccion"), "\n".join(usuario))


# ─────────────────────────────── la plantilla del correo ───────────────────────────────
def bloque_mar(mar, lang):
    t = TXT[lang]
    celdas = []
    if "agua" in mar:
        extra = esc(t["rango"].format(a=fmt(mar["agua_min"], lang), b=fmt(mar["agua_max"], lang)))
        if "agua_dif" in mar:
            d = mar["agua_dif"]
            extra += "<br>" + (esc(t["igual"]) if abs(d) < 0.15 else
                               esc(t["vs"].format(s=t["mas"] if d > 0 else t["menos"], d=fmt(abs(d), lang))))
        celdas.append((t["agua"], f"{fmt(mar['agua'], lang)} °C", extra))
    if "agua_hoy" in mar:
        celdas.append((t["hoy"], f"{mar['agua_hoy']} °C", ""))
    if "ola_max" in mar:
        celdas.append((t["ola"], f"{fmt(mar['ola_max'], lang)} m", ""))
    if "racha_max" in mar:
        celdas.append((t["viento"], f"{mar['racha_max']} km/h", ""))
    if mar.get("luna"):
        lunas = "<br>".join(f"{esc(t['fases'][f])} · {int(d[8:10])}/{int(d[5:7])}" for d, f in mar["luna"])
        celdas.append((t["luna"], "", lunas))
    filas, fila = [], []
    for etiqueta, valor, extra in celdas:
        fila.append(f'<td width="50%" valign="top" style="padding:5px;"><table role="presentation" width="100%" cellpadding="0" '
                    f'cellspacing="0" style="background:{COLOR["cielo"]};border-radius:6px;"><tr><td style="padding:14px 16px;'
                    f'font-family:Arial,Helvetica,sans-serif;"><div style="font-size:11px;letter-spacing:.08em;text-transform:'
                    f'uppercase;color:{COLOR["gris"]};font-weight:700;">{esc(etiqueta)}</div>'
                    + (f'<div style="font-size:26px;font-weight:800;color:{COLOR["marino"]};margin-top:4px;">{valor}</div>' if valor else "")
                    + (f'<div style="font-size:13px;line-height:1.45;color:{COLOR["gris"]};margin-top:4px;">{extra}</div>' if extra else "")
                    + "</td></tr></table></td>")
        if len(fila) == 2:
            filas.append("<tr>" + "".join(fila) + "</tr>")
            fila = []
    if fila:
        filas.append("<tr>" + fila[0] + '<td width="50%"></td></tr>')
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{"".join(filas)}</table>'
            f'<p style="margin:10px 5px 0;font:12px/1.5 Arial,Helvetica,sans-serif;color:{COLOR["gris"]};">{esc(t["fuentes"])}</p>')


def texto_html(s):
    """Texto de la IA a HTML: escapa y deja solo **negritas**."""
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", rf'<strong style="color:{COLOR["marino"]};">\1</strong>', s)


def montar(numero, version, contenido, mar, lang, modo):
    """modo: «borrador» (con el recuadro de aprobación), «web» o «brevo» (con enlaces de baja de Brevo)."""
    t = TXT[lang]
    c = contenido[lang]
    url_web = f"{DOMINIO}/revista/{numero}-{lang}.html"
    secciones = []
    for s in c.get("secciones", []):
        items = "".join(
            f'<tr><td style="padding:0 0 18px;font:16px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">'
            f'<div style="font-weight:800;color:{COLOR["marino"]};font-size:17px;line-height:1.35;">{esc(i.get("titular"))}</div>'
            f'<div style="margin-top:4px;">{texto_html(i.get("texto"))}</div>'
            + (f'<div style="margin-top:4px;font-size:14px;"><a href="{esc(i["url"])}" style="color:{COLOR["azul"]};font-weight:700;">'
               f'{esc(t["leer"])} {esc(i.get("fuente") or "")} →</a></div>' if i.get("url") else "")
            + "</td></tr>" for i in s.get("items", []))
        secciones.append(
            f'<tr><td style="padding:26px 30px 0;"><div style="font:800 13px/1 Arial,Helvetica,sans-serif;letter-spacing:.14em;'
            f'text-transform:uppercase;color:{COLOR["rojo"]};margin-bottom:12px;border-top:3px solid {COLOR["marino"]};padding-top:14px;">'
            f'{esc(s.get("titulo"))}</div><table role="presentation" width="100%" cellpadding="0" cellspacing="0">{items}</table></td></tr>')
    aviso = ""
    if modo == "borrador":
        aviso = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;margin:0 0 14px;">'
                 f'<tr><td style="background:#FFF4D1;border:2px solid {COLOR["amarillo"]};padding:14px 18px;'
                 f'font:14px/1.5 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};"><strong>{esc(t["aviso"].format(v=version))}</strong><br>'
                 f'{esc(t["aviso_p"])}</td></tr></table>')
    if modo == "brevo":
        enlaces_pie = (f'<a href="{{{{ mirror }}}}" style="color:#fff;">{esc(t["web"])}</a> · '
                       f'<a href="{{{{ unsubscribe }}}}" style="color:#fff;">{esc(t["baja"])}</a>')
    else:
        enlaces_pie = f'<a href="{DOMINIO}/{"es/" if lang == "es" else ""}revista.html" style="color:#fff;">seawithjose.es</a>'
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{'<meta name="robots" content="noindex">' if modo == "borrador" else ''}<title>{esc(c.get("asunto"))}</title></head>
<body style="margin:0;padding:0;background:{COLOR["cielo"]};">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{esc(c.get("entradilla"))}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{COLOR["cielo"]};"><tr><td align="center" style="padding:24px 12px;">
{aviso}
<table role="presentation" width="640" cellpadding="0" cellspacing="0" style="width:100%;max-width:640px;background:#fff;">
  <tr><td style="background:{COLOR["marino"]};padding:26px 30px 22px;">
    <table role="presentation" cellpadding="0" cellspacing="0"><tr>
      <td style="width:14px;height:10px;background:{COLOR["azul"]};"></td><td style="width:4px;"></td>
      <td style="width:14px;height:10px;background:{COLOR["amarillo"]};"></td><td style="width:4px;"></td>
      <td style="width:14px;height:10px;background:#fff;"></td><td style="width:4px;"></td>
      <td style="width:14px;height:10px;background:{COLOR["rojo"]};"></td></tr></table>
    <div style="font:700 12px/1.3 Arial,Helvetica,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:{COLOR["amarillo"]};margin-top:14px;">{esc(t["de"])}</div>
    <div style="font:900 38px/1.05 'Arial Narrow',Arial,Helvetica,sans-serif;text-transform:uppercase;color:#fff;margin-top:6px;">{esc(t["nombre"])}</div>
    <div style="font:13px/1.4 Arial,Helvetica,sans-serif;color:#C9D7E6;margin-top:12px;">{esc(t["num"])} {esc(numero)} · {esc(titulo_fecha(numero, lang))}</div>
  </td></tr>
  <tr><td style="padding:26px 30px 0;font:17px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">
    <div style="font:800 24px/1.25 Arial,Helvetica,sans-serif;color:{COLOR["marino"]};margin-bottom:10px;">{esc(c.get("asunto"))}</div>
    {"".join(f'<p style="margin:0 0 12px;">{texto_html(p)}</p>' for p in str(c.get("editorial", "")).split(chr(10) + chr(10)) if p.strip())}
  </td></tr>
  <tr><td style="padding:22px 25px 0;">
    <div style="font:800 13px/1 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:{COLOR["rojo"]};margin:0 5px 12px;border-top:3px solid {COLOR["marino"]};padding-top:14px;">{esc(t["mar_h"])}</div>
    {bloque_mar(mar, lang)}
    {f'<p style="margin:12px 5px 0;font:15px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">{texto_html(c.get("comentario_mar"))}</p>' if c.get("comentario_mar") else ""}
  </td></tr>
  {"".join(secciones)}
  <tr><td style="padding:10px 30px 30px;" align="left">
    <a href="{DOMINIO}/{"es/" if lang == "es" else ""}" style="display:inline-block;background:{COLOR["amarillo"]};color:{COLOR["marino"]};font:700 16px/1 Arial,Helvetica,sans-serif;text-decoration:none;padding:15px 22px;">{esc(t["salidas"])} →</a>
  </td></tr>
  <tr><td style="background:{COLOR["marino"]};padding:20px 30px;font:12px/1.6 Arial,Helvetica,sans-serif;color:#C9D7E6;">
    <strong style="color:#fff;">Sea With Jose</strong> · Puerto José Banús, Marbella<br>{esc(t["pie"])}<br>{enlaces_pie}
  </td></tr>
</table>
</td></tr></table>
</body></html>
"""


# ─────────────────────────────── estado de cada número ───────────────────────────────
def ruta_estado(numero):
    return os.path.join(BORRADORES, f"{numero}.json")


def guardar_estado(e):
    os.makedirs(BORRADORES, exist_ok=True)
    with open(ruta_estado(e["numero"]), "w", encoding="utf-8", newline="\n") as f:
        json.dump(e, f, ensure_ascii=False, indent=1)


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def guardar_vista(e):
    for lang in IDIOMAS:
        escribir(os.path.join(BORRADORES, f"{e['numero']}-v{e['version']}-{lang}.html"),
                 montar(e["numero"], e["version"], e["contenido"], e["mar"], lang, "borrador"))


def enlaces_vista(e):
    return {lang: f"{DOMINIO}/revista/borradores/{e['numero']}-v{e['version']}-{lang}.html" for lang in IDIOMAS}


def salida(comentario, cerrar=False):
    with open(SALIDA_TMP, "w", encoding="utf-8") as f:
        json.dump({"comentario": comentario, "cerrar": cerrar}, f, ensure_ascii=False)


# ─────────────────────────────── GitHub ───────────────────────────────
def github(ruta, datos=None, metodo=None):
    repo = os.environ["GITHUB_REPOSITORY"]
    return pedir_json(f"https://api.github.com/repos/{repo}{ruta}", datos,
                      {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"},
                      metodo)


def editor():
    return os.environ.get("REVISTA_EDITOR") or os.environ.get("GITHUB_REPOSITORY", "/").split("/")[0]


# ─────────────────────────────── órdenes ───────────────────────────────
def cmd_borrador(numero=None, notas=""):
    numero = numero or numero_de(datetime.date.today() + datetime.timedelta(days=1))
    if os.path.exists(ruta_estado(numero)) and json.load(open(ruta_estado(numero), encoding="utf-8"))["estado"] == "publicado":
        sys.exit(f"El número {numero} ya está publicado.")
    mar = datos_mar(numero)
    print("Mar:", texto_mar(mar, "es"))
    contenido = redactar(numero, mar, notas)
    e = {"numero": numero, "version": 1, "estado": "pendiente", "mar": mar, "contenido": contenido,
         "historial": [f"v1 · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC · borrador"]}
    guardar_estado(e)
    guardar_vista(e)
    print("Borrador listo:", numero, enlaces_vista(e))


def cmd_abrir():
    estados = [json.load(open(os.path.join(BORRADORES, f), encoding="utf-8"))
               for f in os.listdir(BORRADORES) if f.endswith(".json")]
    e = max((x for x in estados if x["estado"] == "pendiente"), key=lambda x: x["numero"])
    v = enlaces_vista(e)
    asunto_es = e["contenido"]["es"].get("asunto", "")
    cuerpo = (f"@{editor()} ya está el borrador de la **Bitácora del mar nº {e['numero']}** "
              f"({titulo_fecha(e['numero'], 'es')}).\n\n"
              f"**{asunto_es}**\n\n"
              f"- Vista previa en español: {v['es']}\n- Vista previa en inglés: {v['en']}\n\n"
              "(Los enlaces tardan uno o dos minutos en funcionar.)\n\n"
              "**Responde a este correo** (o comenta aquí):\n"
              "- **OK** → se publica en la web y se envía a los suscritos de cada idioma.\n"
              "- **Cualquier cambio** («quita la noticia de…», «el editorial más corto», «añade que…») → "
              "llega una versión nueva para revisar.\n")
    r = github("/issues", {"title": f"Bitácora del mar nº {e['numero']} · borrador", "body": cuerpo,
                           "labels": ["revista"], "assignees": [editor()]})
    print("Incidencia abierta:", r.get("html_url"))


def es_ok(texto):
    t = re.sub(r"[^a-záéíóúñ ]", " ", texto.lower()).split()
    # Solo un OK limpio («ok», «vale, envíalo», «perfecto»); si hay algo más («ok pero quita…»), decide la IA
    if not t or len(t) > 3 or {"pero", "but", "quita", "cambia", "añade", "remove", "change", "add"} & set(t):
        return False
    return t[0] in {"ok", "okay", "okey", "vale", "adelante", "aprobado", "aprobada",
                                                 "envía", "envia", "enviar", "publica", "publicar", "sí", "si", "perfecto"}


def limpiar_respuesta(texto):
    """Quita la cita del correo original (GitHub ya suele hacerlo)."""
    lineas = []
    for l in (texto or "").splitlines():
        if l.startswith(">") or re.match(r"^(El|On) .+(escribió|wrote):\s*$", l.strip()):
            break
        lineas.append(l)
    return "\n".join(lineas).strip()


def cmd_revisar():
    m = re.search(r"nº (\d{4}-\d{2}-[12])", os.environ.get("ISSUE_TITLE", ""))
    if not m or not os.path.exists(ruta_estado(m.group(1))):
        salida("No encuentro el borrador de esta incidencia.")
        return
    e = json.load(open(ruta_estado(m.group(1)), encoding="utf-8"))
    if e["estado"] == "publicado":
        salida(f"El nº {e['numero']} ya está publicado y enviado; no he hecho nada.")
        return
    respuesta = limpiar_respuesta(os.environ.get("COMMENT_BODY", ""))
    if not respuesta:
        salida("Tu respuesta llegó vacía. Escribe **OK** para enviar o los cambios que quieras.")
        return
    if es_ok(respuesta):
        publicar(e)
        return
    r = ia(instrucciones("revision"), json.dumps({"contenido": e["contenido"], "cifras_es": texto_mar(e["mar"], "es"),
                                                  "cifras_en": texto_mar(e["mar"], "en"), "respuesta_de_jose": respuesta},
                                                 ensure_ascii=False))
    if r.get("decision") == "aprobado":
        publicar(e)
        return
    if r.get("decision") != "correcciones" or not r.get("contenido"):
        salida(f"No tengo claro qué quieres cambiar ({r.get('comentario', 'sin explicación')}). "
               "Escribe **OK** para enviar tal cual, o dime los cambios.")
        return
    e["version"] += 1
    e["contenido"] = r["contenido"]
    cambios = r.get("cambios_aplicados") or []
    e["historial"].append(f"v{e['version']} · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC · "
                          + "; ".join(cambios))
    guardar_estado(e)
    guardar_vista(e)
    v = enlaces_vista(e)
    salida(f"Versión {e['version']} lista.\n\n**Cambios:** " + ("; ".join(cambios) or "—")
           + (f"\n\n**No he podido:** {'; '.join(r['cambios_no_aplicados'])}" if r.get("cambios_no_aplicados") else "")
           + f"\n\n- Español: {v['es']}\n- Inglés: {v['en']}\n\nResponde **OK** para enviar, o más cambios.")


def brevo(ruta, datos=None):
    return pedir_json(f"https://api.brevo.com/v3{ruta}", datos,
                      {"api-key": os.environ["BREVO_API_KEY"], "Accept": "application/json"}, "POST")


def publicar(e):
    numero = e["numero"]
    for lang in IDIOMAS:
        escribir(os.path.join(CARPETA, f"{numero}-{lang}.html"), montar(numero, e["version"], e["contenido"], e["mar"], lang, "web"))
    try:
        indice = json.load(open(INDICE, encoding="utf-8"))
    except (OSError, ValueError):
        indice = []
    indice = [x for x in indice if x["numero"] != numero] + [{
        "numero": numero,
        "fecha": {"es": titulo_fecha(numero, "es"), "en": titulo_fecha(numero, "en"), "ru": titulo_fecha(numero, "en")},
        "titulos": {lang: e["contenido"][lang].get("asunto", "") for lang in IDIOMAS},
        "archivos": {lang: f"{numero}-{lang}.html" for lang in IDIOMAS}}]
    escribir(INDICE, json.dumps(indice, ensure_ascii=False, indent=1))
    subprocess.run([sys.executable, os.path.join(RAIZ, "build.py")], check=True)
    enviados = []
    for lang in IDIOMAS:
        lista = os.environ.get(f"BREVO_LISTA_{lang.upper()}")
        if not (lista and os.environ.get("BREVO_API_KEY")):
            enviados.append(f"{lang}: sin lista o sin clave de Brevo, no enviado")
            continue
        c = e["contenido"][lang]
        camp = brevo("/emailCampaigns", {
            "name": f"Bitácora {numero} ({lang})", "subject": c.get("asunto", TXT[lang]["nombre"]),
            "previewText": c.get("entradilla", "")[:150],
            "sender": {"name": "Sea With Jose", "email": REMITENTE}, "replyTo": os.environ.get("REVISTA_RESPONDER", REMITENTE),
            "recipients": {"listIds": [int(lista)]}, "mirrorActive": True,
            "htmlContent": montar(numero, e["version"], e["contenido"], e["mar"], lang, "brevo")})
        brevo(f"/emailCampaigns/{camp['id']}/sendNow")
        enviados.append(f"{lang}: campaña {camp['id']} enviada a la lista {lista}")
    e["estado"] = "publicado"
    e["historial"].append(f"v{e['version']} · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC · "
                          "aprobado y publicado · " + " · ".join(enviados))
    guardar_estado(e)
    salida(f"Publicado el nº {numero}.\n\n- Web: {DOMINIO}/revista/{numero}-es.html · {DOMINIO}/revista/{numero}-en.html\n"
           + "".join(f"- {x}\n" for x in enviados), cerrar=True)


def cmd_comentar():
    if not os.path.exists(SALIDA_TMP):
        return
    s = json.load(open(SALIDA_TMP, encoding="utf-8"))
    n = os.environ["ISSUE_NUMBER"]
    github(f"/issues/{n}/comments", {"body": s["comentario"]})
    if s.get("cerrar"):
        github(f"/issues/{n}", {"state": "closed"}, "PATCH")
    os.remove(SALIDA_TMP)


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if orden == "borrador":
        cmd_borrador(sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None, os.environ.get("REVISTA_NOTAS", ""))
    elif orden == "abrir":
        cmd_abrir()
    elif orden == "revisar":
        cmd_revisar()
    elif orden == "comentar":
        cmd_comentar()
    else:
        sys.exit(__doc__)
