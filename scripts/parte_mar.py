# -*- coding: utf-8 -*-
"""Parte del mar: previsión oficial de AEMET para la playa Río Verde - Puerto Banús.

    AEMET_API_KEY=... python scripts/parte_mar.py      -> datos/mar.json

Lo ejecuta la Action `parte.yml` dos veces al día. La clave es gratuita
(opendata.aemet.es → «Obtención de API Key») y va como secreto del
repositorio, nunca en la web. Sin clave, el script no hace nada y la web
enseña solo la hora de la puesta de sol.

AEMET devuelve en dos pasos: primero una URL temporal y luego los datos, en
ISO-8859-15. Licencia: reutilización libre citando «información elaborada por
la Agencia Estatal de Meteorología».
"""

import datetime
import json
import os
import sys
import time
import urllib.request

PLAYA = "2906906"                      # Rio Verde - Puerto Banús (Marbella)
API = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/playa/{PLAYA}"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "datos", "mar.json")


def pedir(url, clave=None, reintentos=4):
    cabeceras = {"Accept": "application/json", "User-Agent": "seawithjose.es"}
    if clave:
        cabeceras["api_key"] = clave
    ultimo = None
    for i in range(reintentos):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=cabeceras), timeout=60) as r:
                return r.read()
        except Exception as e:                                    # noqa: BLE001  (AEMET falla a ratos)
            ultimo = e
            time.sleep(5 * (i + 1))
    raise ultimo


def texto(d, campo, n):
    return (d.get(campo, {}).get(f"descripcion{n}") or "").strip().lower()


def main():
    clave = os.environ.get("AEMET_API_KEY", "").strip()
    if not clave:
        print("Sin AEMET_API_KEY: no se actualiza el parte.")
        return 0
    indice = json.loads(pedir(API, clave).decode("utf-8", "replace"))
    if indice.get("estado") != 200 or not indice.get("datos"):
        print(f"AEMET no da datos: {indice}")
        return 1
    bruto = pedir(indice["datos"])
    datos = json.loads(bruto.decode("iso-8859-15"))
    pred = datos[0]["prediccion"]["dia"]
    dias = []
    for d in pred:
        f = str(d.get("fecha"))
        dias.append({
            "fecha": f"{f[:4]}-{f[4:6]}-{f[6:8]}",
            "cielo": [texto(d, "estadoCielo", 1), texto(d, "estadoCielo", 2)],
            "viento": [texto(d, "viento", 1), texto(d, "viento", 2)],
            "oleaje": [texto(d, "oleaje", 1), texto(d, "oleaje", 2)],
            "agua": d.get("tAgua", {}).get("valor1"),
            "maxima": d.get("tMaxima", {}).get("valor1"),
            "uv": d.get("uvMax", {}).get("valor1"),
        })
    salida = {
        "generado": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "playa": datos[0].get("nombre"), "elaborado": datos[0].get("elaborado"),
        "fuente": "Información elaborada por la Agencia Estatal de Meteorología (AEMET)",
        "dias": dias,
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    print(f"Parte actualizado: {[x['fecha'] for x in dias]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
