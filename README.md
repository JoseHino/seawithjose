# Sea With Jose · web

Web de la marca personal de José María Hinojosa: salidas en velero, buceo,
pesca y motos de agua desde Puerto Banús. Inglés en la raíz, español en
`/es/` y ruso en `/ru/`. Dominio: **seawithjose.es** (Hostinger).

## Cómo se cambia

Todo el texto está en `textos.py`, en los tres idiomas. Después de tocarlo:

```bash
python build.py
```

Eso regenera `index.html`, `es/`, `ru/`, las páginas legales, el 404, el
`sitemap.xml` y el `robots.txt`. Luego, `git commit` y `git push`.

| Pieza | Qué es |
|---|---|
| `textos.py` | Textos, teléfono, Instagram y correo. |
| `build.py` | Monta las páginas: carta náutica, experiencias, Jose, buceo, pasos, planificador y preguntas. |
| `assets/estilo.css` | Diseño. Paleta de carta náutica: papel, tinta, isobatas, tierra y magenta para lo que se pulsa. |
| `assets/web.js` | Parte del mar, puesta de sol, planificador de WhatsApp y menú del móvil. |
| `scripts/carta.py` | Isobatas reales de EMODnet (CC BY 4.0) para la carta de la portada → `fuentes/carta.json`. |
| `scripts/recursos.py` | Descarga las tipografías (servidas desde la propia web, sin cookies) y optimiza las fotos. |
| `scripts/parte_mar.py` | Previsión de AEMET para la playa Río Verde – Puerto Banús → `datos/mar.json`. |

## El parte del mar

Lo actualiza la Action `parte.yml` dos veces al día. Necesita una clave
gratuita de AEMET:

1. Pedirla en https://opendata.aemet.es/centrodedescargas/altaUsuario (llega por correo).
2. Guardarla en GitHub: *Settings → Secrets and variables → Actions → New repository
   secret*, con el nombre `AEMET_API_KEY`.
3. Lanzar la Action una vez a mano (*Actions → Parte del mar → Run workflow*).

Sin clave, la web enseña solo la hora de la puesta de sol, que se calcula en
el navegador.

## Dominio

En Hostinger → Dominios → seawithjose.es → DNS:

- Borrar el registro A del aparcamiento.
- Cuatro registros A para `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- Un CNAME para `www` → `josehino.github.io`.

Después, en GitHub: *Settings → Pages → Custom domain* = `seawithjose.es` y
marcar *Enforce HTTPS* cuando GitHub lo permita (unos minutos u horas). Eso
crea el fichero `CNAME` en el repositorio.

## Pendiente

- NIF y domicilio para el aviso legal (LSSI), cuando se den de alta.
- Fotos propias de calidad, sobre todo del velero navegando, de la pesca y de las motos.
- Precios y forma de reserva cuando el barco tenga el despacho para chárter.
