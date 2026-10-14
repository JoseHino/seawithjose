# -*- coding: utf-8 -*-
"""Datos oficiales de AEMET en Marbella: observación horaria y valores climatológicos diarios.

    python scripts/datos_marbella.py              -> añade las últimas 24 h a datos/marbella/horario.json
    python scripts/datos_marbella.py historico    -> rellena datos/marbella/diario.json desde 2004 (una vez)

Estaciones de AEMET en el término municipal:
  6076X  Marbella, Puerto   (puerto deportivo)
  6083X  Marbella

AEMET OpenData solo da la observación horaria de las últimas 24 horas, así que la Action
`datos-marbella.yml` la pide cada tres horas y la va acumulando: el histórico horario empieza el día en
que se puso en marcha. Hacia atrás hay valores diarios (climatológicos) desde que existe cada estación.

Necesita la clave gratuita de AEMET OpenData en AEMET_API_KEY.
Licencia: «© AEMET. Autorizado el uso de la información y su reproducción citando a AEMET como autora».
"""

import datetime
import json
import os
import sys
import time
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(RAIZ, "datos", "marbella")
ESTACIONES = {"6076X": "Marbella, Puerto", "6083X": "Marbella"}
API = "https://opendata.aemet.es/opendata/api"


def pedir(url, reintentos=5):
    ultimo = None
    for i in range(reintentos):
        try:
            req = urllib.request.Request(url, headers={"api_key": os.environ["AEMET_API_KEY"], "Accept": "application/json",
                                                       "User-Agent": "seawithjose-datos"})
            with urllib.request.urlopen(req, timeout=60) as r:
                bruto = r.read()
            try:
                return json.loads(bruto.decode("utf-8"))
            except UnicodeDecodeError:
                return json.loads(bruto.decode("latin-1"))        # AEMET sirve a veces latin-1 sin decirlo
        except Exception as e:  # noqa: BLE001
            ultimo = e
            time.sleep(6 * (i + 1))                                # el cupo de AEMET castiga las ráfagas
    raise RuntimeError(f"{url}: {ultimo}")


def datos(ruta):
    """AEMET contesta con un enlace a los datos; hay que pedirlo aparte."""
    r = pedir(API + ruta)
    if r.get("estado") != 200:
        raise RuntimeError(f"{ruta}: {r.get('estado')} {r.get('descripcion')}")
    return pedir(r["datos"])


def leer(nombre, defecto):
    try:
        return json.load(open(os.path.join(CARPETA, nombre), encoding="utf-8"))
    except (OSError, ValueError):
        return defecto


def escribir(nombre, obj):
    os.makedirs(CARPETA, exist_ok=True)
    with open(os.path.join(CARPETA, nombre), "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def horario():
    total = leer("horario.json", {"fuente": "AEMET OpenData, observación convencional", "estaciones": {}})
    for idema, nombre in ESTACIONES.items():
        try:
            obs = datos(f"/observacion/convencional/datos/estacion/{idema}")
        except Exception as e:  # noqa: BLE001
            print(f"{idema}: sin datos ({e})")
            continue
        est = total["estaciones"].setdefault(idema, {"nombre": nombre, "obs": {}})
        nuevas = 0
        for o in obs:
            hora = o.get("fint")
            if not hora:
                continue
            fila = {k: v for k, v in o.items() if isinstance(v, (int, float)) and k not in ("lat", "lon", "alt")}
            if hora not in est["obs"]:
                nuevas += 1
            est["obs"][hora] = fila
        est["variables"] = sorted({k for f in est["obs"].values() for k in f})
        print(f"{idema} {nombre}: {nuevas} horas nuevas, {len(est['obs'])} en total · variables: {', '.join(est['variables'])}")
        time.sleep(3)
    total["actualizado"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    escribir("horario.json", total)


def historico(desde=2004):
    """Valores diarios, en tramos de seis meses (AEMET no da más de una vez)."""
    total = leer("diario.json", {"fuente": "AEMET OpenData, valores climatológicos diarios", "estaciones": {}})
    hoy = datetime.date.today()
    for idema, nombre in ESTACIONES.items():
        est = total["estaciones"].setdefault(idema, {"nombre": nombre, "dias": {}})
        ini = datetime.date(desde, 1, 1)
        while ini <= hoy:
            fin = min(datetime.date(ini.year + (ini.month + 5) // 12, (ini.month + 5) % 12 + 1, 1)
                      - datetime.timedelta(days=1), hoy)
            ruta = (f"/valores/climatologicos/diarios/datos/fechaini/{ini}T00:00:00UTC/fechafin/{fin}T23:59:59UTC"
                    f"/estacion/{idema}")
            try:
                for d in datos(ruta):
                    fila = {}
                    for k, v in d.items():
                        if k in ("fecha", "indicativo", "nombre", "provincia", "altitud"):
                            continue
                        try:
                            fila[k] = float(str(v).replace(",", "."))
                        except ValueError:
                            if k == "prec" and str(v).strip() == "Ip":        # «Ip»: precipitación inapreciable
                                fila[k] = 0.0
                    est["dias"][d["fecha"]] = fila
            except Exception as e:  # noqa: BLE001
                print(f"{idema} {ini}..{fin}: {e}")
            ini = fin + datetime.timedelta(days=1)
            time.sleep(2)
        est["variables"] = sorted({k for f in est["dias"].values() for k in f})
        print(f"{idema} {nombre}: {len(est['dias'])} días · variables: {', '.join(est['variables'])}")
    escribir("diario.json", total)


if __name__ == "__main__":
    if not os.environ.get("AEMET_API_KEY"):
        sys.exit("Falta AEMET_API_KEY")
    historico() if sys.argv[1:] == ["historico"] else horario()
