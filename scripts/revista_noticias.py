# -*- coding: utf-8 -*-
"""Bitácora del mar: recoge a diario las noticias de cada eje, en español y en inglés.

    python scripts/revista_noticias.py      -> datos/revista/noticias.json

Lo ejecuta la Action `revista-noticias.yml` una vez al día. Los RSS de Google
Noticias solo devuelven los últimos días, así que se acumula: el fichero guarda
una ventana de VENTANA días y la revista toma las de su quincena.

Cada noticia: fecha, eje, idioma, fuente, titular y enlace. No se guarda el
texto del artículo: la revista resume a partir del titular y enlaza a la fuente.
"""

import datetime
import email.utils
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "datos", "revista", "noticias.json")
VENTANA = 40          # días que se conservan
POR_CONSULTA = 25     # titulares que se leen de cada búsqueda

# Búsquedas de Google Noticias por eje e idioma (sintaxis de Google: OR, comillas, when:)
BUSQUEDAS = {
    "es": {
        "local": ['Marbella mar OR playa OR puerto', '"Costa del Sol" mar OR playas OR puerto deportivo'],
        "buceo": ['buceo OR submarinismo', '"buceo" Mediterráneo OR Andalucía'],
        "vela": ['vela regata OR velero', 'náutica puerto deportivo OR "salón náutico"'],
        "pesca": ['"pesca recreativa" OR "pesca deportiva"', 'pesca Mediterráneo veda OR capturas'],
        "viajes": ['viaje buceo OR "destino de buceo"', 'navegar vacaciones velero OR catamarán'],
        "ciencia": ['océano descubrimiento OR investigadores', 'ballena OR tiburón OR delfines OR orcas'],
    },
    "en": {
        "local": ['Marbella sea OR beach OR marina', '"Costa del Sol" sea OR beaches'],
        "buceo": ['"scuba diving"', 'divers reef OR wreck dive'],
        "vela": ['sailing regatta OR yacht', '"America\'s Cup" OR "Ocean Race" OR superyacht'],
        "pesca": ['"sea fishing" OR "sport fishing" OR angling', 'tuna OR swordfish fishing Mediterranean'],
        "viajes": ['"diving holiday" OR liveaboard', '"sailing holiday" OR "yacht charter" destination'],
        "ciencia": ['ocean scientists discovery', 'whale OR shark OR dolphin OR orca'],
    },
}
REGION = {"es": "hl=es&gl=ES&ceid=ES:es", "en": "hl=en-GB&gl=GB&ceid=GB:en"}


def pedir(url, reintentos=3):
    ultimo = None
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Bitacora del mar; seawithjose.es)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(3 * (i + 1))
    print("  sin respuesta:", url, ultimo)
    return None


def limpiar(texto):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", texto or ""))).strip()


def leer(lang, eje, consulta):
    url = (f"https://news.google.com/rss/search?q={urllib.parse.quote(consulta + ' when:14d')}&{REGION[lang]}")
    datos = pedir(url)
    if not datos:
        return []
    salida = []
    for item in list(ET.fromstring(datos).iter("item"))[:POR_CONSULTA]:
        titulo = limpiar(item.findtext("title"))
        fuente = limpiar(item.findtext("source")) or ""
        if fuente and titulo.endswith(" - " + fuente):
            titulo = titulo[: -len(fuente) - 3].strip()
        try:
            fecha = email.utils.parsedate_to_datetime(item.findtext("pubDate")).date().isoformat()
        except Exception:  # noqa: BLE001
            continue
        if len(titulo) < 25:
            continue
        salida.append({"fecha": fecha, "eje": eje, "lang": lang, "fuente": fuente, "titular": titulo,
                       "url": item.findtext("link") or ""})
    return salida


def clave(n):
    return re.sub(r"[^a-z0-9áéíóúñ]+", "", n["titular"].lower())[:80]


def main():
    try:
        viejas = json.load(open(SALIDA, encoding="utf-8")).get("noticias", [])
    except (OSError, ValueError):
        viejas = []
    nuevas = []
    for lang, ejes in BUSQUEDAS.items():
        for eje, consultas in ejes.items():
            for c in consultas:
                nuevas += leer(lang, eje, c)
                time.sleep(1)
    limite = (datetime.date.today() - datetime.timedelta(days=VENTANA)).isoformat()
    vistas, todas = set(), []
    for n in sorted(viejas + nuevas, key=lambda x: x["fecha"], reverse=True):
        k = (n["lang"], clave(n))
        if n["fecha"] < limite or k in vistas:
            continue
        vistas.add(k)
        todas.append(n)
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"actualizado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), "noticias": todas},
                  f, ensure_ascii=False, indent=1)
    por = {}
    for n in todas:
        por[(n["lang"], n["eje"])] = por.get((n["lang"], n["eje"]), 0) + 1
    print(f"{len(todas)} noticias ({len(nuevas)} leídas hoy):", ", ".join(f"{l}/{e} {c}" for (l, e), c in sorted(por.items())))


if __name__ == "__main__":
    main()
