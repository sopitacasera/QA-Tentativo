const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const reports = path.join(root, "reports");
const evidencia = path.join(reports, "evidencia");
const salida = path.join(reports, "report.html");

function leerJson(archivo) {
  if (!fs.existsSync(archivo)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(archivo, "utf8"));
}

function escapar(valor) {
  return String(valor)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const resultados = leerJson(path.join(reports, "cypress-results.json"));
const archivos = fs.existsSync(evidencia)
  ? fs.readdirSync(evidencia).filter((nombre) => nombre.endsWith(".json")).sort()
  : [];
const casos = archivos.map((nombre) => leerJson(path.join(evidencia, nombre)));

const total = resultados ? resultados.totalTests : casos.length;
const pasaron = resultados ? resultados.totalPassed : casos.length;
const fallaron = resultados ? resultados.totalFailed : 0;
const duracion = resultados ? Math.round(resultados.totalDuration / 1000) : 0;
const aprobado = fallaron === 0 && pasaron > 0;

const filas = casos
  .map((caso) => {
    const detalle = escapar(JSON.stringify(caso, null, 2));
    return `<tr>
      <td>Pasó</td>
      <td>${escapar(caso.caso || "")}</td>
      <td><code>${escapar(caso.metodo || "")}</code></td>
      <td>${escapar(caso.http || caso.httpGet || "")}</td>
      <td>${escapar(caso.duracionMs || "")} ms</td>
    </tr>
    <tr class="detalle"><td colspan="5"><pre>${detalle}</pre></td></tr>`;
  })
  .join("\n");

const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <title>Ejercicio 02 - PetStore API</title>
  <style>
    body { font-family: Helvetica, Arial, sans-serif; color: #1f2937; background: #f8fafc; margin: 24px; }
    h1 { font-size: 28px; margin-bottom: 4px; }
    .verdict { max-width: 920px; margin: 16px 0; padding: 14px 16px; background: #fff; border: 1px solid #d6d3d1; border-left: 4px solid ${aprobado ? "#0f766e" : "#b91c1c"}; }
    table { border-collapse: collapse; background: #fff; width: 100%; max-width: 1100px; }
    th, td { border: 1px solid #e5e7eb; padding: 8px 10px; text-align: left; vertical-align: top; }
    th { background: #f1f5f9; }
    pre { white-space: pre-wrap; font-size: 12px; margin: 0; }
  </style>
</head>
<body>
  <h1>Ejercicio 02 - PetStore API</h1>
  <p>Generado el ${new Date().toLocaleString("es-EC")} con Cypress.</p>
  <div class="verdict">
    <h2>Resultado del ejercicio</h2>
    <p><strong>${aprobado ? "Listo para entregar." : "Hay casos en rojo."}</strong>
    ${pasaron} pasaron, ${fallaron} fallaron, en ${duracion} segundos.</p>
    <p>CP-01 crea la mascota. CP-02 la consulta por id. CP-03 cambia el nombre y el estado a sold.
    CP-04 la busca entre las vendidas. CP-05 comprueba que un id inexistente responde 404 y no crea una orden falsa.</p>
    <p>Los hallazgos están en conclusiones.txt.</p>
  </div>
  <table>
    <thead>
      <tr><th>Resultado</th><th>Caso</th><th>Operación</th><th>HTTP</th><th>Duración</th></tr>
    </thead>
    <tbody>
      ${filas || "<tr><td colspan='5'>No hay evidencia. Ejecuta la suite.</td></tr>"}
    </tbody>
  </table>
</body>
</html>
`;

fs.mkdirSync(reports, { recursive: true });
fs.writeFileSync(salida, html, "utf8");
console.log("Informe escrito en reports/report.html");
