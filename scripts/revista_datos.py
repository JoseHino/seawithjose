# -*- coding: utf-8 -*-
"""Bitácora del mar: los datos que el programa analiza para cada número (la IA solo los cuenta).

  · tiempo_quincena()  el tiempo de los últimos 15 días en Marbella (AEMET, Marbella Puerto 6076X)
  · prevision()        la previsión oficial de AEMET para Marbella de los próximos 7 días
  · analisis()         cruza el viento de AEMET (fuerza y dirección) con la temperatura del agua de
                       Copernicus Marine (satélite y modelo de la UE, vía Open-Meteo): qué pasa con el agua
                       al día siguiente según de dónde y con qué fuerza sopla, con todo el histórico desde
                       noviembre de 2022, y los episodios llamativos de la quincena
  · grafica()          una imagen PNG con las dos cosas, para el correo

Todas las cifras salen de aquí. Viento de AEMET: velocidad media del día y dirección de la racha máxima
(los diarios), o la media vectorial de las horas (los días con datos horarios).
"""

import datetime
import json
import math
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIARIO = os.path.join(RAIZ, "datos", "marbella", "diario.json")
HORARIO = os.path.join(RAIZ, "datos", "marbella", "horario.json")
ESTACION = "6076X"            # Marbella, Puerto
LAT, LON = 36.47, -4.95
SST_DESDE = datetime.date(2022, 11, 1)     # Open-Meteo tiene temperatura del agua desde aquí
FUERTE = 15                   # km/h de viento medio diario a partir de los que se analiza su efecto
SECTORES = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
LEVANTE, PONIENTE = {"NE", "E", "SE"}, {"SO", "O", "NO"}


