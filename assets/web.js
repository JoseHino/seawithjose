/* Sea With Jose · comportamiento de la web (sin dependencias) */
(() => {
  const nodo = document.getElementById('datos-pagina');
  const d = nodo ? JSON.parse(nodo.textContent) : {};
  const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

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

  // ── lo que se anima al entrar en pantalla (la carta se sondea y aparece la derrota) ──
  const animables = document.querySelectorAll('.ruta-carta');
  if (!('IntersectionObserver' in window) || sinMovimiento) {
    animables.forEach(el => el.classList.add('visible'));
  } else {
    const obs = new IntersectionObserver(entradas => entradas.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    }), { threshold: 0.25 });
    animables.forEach(el => obs.observe(el));
  }

  // ── utilidades de fecha y hora (siempre en la hora de Madrid) ──
  function hoyEnMadrid(desplazamiento = 0) {
    const fecha = new Date(Date.now() + desplazamiento * 86400000);
    return new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Madrid' }).format(fecha);   // AAAA-MM-DD
  }

  function ahoraEnMadrid() {
    const p = Object.fromEntries(new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
    }).formatToParts(new Date()).map(x => [x.type, x.value]));
    return { fecha: `${p.year}-${p.month}-${p.day}`, hora: Number(p.hour) + Number(p.minute) / 60 };
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

  function crear(etiqueta, texto, clase) {
    const n = document.createElement(etiqueta);
    if (texto != null) n.textContent = texto;
    if (clase) n.className = clase;
    return n;
  }

  const nivelDe = n => Math.min(4, Math.floor((n - 1) / 2));      // 1-2, 3-4, 5-6, 7-8, 9-10
  const hh = h => String(h).padStart(2, '0');

  // ── datos del mar (AEMET, los deja la Action en datos/mar.json) ──
  const necesitaMar = document.querySelector('#mar, #reserva');
  const datosMar = necesitaMar
    ? fetch(`${d.prefijo}datos/mar.json`, { cache: 'no-store' }).then(r => (r.ok ? r.json() : null)).catch(() => null)
    : Promise.resolve(null);

  const mar = document.getElementById('mar');
  if (mar && d.mar) pintarMar(mar, d, datosMar);
  const form = document.getElementById('reserva');
  if (form && d.form) iniciarReserva(form, d, datosMar);
  document.querySelectorAll('[data-tipo]').forEach(a => a.addEventListener('click', () => {
    const radio = form && form.querySelector(`input[name="tipo"][value="${a.dataset.tipo}"]`);
    if (radio) { radio.checked = true; radio.dispatchEvent(new Event('change', { bubbles: true })); }
  }));
  const video = document.querySelector('.barco-video');
  if (video) iniciarVideo(video);
  if (d.pagina === 'buceo') iniciarFiltros();
  if (d.pagina === 'gracias') pintarGracias(d);

  // ── la reserva: formulario, tarjeta de embarque y pago ──
  function iniciarReserva(form, d, promesa) {
    const f = d.form;
    const zona = document.querySelector('.resumen-zona');
    const campo = n => zona.querySelector(`[data-campo="${n}"]`);
    const fecha = form.elements.fecha;
    const personas = form.elements.personas;
    fecha.min = hoyEnMadrid(1);                 // desde mañana: el mismo día se reserva por WhatsApp
    fecha.max = hoyEnMadrid(d.dias);
    const pagos = d.pagos || {};
    const formatoFecha = new Intl.DateTimeFormat(d.lang, { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' });
    const formatoHora = new Intl.DateTimeFormat(d.lang, { hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZone: 'Europe/Madrid' });
    const euros = n => new Intl.NumberFormat(d.lang, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
    const CODIGOS = { buffet: 'bu', paella: 'pa', cocteles: 'co', tarta: 'ta', decoracion: 'de', otra: 'ot' };
    let datos = null;
    promesa.then(x => { datos = x; pintar(); });

    // La salida de atardecer: 1 h 45 min antes de la puesta de sol, redondeada al cuarto de hora
    function horaAtardecer(dia) {
      const salida = new Date(puestaDeSol(new Date(`${dia}T12:00:00Z`)).getTime() - 105 * 60000);
      salida.setUTCMinutes(salida.getUTCMinutes() - (salida.getUTCMinutes() % 15), 0, 0);
      return formatoHora.format(salida);
    }

    function estado() {
      const tipo = form.elements.tipo.value;
      const dia = fecha.value;
      const horaV = form.elements.hora.value;
      const n = Math.min(d.plazas, Math.max(1, parseInt(personas.value, 10) || 1));
      const extras = tipo === 'privada' ? [...form.querySelectorAll('input[name="extras"]:checked')].map(x => x.value) : [];
      const otra = tipo === 'privada' ? form.elements.otra.value.trim() : '';
      const hora = horaV === 'atardecer' ? (dia ? horaAtardecer(dia) : '') : horaV;
      const total = tipo === 'privada' ? d.precios.privada : d.precios.compartida * n;
      return { tipo, dia, horaV, hora, n, extras, otra, nombre: form.elements.nombre.value.trim(), total };
    }

    const textoExtras = e => [...e.extras.map(x => d.extras[x]), e.otra ? `${d.extras.otra}: ${e.otra}` : '']
      .filter(Boolean).join(', ');

    function referencia(e) {
      const extras = [...e.extras, e.otra ? 'otra' : ''].filter(Boolean).map(x => CODIGOS[x]).join('');
      return [e.tipo === 'privada' ? 'P' : 'C', e.dia.replaceAll('-', ''), e.hora.replace(':', ''), `${e.n}p`, extras]
        .filter(Boolean).join('-');
    }

    function mensaje(e, ref) {
      const lineas = [f.msg_inicio, `${f.msg_tipo}: ${f.tipos[e.tipo]}`];
      if (e.dia) lineas.push(`${f.msg_fecha}: ${formatoFecha.format(new Date(`${e.dia}T12:00:00Z`))}`);
      if (e.hora) lineas.push(`${f.msg_hora}: ${e.hora}`);
      lineas.push(`${f.msg_personas}: ${e.n}`);
      if (textoExtras(e)) lineas.push(`${f.msg_extras}: ${textoExtras(e)}`);
      if (e.nombre) lineas.push(`${f.msg_nombre}: ${e.nombre}`);
      lineas.push(`${f.msg_total}: ${euros(e.total)}`);
      if (ref) lineas.push(`${f.msg_ref}: ${ref}`);
      return `https://wa.me/${d.whatsapp}?text=${encodeURIComponent(lineas.join('\n'))}`;
    }

    function enlacePago(e) {
      return e.tipo === 'privada' ? (pagos.privada || '') : ((pagos.compartida || {})[String(e.n)] || '');
    }

    function prevision(e) {
      const p = form.querySelector('.prevision');
      p.hidden = true;
      if (!datos || !e.dia || !e.hora) return;
      const dia = (datos.dias || []).find(x => x.fecha === e.dia);
      const h = parseInt(e.hora, 10);
      const tramo = dia && (dia.tramos || []).find(t => t.notas && h >= t.de - 1 && h < t.a);
      if (!tramo) return;
      const n = tramo.notas.navegar.n;
      p.textContent = f.prevision.replace('{n}', n).replace('{banda}', d.mar.bandas[nivelDe(n)]);
      p.hidden = false;
    }

    function pintar() {
      const e = estado();
      form.querySelector('.extras-form').hidden = e.tipo !== 'privada';
      campo('tipo').textContent = f.tipos[e.tipo];
      campo('fecha').textContent = e.dia ? formatoFecha.format(new Date(`${e.dia}T12:00:00Z`)) : '—';
      campo('hora').textContent = e.hora || '—';
      campo('pax').textContent = e.n;
      zona.querySelector('.resumen-extras').hidden = !textoExtras(e);
      campo('extras').textContent = textoExtras(e) || '—';
      campo('total').textContent = euros(e.total);
      campo('detalle').textContent = e.tipo === 'privada' ? f.detalle_privada : f.detalle_compartida.replace('{n}', e.n);
      const pagar = zona.querySelector('.pagar-texto');
      if (pagar) pagar.textContent = f.pagar.replace('{total}', euros(e.total));
      const atardecer = form.querySelector('.hora-atardecer');
      if (atardecer) atardecer.textContent = e.dia ? horaAtardecer(e.dia) : '';
      form.querySelector('.contador-menos').disabled = e.n <= 1;
      form.querySelector('.contador-mas').disabled = e.n >= d.plazas;
      const wa = zona.querySelector('.enlace-wa');
      if (wa) wa.href = mensaje(e);
      prevision(e);
    }

    form.querySelector('.contador-menos').addEventListener('click', () => { personas.value = estado().n - 1; pintar(); });
    form.querySelector('.contador-mas').addEventListener('click', () => { personas.value = estado().n + 1; pintar(); });
    personas.addEventListener('change', () => { personas.value = estado().n; pintar(); });
    form.addEventListener('input', pintar);
    form.addEventListener('change', pintar);

    form.addEventListener('submit', ev => {
      ev.preventDefault();
      const e = estado();
      const error = form.querySelector('.error');
      const falta = !e.dia ? ['fecha', f.falta_fecha] : !e.horaV ? ['hora', f.falta_hora] : null;
      if (falta) {
        error.textContent = falta[1];
        error.hidden = false;
        const destino = falta[0] === 'fecha' ? fecha : form.querySelector('input[name="hora"]');
        destino.focus();
        return;
      }
      error.hidden = true;
      const ref = referencia(e);
      try { localStorage.setItem('reserva', JSON.stringify({ ...e, ref, lang: d.lang, creada: Date.now() })); } catch (_) { /* sin almacenamiento */ }
      const url = enlacePago(e);
      if (url) {
        window.location.href = `${url}${url.includes('?') ? '&' : '?'}client_reference_id=${encodeURIComponent(ref)}`;
      } else {
        window.open(mensaje(e, ref), '_blank', 'noopener');
      }
    });
    pintar();
  }

  // ── el vídeo del Petit: solo se carga y suena (sin sonido) cuando está a la vista ──
  function iniciarVideo(figura) {
    const v = figura.querySelector('video');
    const b = figura.querySelector('.video-boton');
    const etiqueta = b.querySelector('.visualmente-oculto');
    let manual = false;
    const marcar = () => {
      const sonando = !v.paused;
      b.setAttribute('aria-pressed', String(sonando));
      etiqueta.textContent = sonando ? b.dataset.pausa : b.dataset.play;
    };
    v.addEventListener('play', marcar);
    v.addEventListener('pause', marcar);
    b.addEventListener('click', () => { manual = true; if (v.paused) v.play().catch(() => {}); else v.pause(); });
    if (sinMovimiento || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(entradas => entradas.forEach(e => {
      if (manual) return;
      if (e.isIntersecting) v.play().catch(() => {}); else v.pause();
    }), { threshold: 0.4 }).observe(figura);
  }

  // ── la Senda Azul: filtros por nivel y por cercanía a Banús ──
  function iniciarFiltros() {
    const botones = document.querySelectorAll('.filtro');
    const sitios = document.querySelectorAll('.senda .sitio');
    const vacio = document.querySelector('.senda-vacio');
    botones.forEach(b => b.addEventListener('click', () => {
      botones.forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      const filtro = b.dataset.filtro;
      let visibles = 0;
      sitios.forEach(s => {
        const ver = filtro === 'todos' || (filtro === 'banus' ? s.dataset.banus === 'true'
          : s.dataset.nivel.split(' ').includes(filtro));
        s.hidden = !ver;
        if (ver) visibles += 1;
      });
      vacio.hidden = visibles > 0;
    }));
  }

  // ── reserva recibida: la tarjeta de embarque, recuperada de este navegador ──
  function pintarGracias(d) {
    let r = null;
    try { r = JSON.parse(localStorage.getItem('reserva') || 'null'); } catch (_) { r = null; }
    if (r && r.lang && r.lang !== d.lang && d.prefijo === '' && r.lang !== 'en') {
      window.location.replace(`${r.lang}/gracias.html`);        // Stripe vuelve siempre a la versión inglesa
      return;
    }
    if (!r) { document.querySelector('.gracias-sin').hidden = false; return; }
    const f = d.form, b = d.resumen;
    const euros = n => new Intl.NumberFormat(d.lang, { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
    const formatoFecha = new Intl.DateTimeFormat(d.lang, { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' });
    const extras = [...(r.extras || []).map(x => d.extras[x]), r.otra ? `${d.extras.otra}: ${r.otra}` : ''].filter(Boolean).join(', ');
    const filas = [[b.salida, f.tipos[r.tipo]], [b.fecha, formatoFecha.format(new Date(`${r.dia}T12:00:00Z`))],
      [b.hora, r.hora], [b.pax, r.n], [b.total, euros(r.total)], [f.msg_ref, r.ref]];
    if (extras) filas.splice(4, 0, [b.extras, extras]);
    const dl = document.querySelector('.gracias-resumen dl');
    dl.replaceChildren(...filas.map(([k, v]) => {
      const div = crear('div');
      div.append(crear('dt', k), crear('dd', String(v)));
      return div;
    }));
    document.querySelector('.gracias-resumen').hidden = false;
    const wa = document.querySelector('[data-wa-gracias]');
    const lineas = [f.msg_pagado, `${f.msg_tipo}: ${f.tipos[r.tipo]}`, `${f.msg_fecha}: ${r.dia}`, `${f.msg_hora}: ${r.hora}`,
      `${f.msg_personas}: ${r.n}`, extras ? `${f.msg_extras}: ${extras}` : '', r.nombre ? `${f.msg_nombre}: ${r.nombre}` : '',
      `${f.msg_ref}: ${r.ref}`].filter(Boolean);
    wa.href = `https://wa.me/${d.whatsapp}?text=${encodeURIComponent(lineas.join('\n'))}`;
  }

  // ── el mar, ahora: notas del 1 al 10 por día y tramo (las calcula scripts/parte_mar.py) ──
  async function pintarMar(el, d, promesa) {
    const m = d.mar, datos = await promesa;
    const ahora = ahoraEnMadrid(), manana = hoyEnMadrid(1);
    const pasado = (fecha, t) => fecha < ahora.fecha || (fecha === ahora.fecha && ahora.hora >= t.a);
    const dias = ((datos && datos.dias) || []).filter(x =>
      x.fecha >= ahora.fecha && (x.tramos || []).some(t => t.notas && !pasado(x.fecha, t)));
    const estado = el.querySelector('.notas-estado');
    if (!dias.length) {
      const enlace = crear('a', 'WhatsApp');
      enlace.href = `https://wa.me/${d.whatsapp}?text=${encodeURIComponent(d.form ? d.form.msg_inicio : '')}`;
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
        const n = mejor.notas[act].n, nivel = nivelDe(n);
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
