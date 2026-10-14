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
| `build.py` | Monta las páginas: portada (precios, ruta, reserva, extras, barco, el mar hoy, Jose, cómo llegar, buceo, preguntas), la Senda Azul, gracias y aviso legal. |
| `assets/estilo.css` | Diseño: colores de las banderas del Código (azul, amarillo, rojo), titulares en Sofia Sans Extra Condensed y texto en Sofia Sans. |
| `assets/web.js` | Reserva (resumen, pago o WhatsApp), notas del 1 al 10, vídeo, filtros de buceo, página de gracias y menú del móvil. |
| `scripts/carta.py` | Isobatas reales de EMODnet (CC BY 4.0) para la carta con la ruta → `fuentes/carta.json`. |
| `scripts/mapa.py` | Plano de Puerto Banús con el parking Cristamar, de OpenStreetMap (ODbL) → `fuentes/mapa_banus.json`. |
| `scripts/recursos.py` | Descarga las tipografías (servidas desde la propia web, sin cookies) y optimiza las fotos. |
| `scripts/revista.py` | La Bitácora del mar: ver más abajo. |
| `scripts/parte_mar.py` | Previsión de AEMET y notas del 1 al 10 para navegar, bucear y pescar → `datos/mar.json`. |

## El mar, ahora (parte, notas y cámaras)

La Action `parte.yml` ejecuta `scripts/parte_mar.py` cada tres horas (de 7:15
a 22:15 en verano) y sube `datos/mar.json`. No necesita clave: lee los XML
públicos de AEMET de la playa Río Verde – Puerto Banús, de Marbella por horas
y por días, y el boletín costero de «Aguas costeras de Málaga» (estado de la
mar, fuerza del viento, mar de fondo y avisos). Licencia de AEMET: uso libre
citándola como autora, y la web la cita.

Con eso la web pinta el parte de la portada y la sección «El mar, ahora»:

- **Notas del 1 al 10** para navegar, bucear y pescar, por tramos de 8 a 14 h y
  de 14 a 20 h, para hoy y los dos días siguientes. Las reglas están en
  `notas()` de `scripts/parte_mar.py` y se explican en la propia web («Cómo
  pongo la nota»). Para cambiarlas, se toca esa función y se lanza la Action a
  mano (*Actions → Parte del mar → Run workflow*).
- **Cámaras en directo**: SkylineWebcams (puerto deportivo, y puerto y paseo
  marítimo) y meteo365 (playa de El Cable y La Bajadilla). Ninguna deja
  incrustarse en otras webs (bloquean los iframes y sus directos de YouTube no
  se pueden insertar), así que cada tarjeta abre la cámara en su web. Si algún
  día hay permiso de una de ellas, o una cámara propia emitiendo en YouTube, se
  cambia la tarjeta por el vídeo. Las direcciones están en `textos.py`.

Sin datos (AEMET caído), la portada enseña la puesta de sol, que se calcula en
el navegador, y la sección invita a escribir por WhatsApp.

## La Bitácora del mar (revista quincenal)

Revista gratuita cada quince días, en español e inglés: el mar de la quincena frente a Puerto Banús (agua,
olas, viento y luna) y lo más interesante de Marbella, buceo, vela y barcos, pesca, viajes por mar y el océano.
Página: `revista.html` (EN), `es/revista.html`, `ru/revista.html`; números publicados en `revista/`.

| Pieza | Qué hace |
|---|---|
| `revista-noticias.yml` → `scripts/revista_noticias.py` | Cada día guarda titulares de Google Noticias por eje e idioma en `datos/revista/noticias.json` (40 días). |
| `revista-borrador.yml` → `scripts/revista.py borrador` | Días 1 y 16 (o a mano): cifras del mar (Open-Meteo y AEMET), la IA redacta los dos idiomas y se abre una incidencia con la etiqueta `revista` que menciona a Jose. |
| `revista-revision.yml` → `scripts/revista.py revisar` | Cuando Jose contesta la incidencia (respondiendo al correo de GitHub): «OK» publica en la web y envía con Brevo; si pide cambios, la IA hace la versión siguiente. |
| `revista/instrucciones_*.md` | Lo que se le pide a la IA. Se cambian aquí, sin tocar código. **La IA no escribe cifras**: la tabla del mar la monta el script. |

Necesita en GitHub (*Settings → Secrets and variables → Actions*):

- Secretos: `OPENAI_API_KEY` y `BREVO_API_KEY`.
- Variables: `BREVO_LISTA_ES` y `BREVO_LISTA_EN` (ID de cada lista de Brevo). Opcionales: `REVISTA_MODELO`
  (por defecto `gpt-5.6-terra`), `REVISTA_REMITENTE` (por defecto `jose@seawithjose.es`, dominio ya
  autenticado en Brevo) y `REVISTA_RESPONDER` (adonde van las respuestas de los lectores).
- En `textos.py`, `REVISTA_FORMS`: el enlace del formulario de Brevo de cada idioma. Al confirmar, el formulario
  debe volver a `https://seawithjose.es/revista.html?suscripcion=pendiente` y `…?suscripcion=ok`.

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
