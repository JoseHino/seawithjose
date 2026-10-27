# -*- coding: utf-8 -*-
"""Bitácora del mar: ¿cuándo salir al mar la semana que viene? (lo calcula el programa; la IA solo lo cuenta)

  · horas()      previsión hora a hora frente a Puerto Banús: viento, rachas y dirección, probabilidad de lluvia
                 (Open-Meteo, modelos de AEMET/ECMWF), olas y nivel del mar con la marea (Open-Meteo Marine)
  · mareas()     pleamares y bajamares de cada día, sacadas del nivel del mar hora a hora
  · solunar()    sol y luna de cada día (salida, puesta, tránsitos, fase) y los periodos de actividad de los peces
                 de la teoría solunar: mayores (tránsitos de la luna, 2 h) y menores (salida y puesta de la luna, 1 h)
  · plan()       para cada día y actividad (vela, pesca a fondo, curricán) una nota de 0 a 3 con su motivo, y
                 las mejores horas de pesca (los periodos solunares de día, mejor si coinciden con el alba o el ocaso)
  · grafica_semana() y grafica_plan()  las imágenes del correo

Los umbrales de cada actividad están en UMBRALES: son los de un velero de 12 m con gente sin experiencia.
"""

import datetime
import json
import math
import os
import urllib.parse
import urllib.request

LAT, LON = 36.44, -4.95                  # 3 km al sur de Puerto Banús, en mar abierto (para olas y viento)
ZONA = "Europe/Madrid"
DIA_DESDE, DIA_HASTA = 9, 20             # horas de luz en las que se sale (para las notas de cada día)
LEVANTE, PONIENTE = {"NE", "E", "SE"}, {"SO", "O", "NO"}
SECTORES = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]

# km/h de viento medio, km/h de racha, m de ola y % de lluvia a partir de los que la nota baja
UMBRALES = {
    "vela":   {"bueno": {"viento": (8, 24), "racha": 35, "ola": 1.0, "lluvia": 30},
               "regular": {"viento": (4, 30), "racha": 45, "ola": 1.5, "lluvia": 60}},
    "fondo":  {"bueno": {"viento": (0, 14), "racha": 25, "ola": 0.6, "lluvia": 30},
               "regular": {"viento": (0, 20), "racha": 35, "ola": 1.0, "lluvia": 60}},
    "currican": {"bueno": {"viento": (0, 18), "racha": 30, "ola": 0.8, "lluvia": 30},
                 "regular": {"viento": (0, 25), "racha": 40, "ola": 1.3, "lluvia": 60}},
}


def pedir_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "seawithjose-revista"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def sector(grados):
    return SECTORES[int(((grados % 360) + 22.5) // 45) % 8]


# ─────────────────────────────── la previsión hora a hora ───────────────────────────────
def horas(desde, dias=7):
    hasta = desde + datetime.timedelta(days=dias - 1)
    rango = {"start_date": desde.isoformat(), "end_date": hasta.isoformat(), "timezone": ZONA}
    t = pedir_json("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": LAT, "longitude": LON, **rango,
        "hourly": "wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation_probability,precipitation,temperature_2m"}))["hourly"]
    m = pedir_json("https://marine-api.open-meteo.com/v1/marine?" + urllib.parse.urlencode({
        "latitude": LAT, "longitude": LON, **rango,
        "hourly": "wave_height,wave_period,sea_level_height_msl,sea_surface_temperature"}))["hourly"]
    nivel = dict(zip(m["time"], m.get("sea_level_height_msl", [])))
    ola = dict(zip(m["time"], m.get("wave_height", [])))
    periodo = dict(zip(m["time"], m.get("wave_period", [])))
    agua = dict(zip(m["time"], m.get("sea_surface_temperature", [])))
    out = []
    for i, h in enumerate(t["time"]):
        out.append({"hora": h, "viento": t["wind_speed_10m"][i], "dir": t["wind_direction_10m"][i],
                    "racha": t["wind_gusts_10m"][i], "lluvia": t["precipitation_probability"][i],
                    "mm": t["precipitation"][i], "temp": t["temperature_2m"][i],
                    "ola": ola.get(h), "periodo": periodo.get(h), "nivel": nivel.get(h), "agua": agua.get(h)})
    return out


