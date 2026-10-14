/**
 * Bitácora del mar · pedir un número por correo
 *
 * Va en Google Apps Script (script.google.com), en la cuenta de Gmail de Jose. Cada 5 minutos busca los
 * correos enviados a la dirección de la Bitácora y, por cada uno, pide a GitHub que prepare el borrador
 * (evento «revista» del workflow revista-borrador.yml). Lo escrito en el correo llega a la IA como notas.
 * Luego llega el borrador de siempre: se responde OK y se envía a todos los suscriptores.
 *
 * - Número: si el asunto lleva uno (2026-11-1, 2026-11-2 o 2026-11-05), se usa; si no, sale un número
 *   especial con la fecha de hoy (AAAA-MM-DD).
 * - Solo hace caso a los correos que manda Jose (REMITENTE). El resto los marca y no hace nada.
 * - Necesita, en Configuración del proyecto → Propiedades del script, GITHUB_TOKEN = un token de GitHub con
 *   permiso «Contents: Read and write» solo en el repositorio JoseHino/seawithjose.
 *
 * Puesta en marcha: pegar este código, guardar, elegir la función «configurar» y pulsar Ejecutar (pide permiso
 * para leer Gmail y conectarse a internet). Para probar sin esperar, ejecutar «revisar».
 */

const DIRECCION = 'josemariahf612+bitacora@gmail.com';
const REMITENTE = 'josemariahf612@gmail.com';
const REPO = 'JoseHino/seawithjose';
const ETIQUETA = 'Bitacora-pedido';

function revisar() {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('Falta GITHUB_TOKEN en las propiedades del script.');
  const etiqueta = GmailApp.getUserLabelByName(ETIQUETA) || GmailApp.createLabel(ETIQUETA);
  const hilos = GmailApp.search('to:' + DIRECCION + ' -label:' + ETIQUETA + ' newer_than:2d');
  hilos.forEach(function (hilo) {
    const mensajes = hilo.getMessages().filter(function (m) {
      return (m.getTo() + ' ' + m.getCc()).toLowerCase().indexOf(DIRECCION) >= 0;
    });
    const m = mensajes[mensajes.length - 1];
    if (!m || m.getFrom().toLowerCase().indexOf(REMITENTE) < 0) {
      hilo.addLabel(etiqueta);                       // de otra persona: no se hace nada
      return;
    }
    const asunto = m.getSubject() || '';
    const cuerpo = (m.getPlainBody() || '').split(/\n>|\nEl .+escribió:|\nOn .+wrote:/)[0].trim().slice(0, 3000);
    const encontrado = asunto.match(/\d{4}-\d{2}-(?:\d{2}|[12])\b/);
    const numero = encontrado ? encontrado[0] : Utilities.formatDate(new Date(), 'Europe/Madrid', 'yyyy-MM-dd');
    const r = UrlFetchApp.fetch('https://api.github.com/repos/' + REPO + '/dispatches', {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' },
      payload: JSON.stringify({ event_type: 'revista', client_payload: { numero: numero, notas: (asunto + '\n' + cuerpo).trim() } })
    });
    if (r.getResponseCode() === 204) {
      hilo.addLabel(etiqueta);
      console.log('Borrador pedido: ' + numero);
    } else {
      console.error('GitHub contestó ' + r.getResponseCode() + ': ' + r.getContentText());   // se reintenta en 5 min
    }
  });
}

function configurar() {
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('revisar').timeBased().everyMinutes(5).create();
  revisar();
}
