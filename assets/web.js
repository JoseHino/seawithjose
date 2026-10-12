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

  // ── parte del mar ──
  const parte = document.querySelector('.parte');
  if (parte && d.parte) pintarParte(parte, d);

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

  async function pintarParte(el, d) {
    const t = d.parte;
    const hoy = hoyEnMadrid();
    let dia = null, etiqueta = '';
    try {
      const r = await fetch(`${d.prefijo}datos/mar.json`, { cache: 'no-store' });
      if (r.ok) {
        const datos = await r.json();
        const dias = datos.dias || [];
        dia = dias.find(x => x.fecha === hoy) || null;
        if (!dia) {
          const siguiente = dias.find(x => x.fecha === hoyEnMadrid(1));
          if (siguiente) { dia = siguiente; etiqueta = 'manana'; }
        }
      }
    } catch (e) { /* sin parte: se queda la puesta de sol y el mensaje */ }

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
      if (doble(dia.cielo)) filas.push([t.cielo, doble(dia.cielo)]);
      if (dia.uv != null) filas.push([t.uv, String(dia.uv)]);
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
})();
