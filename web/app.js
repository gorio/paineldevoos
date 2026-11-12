"use strict";
const $ = id => document.getElementById(id);
function cell(row, text, bold = false) {
  const td = document.createElement("td");
  const el = bold ? document.createElement("strong") : document.createTextNode(text || "—");
  if (bold) el.textContent = text || "—";
  td.appendChild(el);
  row.appendChild(td);
}
async function refresh() {
  const params = new URLSearchParams({ mode: $("mode").value, direction: $("direction").value, q: $("search").value });
  const response = await fetch("/api/v1/flights?" + params, {cache:"no-store"});
  if (!response.ok) throw new Error("Falha na consulta");
  const data = await response.json();
  $("count").textContent = data.count;
  $("departures").textContent = data.flights.filter(f => f.direction === "departure").length;
  $("arrivals").textContent = data.flights.filter(f => f.direction === "arrival").length;
  $("date").textContent = data.flight_date || "Sem dados";
  $("source").textContent = data.mode === "demo"
    ? "Demonstração: registros 100% fictícios. Nenhuma atualização em tempo real."
    : "Dados importados manualmente (não verificados). Coleta: " + (data.last_updated_at || "ainda não realizada") + " UTC.";
  $("rows").replaceChildren();
  for (const f of data.flights) {
    const tr = document.createElement("tr");
    cell(tr, f.scheduled_local, true);
    cell(tr, f.estimated_local);
    cell(tr, f.flight_number, true);
    cell(tr, f.direction === "departure" ? "Partida" : "Chegada");
    cell(tr, f.route);
    cell(tr, f.status);
    cell(tr, f.terminal);
    $("rows").appendChild(tr);
  }
  if (!data.count) {
    const tr = document.createElement("tr"); const td = document.createElement("td");
    td.colSpan = 7; td.textContent = "Nenhum voo encontrado nesta origem/filtro."; tr.appendChild(td); $("rows").appendChild(tr);
  }
}
const update = () => refresh().catch(e => { $("message").textContent = e.message; });
for (const id of ["mode","direction","search"]) $(id).addEventListener(id === "search" ? "input" : "change", update);
$("refresh").addEventListener("click", update);
$("import").addEventListener("click", async () => {
  $("message").textContent = "Validando...";
  try {
    const data = JSON.parse($("payload").value);
    const res = await fetch("/api/v1/manual-import", {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
    const info = await res.json();
    if (!res.ok) throw new Error(info.error || "Falha ao importar");
    $("message").textContent = info.imported + " registros importados. Somente memória desta sessão; não persistidos.";
    $("mode").value = "manual";
    await refresh();
  } catch (e) { $("message").textContent = "Erro: " + e.message; }
});
update();