# ─────────────────────────────── mareas ───────────────────────────────
def mareas(hs):
    """Pleamares y bajamares: máximos y mínimos locales del nivel del mar (interpolados entre horas)."""
    serie = [(h["hora"], h["nivel"]) for h in hs if h["nivel"] is not None]
    extremos = []
    for i in range(1, len(serie) - 1):
        (_, a), (h, b), (_, c) = serie[i - 1], serie[i], serie[i + 1]
        if (b > a and b >= c) or (b < a and b <= c):
            # parábola por los tres puntos: hora y altura del extremo, con minutos
            den = a - 2 * b + c
            dx = 0.5 * (a - c) / den if den else 0
            altura = b - 0.25 * (a - c) * dx
            momento = datetime.datetime.fromisoformat(h) + datetime.timedelta(hours=dx)
            extremos.append({"tipo": "pleamar" if b > a else "bajamar", "momento": momento.strftime("%Y-%m-%dT%H:%M"),
                             "altura": round(altura, 2)})
    por_dia = {}
    for e in extremos:
        por_dia.setdefault(e["momento"][:10], []).append(e)
    for dia, lista in por_dia.items():
        alturas = [e["altura"] for e in lista]
        por_dia[dia] = {"extremos": lista, "carrera_cm": round((max(alturas) - min(alturas)) * 100) if len(lista) > 1 else None}
    return por_dia


# ─────────────────────────────── sol, luna y periodos solunares ───────────────────────────────
def solunar(desde, dias=7):
    import ephem
    from zoneinfo import ZoneInfo
    madrid = ZoneInfo(ZONA)
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.elevation = str(LAT), str(LON), 0
    obs.pressure = 0
    obs.horizon = "-0:34"
    local = lambda d: ephem.Date(d).datetime().replace(tzinfo=datetime.timezone.utc).astimezone(madrid)  # noqa: E731
    out = {}
    for n in range(dias):
        dia = desde + datetime.timedelta(days=n)
        ini = datetime.datetime.combine(dia, datetime.time(0, 0), madrid).astimezone(datetime.timezone.utc)
        fin = ini + datetime.timedelta(days=1)

        def en_el_dia(funcion, cuerpo):
            obs.date = ephem.Date(ini)
            try:
                x = local(funcion(cuerpo))
            except (ephem.AlwaysUpError, ephem.NeverUpError):
                return None
            return x if x < fin.astimezone(madrid) else None

        sol, luna = ephem.Sun(), ephem.Moon()
        amanecer, ocaso = en_el_dia(obs.next_rising, sol), en_el_dia(obs.next_setting, sol)
        sale, pone = en_el_dia(obs.next_rising, luna), en_el_dia(obs.next_setting, luna)
        transito, antitransito = en_el_dia(obs.next_transit, luna), en_el_dia(obs.next_antitransit, luna)
        obs.date = ephem.Date(ini + datetime.timedelta(hours=12))
        luna.compute(obs)
        iluminada = round(luna.moon_phase * 100)
        # días a la luna nueva o llena más cercana (con sus fechas exactas) y si la luna crece o mengua
        ahora = obs.date
        cerca = min(abs(float(ahora - f(ahora))) for f in (ephem.previous_new_moon, ephem.next_new_moon,
                                                            ephem.previous_full_moon, ephem.next_full_moon))
        edad = round(float(ahora - ephem.previous_new_moon(ahora)), 1)
        periodos = []
        for momento, tipo in ((transito, "mayor"), (antitransito, "mayor"), (sale, "menor"), (pone, "menor")):
            if momento:
                media = datetime.timedelta(hours=1 if tipo == "mayor" else 0.5)
                periodos.append({"tipo": tipo, "desde": (momento - media).strftime("%H:%M"),
                                 "hasta": (momento + media).strftime("%H:%M"), "centro": momento.strftime("%H:%M"),
                                 "alba_ocaso": any(x and abs((momento - x).total_seconds()) <= 3600 for x in (amanecer, ocaso))})
        periodos.sort(key=lambda p: p["centro"])
        # nota de actividad (1-4), como las tablas solunares: más cerca de luna nueva o llena, más actividad;
        # y un punto más si un periodo mayor coincide con el alba o el ocaso
        nota = 4 if cerca <= 1.5 else 3 if cerca <= 3.5 else 2 if cerca <= 5.5 else 1
        if nota < 4 and any(p["tipo"] == "mayor" and p["alba_ocaso"] for p in periodos):
            nota += 1
        out[dia.isoformat()] = {
            "amanecer": amanecer.strftime("%H:%M") if amanecer else None, "ocaso": ocaso.strftime("%H:%M") if ocaso else None,
            "luna_sale": sale.strftime("%H:%M") if sale else None, "luna_pone": pone.strftime("%H:%M") if pone else None,
            "iluminada": iluminada, "edad": edad,
            "creciente": ephem.previous_new_moon(ahora) > ephem.previous_full_moon(ahora), "actividad": nota, "periodos": periodos}
    return out


