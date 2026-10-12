# -*- coding: utf-8 -*-
"""El mar, ahora: previsión oficial de AEMET y notas del 1 al 10 para navegar, bucear y pescar.

    python scripts/parte_mar.py      -> datos/mar.json

Lo ejecuta la Action `parte.yml` cada tres horas. Usa los XML públicos de
AEMET, que no piden clave:

  · playa Río Verde - Puerto Banús: cielo, viento y oleaje de mañana y tarde y
    temperatura del agua, para tres días;
  · Marbella por horas: viento y rachas en km/h, cielo, lluvia y tormenta (dos días);
  · Marbella por días: lo mismo en tramos de 12 h, para el tercer día;
  · boletín costero de Andalucía oriental: estado de la mar (escala Douglas),
    fuerza del viento (Beaufort), mar de fondo y avisos de «Aguas costeras de Málaga».

Licencia: «Autorizado el uso de la información y su reproducción citando a
AEMET como autora de la misma».

La nota es orientativa y sale de las reglas de `notas()`: para bucear y pescar
manda el estado de la mar; para navegar a vela, que haya viento sin pasarse.
Tormenta, niebla, lluvia y avisos restan en las tres.
"""

import datetime
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter

PLAYA = "2906906"                       # Río Verde - Puerto Banús (Marbella)
MUNICIPIO = "29069"                     # Marbella
COSTERA, ZONA = "FQXX47MM", "8012910"   # Andalucía oriental · Aguas costeras de Málaga
URLS = {
    "playa": f"https://www.aemet.es/xml/playas/play_v2_{PLAYA}.xml",
    "horas": f"https://www.aemet.es/xml/municipios_h/localidad_h_{MUNICIPIO}.xml",
    "dias": f"https://www.aemet.es/xml/municipios/localidad_{MUNICIPIO}.xml",
    "costera": f"https://www.aemet.es/xml/maritima/{COSTERA}.xml",
}
TRAMOS = [(8, 14), (14, 20)]            # de mañana y de tarde, los mismos tramos que usa AEMET
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "datos", "mar.json")

OLEAJE_PLAYA = {"débil": 1, "moderado": 2, "fuerte": 3}
# Estado de la mar del parte costero → 0 rizada · 1 marejadilla · 2 marejada · 3 fuerte marejada · 4 gruesa o más.
# Van de mayor a menor para que «fuerte marejada» no cuente también como «marejada».
# Si dos motivos restan lo mismo, se cuenta el que está antes en esta lista
RELIEVE = ["aviso", "temporal", "tormenta", "mar_fuerte", "viento_fuerte", "marejada", "mar_de_fondo", "niebla",
           "rachas", "lluvia", "viento_fresco", "sin_viento", "poco_viento", "viento", "agua_fria", "marejadilla"]
DOUGLAS = [(r"mar montañosa|montañosa|enorme|arbolada|muy gruesa|gruesa", 4), (r"fuerte marejada", 3),
           (r"marejadilla", 1), (r"marejada", 2), (r"rizada|mar en calma|calma", 0)]


# ─────────────────────────────── descarga ───────────────────────────────
def pedir(url, reintentos=4):
    ultimo = None
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "seawithjose.es (parte del mar)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as e:                                    # noqa: BLE001  (AEMET falla a ratos)
            ultimo = e
            time.sleep(4 * (i + 1))
    print(f"  ✗ {url}: {ultimo}")
    return None


def num(s):
    s = (s or "").strip().replace(",", ".")
    if s.lower() == "ip":                                         # precipitación inapreciable
        return 0.1
    try:
        return float(s) if "." in s else int(s)
    except ValueError:
        return None


