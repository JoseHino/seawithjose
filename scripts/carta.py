# -*- coding: utf-8 -*-
"""Carta náutica de la portada: isobatas reales de la costa de Marbella.

    python scripts/carta.py      -> fuentes/carta.json (trazados ya proyectados)

Batimetría: EMODnet Bathymetry (DTM europeo, ~115 m), licencia CC BY 4.0, que
permite el uso comercial citando la fuente. NO se usan los datos del IHM del
gemelo digital: su licencia no está aclarada para webs públicas.

El resultado son trazados en coordenadas de un lienzo de ANCHO x ALTO, ya
suavizados, que build.py pinta como SVG en línea (así las líneas se animan y
toman los colores de la web).
"""

import json
import math
import os
import sys
import urllib.request

import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape, LineString, MultiLineString, box
from shapely.ops import unary_union, linemerge

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIF = os.path.join(RAIZ, "fuentes", "emodnet_marbella.tif")
SALIDA = os.path.join(RAIZ, "fuentes", "carta.json")

# Encuadre de la lámina: de San Pedro Alcántara a Marbella
W, E, S, N = -5.005, -4.875, 36.430, 36.515
ANCHO = 1000
ALTO = round(ANCHO * (N - S) / ((E - W) * math.cos(math.radians((N + S) / 2))))
PROFUNDIDADES = [5, 10, 20, 30, 50, 75, 100, 150]

EMOD = ("https://ows.emodnet-bathymetry.eu/wcs?service=WCS&version=2.0.1&request=GetCoverage"
        "&coverageId=emodnet__mean&format=image/tiff&subset=Lat({s},{n})&subset=Long({w},{e})")


def descargar():
    if os.path.exists(TIF):
        return
    os.makedirs(os.path.dirname(TIF), exist_ok=True)
    url = EMOD.format(s=S - 0.01, n=N + 0.01, w=W - 0.01, e=E + 0.01)
    with urllib.request.urlopen(url, timeout=180) as r:
        datos = r.read()
    if not datos.startswith((b"II*", b"MM\x00*")):
        sys.exit("EMODnet no ha devuelto un GeoTIFF: " + datos[:300].decode("utf-8", "replace"))
    open(TIF, "wb").write(datos)


def proyectar(lon, lat):
    return (round((lon - W) / (E - W) * ANCHO, 1), round((N - lat) / (N - S) * ALTO, 1))


def chaikin(coords, vueltas=3, cerrado=False):
    """Suaviza la escalera de los píxeles sin mover la forma general."""
    pts = list(coords)
    for _ in range(vueltas):
        nuevos = [] if cerrado else [pts[0]]
        rango = range(len(pts)) if cerrado else range(len(pts) - 1)
        for i in rango:
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            nuevos += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1),
                       (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        if not cerrado:
            nuevos.append(pts[-1])
        pts = nuevos
    return pts


def a_trazado(coords, cerrado=False):
    pts = [tuple(round(v) for v in proyectar(x, y)) for x, y in coords]
    if len(pts) < 2:
        return ""
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    return d + ("Z" if cerrado else "")


def main():
    descargar()
    with rasterio.open(TIF) as src:
        z = src.read(1).astype("float64")
        nodata = src.nodata
        tr = src.transform
    tierra = np.isnan(z) | (z > 0)
    if nodata is not None:
        tierra |= (z == nodata)
    prof = np.where(tierra, 0, -z)          # metros, positivo hacia abajo
    print(f"Rejilla {z.shape}, profundidad máx. {prof.max():.0f} m")

    marco = box(W, S, E, N)
    borde = marco.exterior

    # Tierra: polígonos de las celdas sin fondo
    poligonos = [shape(g) for g, v in shapes(tierra.astype("uint8"), transform=tr) if v == 1]
    tierra_geo = unary_union(poligonos).intersection(marco).simplify(0.0006)
    trazados_tierra = []
    for p in getattr(tierra_geo, "geoms", [tierra_geo]):
        if p.is_empty or p.area < 1e-6:
            continue
        anillo = list(p.exterior.coords)[:-1]
        trazados_tierra.append(a_trazado(chaikin(anillo, 2, cerrado=True), cerrado=True))

    # Isobatas: borde de la zona más profunda que cada valor, sin el marco
    isobatas = []
    for d in PROFUNDIDADES:
        mascara = (prof >= d).astype("uint8")
        pols = [shape(g) for g, v in shapes(mascara, transform=tr) if v == 1]
        if not pols:
            continue
        zona = unary_union(pols)
        lineas = zona.boundary.difference(borde.buffer(0.0008)).intersection(marco)
        lineas = linemerge(lineas) if not isinstance(lineas, LineString) else lineas
        for l in getattr(lineas, "geoms", [lineas]):
            if l.is_empty or l.length < 0.006:
                continue
            l = l.simplify(0.0005)
            isobatas.append({"m": d, "d": a_trazado(chaikin(list(l.coords), 3))})
        print(f"  isobata {d} m: {sum(1 for i in isobatas if i['m'] == d)} tramos")

    # Sondas: profundidades reales en una malla con algo de desorden, solo en el mar
    rng = np.random.default_rng(7)
    sondas = []
    for lat in np.linspace(S + 0.005, N - 0.008, 7):
        for lon in np.linspace(W + 0.006, E - 0.006, 9):
            lon_j, lat_j = lon + rng.uniform(-0.003, 0.003), lat + rng.uniform(-0.002, 0.002)
            fila, col = ~tr * (lon_j, lat_j)
            fila, col = int(col), int(fila)
            if 0 <= fila < prof.shape[0] and 0 <= col < prof.shape[1] and prof[fila, col] >= 4:
                x, y = proyectar(lon_j, lat_j)
                sondas.append({"x": x, "y": y, "m": int(round(prof[fila, col]))})

    carta = {
        "ancho": ANCHO, "alto": ALTO, "encuadre": [W, S, E, N],
        "fuente": "EMODnet Bathymetry Consortium · CC BY 4.0",
        "tierra": trazados_tierra, "isobatas": isobatas, "sondas": sondas,
        "lugares": {   # posiciones aproximadas, solo para rotular la carta
            "banus": proyectar(-4.9530, 36.4846),
            "sanpedro": proyectar(-4.9905, 36.4865),
            "marbella": proyectar(-4.8860, 36.5100),
            "galeon": proyectar(-4.9800, 36.4750),
            "rioverde": proyectar(-4.9395, 36.4930),
            "alboran": proyectar(-4.9750, 36.4370),
        },
    }
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(carta, f, ensure_ascii=False)
    print(f"Listo: {SALIDA} · {ALTO=} · tierra {len(trazados_tierra)} · isobatas {len(isobatas)} · sondas {len(sondas)}")


if __name__ == "__main__":
    main()
