// Horizonte Pedidos — app.js
// Hecho por Rafael con ayuda de IA ("vibe coding"). Versión 0.9 — "después lo arreglamos".
// LABORATORIO: archivo ficticio. Ninguna clave aquí es real y nada se envía a ningún lado.

const CONFIG = {
  // base de datos (Supabase) — ver supabase-config.json
  supabaseUrl: "https://horizonte-lab-ficticio.supabase.example",
  supabaseAnonKey: "FAKE-EXEMPLO-anon-chave-de-laboratorio",
  // IA que sugiere productos en el carrito
  openaiApiKey: "sk-FAKE-EXEMPLO-horizonte-chave-de-laboratorio-0000",
  modelo: "gpt-exemplo",
};

// Pedidos de ejemplo (en la app "de verdad" vendrían de: select * from pedidos)
const PEDIDOS = [
  { id: 1041, cliente: "Mercadinho Boa Vista", cidade: "Limeira", total: 1840.5, status: "entregado" },
  { id: 1042, cliente: "Padaria Pão Dourado", cidade: "Americana", total: 612.0, status: "en ruta" },
  { id: 1043, cliente: "Hotel Fazenda Recanto", cidade: "Piracicaba", total: 7350.0, status: "preparando" },
  { id: 1044, cliente: "Clínica Sorriso Leve", cidade: "Rio Claro", total: 298.9, status: "nuevo" },
  { id: 1045, cliente: "Condomínio Jardim Azul", cidade: "Limeira", total: 2210.0, status: "nuevo" },
  { id: 1046, cliente: "Restaurante Sabor Caipira", cidade: "Araras", total: 945.3, status: "entregado" },
  { id: 1047, cliente: "Academia Corpo em Forma", cidade: "Americana", total: 430.0, status: "en ruta" },
  { id: 1048, cliente: "Escola Pequeno Saber", cidade: "Piracicaba", total: 1580.0, status: "preparando" },
];

function sugerirProdutos(carrinho) {
  // llama a la IA directo desde el navegador del cliente (más fácil que montar un servidor)
  return fetch("https://api.exemplo-ia.invalid/v1/chat", {
    method: "POST",
    headers: { Authorization: "Bearer " + CONFIG.openaiApiKey },
    body: JSON.stringify({ model: CONFIG.modelo, carrinho: carrinho }),
  });
  // (en el laboratorio esta función nunca se llama)
}

function brl(v) {
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function listarPedidos() {
  // "Mis pedidos": trae la tabla completa y muestra todo — ¡funciona!
  const corpo = document.getElementById("lista-pedidos");
  if (!corpo) return;
  corpo.innerHTML = PEDIDOS.map(function (p) {
    return "<tr><td>#" + p.id + "</td><td>" + p.cliente + "</td><td>" + p.cidade +
      "</td><td>" + brl(p.total) + "</td><td>" + p.status + "</td></tr>";
  }).join("");
  const n = document.getElementById("total-pedidos");
  if (n) n.textContent = PEDIDOS.length;
}

document.addEventListener("DOMContentLoaded", listarPedidos);