# ─────────────────────────────── lectura ───────────────────────────────
def leer_playa(raiz):
    dias = {}
    for d in raiz.iter("dia"):
        f = d.get("fecha", "")
        par = lambda tag: [((d.find(tag).get(f"descripcion{n}") if d.find(tag) is not None else "") or "").strip().lower()
                           for n in (1, 2)]
        valor = lambda tag: num(d.find(tag).get("valor1")) if d.find(tag) is not None else None
        dias[f"{f[:4]}-{f[4:6]}-{f[6:8]}"] = {
            "cielo": par("estado_cielo"), "viento": par("viento"), "oleaje": par("oleaje"),
            "agua": valor("t_agua"), "maxima": valor("t_maxima"), "uv": valor("uv_max"),
        }
    return dias


def leer_horas(raiz):
    """{fecha: {"h": {hora: {kmh, dir, racha, cielo}}, "p": {"0814": {lluvia, tormenta}}}}"""
    out = {}
    for d in raiz.iter("dia"):
        horas, probs = {}, {}
        hora = lambda e: num(e.get("periodo")) if (e.get("periodo") or "").isdigit() else None
        for e in d.findall("estado_cielo"):
            if hora(e) is not None:
                horas.setdefault(hora(e), {})["cielo"] = (e.text or "").strip().rstrip("n")
        for e in d.findall("viento"):
            if hora(e) is not None:
                h = horas.setdefault(hora(e), {})
                h["dir"], h["kmh"] = (e.findtext("direccion") or "").strip(), num(e.findtext("velocidad"))
        for e in d.findall("racha_max"):
            if hora(e) is not None:
                horas.setdefault(hora(e), {})["racha"] = num(e.text)
        for tag, clave in (("prob_precipitacion", "lluvia"), ("prob_tormenta", "tormenta")):
            for e in d.findall(tag):
                probs.setdefault(e.get("periodo"), {})[clave] = num(e.text)
        out[d.get("fecha")] = {"h": horas, "p": probs}
    return out


def leer_dias(raiz):
    """{fecha: {"06-12": {kmh, dir, racha, lluvia, cielo}, ...}}"""
    out = {}
    for d in raiz.iter("dia"):
        per = {}
        for e in d.findall("viento"):
            p = per.setdefault(e.get("periodo") or "00-24", {})
            p["dir"], p["kmh"] = (e.findtext("direccion") or "").strip(), num(e.findtext("velocidad"))
        for tag, clave in (("racha_max", "racha"), ("prob_precipitacion", "lluvia")):
            for e in d.findall(tag):
                per.setdefault(e.get("periodo") or "00-24", {})[clave] = num(e.text)
        for e in d.findall("estado_cielo"):
            per.setdefault(e.get("periodo") or "00-24", {})["cielo"] = (e.text or "").strip().rstrip("n")
        out[d.get("fecha")] = per
    return out


def clases_mar(texto):
    t, clases = texto.lower(), []
    for patron, clase in DOUGLAS:
        regex = r"\b(?:%s)\b" % patron
        if re.search(regex, t):
            clases.append(clase)
            t = re.sub(regex, " ", t)
    return clases


