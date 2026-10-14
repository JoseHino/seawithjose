/* Sea With Jose · los datos del mar en Marbella
   Lee datos/marbella/horario.json (observación horaria de AEMET, acumulada cada 3 h por la Action
   datos-marbella.yml) y datos/marbella/diario.json (valores climatológicos diarios desde 2004).
   Donde hay datos horarios se pintan por horas; antes, un punto por día.
   Textos y nombres de variables: los pone build.py en #datos-pagina (t.datos). */
(function () {
  "use strict";
  var P = JSON.parse(document.getElementById("datos-pagina").textContent);
  var T = P.datos, PRE = P.prefijo || "";
  var lang = P.lang === "es" ? "es" : (P.lang === "ru" ? "ru" : "en");
  var MS = 3.6, NUDOS = 1.943844;

  // Cada variable: campo horario, campo diario, conversión, unidad y tipo de gráfica
  var VARS = {
    viento: { h: "vv", d: "velmedia", f: MS, u: "km/h", color: "#1F4E9A" },
    racha: { h: "vmax", d: "racha", f: MS, u: "km/h", color: "#D2232A" },
    dir: { h: "dv", d: "dir", f: 1, u: "°", color: "#0B2D52", dir: true },
    lluvia: { h: "prec", d: "prec", f: 1, u: "mm", color: "#2A9DD8", barras: true },
    temp: { h: "ta", d: "tmed", f: 1, u: "°C", color: "#F2B300" },
    humedad: { h: "hr", d: "hrMedia", f: 1, u: "%", color: "#4E5F70" }
  };
  var RANGOS = { "7": 7, "30": 30, "365": 365, "todo": 0 };

  var estado = { est: "6076X", v1: "viento", v2: "racha", rango: "7", x: "dir", y: "viento" };
  var horario = null, diario = null, grafica = null, cruce = null;

  function $(s) { return document.querySelector(s); }
  function fmt(n, d) { return n == null ? "–" : n.toLocaleString(P.lang, { maximumFractionDigits: d == null ? 1 : d }); }

  function valorDiario(clave, v, fila) {
    var x = fila[v.d];
    if (x == null) return null;
    if (v.dir) { if (x >= 88) return null; x = x * 10; }       // AEMET: decenas de grado; 88 y 99 = sin dato o variable
    return x * v.f;
  }

  // Serie de una variable: puntos {x: fecha, y: valor, h: true si es horario}
  function serie(clave) {
    var v = VARS[clave], pts = [], inicioHorario = null;
    var obs = (horario.estaciones[estado.est] || {}).obs || {};
    var horas = Object.keys(obs).sort();
    if (horas.length) inicioHorario = new Date(horas[0]);
    var dias = (diario.estaciones[estado.est] || {}).dias || {};
    Object.keys(dias).sort().forEach(function (f) {
      var t = new Date(f + "T12:00:00");
      if (inicioHorario && t >= new Date(inicioHorario.getTime() - 12 * 3600e3)) return;
      var y = valorDiario(clave, v, dias[f]);
      if (y != null) pts.push({ x: t, y: y, h: false });
    });
    horas.forEach(function (h) {
      var y = obs[h][v.h];
      if (y != null) pts.push({ x: new Date(h), y: y * v.f, h: true });
    });
    return pts;
  }

  function limites() {
    var fin = new Date(), dias = RANGOS[estado.rango];
    return { min: dias ? new Date(fin.getTime() - dias * 864e5) : undefined, max: fin };
  }

  function datasetDe(clave, eje) {
    var v = VARS[clave];
    return {
      label: T.vars[clave] + " (" + v.u + ")", data: serie(clave), yAxisID: eje,
      type: v.barras ? "bar" : "line", borderColor: v.color, backgroundColor: v.barras ? v.color : v.color + "22",
      pointRadius: v.dir ? 2 : 0, showLine: !v.dir, borderWidth: 2, tension: 0, spanGaps: false,
      parsing: false
    };
  }

  function pintarGrafica() {
    var l = limites();
    var ds = [datasetDe(estado.v1, "y")];
    if (estado.v2 && estado.v2 !== estado.v1) ds.push(datasetDe(estado.v2, "y2"));
    var ejeY = function (clave, lado) {
      var v = VARS[clave];
      return { position: lado, display: !!clave, title: { display: true, text: clave ? T.vars[clave] + " (" + v.u + ")" : "" },
               min: v && v.dir ? 0 : undefined, max: v && v.dir ? 360 : undefined,
               ticks: v && v.dir ? { stepSize: 90, callback: function (g) { return T.rumbos[Math.round(g / 45) % 8] || g; } } : {},
               grid: { drawOnChartArea: lado === "left" } };
    };
    var cfg = {
      data: { datasets: ds },
      options: {
        responsive: true, maintainAspectRatio: false, animation: false, interaction: { mode: "nearest", axis: "x", intersect: false },
        scales: {
          x: { type: "time", min: l.min, max: l.max, time: { tooltipFormat: "dd/MM/yyyy HH:mm",
               displayFormats: { hour: "HH:mm", day: "dd/MM", week: "dd/MM", month: "MM/yyyy", quarter: "MM/yyyy", year: "yyyy" } } },
          y: ejeY(estado.v1, "left"),
          y2: ejeY(estado.v2 !== estado.v1 ? estado.v2 : null, "right")
        },
        plugins: {
          legend: { position: "bottom" },
          tooltip: { callbacks: { label: function (c) {
            var clave = c.datasetIndex === 0 ? estado.v1 : estado.v2, v = VARS[clave], y = c.parsed.y;
            var txt = T.vars[clave] + ": " + fmt(y) + " " + v.u;
            if (v.f === MS) txt += " (" + fmt(y / MS * NUDOS) + " kn)";
            if (v.dir) txt += " · " + T.rumbos[Math.round(y / 45) % 8];
            if (!c.raw.h) txt += " · " + T.diario;
            return txt;
          } } },
          zoom: { pan: { enabled: true, mode: "x" }, zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: "x" } }
        }
      }
    };
    if (grafica) grafica.destroy();
    grafica = new Chart($("#grafica-serie"), cfg);
  }

  // ───── cruce de dos variables ─────
  function pares(cx, cy) {
    var sx = serie(cx), sy = serie(cy), m = {}, out = [], l = limites();
    sx.forEach(function (p) { m[p.x.getTime()] = p.y; });
    sy.forEach(function (p) {
      var t = p.x.getTime();
      if (m[t] != null && (!l.min || p.x >= l.min)) out.push({ x: m[t], y: p.y });
    });
    return out;
  }

  function pearson(ps) {
    var n = ps.length; if (n < 3) return null;
    var mx = 0, my = 0; ps.forEach(function (p) { mx += p.x; my += p.y; }); mx /= n; my /= n;
    var a = 0, b = 0, c = 0;
    ps.forEach(function (p) { a += (p.x - mx) * (p.y - my); b += (p.x - mx) * (p.x - mx); c += (p.y - my) * (p.y - my); });
    return b && c ? a / Math.sqrt(b * c) : null;
  }

  function pintarCruce() {
    var cx = estado.x, cy = estado.y, vx = VARS[cx], vy = VARS[cy], ps = pares(cx, cy), cfg, texto;
    if (vx.dir && !vy.dir) {
      // Con una dirección, lo útil es la media por rumbo
      var suma = [0, 0, 0, 0, 0, 0, 0, 0], n = [0, 0, 0, 0, 0, 0, 0, 0];
      ps.forEach(function (p) { var s = Math.round(p.x / 45) % 8; suma[s] += p.y; n[s]++; });
      cfg = { type: "bar", data: { labels: T.rumbos, datasets: [{ label: T.vars[cy] + " (" + vy.u + ")",
              data: suma.map(function (s, i) { return n[i] ? s / n[i] : null; }), backgroundColor: vy.color }] },
              options: { responsive: true, maintainAspectRatio: false, animation: false,
                         scales: { x: { title: { display: true, text: T.vars[cx] } }, y: { title: { display: true, text: T.media + " " + T.vars[cy] + " (" + vy.u + ")" } } } } };
      texto = T.cruce_rumbo.replace("{n}", fmt(ps.length, 0));
    } else {
      var r = pearson(ps);
      cfg = { type: "scatter", data: { datasets: [{ label: T.vars[cx] + " / " + T.vars[cy], data: ps, pointRadius: 2,
              backgroundColor: vy.color + "88" }] },
              options: { responsive: true, maintainAspectRatio: false, animation: false, plugins: { legend: { display: false } },
                         scales: { x: { title: { display: true, text: T.vars[cx] + " (" + vx.u + ")" } },
                                   y: { title: { display: true, text: T.vars[cy] + " (" + vy.u + ")" } } } } };
      texto = r == null ? T.pocos : T.cruce_r.replace("{r}", fmt(r, 2)).replace("{n}", fmt(ps.length, 0))
        .replace("{lectura}", Math.abs(r) >= 0.6 ? T.fuerte : Math.abs(r) >= 0.3 ? T.moderada : T.debil);
    }
    if (cruce) cruce.destroy();
    cruce = new Chart($("#grafica-cruce"), cfg);
    $("#cruce-texto").textContent = texto;
  }

  function resumen() {
    var obs = (horario.estaciones[estado.est] || {}).obs || {}, horas = Object.keys(obs).sort();
    if (!horas.length) return;
    var u = obs[horas[horas.length - 1]], h = new Date(horas[horas.length - 1]);
    var celdas = [
      [T.vars.viento, fmt(u.vv * MS, 0) + " km/h", fmt(u.vv * NUDOS, 0) + " kn · " + (T.rumbos[Math.round(u.dv / 45) % 8] || "")],
      [T.vars.racha, fmt(u.vmax * MS, 0) + " km/h", fmt(u.vmax * NUDOS, 0) + " kn"],
      [T.vars.temp, fmt(u.ta) + " °C", T.vars.humedad + " " + fmt(u.hr, 0) + " %"],
      [T.vars.lluvia, fmt(u.prec) + " mm", T.ultima_hora]
    ];
    $("#datos-ahora").innerHTML = celdas.map(function (c) {
      return '<div class="dato"><span class="dato-etiqueta">' + c[0] + '</span><span class="dato-valor">' + c[1] +
             '</span><span class="dato-extra">' + c[2] + "</span></div>";
    }).join("");
    $("#datos-hora").textContent = T.actualizado + " " + h.toLocaleString(P.lang, { dateStyle: "short", timeStyle: "short" });
  }

  function csv() {
    var filas = [["fecha", "resolucion"].concat(Object.keys(VARS))], todas = {};
    Object.keys(VARS).forEach(function (k) {
      serie(k).forEach(function (p) {
        var t = p.x.toISOString(); todas[t] = todas[t] || { h: p.h }; todas[t][k] = p.y;
      });
    });
    Object.keys(todas).sort().forEach(function (t) {
      filas.push([t, todas[t].h ? "hora" : "dia"].concat(Object.keys(VARS).map(function (k) {
        return todas[t][k] == null ? "" : Math.round(todas[t][k] * 10) / 10; })));
    });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([filas.map(function (f) { return f.join(","); }).join("\n")], { type: "text/csv" }));
    a.download = "marbella-" + estado.est + ".csv"; a.click();
  }

  function enganchar() {
    document.querySelectorAll("[data-rango]").forEach(function (b) {
      b.addEventListener("click", function () {
        estado.rango = b.getAttribute("data-rango");
        document.querySelectorAll("[data-rango]").forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        pintarGrafica(); pintarCruce();
      });
    });
    [["#sel-v1", "v1"], ["#sel-v2", "v2"], ["#sel-x", "x"], ["#sel-y", "y"], ["#sel-est", "est"]].forEach(function (p) {
      $(p[0]).addEventListener("change", function (e) {
        estado[p[1]] = e.target.value;
        if (p[1] === "est") resumen();
        pintarGrafica(); pintarCruce();
      });
    });
    $("#boton-zoom").addEventListener("click", function () { grafica.resetZoom(); });
    $("#boton-csv").addEventListener("click", csv);
  }

  Promise.all([fetch(PRE + "datos/marbella/horario.json", { cache: "no-store" }).then(function (r) { return r.json(); }),
               fetch(PRE + "datos/marbella/diario.json").then(function (r) { return r.json(); })])
    .then(function (d) {
      horario = d[0]; diario = d[1];
      Chart.defaults.font.family = "'Sofia Sans', system-ui, sans-serif";
      Chart.defaults.color = "#4E5F70";
      enganchar(); resumen(); pintarGrafica(); pintarCruce();
    })
    .catch(function () { $("#datos-error").hidden = false; });
})();
