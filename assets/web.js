/* Sea With Jose · comportamiento de la web (sin dependencias) */
(() => {
  const nodo = document.getElementById('datos-pagina');
  const d = nodo ? JSON.parse(nodo.textContent) : {};

  // ── menú del móvil ──
  const boton = document.querySelector('.menu-boton');
  const nav = document.getElementById('navegacion');
  if (boton && nav) {
    const cerrar = () => { boton.setAttribute('aria-expanded', 'false'); nav.classList.remove('abierta'); };
    boton.addEventListener('click', () => {
      const abrir = boton.getAttribute('aria-expanded') !== 'true';
      boton.setAttribute('aria-expanded', String(abrir));
      nav.classList.toggle('abierta', abrir);
    });
    nav.addEventListener('click', e => { if (e.target.closest('a')) cerrar(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') cerrar(); });
  }

  // ── filete de la cabecera al bajar ──
  const cabecera = document.querySelector('.cabecera');
  const marcar = () => cabecera && cabecera.classList.toggle('con-borde', window.scrollY > 8);
  window.addEventListener('scroll', marcar, { passive: true });
  marcar();

  // ── parte del mar (portada) y «el mar, ahora»: los dos leen datos/mar.json ──
  const parte = document.querySelector('.parte');
  const mar = document.getElementById('mar');
  const datosMar = (parte || mar)
    ? fetch(`${d.prefijo}datos/mar.json`, { cache: 'no-store' }).then(r => (r.ok ? r.json() : null)).catch(() => null)
    : Promise.resolve(null);
  if (parte && d.parte) pintarParte(parte, d, datosMar);
  if (mar && d.mar) pintarMar(mar, d, datosMar);

  // ── planificador → WhatsApp ──
  const form = document.getElementById('planificador');
  if (form && d.plan) {
    const fecha = form.querySelector('input[type="date"]');
    if (fecha) fecha.min = hoyEnMadrid();
    form.addEventListener('submit', e => {
      e.preventDefault();
      const p = d.plan, f = new FormData(form), lineas = [p.msg_inicio];
      const anadir = (clave, valor) => { if (valor) lineas.push(`${clave}: ${valor}`); };
      anadir(p.msg_actividad, f.get('actividad'));
      const dia = f.get('fecha');
      if (dia) {
        const formato = new Intl.DateTimeFormat(d.lang, { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
        anadir(p.msg_fecha, formato.format(new Date(dia + 'T00:00:00Z')));
      }
      anadir(p.msg_personas, f.get('personas'));
      anadir(p.msg_nombre, String(f.get('nombre') || '').trim());
      anadir(p.msg_notas, String(f.get('notas') || '').trim());
      window.open(`https://wa.me/${d.whatsapp}?text=${encodeURIComponent(lineas.join('\n'))}`, '_blank', 'noopener');
    });
  }

  function hoyEnMadrid(desplazamiento = 0) {
    const fecha = new Date(Date.now() + desplazamiento * 86400000);
    return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Madrid' }).format(fecha);   // AAAA-MM-DD
  }

  // Puesta de sol con la ecuación del amanecer (NOAA simplificada), en Puerto Banús
  function puestaDeSol(diaUTC, lat = 36.4846, lon = -4.953) {
    const rad = Math.PI / 180;
    const jd = diaUTC.getTime() / 86400000 + 2440587.5;
    const n = Math.round(jd - 2451545.0 + 0.0008);
    const jEstrella = n - lon / 360;
    const M = (357.5291 + 0.98560028 * jEstrella) % 360;
    const C = 1.9148 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 0.0003 * Math.sin(3 * M * rad);
    const lambda = (M + C + 180 + 102.9372) % 360;
    const jTransito = 2451545.0 + jEstrella + 0.0053 * Math.sin(M * rad) - 0.0069 * Math.sin(2 * lambda * rad);
    const senDec = Math.sin(lambda * rad) * Math.sin(23.4397 * rad);
    const cosDec = Math.cos(Math.asin(senDec));
    const cosW = (Math.sin(-0.833 * rad) - Math.sin(lat * rad) * senDec) / (Math.cos(lat * rad) * cosDec);
    const jPuesta = jTransito + (Math.acos(cosW) / rad) / 360;
    return new Date((jPuesta - 2440587.5) * 86400000);
  }

  async function pintarParte(el, d, promesa) {
    const t = d.parte;
    const hoy = hoyEnMadrid();
    let dia = null, etiqueta = '';
    const datos = await promesa;              // sin parte: se queda la puesta de sol y el mensaje
    if (datos) {
      const dias = datos.dias || [];
      dia = dias.find(x => x.fecha === hoy) || null;
      if (!dia) {
        const siguiente = dias.find(x => x.fecha === hoyEnMadrid(1));
        if (siguiente) { dia = siguiente; etiqueta = 'manana'; }
      }
    }

    const palabra = s => (t.palabras[String(s || '').toLowerCase()] || s || '').trim();
    const doble = par => {
      const [a, b] = par || [];
      if (!a && !b) return '';
      if (!b || a === b) return palabra(a || b);
      return `${palabra(a)} (${t.manana}) · ${palabra(b)} (${t.tarde})`;
    };
    const filas = [];
    if (dia) {
      if (dia.agua != null) filas.push([t.agua, `${dia.agua} °C`]);
      if (dia.maxima != null) filas.push([t.aire, `${dia.maxima} °C`]);
      if (doble(dia.viento)) filas.push([t.viento, doble(dia.viento)]);
      if (doble(dia.oleaje)) filas.push([t.oleaje, doble(dia.oleaje)]);
    }
    const base = dia ? new Date(`${dia.fecha}T12:00:00Z`) : new Date(`${hoy}T12:00:00Z`);
    const hora = new Intl.DateTimeFormat(d.lang, { hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'Europe/Madrid' });
    filas.push([t.puesta, hora.format(puestaDeSol(base))]);

    const dl = el.querySelector('.parte-datos');
    dl.replaceChildren(...filas.flatMap(([k, v]) => {
      const dt = document.createElement('dt'), dd = document.createElement('dd');
      dt.textContent = k; dd.textContent = v;
      return [dt, dd];
    }));
    if (etiqueta) el.querySelector('.parte-titulo').textContent = t.titulo_manana;
    el.querySelector('.parte-lectura').textContent = dia ? lectura(dia, t) : '';
    el.querySelector('.parte-fuente').textContent = dia ? t.fuente : t.sin_datos;
  }

  function lectura(dia, t) {
    const [vm, vt] = dia.viento || [], [om, ot] = dia.oleaje || [];
    if ([vm, vt, om, ot].includes('fuerte')) return t.lecturas.movida;
    if (om === 'débil' && vm === 'flojo') return t.lecturas.calma;
    if (vt === 'moderado' && ot !== 'fuerte') return t.lecturas.brisa;
    return '';
  }

  // ── el mar, ahora: notas del 1 al 10 por día y tramo (las calcula scripts/parte_mar.py) ──
  function ahoraEnMadrid() {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    }).formatToParts(new Date()).map(x => [x.type, x.value]));
    return { fecha: `${p.year}-${p.month}-${p.day}`, hora: Number(p.hour) + Number(p.minute) / 60 };
  }

  function crear(etiqueta, texto, clase) {
    const n = document.createElement(etiqueta);
    if (texto != null) n.textContent = texto;
    if (clase) n.className = clase;
    return n;
  }

  async function pintarMar(el, d, promesa) {
    const m = d.mar, datos = await promesa;
    const ahora = ahoraEnMadrid(), manana = hoyEnMadrid(1);
    const pasado = (fecha, t) => fecha < ahora.fecha || (fecha === ahora.fecha && ahora.hora >= t.a);
    const dias = ((datos && datos.dias) || []).filter(x =>
      x.fecha >= ahora.fecha && (x.tramos || []).some(t => t.notas && !pasado(x.fecha, t)));
    const estado = el.querySelector('.notas-estado');
    if (!dias.length) {
      const enlace = crear('a', 'WhatsApp');
      enlace.href = `https://wa.me/${d.whatsapp}?text=${encodeURIComponent(d.plan.msg_inicio)}`;
      estado.replaceChildren(`${m.sin_datos} `, enlace);
      return;
    }
    estado.hidden = true;
    el.querySelector('.indices').hidden = false;
    el.querySelector('.notas-detalle').hidden = false;

    const mediodia = f => new Date(`${f}T12:00:00Z`);
    const diaSemana = new Intl.DateTimeFormat(d.lang, { weekday: 'long', timeZone: 'UTC' });
    const diaCorto = new Intl.DateTimeFormat(d.lang, { day: 'numeric', month: 'short', timeZone: 'UTC' });
    const nombreDia = f => {
      if (f === ahora.fecha) return m.hoy;
      if (f === manana) return m.manana;
      const s = diaSemana.format(mediodia(f));
      return s.charAt(0).toUpperCase() + s.slice(1);
    };
    const hh = h => String(h).padStart(2, '0');
    const tramo = t => `${hh(t.de)}–${hh(t.a)} ${m.tramo}`;

    const botones = dias.map((x, i) => {
      const b = crear('button', null, 'dia');
      b.type = 'button';
      b.append(crear('span', nombreDia(x.fecha)), crear('small', diaCorto.format(mediodia(x.fecha))));
      b.addEventListener('click', () => elegir(i));
      return b;
    });
    el.querySelector('.dias').replaceChildren(...botones);

    function elegir(i) {
      botones.forEach((b, j) => b.setAttribute('aria-pressed', String(i === j)));
      pintarDia(dias[i]);
    }

    function pintarDia(dia) {
      const tramos = dia.tramos.filter(t => t.notas);
      const vivos = tramos.filter(t => !pasado(dia.fecha, t));
      for (const art of el.querySelectorAll('.indice')) {
        const act = art.dataset.act;
        const mejor = vivos.reduce((a, t) => (!a || t.notas[act].n > a.notas[act].n ? t : a), null);
        const n = mejor.notas[act].n, nivel = Math.min(4, Math.floor((n - 1) / 2));
        const destaca = vivos.length > 1 && vivos.every(t => t === mejor || t.notas[act].n < n);
        art.dataset.nivel = nivel;
        art.querySelector('.indice-n').textContent = n;
        art.querySelector('.indice-banda').textContent = m.bandas[nivel];
        art.querySelectorAll('.indice-escala i').forEach((c, i) => c.classList.toggle('lleno', i < n));
        art.querySelector('.indice-frase').textContent = m.motivos[mejor.notas[act].m] || '';
        art.querySelector('.indice-tramos').replaceChildren(...tramos.map(t => {
          const ya = pasado(dia.fecha, t);
          const li = crear('li', null, ya ? 'pasado' : (destaca && t === mejor ? 'mejor' : ''));
          li.append(crear('span', tramo(t)), crear('strong', ya ? m.pasado : String(t.notas[act].n)));
          return li;
        }));
      }
      pintarBitacora(dia, tramos);
    }

    function pintarBitacora(dia, tramos) {
      const viento = t => {
        if (t.viento == null) return '–';
        if (t.dir === 'C' || t.viento < 2) return m.rumbos.C;
        return `${m.rumbos[t.dir] || t.dir} ${t.viento} ${m.kmh}`;
      };
      const filas = [
        [m.tabla.viento, viento],
        [m.tabla.racha, t => (t.racha == null ? '–' : `${t.racha} ${m.kmh}`)],
        [m.tabla.mar, t => (t.mar == null ? '–' : m.mar_clases[t.mar] + (t.fondo ? ` + ${m.tabla.fondo}` : ''))],
        [m.tabla.cielo, t => m.cielos[t.cielo] || '–'],
        [m.tabla.lluvia, t => (t.lluvia == null ? '–' : `${t.lluvia} %`)],
      ];
      const cabeza = crear('tr');
      cabeza.append(crear('td'), ...tramos.map(t => {
        const th = crear('th', tramo(t), pasado(dia.fecha, t) ? 'pasado' : '');
        th.scope = 'col';
        return th;
      }));
      const cuerpo = filas.map(([titulo, valor]) => {
        const tr = crear('tr'), th = crear('th', titulo);
        th.scope = 'row';
        tr.append(th, ...tramos.map(t => crear('td', valor(t), pasado(dia.fecha, t) ? 'pasado' : '')));
        return tr;
      });
      if (dia.agua != null) {
        const tr = crear('tr'), th = crear('th', m.tabla.agua), td = crear('td', `${dia.agua} °C`);
        th.scope = 'row';
        td.colSpan = tramos.length;
        tr.append(th, td);
        cuerpo.push(tr);
      }
      const thead = crear('thead'), tbody = crear('tbody');
      thead.append(cabeza);
      tbody.append(...cuerpo);
      el.querySelector('.bitacora-mar').replaceChildren(thead, tbody);
    }

    // Parte costero y avisos: valen para las 24 h que da AEMET, sea cual sea el día elegido
    const c = datos.costera;
    if (c && c.texto) {
      const caja = el.querySelector('.costera');
      const piezas = [crear('p', m.costera_h, 'costera-titulo')];
      if (c.fuerza && c.mar) {
        const f = c.fuerza[0] === c.fuerza[1] ? `${c.fuerza[0]}` : `${c.fuerza[0]}–${c.fuerza[1]}`;
        const estadoMar = c.mar[0] === c.mar[1] ? m.mar_cortos[c.mar[0]]
          : m.mar_cortos[c.mar[0]] + m.costera_a + m.mar_cortos[c.mar[1]];
        piezas.push(crear('p', m.costera_resumen.replace('{f}', f).replace('{m}', estadoMar)));
      }
      const original = crear('p', `${m.costera_texto} `, 'costera-original');
      original.append(crear('q', c.texto));
      piezas.push(original);
      if (c.fin) {
        const fin = new Intl.DateTimeFormat(d.lang, {
          weekday: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'UTC',
        }).format(new Date(`${c.fin}Z`));                     // AEMET da la hora oficial de España, sin zona
        piezas.push(crear('p', m.costera_hasta.replace('{fin}', fin), 'costera-hasta'));
      }
      caja.replaceChildren(...piezas);
      caja.hidden = false;
    }
    if (c && c.aviso) {
      const aviso = el.querySelector('.aviso-mar');
      aviso.replaceChildren(crear('strong', m.aviso_h), crear('p', c.aviso));
      aviso.hidden = false;
    }
    if (datos.generado) {
      const hora = new Intl.DateTimeFormat(d.lang, {
        weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'Europe/Madrid',
      }).format(new Date(datos.generado));
      el.querySelector('.notas-fuente').textContent = m.fuente.replace('{hora}', hora);
    }
    elegir(0);
  }
})();