def leer_costera(raiz):
    zona = next((z for z in raiz.iter("zona") if z.get("id") == ZONA), None)
    if zona is None:
        return None
    texto = " ".join((s.findtext("texto") or "").strip() for s in zona.iter("subzona"))
    texto = re.sub(r"\s+", " ", texto).strip(" .") + "."
    bajo = texto.lower()
    fondo = re.search(r"mar de fondo([^.]*)", bajo)
    sin_fondo = re.sub(r"mar de fondo[^.]*\.?", " ", bajo)
    sin_alturas = re.sub(r"\d+(?:[.,]\d+)?\s*(?:a\s*\d+(?:[.,]\d+)?\s*)?(?:m|metros?)\b", " ", sin_fondo)
    sin_alturas = re.sub(r"(?:las|hasta|desde)\s+\d{1,2}(?::\d\d)?|\d{1,2}(?::\d\d)?\s*(?:h|horas|utc)\b", " ", sin_alturas)
    fuerzas = [int(n) for n in re.findall(r"\b(\d{1,2})\b", re.sub(r"visibilidad[^.]*", " ", sin_alturas))
               if int(n) <= 12]
    clases = clases_mar(sin_fondo)
    alturas = [num(x) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*(?:m|metros?)\b", fondo.group(1))] if fondo else []
    aviso = " ".join((a.findtext("texto") or "").strip() for a in raiz.iter("aviso")).strip()
    hay_aviso = bool(aviso) and not aviso.lower().startswith("no hay aviso") and "málaga" in aviso.lower()
    return {
        "zona": zona.get("nombre"), "texto": texto,
        "elaborado": raiz.findtext("origen/elaborado"),
        "inicio": raiz.findtext("prediccion/inicio"), "fin": raiz.findtext("prediccion/fin"),
        "fuerza": [min(fuerzas), max(fuerzas)] if fuerzas else None,
        "mar": [min(clases), max(clases)] if clases else None,
        "fondo": bool(fondo), "fondo_m": max(alturas) if alturas else None,
        "aviso": aviso if hay_aviso else None,
    }


# ─────────────────────────────── cálculo ───────────────────────────────
def cielo_de(codigos):
    """Un rótulo para el tramo a partir de los códigos de cielo de AEMET
    (decenas: 1 sin nada · 2 lluvia · 3 nieve · 4 lluvia escasa · 5 tormenta · 6 tormenta y lluvia escasa ·
    7 nieve escasa; unidades: 1 despejado … 6 cubierto, 7 nubes altas; 81 niebla, 82 bruma, 83 calima)."""
    codigos = [c for c in codigos if c and c.isdigit()]
    if not codigos:
        return None
    decenas = {c[0] for c in codigos}
    if decenas & {"5", "6"}:
        return "tormenta"
    if sum(c in ("81", "82") for c in codigos) >= 2:
        return "niebla" if codigos.count("81") >= codigos.count("82") else "bruma"
    if decenas & {"2"}:
        return "lluvia"
    if decenas & {"4", "3", "7"}:
        return "lluvia_escasa"
    c = Counter(codigos).most_common(1)[0][0]
    return {"11": "despejado", "12": "poco_nuboso", "13": "intervalos", "14": "nuboso", "15": "nuboso",
            "16": "cubierto", "17": "nubes_altas", "81": "niebla", "82": "bruma", "83": "calima"}.get(c, "nuboso")


def condiciones(fecha, de, a, playa, horas, dias, costera):
    """Lo que se espera en un tramo: viento y rachas (km/h), mar (0-4), lluvia y tormenta (%), horas de niebla…"""
    c = {"de": de, "a": a}
    hs = horas.get(fecha, {}).get("h", {})
    sel = [hs[h] for h in range(de, a) if h in hs]
    if len(sel) >= 3:
        vel = [x["kmh"] for x in sel if x.get("kmh") is not None]
        rachas = [x["racha"] for x in sel if x.get("racha") is not None]
        rumbos = [x["dir"] for x in sel if x.get("dir") and x["dir"] != "C"]
        cielos = [x.get("cielo") for x in sel]
        p = horas[fecha]["p"].get(f"{de:02d}{a:02d}", {})
        c.update(viento=round(sum(vel) / len(vel)) if vel else None, racha=max(rachas) if rachas else None,
                 dir=Counter(rumbos).most_common(1)[0][0] if rumbos else "C",
                 lluvia=p.get("lluvia"), tormenta=p.get("tormenta"),
                 niebla=sum(1 for x in cielos if x in ("81", "82")), cielo=cielo_de(cielos))
    else:
        per = dias.get(fecha, {})
        claves = ("06-12", "00-12", "00-24") if de < 12 else ("12-18", "12-24", "00-24")
        p = next((per[k] for k in claves if per.get(k, {}).get("kmh") is not None), None)
        if p:
            cod = p.get("cielo")
            c.update(viento=p.get("kmh"), racha=p.get("racha"), dir=p.get("dir") or "C",
                     lluvia=p.get("lluvia"), tormenta=60 if cod and cod[0] in "56" else 0,
                     niebla=3 if cod in ("81", "82") else 0, cielo=cielo_de([cod]))
    # El mar: lo que diga la previsión de la playa y, si cubre el tramo, el parte costero (manda el peor)
    olas = (playa.get(fecha) or {}).get("oleaje") or ["", ""]
    mar = OLEAJE_PLAYA.get(olas[0 if de < 14 else 1])
    c.update(fondo=False, fuerza=None, aviso=False)
    if costera and costera.get("inicio") and costera.get("fin"):
        medio = datetime.datetime.fromisoformat(f"{fecha}T{(de + a) // 2:02d}:00:00")
        if datetime.datetime.fromisoformat(costera["inicio"]) <= medio < datetime.datetime.fromisoformat(costera["fin"]):
            if costera.get("mar"):
                mar = max(mar if mar is not None else 0, costera["mar"][1])
            c.update(fondo=costera["fondo"], fuerza=costera["fuerza"][1] if costera.get("fuerza") else None,
                     aviso=bool(costera.get("aviso")))
    c["mar"] = mar
    c["agua"] = (playa.get(fecha) or {}).get("agua")
    return c


def notas(c):
    """Nota del 1 al 10 y motivo principal para navegar a vela, bucear y pescar.

    Navegar: lo ideal es viento de 13 a 28 km/h (fuerza 3-4). Con menos de 5 km/h se va a
    motor; de 34 km/h para arriba, o con marejada, baja mucho.
    Bucear: manda el estado de la mar (marejadilla o menos, bien; marejada, regular; más, no).
    Pescar: mar hasta marejadilla y viento por debajo de 22 km/h.
    En las tres restan la tormenta, la niebla, la lluvia y el mar de fondo; con aviso costero
    de AEMET o temporal (fuerza 7 o más), la nota no pasa de 2."""
    v, mar = c.get("viento"), c.get("mar")
    if v is None or mar is None:
        return None
    racha, lluvia = c.get("racha") or 0, c.get("lluvia") or 0
    tormenta, niebla, agua = c.get("tormenta") or 0, c.get("niebla") or 0, c.get("agua")
    fuerza = c.get("fuerza") or 0

    def comunes(restas, niebla_pesa, lluvia_pesa):
        if tormenta >= 15:
            restas.append((2, "tormenta"))
        if niebla >= 3:
            restas.append((niebla_pesa, "niebla"))
        elif niebla >= 1:
            restas.append((1, "niebla"))
        if lluvia >= 70:
            restas.append((lluvia_pesa, "lluvia"))
        elif lluvia >= 40 and lluvia_pesa > 1:
            restas.append((1, "lluvia"))
        if fuerza == 6:
            restas.append((2, "viento_fuerte"))

    def cerrar(restas, bien):
        nota, motivo = 10 - sum(r for r, _ in restas), None
        if restas:                       # el que más resta; si empatan, el más llamativo
            motivo = max(restas, key=lambda r: (r[0], -RELIEVE.index(r[1])))[1]
        for tope, clave, cumple in ((2, "aviso", c.get("aviso")), (2, "temporal", fuerza >= 7),
                                    (3, "tormenta", tormenta >= 40)):
            if cumple and nota > tope:
                nota, motivo = tope, clave
        nota = max(1, min(10, nota))
        return {"n": nota, "m": motivo if nota <= 8 and motivo else bien}

    # Navegar a vela
    r = []
    for hasta, resta, clave in ((5, 6, "sin_viento"), (9, 4, "poco_viento"), (13, 2, "poco_viento"),
                                (28.5, 0, None), (34.5, 3, "viento_fresco"), (40.5, 6, "viento_fuerte")):
        if v < hasta:
            if resta:
                r.append((resta, clave))
            break
    else:
        r.append((8, "viento_fuerte"))
    r += [x for x in ((0, None), (0, None), (2, "marejada"), (6, "mar_fuerte"), (8, "mar_fuerte"))[mar:mar + 1] if x[0]]
    if racha >= 50:
        r.append((3, "rachas"))
    elif racha >= 40:
        r.append((1, "rachas"))
    comunes(r, 3, 2)
    navegar = cerrar(r, "buen_viento")

    # Bucear
    r = [x for x in ((0, None), (1, "marejadilla"), (5, "marejada"), (8, "mar_fuerte"), (9, "mar_fuerte"))[mar:mar + 1] if x[0]]
    if v > 38:
        r.append((7, "viento_fuerte"))
    elif v > 30:
        r.append((5, "viento_fuerte"))
    elif v > 20:
        r.append((2, "viento"))
    elif v > 14:
        r.append((1, "viento"))
    if c.get("fondo"):
        r.append((2, "mar_de_fondo"))
    if agua is not None and agua < 15:
        r.append((1, "agua_fria"))
    comunes(r, 1, 1)
    bucear = cerrar(r, "mar_tranquila")

    # Pescar
    r = [x for x in ((0, None), (0, None), (5, "marejada"), (7, "mar_fuerte"), (9, "mar_fuerte"))[mar:mar + 1] if x[0]]
    if v > 38:
        r.append((7, "viento_fuerte"))
    elif v > 30:
        r.append((5, "viento_fuerte"))
    elif v > 22:
        r.append((2, "viento"))
    if racha >= 45:
        r.append((1, "rachas"))
    if c.get("fondo"):
        r.append((1, "mar_de_fondo"))
    comunes(r, 2, 2)
    pescar = cerrar(r, "mar_tranquila")
    return {"navegar": navegar, "bucear": bucear, "pescar": pescar}


# ─────────────────────────────── salida ───────────────────────────────
def hoy_en_madrid():
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Madrid")).date().isoformat()
    except Exception:                                             # noqa: BLE001  (Windows sin tzdata)
        return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).date().isoformat()