# ─────────────────────────────── las notas de cada día ───────────────────────────────
def resumen_dia(hs, dia):
    luz = [h for h in hs if h["hora"][:10] == dia and DIA_DESDE <= int(h["hora"][11:13]) < DIA_HASTA]
    if not luz:
        return None
    val = lambda k: [h[k] for h in luz if h[k] is not None]  # noqa: E731
    dirs = [sector(h["dir"]) for h in luz if h["dir"] is not None]
    dominante = max(set(dirs), key=dirs.count) if dirs else None
    return {"viento": round(sum(val("viento")) / len(val("viento"))) if val("viento") else None,
            "viento_max": round(max(val("viento"))) if val("viento") else None,
            "racha": round(max(val("racha"))) if val("racha") else None,
            "dir": dominante, "ola": round(max(val("ola")), 1) if val("ola") else None,
            "lluvia": max(val("lluvia")) if val("lluvia") else None,
            "mm": round(sum(val("mm")), 1) if val("mm") else 0,
            "temp_max": round(max(val("temp"))) if val("temp") else None,
            "agua": round(sum(val("agua")) / len(val("agua")), 1) if val("agua") else None}


def nota(actividad, r):
    """0 nada aconsejable · 1 regular · 2 bueno · 3 muy bueno; y el motivo principal."""
    def cumple(u):
        lo, hi = u["viento"]
        fallos = []
        if r["viento"] is not None and r["viento"] > hi:
            fallos.append("mucho viento")
        if r["viento"] is not None and r["viento"] < lo:
            fallos.append("poco viento")
        if r["racha"] is not None and r["racha"] > u["racha"]:
            fallos.append("rachas fuertes")
        if r["ola"] is not None and r["ola"] > u["ola"]:
            fallos.append("mar movida")
        if r["lluvia"] is not None and r["lluvia"] > u["lluvia"]:
            fallos.append("probable lluvia")
        return fallos
    u = UMBRALES[actividad]
    malos, regulares = cumple(u["regular"]), cumple(u["bueno"])
    if malos:
        return 0, malos
    if regulares:
        return 1, regulares
    # muy bueno: bastante por debajo de los límites
    tranquilo = (r["ola"] or 0) <= u["bueno"]["ola"] * 0.6 and (r["lluvia"] or 0) <= 15
    if actividad == "vela":
        tranquilo = tranquilo and 12 <= (r["viento"] or 0) <= 20
    return (3 if tranquilo else 2), []


def plan(hs, sol, mar, aemet=None):
    """`aemet`: la previsión diaria de AEMET (revista_datos.prevision). Su probabilidad de lluvia manda si es mayor
    que la del modelo hora a hora: la tabla de AEMET sale en el correo y las notas no pueden contradecirla."""
    lluvia_aemet = {p["fecha"]: p["lluvia"] for p in (aemet or []) if p.get("lluvia") is not None}
    dias = []
    for dia in sorted({h["hora"][:10] for h in hs}):
        r = resumen_dia(hs, dia)
        if not r:
            continue
        if dia in lluvia_aemet:
            r["lluvia"] = max(r["lluvia"] or 0, lluvia_aemet[dia])
        s = sol.get(dia, {})
        notas = {a: nota(a, r) for a in UMBRALES}
        # la pesca también depende de la actividad solunar: un día de luna alta sube medio punto
        mejores = [p for p in s.get("periodos", [])
                   if s.get("amanecer") and s.get("ocaso") and s["amanecer"] <= p["centro"] <= s["ocaso"]]
        mejores.sort(key=lambda p: (p["tipo"] != "mayor", not p["alba_ocaso"]))
        dias.append({"fecha": dia, **r, "notas": {a: n for a, (n, _) in notas.items()},
                     "motivos": {a: m for a, (_, m) in notas.items()},
                     "actividad_peces": s.get("actividad"), "horas_pesca": mejores[:2],
                     "mareas": (mar.get(dia) or {}).get("extremos", []), "carrera_cm": (mar.get(dia) or {}).get("carrera_cm")})
    return dias


