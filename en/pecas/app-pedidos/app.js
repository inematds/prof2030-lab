// Horizonte Pedidos — app.js
// Made by Rafael with the help of AI ("vibe coding"). Version 0.9 — "we'll fix it later".
// LAB: fictional file. No key here is real and nothing is sent anywhere.

const CONFIG = {
  // database (Supabase) — see supabase-config.json
  supabaseUrl: "https://horizonte-lab-ficticio.supabase.example",
  supabaseAnonKey: "FAKE-EXEMPLO-anon-chave-de-laboratorio",
  // AI that suggests products in the cart
  openaiApiKey: "sk-FAKE-EXEMPLO-horizonte-chave-de-laboratorio-0000",
  modelo: "gpt-exemplo",
};

// Sample orders (in the "real" app they would come from: select * from pedidos)
const PEDIDOS = [
  { id: 1041, cliente: "Mercadinho Boa Vista", cidade: "Limeira", total: 1840.5, status: "delivered" },
  { id: 1042, cliente: "Padaria Pão Dourado", cidade: "Americana", total: 612.0, status: "on the way" },
  { id: 1043, cliente: "Hotel Fazenda Recanto", cidade: "Piracicaba", total: 7350.0, status: "picking" },
  { id: 1044, cliente: "Clínica Sorriso Leve", cidade: "Rio Claro", total: 298.9, status: "new" },
  { id: 1045, cliente: "Condomínio Jardim Azul", cidade: "Limeira", total: 2210.0, status: "new" },
  { id: 1046, cliente: "Restaurante Sabor Caipira", cidade: "Araras", total: 945.3, status: "delivered" },
  { id: 1047, cliente: "Academia Corpo em Forma", cidade: "Americana", total: 430.0, status: "on the way" },
  { id: 1048, cliente: "Escola Pequeno Saber", cidade: "Piracicaba", total: 1580.0, status: "picking" },
];

function sugerirProdutos(carrinho) {
  // calls the AI directly from the customer's browser (easier than setting up a server)
  return fetch("https://api.exemplo-ia.invalid/v1/chat", {
    method: "POST",
    headers: { Authorization: "Bearer " + CONFIG.openaiApiKey },
    body: JSON.stringify({ model: CONFIG.modelo, carrinho: carrinho }),
  });
  // (in the lab this function is never called)
}

function brl(v) {
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function listarPedidos() {
  // "My orders": fetches the entire table and shows everything — it works!
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