def main():
    raices = {k: pedir(u) for k, u in URLS.items()}
    if raices["playa"] is None and raices["horas"] is None:
        print("AEMET no responde: se deja el parte anterior.")
        return 1
    playa = leer_playa(raices["playa"]) if raices["playa"] is not None else {}
    horas = leer_horas(raices["horas"]) if raices["horas"] is not None else {}
    dias_m = leer_dias(raices["dias"]) if raices["dias"] is not None else {}
    costera = leer_costera(raices["costera"]) if raices["costera"] is not None else None

    hoy = hoy_en_madrid()
    fechas = [f for f in sorted(set(playa) | set(horas)) if f >= hoy][:3]
    dias = []
    for fecha in fechas:
        p = playa.get(fecha, {})
        tramos = []
        for de, a in TRAMOS:
            c = condiciones(fecha, de, a, playa, horas, dias_m, costera)
            c["notas"] = notas(c)
            tramos.append(c)
        dias.append({"fecha": fecha, "cielo": p.get("cielo", ["", ""]), "viento": p.get("viento", ["", ""]),
                     "oleaje": p.get("oleaje", ["", ""]), "agua": p.get("agua"), "maxima": p.get("maxima"),
                     "uv": p.get("uv"), "tramos": tramos})

    elaborado = {k: (raices[k].findtext("elaborado") or raices[k].findtext("origen/elaborado"))
                 for k in ("playa", "horas") if raices[k] is not None}
    salida = {
        "generado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "elaborado": elaborado,
        "fuente": "Información elaborada por la Agencia Estatal de Meteorología (AEMET)",
        "dias": dias, "costera": costera,
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    for d in dias:
        print(d["fecha"], " · ".join(
            f'{t["de"]:02d}-{t["a"]:02d} h ' + (" ".join(f'{k[:3]} {v["n"]}' for k, v in t["notas"].items())
                                               if t["notas"] else "sin datos") for t in d["tramos"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