def texto_plan(dias):
    """Los hechos para la IA, en texto llano."""
    nombres = {0: "no aconsejable", 1: "regular", 2: "bueno", 3: "muy bueno"}
    lineas = [f"Notas por actividad entre las {DIA_DESDE}:00 y las {DIA_HASTA}:00 (0 no aconsejable, 1 regular, 2 bueno, 3 muy bueno), "
              "con viento medio y máximo, racha, dirección dominante, ola máxima (m), probabilidad máxima de lluvia (%) y lluvia (mm):"]
    for d in dias:
        lineas.append(
            f"{d['fecha']}: vela {nombres[d['notas']['vela']]}"
            + (f" ({', '.join(d['motivos']['vela'])})" if d['motivos']['vela'] else "")
            + f"; pesca a fondo {nombres[d['notas']['fondo']]}"
            + (f" ({', '.join(d['motivos']['fondo'])})" if d['motivos']['fondo'] else "")
            + f"; curricán {nombres[d['notas']['currican']]}"
            + (f" ({', '.join(d['motivos']['currican'])})" if d['motivos']['currican'] else "")
            + f" · viento {d['viento']} km/h (máx {d['viento_max']}), racha {d['racha']} km/h, del {d['dir']}, ola {d['ola']} m, "
            f"lluvia {d['lluvia']} % ({d['mm']} mm), {d['temp_max']} °C, agua {d['agua']} °C · actividad de peces "
            f"{d['actividad_peces']}/4 · mejores horas de pesca: "
            + (", ".join(f"{p['desde']}-{p['hasta']} ({p['tipo']}{', con el alba o el ocaso' if p['alba_ocaso'] else ''})"
                         for p in d["horas_pesca"]) or "ninguna de día")
            + " · mareas: " + (", ".join(f"{e['tipo']} {e['momento'][11:]}" for e in d["mareas"]) or "—")
            + (f" (carrera {d['carrera_cm']} cm)" if d.get("carrera_cm") else ""))
    return "\n".join(lineas)


# ─────────────────────────────── gráficas ───────────────────────────────
def _estilo(ax):
    ax.tick_params(labelsize=7)
    ax.spines["top"].set_visible(False)


