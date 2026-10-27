# -*- coding: utf-8 -*-
"""Bitácora del mar: la newsletter semanal del tiempo en Marbella de Sea With Jose, en español y en inglés.

    python scripts/revista.py borrador [AAAA-MM-DD]  prepara el número del día de envío indicado y su versión 1
    python scripts/revista.py abrir                  abre la incidencia de GitHub para aprobarlo (tras subir los ficheros)
    python scripts/revista.py revisar                lee la respuesta de Jose: OK publica y programa el envío; si no, nueva versión
    python scripts/revista.py comentar               contesta en la incidencia (tras subir los ficheros)

Cada número es el tiempo en Marbella: cómo han sido los últimos 7 días (AEMET, Marbella Puerto), qué dice la
previsión de AEMET para la semana que entra, y el mar (agua, olas, racha y luna). Se envía cada semana el día
DIA_ENVIO a la HORA_ENVIO (hora de Madrid). Para cambiarlo, toca esas dos constantes y el cron de
`revista-borrador.yml` (el borrador sale unas horas antes, para que Jose lo apruebe a tiempo).

El circuito, todo en GitHub Actions y sin servidor:

  1. `revista-borrador.yml` (el día de envío por la mañana, o a mano) ejecuta `borrador`: junta los datos del
     tiempo y del mar y la IA escribe los comentarios en los dos idiomas. El HTML lo monta este script con la
     plantilla de abajo: la IA no escribe ninguna cifra.
  2. `abrir` crea una incidencia con la etiqueta «revista» que menciona a Jose:
     GitHub se la manda por correo con los enlaces a la vista previa.
  3. Jose responde a ese correo (o comenta en la incidencia). `revista-revision.yml`
     ejecuta `revisar`: «OK» → se publica en seawithjose.es/revista/ y se programa en Brevo para el día y la hora
     de envío (si ya han pasado, sale en el momento); cualquier otra cosa → la IA aplica los cambios y sale la
     versión siguiente.

Variables de entorno (secretos y variables del repositorio):
  OPENAI_API_KEY, REVISTA_MODELO (por defecto gpt-5.6-terra)
  BREVO_API_KEY, BREVO_LISTA_ES, BREVO_LISTA_EN, REVISTA_REMITENTE (por defecto jose@seawithjose.es), REVISTA_REMITENTE_NOMBRE
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
PARTE = os.path.join(RAIZ, "datos", "mar.json")
SALIDA_TMP = os.path.join(RAIZ, ".revista_salida.json")
ULTIMO_TMP = os.path.join(RAIZ, ".revista_ultimo")
DOMINIO = "https://seawithjose.es"
LAT, LON = 36.47, -4.95                       # frente a Puerto Banús
IDIOMAS = ("es", "en")
DIA_ENVIO = 1                                 # 0 lunes … 6 domingo (martes; más adelante, domingo = 6)
HORA_ENVIO = (14, 0)                          # hora de Madrid (más adelante, (17, 0))
DIAS = 7                                      # días que repasa cada número

MODELO = os.environ.get("REVISTA_MODELO") or "gpt-5.6-terra"
REMITENTE = os.environ.get("REVISTA_REMITENTE") or "jose@seawithjose.es"
REMITENTE_NOMBRE = os.environ.get("REVISTA_REMITENTE_NOMBRE") or "Jose · Sea With Jose"

COLOR = {"marino": "#0B2D52", "azul": "#1F4E9A", "amarillo": "#FFC20E", "rojo": "#D2232A", "tinta": "#0D1B2A",
         "gris": "#4E5F70", "cielo": "#E7F1F7", "linea": "#CFDCE5"}

TXT = {
    "es": {"nombre": "Bitácora del mar", "de": "Sea With Jose · El tiempo en Marbella", "num": "Nº", "semana": "Semana del {d}",
           "meses": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split(),
           "mar_h": "El mar", "agua": "Agua (media de la semana)", "rango": "mín. {a} · máx. {b} °C",
           "vs": "{d} °C {s} que hace un año", "mas": "más", "menos": "menos", "igual": "igual que hace un año",
           "ola": "Ola más alta (últimos 7 días)", "viento": "Racha más fuerte", "luna": "Luna", "hoy": "Agua hoy (AEMET)",
           "fases": {"nueva": "Luna nueva", "llena": "Luna llena", "creciente": "Cuarto creciente", "menguante": "Cuarto menguante"},
           "fuentes": "Datos: Open-Meteo (Copernicus Marine, ERA5) y AEMET, frente a Puerto Banús.",
           "datos_h": "Lo que dicen los datos", "tiempo_h": "Los últimos 7 días", "prevision_h": "La semana que viene",
           "ultimos": "Los últimos 7 días", "proximos": "Previsión de AEMET para Marbella",
           "t_max": "Máxima", "t_min": "Mínima", "t_lluvia": "Lluvia", "t_racha": "Racha más fuerte", "t_viento": "Viento",
           "dias_lluvia": "{n} día(s) de lluvia", "levante_poniente": "{l} días de levante · {p} de poniente",
           "dias_sem": "lun mar mié jue vie sáb dom".split(),
           "graf_alt": "Gráfica: temperatura del agua y viento en la quincena, y cambio medio del agua según la dirección del viento",
           "fuentes_tiempo": "Datos: AEMET, estación Marbella Puerto (6076X) y predicción para Marbella. Agua: Copernicus Marine (satélite y modelo de la UE).",
           "leer": "Leer en", "web": "Ver en la web", "datos": "Ver todos los datos de Marbella, hora a hora", "baja": "Darse de baja",
           "pie": "Recibes la Bitácora porque te suscribiste en seawithjose.es.", "salidas": "Salir a navegar, bucear o pescar conmigo",
           "pesca_h": "La pesca esta semana", "actividad": ["", "baja", "media", "alta", "muy alta"],
           "graf_pesca_alt": "Gráfica: las mejores horas para pescar cada día de la semana que viene y la actividad de los peces",
           "salir_h": "¿Cuándo salir al mar?", "c_dia": "Día", "c_vela": "Vela", "c_fondo": "Pesca a fondo",
           "c_currican": "Curricán", "c_peces": "Peces", "c_horas": "Mejores horas de pesca", "c_mareas": "Mareas",
           "notas": ["No", "Regular", "Bueno", "Muy bueno"], "pleamar": "Pleamar", "bajamar": "Bajamar",
           "leyenda_salir": ("Notas entre las 9:00 y las 20:00 para un velero de 12 m: viento, rachas, ola y lluvia (Open-Meteo y Copernicus). "
                             "Peces: actividad de 1 a 4 según la teoría solunar (fase de la luna y si un periodo mayor coincide con el alba "
                             "o el ocaso). Mejores horas: los periodos solunares de día; ★ = coincide con el alba o el ocaso. Mareas: pleamares (▲) "
                             "y bajamares (▼), del modelo de nivel del mar de Copernicus Marine."),
           "graf_semana_alt": "Gráfica: temperatura del agua y viento de cada día de la semana pasada",
           "graf_plan_alt": "Gráfica: viento, rachas, olas, marea y probabilidad de lluvia de la semana que viene, hora a hora",
           "aviso": "Borrador para tu aprobación · versión {v}",
           "aviso_p": "Responde «OK» al correo de GitHub (o comenta en la incidencia) y se publica y se programa el envío. Si quieres cambios, escríbelos en tu respuesta."},
    "en": {"nombre": "The Sea Logbook", "de": "Sea With Jose · Marbella weather", "num": "No.", "semana": "Week of {d}",
           "meses": "January February March April May June July August September October November December".split(),
           "mar_h": "The sea", "agua": "Water (weekly average)", "rango": "min {a} · max {b} °C",
           "vs": "{d} °C {s} than a year ago", "mas": "warmer", "menos": "cooler", "igual": "same as a year ago",
           "ola": "Highest wave (last 7 days)", "viento": "Strongest gust", "luna": "Moon", "hoy": "Water today (AEMET)",
           "fases": {"nueva": "New moon", "llena": "Full moon", "creciente": "First quarter", "menguante": "Last quarter"},
           "fuentes": "Data: Open-Meteo (Copernicus Marine, ERA5) and AEMET, off Puerto Banús.",
           "datos_h": "What the data say", "tiempo_h": "The last 7 days", "prevision_h": "The week ahead",
           "ultimos": "The last 7 days", "proximos": "AEMET forecast for Marbella",
           "t_max": "High", "t_min": "Low", "t_lluvia": "Rain", "t_racha": "Strongest gust", "t_viento": "Wind",
           "dias_lluvia": "{n} rainy day(s)", "levante_poniente": "{l} easterly days · {p} westerly",
           "dias_sem": "Mon Tue Wed Thu Fri Sat Sun".split(),
           "graf_alt": "Chart: water temperature and wind this fortnight, and average change in the water by wind direction",
           "fuentes_tiempo": "Data: AEMET, Marbella Marina station (6076X) and Marbella forecast. Water: Copernicus Marine (EU satellite and model).",
           "leer": "Read on", "web": "View on the website", "datos": "See all the Marbella data, hour by hour", "baja": "Unsubscribe",
           "pie": "You get the Logbook because you subscribed at seawithjose.es.", "salidas": "Come sailing, diving or fishing with me",
           "pesca_h": "Fishing this week", "actividad": ["", "low", "fair", "high", "very high"],
           "graf_pesca_alt": "Chart: the best hours to fish each day of the week ahead and fish activity",
           "salir_h": "When to go out to sea?", "c_dia": "Day", "c_vela": "Sailing", "c_fondo": "Bottom fishing",
           "c_currican": "Trolling", "c_peces": "Fish", "c_horas": "Best fishing hours", "c_mareas": "Tides",
           "notas": ["No", "Fair", "Good", "Very good"], "pleamar": "High tide", "bajamar": "Low tide",
           "leyenda_salir": ("Ratings from 9:00 to 20:00 for a 12 m sailing boat: wind, gusts, waves and rain (Open-Meteo and Copernicus). "
                             "Fish: activity from 1 to 4 according to solunar theory (moon phase and whether a major period falls at "
                             "dawn or dusk). Best hours: the daytime solunar periods; ★ = at dawn or dusk. Tides: high (▲) and low (▼), "
                             "from the Copernicus Marine sea-level model."),
           "graf_semana_alt": "Chart: water temperature and wind for each day of last week",
           "graf_plan_alt": "Chart: wind, gusts, waves, tide and chance of rain for the week ahead, hour by hour",
           "aviso": "Draft for your approval · version {v}",
           "aviso_p": "Reply “OK” to the GitHub email (or comment on the issue) and it will be published and scheduled."},
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
    """El número es la fecha de envío (AAAA-MM-DD): el primer día de envío desde `fecha`, incluida."""
    fecha += datetime.timedelta(days=(DIA_ENVIO - fecha.weekday()) % 7)
    return fecha.isoformat()


def salida_de(numero):
    return datetime.date.fromisoformat(numero)


def periodo(numero):
    """Días que repasa un número: los DIAS anteriores a su envío."""
    fin = salida_de(numero) - datetime.timedelta(days=1)
    return fin - datetime.timedelta(days=DIAS - 1), fin


def envio(numero):
    """Día y hora de envío, en hora de Madrid."""
    from zoneinfo import ZoneInfo
    return datetime.datetime.combine(salida_de(numero), datetime.time(*HORA_ENVIO), ZoneInfo("Europe/Madrid"))


def fecha_larga(d, lang):
    mes = TXT[lang]["meses"][d.month - 1]
    return f"{d.day} de {mes} de {d.year}" if lang == "es" else f"{d.day} {mes} {d.year}"


def titulo_fecha(numero, lang):
    return TXT[lang]["semana"].format(d=fecha_larga(salida_de(numero), lang))


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
    # las dos próximas fases de la luna (en una semana puede no haber ninguna), que es lo que le sirve a quien pesca
    salida = salida_de(numero)
    out["luna"] = [(d.isoformat(), f) for d, f in fases_luna(salida, salida + datetime.timedelta(days=15))][:2]
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
    if mar.get("luna"):
        partes.append("luna: " + ", ".join(f"{t['fases'][f]} {d}" for d, f in mar["luna"]))
    return "; ".join(partes)


# ─────────────────────────────── enlaces de las noticias (solo números antiguos) ───────────────────────────────
def resolver(contenido, refs):
    """Pone a cada noticia el enlace y la fuente exactos de su código. Una noticia sin código válido se queda sin
    enlace (nunca con uno inventado); una sección que se queda vacía, desaparece."""
    validas = {r["url"] for r in refs.values()}
    avisos = []
    for lang in IDIOMAS:
        for s in contenido.get(lang, {}).get("secciones", []):
            for i in s.get("items", []):
                r = refs.get(str(i.get("ref", "")).strip())
                if r:
                    i["url"], i["fuente"] = r["url"], r["fuente"]
                elif i.get("url") not in validas:
                    if i.get("url"):
                        avisos.append(f"{lang}: «{i.get('titular', '')[:60]}» sin enlace válido")
                    i["url"] = ""
            s["items"] = [i for i in s.get("items", []) if i.get("titular")]
        if lang in contenido:
            contenido[lang]["secciones"] = [s for s in contenido[lang].get("secciones", []) if s["items"]]
    for a in avisos:
        print("  aviso:", a)
    return contenido


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
    salida = salida_de(numero)
    usuario = [f"NÚMERO: {numero} (sale el {salida.isoformat()}, {['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'][salida.weekday()]})",
               f"NOTAS DE JOSE: {notas or '(ninguna)'}",
               f"\nCIFRAS DEL MAR ({mar['desde']} a {mar['hasta']}): {texto_mar(mar, 'es')}",
               f"\nTIEMPO DE LOS ÚLTIMOS {DIAS} DÍAS (AEMET, Marbella Puerto): {json.dumps(mar.get('tiempo') or {}, ensure_ascii=False)}",
               f"\nPREVISIÓN DE AEMET PARA MARBELLA, DÍA A DÍA: {json.dumps(mar.get('prevision') or [], ensure_ascii=False)}"]
    if mar.get("hechos"):
        usuario += ["\n=== HECHOS CALCULADOS: EL AGUA FRENTE AL VIENTO (para «datos_titulo» y «datos_texto») ===", mar["hechos"]]
    if mar.get("hechos_salir"):
        usuario += ["\n=== PLAN PARA SALIR AL MAR LA SEMANA QUE VIENE (para «pesca_comentario», «salir_comentario» y «prevision_comentario») ===",
                    mar["hechos_salir"]]
    return ia(instrucciones("redaccion"), "\n".join(usuario)), {}


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
    # la racha va en «Los últimos 7 días», con el dato oficial de AEMET (el de Open-Meteo es de modelo y no coincide)
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


def titulo_seccion(texto):
    return (f'<div style="font:800 13px/1 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;'
            f'color:{COLOR["rojo"]};margin-bottom:12px;border-top:3px solid {COLOR["marino"]};padding-top:14px;">{esc(texto)}</div>')


def bloque_tiempo(c, mar, lang):
    """Dos bloques: cómo han sido los últimos días y la previsión de la semana que viene, cada uno con su comentario."""
    t, q, prev = TXT[lang], mar.get("tiempo") or {}, mar.get("prevision") or []
    if not (q or prev):
        return bloque_datos(c, mar, lang) + bloque_salir(c, mar, lang)
    def dia(f):
        d = datetime.date.fromisoformat(f)
        return f"{t['dias_sem'][d.weekday()]} {d.day}/{d.month}"
    def parrafos(texto):
        return "".join(f'<p style="margin:0 0 12px;">{texto_html(p)}</p>' for p in str(texto or "").split("\n\n") if p.strip())
    celdas = []
    if "tmax" in q:
        celdas.append((t["t_max"], f"{fmt(q['tmax'], lang)} °C", dia(q["tmax_dia"])))
    if "tmin" in q:
        celdas.append((t["t_min"], f"{fmt(q['tmin'], lang)} °C", dia(q["tmin_dia"])))
    if "lluvia_total" in q:
        celdas.append((t["t_lluvia"], f"{fmt(q['lluvia_total'], lang)} mm", t["dias_lluvia"].format(n=q["dias_lluvia"])))
    if "racha_max" in q:
        celdas.append((t["t_racha"], f"{q['racha_max']} km/h", f"{q.get('racha_dir', '')} · {dia(q['racha_dia'])}"))
    tarjetas = "".join(
        f'<td width="25%" valign="top" style="padding:4px;"><div style="background:{COLOR["cielo"]};padding:12px;font-family:Arial,Helvetica,sans-serif;">'
        f'<div style="font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:{COLOR["gris"]};font-weight:700;">{esc(a)}</div>'
        f'<div style="font-size:20px;font-weight:800;color:{COLOR["marino"]};margin-top:3px;">{esc(b)}</div>'
        f'<div style="font-size:12px;color:{COLOR["gris"]};margin-top:2px;">{esc(x)}</div></div></td>' for a, b, x in celdas)
    extra = (f'<p style="margin:8px 4px 0;font:13px/1.5 Arial,Helvetica,sans-serif;color:{COLOR["gris"]};">'
             f'{esc(t["levante_poniente"].format(l=q["dias_levante"], p=q["dias_poniente"]))}</p>') if "dias_levante" in q else ""
    filas = "".join(
        f'<tr><td style="padding:7px 6px;border-bottom:1px solid {COLOR["linea"]};font-weight:700;color:{COLOR["marino"]};">{esc(dia(p["fecha"]))}</td>'
        f'<td style="padding:7px 6px;border-bottom:1px solid {COLOR["linea"]};">{esc(p.get("cielo") or "")}</td>'
        f'<td style="padding:7px 6px;border-bottom:1px solid {COLOR["linea"]};white-space:nowrap;">{p["tmax"] if p.get("tmax") is not None else "–"}° / {p["tmin"] if p.get("tmin") is not None else "–"}°</td>'
        f'<td style="padding:7px 6px;border-bottom:1px solid {COLOR["linea"]};white-space:nowrap;">{"" if p.get("lluvia") is None else str(p["lluvia"]) + " %"}</td>'
        f'<td style="padding:7px 6px;border-bottom:1px solid {COLOR["linea"]};white-space:nowrap;">{esc(p.get("viento_dir") or "")} {p.get("viento") or ""}{" km/h" if p.get("viento") else ""}</td></tr>'
        for p in prev)
    caja = f'<tr><td style="padding:26px 30px 0;font:16px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">'
    ultimos = (caja + titulo_seccion(t["tiempo_h"]) + parrafos(c.get("tiempo_comentario"))
               + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>{tarjetas}</tr></table>{extra}'
               + "</td></tr>") if celdas else ""
    proximos = (caja + titulo_seccion(t["prevision_h"]) + parrafos(c.get("prevision_comentario"))
                + imagen(mar, "plan", lang, t["graf_plan_alt"])
                + f'<div style="font:700 14px/1.3 Arial,Helvetica,sans-serif;color:{COLOR["marino"]};margin:4px 0 4px;">{esc(t["proximos"])}</div>'
                f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font:13px/1.4 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">{filas}</table>'
                + f'<p style="margin:10px 0 0;font:12px/1.5 Arial,Helvetica,sans-serif;color:{COLOR["gris"]};">{esc(t["fuentes_tiempo"])}</p>'
                + "</td></tr>") if prev else ""
    return ultimos + bloque_datos(c, mar, lang) + proximos + bloque_pesca(c, mar, lang) + bloque_salir(c, mar, lang)


def bloque_pesca(c, mar, lang):
    """La pesca esta semana: el comentario y la gráfica de las mejores horas de cada día."""
    t = TXT[lang]
    if not (c.get("pesca_comentario") or (mar.get("graficas") or {}).get("pesca")):
        return ""
    return (f'<tr><td style="padding:26px 30px 0;font:16px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">'
            + titulo_seccion(t["pesca_h"])
            + "".join(f'<p style="margin:0 0 12px;">{texto_html(p)}</p>' for p in str(c.get("pesca_comentario", "")).split("\n\n") if p.strip())
            + imagen(mar, "pesca", lang, t["graf_pesca_alt"])
            + "</td></tr>")


def imagen(mar, nombre, lang, alt):
    url = (mar.get("graficas") or {}).get(nombre, {}).get(lang)
    return (f'<img src="{esc(url)}" width="580" alt="{esc(alt)}" style="display:block;width:100%;max-width:580px;height:auto;'
            f'margin:6px 0 14px;border:1px solid {COLOR["linea"]};">') if url else ""


def bloque_datos(c, mar, lang):
    """Lo que dicen los datos: una coincidencia de la semana con su explicación, y la gráfica del agua y el viento."""
    t = TXT[lang]
    if not (c.get("datos_texto") or (mar.get("graficas") or {}).get("semana")):
        return ""
    return (f'<tr><td style="padding:26px 30px 0;font:16px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">'
            + titulo_seccion(t["datos_h"])
            + (f'<div style="font:800 19px/1.3 Arial,Helvetica,sans-serif;color:{COLOR["marino"]};margin-bottom:8px;">{esc(c["datos_titulo"])}</div>' if c.get("datos_titulo") else "")
            + "".join(f'<p style="margin:0 0 12px;">{texto_html(p)}</p>' for p in str(c.get("datos_texto", "")).split("\n\n") if p.strip())
            + imagen(mar, "semana", lang, t["graf_semana_alt"])
            + "</td></tr>")


def bloque_salir(c, mar, lang):
    """¿Cuándo salir al mar?: la nota de cada día para vela, pesca a fondo y curricán, la actividad de los peces,
    las mejores horas de pesca y las mareas."""
    t, dias = TXT[lang], mar.get("plan") or []
    if not dias:
        return ""
    fondo = {3: "#1E7B3A", 2: "#5DB36B", 1: COLOR["amarillo"], 0: COLOR["rojo"]}
    letra = {3: "#fff", 2: "#fff", 1: COLOR["marino"], 0: "#fff"}
    celda = f'padding:6px 4px;border-bottom:1px solid {COLOR["linea"]};vertical-align:middle;'
    def dia(f):
        d = datetime.date.fromisoformat(f)
        return f"{t['dias_sem'][d.weekday()]} {d.day}/{d.month}"
    def nota(n):
        return (f'<span style="display:inline-block;min-width:58px;padding:3px 4px;border-radius:3px;text-align:center;'
                f'background:{fondo[n]};color:{letra[n]};font-weight:700;font-size:11px;">{esc(t["notas"][n])}</span>')
    filas = []
    for d in dias:
        peces = "●" * (d.get("actividad_peces") or 0) + "○" * (4 - (d.get("actividad_peces") or 0))
        horas = "<br>".join(f'{p["desde"]}–{p["hasta"]}{" ★" if p["alba_ocaso"] else ""}' for p in d.get("horas_pesca", [])) or "—"
        mareas = "<br>".join(f'{"▲" if e["tipo"] == "pleamar" else "▼"} {e["momento"][11:]}' for e in d.get("mareas", [])) or "—"
        filas.append(
            f'<tr><td style="{celda}font-weight:700;color:{COLOR["marino"]};white-space:nowrap;">{esc(dia(d["fecha"]))}</td>'
            f'<td style="{celda}" align="center">{nota(d["notas"]["vela"])}</td>'
            f'<td style="{celda}" align="center">{nota(d["notas"]["fondo"])}</td>'
            f'<td style="{celda}" align="center">{nota(d["notas"]["currican"])}</td>'
            f'<td style="{celda}color:{COLOR["azul"]};white-space:nowrap;letter-spacing:1px;" align="center">{peces}'
            f'<br><span style="letter-spacing:0;font-size:10px;color:{COLOR["gris"]};">{esc(t["actividad"][d.get("actividad_peces") or 0])}</span></td>'
            f'<td style="{celda}white-space:nowrap;">{horas}</td>'
            f'<td style="{celda}white-space:nowrap;color:{COLOR["gris"]};">{mareas}</td></tr>')
    cabecera = "".join(f'<th style="padding:6px 4px;border-bottom:2px solid {COLOR["marino"]};font-size:10px;letter-spacing:.06em;'
                       f'text-transform:uppercase;color:{COLOR["gris"]};text-align:left;">{esc(t[k])}</th>'
                       for k in ("c_dia", "c_vela", "c_fondo", "c_currican", "c_peces", "c_horas", "c_mareas"))
    return (f'<tr><td style="padding:26px 30px 0;font:16px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">'
            + titulo_seccion(t["salir_h"])
            + "".join(f'<p style="margin:0 0 12px;">{texto_html(p)}</p>' for p in str(c.get("salir_comentario", "")).split("\n\n") if p.strip())
            + f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;'
              f'font:12px/1.35 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};"><tr>{cabecera}</tr>{"".join(filas)}</table>'
            + f'<p style="margin:10px 0 0;font:12px/1.5 Arial,Helvetica,sans-serif;color:{COLOR["gris"]};">{esc(t["leyenda_salir"])}</p>'
            + "</td></tr>")


def texto_html(s):
    """Texto de la IA a HTML: escapa y deja solo **negritas**."""
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", rf'<strong style="color:{COLOR["marino"]};">\1</strong>', s)


def montar(numero, version, contenido, mar, lang, modo):
    """modo: «borrador» (con el recuadro de aprobación), «web» o «brevo» (con enlaces de baja de Brevo)."""
    t = TXT[lang]
    c = contenido[lang]
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
  {bloque_tiempo(c, mar, lang)}
  <tr><td style="padding:22px 25px 0;">
    <div style="font:800 13px/1 Arial,Helvetica,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:{COLOR["rojo"]};margin:0 5px 12px;border-top:3px solid {COLOR["marino"]};padding-top:14px;">{esc(t["mar_h"])}</div>
    {bloque_mar(mar, lang)}
    {f'<p style="margin:12px 5px 0;font:15px/1.6 Arial,Helvetica,sans-serif;color:{COLOR["tinta"]};">{texto_html(c.get("comentario_mar"))}</p>' if c.get("comentario_mar") else ""}
    <p style="margin:14px 5px 0;"><a href="{DOMINIO}/{"es/" if lang == "es" else ""}datos.html" style="color:{COLOR["azul"]};font:700 15px/1.4 Arial,Helvetica,sans-serif;">{esc(t["datos"])} →</a></p>
  </td></tr>
  <tr><td style="padding:26px 30px 30px;" align="left">
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
def analizar(numero, mar):
    """El tiempo de los últimos días, la previsión de AEMET y el cruce del agua con el viento (revista_datos.py);
    el plan para salir al mar la semana que viene (revista_salir.py); y las gráficas de cada idioma."""
    import revista_datos as rd
    import revista_salir as rs
    ini, fin = periodo(numero)
    salida = salida_de(numero)
    for clave, funcion in (("tiempo", lambda: rd.tiempo_quincena(ini, fin)), ("prevision", rd.prevision),
                           ("analisis", lambda: rd.analisis(ini, fin))):
        try:
            mar[clave] = funcion()
        except Exception as e:  # noqa: BLE001
            print(f"  {clave}: {e}")
    if mar.get("analisis"):
        mar["hechos"] = rd.texto_analisis(mar["analisis"], mar.get("tiempo"), mar.get("prevision"))
    horas = None
    try:
        horas = rs.horas(salida, DIAS)
        mar["plan"] = rs.plan(horas, rs.solunar(salida, DIAS), rs.mareas(horas), mar.get("prevision"))
        mar["hechos_salir"] = rs.texto_plan(mar["plan"])
    except Exception as e:  # noqa: BLE001
        print(f"  plan: {e}")
    for lang in IDIOMAS:
        for nombre, hacer in (("semana", lambda r, l: rs.grafica_semana(mar["analisis"]["quincena"], r, l) if mar.get("analisis") else None),
                              ("plan", lambda r, l: rs.grafica_plan(horas, None, r, l) if horas else None),
                              ("pesca", lambda r, l: rs.grafica_pesca(mar["plan"], r, l) if mar.get("plan") else None)):
            ruta = os.path.join(CARPETA, "graficas", f"{numero}-{nombre}-{lang}.png")
            try:
                hacer(ruta, lang)
                if os.path.exists(ruta):
                    mar.setdefault("graficas", {}).setdefault(nombre, {})[lang] = f"{DOMINIO}/revista/graficas/{numero}-{nombre}-{lang}.png"
            except Exception as e:  # noqa: BLE001
                print(f"  gráfica {nombre} {lang}: {e}")


def cmd_borrador(numero=None, notas=""):
    numero = numero or numero_de(datetime.date.today())
    if os.path.exists(ruta_estado(numero)) and json.load(open(ruta_estado(numero), encoding="utf-8"))["estado"] == "publicado":
        sys.exit(f"El número {numero} ya está publicado.")
    mar = datos_mar(numero)
    print("Mar:", texto_mar(mar, "es"))
    analizar(numero, mar)
    contenido, refs = redactar(numero, mar, notas)
    e = {"numero": numero, "version": 1, "estado": "pendiente", "mar": mar, "contenido": contenido, "refs": refs,
         "historial": [f"v1 · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC · borrador"]}
    guardar_estado(e)
    guardar_vista(e)
    with open(ULTIMO_TMP, "w", encoding="utf-8") as f:     # para que «abrir» abra justo este número
        f.write(numero)
    print("Borrador listo:", numero, enlaces_vista(e))


def cmd_abrir():
    e = json.load(open(ruta_estado(open(ULTIMO_TMP, encoding="utf-8").read().strip()), encoding="utf-8"))
    v = enlaces_vista(e)
    asunto_es = e["contenido"]["es"].get("asunto", "")
    cuerpo = (f"@{editor()} ya está el borrador de la **Bitácora del mar nº {e['numero']}** "
              f"({titulo_fecha(e['numero'], 'es')}).\n\n"
              f"**{asunto_es}**\n\n"
              f"- Vista previa en español: {v['es']}\n- Vista previa en inglés: {v['en']}\n\n"
              "(Los enlaces tardan uno o dos minutos en funcionar.)\n\n"
              "**Responde a este correo** (o comenta aquí):\n"
              f"- **OK** → se publica en la web y se programa el envío a los suscritos de cada idioma para el "
              f"{fecha_larga(salida_de(e['numero']), 'es')} a las {HORA_ENVIO[0]}:{HORA_ENVIO[1]:02d} "
              "(si apruebas más tarde, sale en el momento).\n"
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


def hora_pedida(texto):
    """«OK 18:30», «ok a las 19», «vale 9.15h» → (18, 30)…; sin hora, None (sale a la HORA_ENVIO)."""
    m = re.search(r"\b([01]?\d|2[0-3])(?:[:.h]([0-5]\d))?\s*(?:h|horas?)?\b", texto)
    return (int(m.group(1)), int(m.group(2) or 0)) if m else None


def limpiar_respuesta(texto):
    """Quita la cita del correo original (GitHub ya suele hacerlo)."""
    lineas = []
    for l in (texto or "").splitlines():
        # la cabecera de la cita («El mié, 14 oct 2026 a las 22:08, … escribió:») a veces se parte en dos líneas
        if (l.startswith(">") or re.match(r"^(El|On) \S+.*\d{4}", l.strip())
                or re.search(r"(escribió|wrote):\s*$", l)):
            break
        lineas.append(l)
    return "\n".join(lineas).strip()


def cmd_revisar():
    m = re.search(r"nº (\d{4}-\d{2}-(?:\d{2}|[12]))", os.environ.get("ISSUE_TITLE", ""))
    if not m or not os.path.exists(ruta_estado(m.group(1))):
        salida("No encuentro el borrador de esta incidencia.")
        return
    e = json.load(open(ruta_estado(m.group(1)), encoding="utf-8"))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["numero"]):
        salida(f"El nº {e['numero']} es de la revista quincenal antigua, con noticias; ya no se publica ni se envía.",
               cerrar=True)
        return
    if e["estado"] == "publicado":
        salida(f"El nº {e['numero']} ya está publicado y enviado; no he hecho nada.")
        return
    respuesta = limpiar_respuesta(os.environ.get("COMMENT_BODY", ""))
    if not respuesta:
        salida("Tu respuesta llegó vacía. Escribe **OK** para enviar o los cambios que quieras.")
        return
    if es_ok(respuesta):
        publicar(e, hora_pedida(respuesta))
        return
    r = ia(instrucciones("revision"), json.dumps({"contenido": e["contenido"], "cifras_es": texto_mar(e["mar"], "es"),
                                                  "cifras_en": texto_mar(e["mar"], "en"), "tiempo_ultimos_dias": e["mar"].get("tiempo"),
                                                  "prevision_aemet": e["mar"].get("prevision"), "agua_y_viento": e["mar"].get("hechos"),
                                                  "plan_para_salir": e["mar"].get("hechos_salir"), "respuesta_de_jose": respuesta},
                                                 ensure_ascii=False))
    if r.get("decision") == "aprobado":
        publicar(e, hora_pedida(respuesta))
        return
    if r.get("decision") != "correcciones" or not r.get("contenido"):
        salida(f"No tengo claro qué quieres cambiar ({r.get('comentario', 'sin explicación')}). "
               "Escribe **OK** para enviar tal cual, o dime los cambios.")
        return
    e["version"] += 1
    e["contenido"] = resolver(r["contenido"], e.get("refs", {}))
    cambios = r.get("cambios_aplicados") or []
    e["historial"].append(f"v{e['version']} · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC · "
                          + "; ".join(cambios))
    guardar_estado(e)
    guardar_vista(e)
    v = enlaces_vista(e)
    salida(f"Versión {e['version']} lista.\n\n**Cambios:** " + ("; ".join(cambios) or "—")
           + (f"\n\n**No he podido:** {'; '.join(r['cambios_no_aplicados'])}" if r.get("cambios_no_aplicados") else "")
           + f"\n\n- Español: {v['es']}\n- Inglés: {v['en']}\n\nResponde **OK** para enviar, o más cambios.")


def brevo(ruta, datos=None, metodo="POST"):
    return pedir_json(f"https://api.brevo.com/v3{ruta}", datos,
                      {"api-key": os.environ["BREVO_API_KEY"], "Accept": "application/json"}, metodo)


def publicar(e, hora=None):
    """`hora`: (h, m) si Jose pide otra hora al aprobar; si no, la HORA_ENVIO del día del número. Si esa hora ya ha
    pasado, el envío sale en el momento."""
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
    hechos = e.setdefault("enviados", {})          # idioma → campaña: lo ya enviado no se repite nunca
    cuando = envio(numero)
    if hora:
        from zoneinfo import ZoneInfo
        hoy = datetime.datetime.now(ZoneInfo("Europe/Madrid")).date()
        cuando = datetime.datetime.combine(max(hoy, salida_de(numero)), datetime.time(*hora), ZoneInfo("Europe/Madrid"))
    programar =cuando > datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
    for lang in IDIOMAS:
        lista = os.environ.get(f"BREVO_LISTA_{lang.upper()}")
        if hechos.get(lang):
            enviados.append(f"{lang}: ya enviado antes (campaña {hechos[lang]})")
            continue
        if not (lista and os.environ.get("BREVO_API_KEY")):
            enviados.append(f"{lang}: sin lista o sin clave de Brevo, no enviado")
            continue
        try:
            info = brevo(f"/contacts/lists/{int(lista)}", metodo="GET")
            suscritos = info.get("uniqueSubscribers", info.get("totalSubscribers", 0))
        except Exception:  # noqa: BLE001
            suscritos = None
        if suscritos == 0:
            enviados.append(f"{lang}: la lista {lista} aún no tiene suscriptores, no enviado")
            continue
        c = e["contenido"][lang]
        try:
            camp = brevo("/emailCampaigns", {
                "name": f"Bitácora {numero} ({lang})", "subject": c.get("asunto", TXT[lang]["nombre"]),
                "previewText": c.get("entradilla", "")[:150],
                "sender": {"name": REMITENTE_NOMBRE, "email": REMITENTE}, "replyTo": os.environ.get("REVISTA_RESPONDER", REMITENTE),
                "recipients": {"listIds": [int(lista)]}, "mirrorActive": True,
                "htmlContent": montar(numero, e["version"], e["contenido"], e["mar"], lang, "brevo"),
                **({"scheduledAt": cuando.isoformat()} if programar else {})})
            if not programar:
                brevo(f"/emailCampaigns/{camp['id']}/sendNow")
        except Exception as error:  # noqa: BLE001  (un idioma que falla no impide publicar ni enviar el otro)
            enviados.append(f"{lang}: Brevo no lo ha aceptado, no enviado ({str(error)[-160:]})")
            continue
        hechos[lang] = camp["id"]
        guardar_estado(e)
        enviados.append(f"{lang}: campaña {camp['id']} "
                        + (f"programada para el {cuando:%d/%m a las %H:%M}" if programar else "enviada")
                        + f" a la lista {lista}" + (f" ({suscritos} suscriptores)" if suscritos else ""))
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
