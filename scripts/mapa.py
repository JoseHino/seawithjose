# -*- coding: utf-8 -*-
"""Plano de Puerto Banús para «Cómo llegar»: el puerto, las calles y el parking Cristamar.

    python scripts/mapa.py      -> fuentes/mapa_banus.json (trazados ya proyectados)

Datos: © colaboradores de OpenStreetMap, licencia ODbL (se cita en la web). El
extracto se descarga una vez de Overpass a fuentes/osm_banus.json; build.py
pinta el plano como SVG en línea con los colores de la web.
"""

import json
import math
import os
import sys
import urllib.parse
import urllib.request

from shapely.geometry import LineString, MultiLineString, Polygon, box
from shapely.ops import linemerge, unary_union

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OSM = os.path.join(RAIZ, "fuentes", "osm_banus.json")
SALIDA = os.path.join(RAIZ, "fuentes", "mapa_banus.json")

# Encuadre: el puerto deportivo, Avenida Julio Iglesias y el centro comercial Cristamar
W, E, S, N = -4.9615, -4.9415, 36.4800, 36.4930
ANCHO = 1000
ALTO = round(ANCHO * (N - S) / ((E - W) * math.cos(math.radians((N + S) / 2))))
PARKING = (-4.95039, 36.49013)          # Parking Cristamar (nodo 1042923293 de OSM), calle Francisco Villalón

CONSULTA = ('[out:json][timeout:90];(way["natural"="coastline"]({b});way["man_made"~"pier|breakwater|groyne"]({b});'
            'way["leisure"="marina"]({b});way["highway"]({b});way["building"]({b});way["natural"~"water|beach"]({b});'
            ');out geom tags;')


def descargar():
    if os.path.exists(OSM):
        return
    b = f"{S - 0.003},{W - 0.004},{N + 0.003},{E + 0.004}"
    datos = urllib.parse.urlencode({"data": CONSULTA.format(b=b)}).encode()
    req = urllib.request.Request("https://overpass.kumi.systems/api/interpreter", data=datos,
                                 headers={"User-Agent": "seawithjose.es (plano del parking)"})
    with urllib.request.urlopen(req, timeout=200) as r:
        open(OSM, "wb").write(r.read())


def proyectar(lon, lat):
    return ((lon - W) / (E - W) * ANCHO, (N - lat) / (N - S) * ALTO)


def trazado(geom, cerrar=False):
    partes = getattr(geom, "geoms", [geom])
    d = []
    for g in partes:
        if g.is_empty:
            continue
        if g.geom_type == "Polygon":
            for anillo in [g.exterior, *g.interiors]:
                pts = [proyectar(x, y) for x, y in anillo.coords]
                d.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
        else:
            pts = [proyectar(x, y) for x, y in g.coords]
            d.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + ("Z" if cerrar else ""))
    return " ".join(d)


def main():
    descargar()
    elementos = json.load(open(OSM, encoding="utf-8"))["elements"]
    marco = box(W, S, E, N)

    def linea(e):
        return LineString([(p["lon"], p["lat"]) for p in e["geometry"]])

    def poligono(e):
        pts = [(p["lon"], p["lat"]) for p in e["geometry"]]
        return Polygon(pts) if len(pts) >= 4 and pts[0] == pts[-1] else None

    # El mar: la línea de costa (va de oeste a este con el mar a la derecha, como manda OSM) cerrada por el sur
    costa = linemerge(unary_union([linea(e) for e in elementos if e.get("tags", {}).get("natural") == "coastline"]))
    pts = list(costa.coords)
    lejos = 0.05
    anillo = pts + [(pts[-1][0] + lejos, pts[-1][1]), (pts[-1][0] + lejos, S - lejos), (pts[0][0] - lejos, S - lejos),
                    (pts[0][0] - lejos, pts[0][1])]
    mar = Polygon(anillo).buffer(0).intersection(marco)

    edificios, diques, calles = [], [], {"grande": [], "media": [], "fina": [], "peatonal": []}
    for e in elementos:
        t = e.get("tags", {})
        if "geometry" not in e:
            continue
        if "building" in t:
            p = poligono(e)
            if p is not None and p.is_valid and p.intersects(marco):
                edificios.append(p.intersection(marco))
        elif t.get("man_made") in ("pier", "breakwater", "groyne"):
            g = poligono(e) or linea(e)
            if g.intersects(marco):
                diques.append((g.geom_type, g.intersection(marco)))
        elif "highway" in t:
            g = linea(e).intersection(marco)
            if g.is_empty:
                continue
            h = t["highway"]
            clase = ("grande" if h in ("motorway", "trunk", "primary", "secondary")
                     else "media" if h in ("tertiary", "tertiary_link", "secondary_link", "trunk_link")
                     else "peatonal" if h in ("pedestrian", "footway", "steps", "path")
                     else "fina" if h in ("residential", "unclassified", "living_street", "service") else None)
            if clase:
                calles[clase].append(g)

    plano = {
        "ancho": ANCHO, "alto": ALTO, "encuadre": [W, S, E, N],
        "fuente": "© OpenStreetMap contributors · ODbL",
        "mar": trazado(mar.simplify(0.00002)),
        "edificios": trazado(unary_union(edificios).simplify(0.000015)),
        "diques": [trazado(g.simplify(0.00001), cerrar=(tipo == "Polygon")) for tipo, g in diques if not g.is_empty],
        "diques_tipo": [tipo for tipo, g in diques if not g.is_empty],
        "calles": {k: trazado(MultiLineString([*(x for g in v for x in getattr(g, "geoms", [g]))]).simplify(0.00001))
                   for k, v in calles.items() if v},
        "parking": proyectar(*PARKING),
    }
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(plano, f, ensure_ascii=False)
    print(f"Plano {ANCHO}x{ALTO}: {len(edificios)} edificios, {len(diques)} diques, "
          f"{sum(len(v) for v in calles.values())} calles → {SALIDA}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