def grafica_semana(semana, ruta, lang="es"):
    """La semana pasada: agua (línea) y viento medio de cada día (barras, rojo levante, azul poniente)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    marino, azul, rojo, gris = "#0B2D52", "#1F4E9A", "#D2232A", "#9AAAB8"
    T = {"es": ("El agua y el viento, día a día", "Agua (°C)", "Viento medio (km/h)", "Levante", "Poniente", "Otros",
                "Agua: Copernicus Marine · Viento: AEMET, Marbella Puerto"),
         "en": ("Water and wind, day by day", "Water (°C)", "Mean wind (km/h)", "Easterly", "Westerly", "Other",
                "Water: Copernicus Marine · Wind: AEMET, Marbella Marina")}[lang]
    q = [x for x in semana if x["agua"] is not None or x["viento"] is not None]
    fechas = [datetime.date.fromisoformat(x["fecha"]) for x in q]
    fig, ax1 = plt.subplots(figsize=(7.2, 3.4), dpi=150)
    ax2 = ax1.twinx()
    ax2.bar(fechas, [x["viento"] or 0 for x in q], width=.7, alpha=.4, zorder=1,
            color=[rojo if x["dir"] in LEVANTE else azul if x["dir"] in PONIENTE else gris for x in q])
    for f, x in zip(fechas, q):
        if x["viento"]:
            ax2.text(f, x["viento"], f"{x['dir'] or ''}", ha="center", va="bottom", fontsize=7, color="#4E5F70")
    ax2.set_ylabel(T[2], fontsize=8, color="#4E5F70")
    ax1.set_zorder(ax2.get_zorder() + 1); ax1.patch.set_visible(False)
    con = [(f, x["agua"]) for f, x in zip(fechas, q) if x["agua"] is not None]
    ax1.plot([f for f, _ in con], [a for _, a in con], color=marino, lw=2.6, marker="o", ms=4)
    for f, a in con:
        ax1.text(f, a + 0.06, f"{a:.1f}".replace(".", "," if lang == "es" else "."), ha="center", fontsize=7, color=marino)
    ax1.set_ylabel(T[1], fontsize=8, color=marino)
    ax1.set_title(T[0], loc="left", fontsize=10, fontweight="bold", color=marino)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax1.legend(handles=[Patch(color=rojo, alpha=.5, label=T[3]), Patch(color=azul, alpha=.5, label=T[4]),
                        Patch(color=gris, alpha=.5, label=T[5])], fontsize=7, loc="upper left",
               bbox_to_anchor=(0, -0.12), frameon=False, ncol=3)
    for ax in (ax1, ax2):
        _estilo(ax)
    fig.text(0.01, 0.01, T[6], fontsize=6.5, color="#4E5F70")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta)
    plt.close(fig)


def grafica_plan(hs, mar, ruta, lang="es"):
    """La semana que viene, hora a hora: viento y rachas, olas, marea y probabilidad de lluvia."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    marino, azul, rojo, amarillo, gris = "#0B2D52", "#1F4E9A", "#D2232A", "#FFC20E", "#9AAAB8"
    T = {"es": ("La semana que viene, hora a hora", "Viento medio", "Rachas", "km/h", "Ola (m)", "Marea (cm)",
                "Lluvia (%)", "Previsión: Open-Meteo (modelos de AEMET y ECMWF) y Copernicus Marine, 3 km al sur de Puerto Banús"),
         "en": ("The week ahead, hour by hour", "Mean wind", "Gusts", "km/h", "Wave (m)", "Tide (cm)",
                "Rain (%)", "Forecast: Open-Meteo (AEMET and ECMWF models) and Copernicus Marine, 3 km south of Puerto Banús")}[lang]
    t = [datetime.datetime.fromisoformat(h["hora"]) for h in hs]
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(7.2, 6.2), dpi=150, sharex=True,
                                     gridspec_kw={"height_ratios": [1.3, 1, .7]})
    # días: franjas de noche en gris claro
    for h, x in zip(t, hs):
        if not (DIA_DESDE <= h.hour < DIA_HASTA):
            for ax in (a1, a2, a3):
                ax.axvspan(h, h + datetime.timedelta(hours=1), color="#EEF3F7", lw=0, zorder=0)
    a1.plot(t, [h["viento"] for h in hs], color=marino, lw=1.8, label=T[1])
    a1.plot(t, [h["racha"] for h in hs], color=rojo, lw=1, alpha=.7, label=T[2])
    # flechas de dirección cada 6 horas
    for h, x in zip(t, hs):
        if h.hour % 6 == 0 and x["dir"] is not None:
            ang = math.radians(270 - x["dir"])    # el viento VIENE de dir: la flecha apunta hacia donde va
            a1.annotate("", xy=(h + datetime.timedelta(hours=math.cos(ang) * 2.5), -4 + math.sin(ang) * 3),
                        xytext=(h, -4), arrowprops={"arrowstyle": "->", "color": "#4E5F70", "lw": .8}, annotation_clip=False)
    a1.set_ylim(bottom=-8)
    a1.set_ylabel(T[3], fontsize=8)
    a1.legend(fontsize=7, loc="upper left", frameon=False, ncol=2)
    a1.set_title(T[0], loc="left", fontsize=10, fontweight="bold", color=marino)
    a2.plot(t, [h["ola"] for h in hs], color=azul, lw=1.8)
    a2.set_ylabel(T[4], fontsize=8, color=azul)
    a2b = a2.twinx()
    niveles = [h["nivel"] for h in hs if h["nivel"] is not None]
    media = sum(niveles) / len(niveles) if niveles else 0
    a2b.plot(t, [(h["nivel"] - media) * 100 if h["nivel"] is not None else None for h in hs], color=gris, lw=1, ls="--")
    a2b.set_ylabel(T[5], fontsize=8, color="#4E5F70")
    a3.bar(t, [h["lluvia"] or 0 for h in hs], width=1 / 24, color=amarillo)
    a3.set_ylim(0, 100)
    a3.set_ylabel(T[6], fontsize=8)
    a3.xaxis.set_major_locator(mdates.DayLocator())
    a3.xaxis.set_major_formatter(mdates.DateFormatter("%a %d" if lang == "en" else "%d/%m"))
    for ax in (a1, a2, a2b, a3):
        _estilo(ax)
    fig.text(0.01, 0.005, T[7], fontsize=6.5, color="#4E5F70")
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta)
    plt.close(fig)