def pedir_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "seawithjose-revista"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def sector(grados):
    return SECTORES[int(((grados % 360) + 22.5) // 45) % 8]


# ─────────────────────────────── viento y tiempo diarios de AEMET ───────────────────────────────
def dias_aemet():
    """{fecha: {viento (km/h), dir (grados), racha (km/h), tmax, tmin, tmed, prec}} combinando los diarios
    climatológicos y, para los días que aún no tienen diario, la media de las horas guardadas."""
    out = {}
    try:
        diario = json.load(open(DIARIO, encoding="utf-8"))["estaciones"][ESTACION]["dias"]
    except (OSError, KeyError, ValueError):
        diario = {}
    for f, d in diario.items():
        fila = {}
        if d.get("velmedia") is not None:
            fila["viento"] = d["velmedia"] * 3.6
        if d.get("racha") is not None:
            fila["racha"] = d["racha"] * 3.6
        if d.get("dir") is not None and d["dir"] < 88:
            fila["dir"] = d["dir"] * 10
        for k in ("tmax", "tmin", "tmed", "prec"):
            if d.get(k) is not None:
                fila[k] = d[k]
        out[f] = fila
    try:
        obs = json.load(open(HORARIO, encoding="utf-8"))["estaciones"][ESTACION]["obs"]
    except (OSError, KeyError, ValueError):
        obs = {}
    horas = {}
    for h, o in obs.items():
        horas.setdefault(h[:10], []).append(o)
    for f, lista in horas.items():
        if f in out or len(lista) < 18:          # un día con menos de 18 horas no es representativo
            continue
        vv = [o["vv"] for o in lista if o.get("vv") is not None]
        u = sum(o["vv"] * math.sin(math.radians(o["dv"])) for o in lista if o.get("vv") is not None and o.get("dv") is not None)
        v = sum(o["vv"] * math.cos(math.radians(o["dv"])) for o in lista if o.get("vv") is not None and o.get("dv") is not None)
        ta = [o["ta"] for o in lista if o.get("ta") is not None]
        fila = {"viento": sum(vv) / len(vv) * 3.6} if vv else {}
        if u or v:
            fila["dir"] = math.degrees(math.atan2(u, v)) % 360
        rachas = [o["vmax"] for o in lista if o.get("vmax") is not None]
        if rachas:
            fila["racha"] = max(rachas) * 3.6
        if ta:
            fila.update(tmax=max(ta), tmin=min(ta), tmed=sum(ta) / len(ta))
        fila["prec"] = sum(o.get("prec") or 0 for o in lista)
        out[f] = fila
    return out


def tiempo_quincena(ini, fin):
    dias = dias_aemet()
    sel = {f: d for f, d in dias.items() if ini.isoformat() <= f <= fin.isoformat()}
    if not sel:
        return {}
    r = {"desde": ini.isoformat(), "hasta": fin.isoformat(), "dias_con_datos": len(sel)}
    con = lambda k: [(f, d[k]) for f, d in sorted(sel.items()) if d.get(k) is not None]  # noqa: E731
    if con("tmax"):
        f, x = max(con("tmax"), key=lambda p: p[1]); r.update(tmax=round(x, 1), tmax_dia=f)
    if con("tmin"):
        f, x = min(con("tmin"), key=lambda p: p[1]); r.update(tmin=round(x, 1), tmin_dia=f)
    if con("prec"):
        lluvias = con("prec")
        r.update(lluvia_total=round(sum(x for _, x in lluvias), 1), dias_lluvia=sum(1 for _, x in lluvias if x >= 1))
    if con("racha"):
        f, x = max(con("racha"), key=lambda p: p[1])
        r.update(racha_max=round(x), racha_dia=f)
        if sel[f].get("dir") is not None:
            r["racha_dir"] = sector(sel[f]["dir"])
    if con("viento"):
        r["viento_medio"] = round(sum(x for _, x in con("viento")) / len(con("viento")))
    if con("dir"):
        cuenta = {}
        for _, x in con("dir"):
            cuenta[sector(x)] = cuenta.get(sector(x), 0) + 1
        r["dir_dominante"] = max(cuenta, key=cuenta.get)
        r["dias_levante"] = sum(n for s, n in cuenta.items() if s in LEVANTE)
        r["dias_poniente"] = sum(n for s, n in cuenta.items() if s in PONIENTE)
    return r


# ─────────────────────────────── previsión oficial de AEMET (7 días) ───────────────────────────────
def prevision():
    req = urllib.request.Request("https://www.aemet.es/xml/municipios/localidad_29069.xml",
                                 headers={"User-Agent": "seawithjose-revista"})
    raiz = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
    out = []
    for dia in raiz.iter("dia"):
        def periodo(tag, campo=None):
            vals = []
            for e in dia.findall(tag):
                x = e.find(campo).text if campo is not None and e.find(campo) is not None else (e.get("descripcion") if tag == "estado_cielo" else e.text)
                vals.append((e.get("periodo") or "00-24", x))
            return vals
        cielos = [(p, x) for p, x in periodo("estado_cielo") if x]
        cielo = next((x for p, x in cielos if p == "00-24"), None) or next((x for p, x in cielos if p in ("12-24", "06-12", "12-18")), cielos[0][1] if cielos else "")
        lluvia = [int(x) for p, x in periodo("prob_precipitacion") if x and x.strip().isdigit()]
        vientos = []
        for e in dia.findall("viento"):
            d, v = e.findtext("direccion"), e.findtext("velocidad")
            if d and v and v.strip().isdigit():
                vientos.append((int(v), d.strip(), e.get("periodo") or "00-24"))
        rachas = [int(e.text) for e in dia.findall("racha_max") if e.text and e.text.strip().isdigit()]
        viento = next(((v, d) for v, d, p in vientos if p == "00-24"), None) or (max(vientos)[:2] if vientos else None)
        out.append({"fecha": dia.get("fecha"), "cielo": cielo,
                    "tmax": int(dia.findtext("temperatura/maxima")) if (dia.findtext("temperatura/maxima") or "").strip().lstrip("-").isdigit() else None,
                    "tmin": int(dia.findtext("temperatura/minima")) if (dia.findtext("temperatura/minima") or "").strip().lstrip("-").isdigit() else None,
                    "lluvia": max(lluvia) if lluvia else None,
                    "viento": viento[0] if viento else None, "viento_dir": (viento[1] or "").replace("C", "calma") if viento else None,
                    "racha": max(rachas) if rachas else None})
    hoy = datetime.date.today().isoformat()
    return [d for d in out if d["fecha"] >= hoy][:7]


# ─────────────────────────────── el agua frente al viento ───────────────────────────────
def sst_diaria(desde, hasta):
    url = ("https://marine-api.open-meteo.com/v1/marine?"
           + urllib.parse.urlencode({"latitude": LAT, "longitude": LON, "hourly": "sea_surface_temperature",
                                     "start_date": desde.isoformat(), "end_date": hasta.isoformat(),
                                     "timezone": "Europe/Madrid"}))
    h = pedir_json(url).get("hourly", {})
    por_dia = {}
    for t, x in zip(h.get("time", []), h.get("sea_surface_temperature", [])):
        if x is not None:
            por_dia.setdefault(t[:10], []).append(x)
    return {f: sum(v) / len(v) for f, v in por_dia.items() if len(v) >= 12}


def analisis(ini, fin):
    dias = dias_aemet()
    sst = sst_diaria(SST_DESDE, fin)
    fechas = sorted(sst)
    # ΔSST del día siguiente frente al viento de cada día
    pares = []
    for f in fechas:
        sig = (datetime.date.fromisoformat(f) + datetime.timedelta(days=1)).isoformat()
        d = dias.get(f, {})
        if sig in sst and d.get("viento") is not None and d.get("dir") is not None:
            pares.append({"fecha": f, "viento": d["viento"], "sector": sector(d["dir"]), "delta": sst[sig] - sst[f]})
    media = lambda xs: round(sum(xs) / len(xs), 2) if xs else None  # noqa: E731
    por_sector = {}
    for s in SECTORES:
        xs = [p["delta"] for p in pares if p["sector"] == s and p["viento"] >= FUERTE]
        if len(xs) >= 5:
            por_sector[s] = {"media": media(xs), "n": len(xs)}
    tramos = {}
    for grupo, nombre in ((PONIENTE, "poniente"), (LEVANTE, "levante")):
        for lo, hi, etiqueta in ((0, 10, "flojo (<10 km/h)"), (10, 20, "moderado (10-20 km/h)"), (20, 999, "fuerte (>20 km/h)")):
            xs = [p["delta"] for p in pares if p["sector"] in grupo and lo <= p["viento"] < hi]
            if len(xs) >= 5:
                tramos.setdefault(nombre, {})[etiqueta] = {"media": media(xs), "n": len(xs)}
    # la quincena
    quincena = []
    d = ini
    while d <= fin:
        f = d.isoformat()
        w = dias.get(f, {})
        quincena.append({"fecha": f, "agua": round(sst[f], 1) if f in sst else None,
                         "viento": round(w["viento"]) if w.get("viento") is not None else None,
                         "dir": sector(w["dir"]) if w.get("dir") is not None else None})
        d += datetime.timedelta(days=1)
    con_agua = [q for q in quincena if q["agua"] is not None]
    episodios = []
    for i in range(len(con_agua) - 2):
        a, b = con_agua[i], con_agua[i + 2]
        episodios.append({"desde": a["fecha"], "hasta": b["fecha"], "cambio": round(b["agua"] - a["agua"], 1),
                          "vientos": [(q["dir"], q["viento"]) for q in con_agua[i:i + 2]]})
    # lo normal en estas fechas: el cambio del agua en la misma quincena de los años anteriores
    normal = []
    for anios in (1, 2, 3):
        try:
            a0, a1 = ini.replace(year=ini.year - anios).isoformat(), fin.replace(year=fin.year - anios).isoformat()
        except ValueError:
            continue
        if a0 in sst and a1 in sst:
            normal.append(sst[a1] - sst[a0])
    bajada = min(episodios, key=lambda e: e["cambio"]) if episodios else None
    subida = max(episodios, key=lambda e: e["cambio"]) if episodios else None
    return {"pares_historicos": len(pares), "desde_historico": fechas[0] if fechas else None,
            "por_sector": por_sector, "tramos": tramos, "quincena": quincena,
            "mayor_bajada_2_dias": bajada if bajada and bajada["cambio"] <= -0.3 else None,
            "mayor_subida_2_dias": subida if subida and subida["cambio"] >= 0.3 else None,
            "agua_inicio": con_agua[0]["agua"] if con_agua else None, "agua_fin": con_agua[-1]["agua"] if con_agua else None,
            "cambio_quincena": round(con_agua[-1]["agua"] - con_agua[0]["agua"], 1) if len(con_agua) > 1 else None,
            "cambio_normal": round(sum(normal) / len(normal), 1) if normal else None, "anios_normal": len(normal)}


def texto_analisis(a, t, p):
    """Los hechos en texto llano, para que la IA los cuente sin inventar."""
    lineas = [f"Histórico: {a['pares_historicos']} días desde {a['desde_historico']} con viento de AEMET (Marbella Puerto) "
              "y temperatura del agua de Copernicus Marine."]
    if a["por_sector"]:
        lineas.append(f"Cambio medio del agua al día siguiente con viento medio ≥ {FUERTE} km/h, por dirección: "
                      + "; ".join(f"{s} {v['media']:+} °C ({v['n']} días)" for s, v in a["por_sector"].items()))
    for nombre, tr in a["tramos"].items():
        lineas.append(f"Con {nombre}: " + "; ".join(f"{k} {v['media']:+} °C ({v['n']} días)" for k, v in tr.items()))
    lineas.append("Quincena día a día (fecha: agua °C · viento medio km/h · dirección): "
                  + "; ".join(f"{q['fecha'][5:]}: {q['agua']} · {q['viento']} · {q['dir']}" for q in a["quincena"]))
    if a.get("cambio_quincena") is not None:
        lineas.append(f"El agua pasó de {a['agua_inicio']} a {a['agua_fin']} °C en la quincena ({a['cambio_quincena']:+} °C)"
                      + (f"; en las mismas fechas de los {a['anios_normal']} años anteriores cambió de media "
                         f"{a['cambio_normal']:+} °C (lo normal por la época)" if a.get("cambio_normal") is not None else ""))
    for clave, nombre in (("mayor_bajada_2_dias", "Mayor bajada en 2 días"), ("mayor_subida_2_dias", "Mayor subida en 2 días")):
        e = a.get(clave)
        if e:
            lineas.append(f"{nombre}: {e['cambio']:+} °C del {e['desde']} al {e['hasta']}, con viento "
                          + ", ".join(f"{d} {v} km/h" for d, v in e["vientos"]))
    if t:
        lineas.append("Tiempo de la quincena (AEMET Marbella Puerto): " + json.dumps(t, ensure_ascii=False))
    if p:
        lineas.append("Previsión AEMET Marbella próximos días: " + json.dumps(p, ensure_ascii=False))
    return "\n".join(lineas)


# ─────────────────────────────── la gráfica del correo ───────────────────────────────
def grafica(a, ruta, lang="es"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    marino, azul, rojo, gris = "#0B2D52", "#1F4E9A", "#D2232A", "#9AAAB8"
    T = {"es": ("Temperatura del agua y viento en la quincena", "Agua (°C)", "Viento medio (km/h)",
                f"Cambio medio del agua al día siguiente con viento de más de {FUERTE} km/h", "°C", "Levante", "Poniente", "Otros",
                "Agua: Copernicus Marine · Viento: AEMET, Marbella Puerto"),
         "en": ("Water temperature and wind this fortnight", "Water (°C)", "Mean wind (km/h)",
                f"Average next-day change in water temperature with wind above {FUERTE} km/h", "°C", "Easterly", "Westerly", "Other",
                "Water: Copernicus Marine · Wind: AEMET, Marbella Marina")}[lang]
    q = [x for x in a["quincena"] if x["agua"] is not None or x["viento"] is not None]
    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(7.2, 6.4), dpi=150, gridspec_kw={"height_ratios": [1.25, 1]})
    fechas = [datetime.date.fromisoformat(x["fecha"]) for x in q]
    colores = [rojo if x["dir"] in LEVANTE else azul if x["dir"] in PONIENTE else gris for x in q]
    ax2 = ax1.twinx()
    ax2.bar(fechas, [x["viento"] or 0 for x in q], color=colores, alpha=.35, width=.8, zorder=1)
    ax2.set_ylabel(T[2], color="#4E5F70", fontsize=8)
    ax1.set_zorder(ax2.get_zorder() + 1); ax1.patch.set_visible(False)
    ax1.plot([f for f, x in zip(fechas, q) if x["agua"] is not None], [x["agua"] for x in q if x["agua"] is not None],
             color=marino, lw=2.4, marker="o", ms=3)
    ax1.set_ylabel(T[1], color=marino, fontsize=8)
    ax1.set_title(T[0], loc="left", fontsize=10, fontweight="bold", color=marino)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    from matplotlib.patches import Patch
    ax1.legend(handles=[Patch(color=rojo, alpha=.5, label=T[5]), Patch(color=azul, alpha=.5, label=T[6]),
                        Patch(color=gris, alpha=.5, label=T[7])], fontsize=7, loc="upper left",
               bbox_to_anchor=(0, -0.1), frameon=False, ncol=3)
    sec = [s for s in SECTORES if s in a["por_sector"]]
    vals = [a["por_sector"][s]["media"] for s in sec]
    ax3.bar(sec, vals, color=[rojo if s in LEVANTE else azul if s in PONIENTE else gris for s in sec])
    ax3.axhline(0, color="#4E5F70", lw=.8)
    ax3.set_title(T[3], loc="left", fontsize=9, fontweight="bold", color=marino)
    ax3.set_ylabel(T[4], fontsize=8)
    for i, v in enumerate(vals):
        ax3.text(i, v, f"{v:+.2f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=7)
    for ax in (ax1, ax2, ax3):
        ax.tick_params(labelsize=7)
        for lado in ("top",):
            ax.spines[lado].set_visible(False)
    fig.text(0.01, 0.005, T[8], fontsize=6.5, color="#4E5F70")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta)
    plt.close(fig)
