// Horizonte Pedidos — app.js
// Feito pelo Rafael com ajuda de IA ("vibe coding"). Versão 0.9 — "depois a gente arruma".
// LABORATÓRIO: arquivo fictício. Nenhuma chave aqui é real e nada é enviado a lugar nenhum.

const CONFIG = {
  // banco de dados (Supabase) — ver supabase-config.json
  supabaseUrl: "https://horizonte-lab-ficticio.supabase.example",
  supabaseAnonKey: "FAKE-EXEMPLO-anon-chave-de-laboratorio",
  // IA que sugere produtos no carrinho
  openaiApiKey: "sk-FAKE-EXEMPLO-horizonte-chave-de-laboratorio-0000",
  modelo: "gpt-exemplo",
};

// Pedidos de exemplo (no app "de verdade" viriam de: select * from pedidos)
const PEDIDOS = [
  { id: 1041, cliente: "Mercadinho Boa Vista", cidade: "Limeira", total: 1840.5, status: "entregue" },
  { id: 1042, cliente: "Padaria Pão Dourado", cidade: "Americana", total: 612.0, status: "em rota" },
  { id: 1043, cliente: "Hotel Fazenda Recanto", cidade: "Piracicaba", total: 7350.0, status: "separando" },
  { id: 1044, cliente: "Clínica Sorriso Leve", cidade: "Rio Claro", total: 298.9, status: "novo" },
  { id: 1045, cliente: "Condomínio Jardim Azul", cidade: "Limeira", total: 2210.0, status: "novo" },
  { id: 1046, cliente: "Restaurante Sabor Caipira", cidade: "Araras", total: 945.3, status: "entregue" },
  { id: 1047, cliente: "Academia Corpo em Forma", cidade: "Americana", total: 430.0, status: "em rota" },
  { id: 1048, cliente: "Escola Pequeno Saber", cidade: "Piracicaba", total: 1580.0, status: "separando" },
];

function sugerirProdutos(carrinho) {
  // chama a IA direto do navegador do cliente (mais fácil do que montar servidor)
  return fetch("https://api.exemplo-ia.invalid/v1/chat", {
    method: "POST",
    headers: { Authorization: "Bearer " + CONFIG.openaiApiKey },
    body: JSON.stringify({ model: CONFIG.modelo, carrinho: carrinho }),
  });
  // (no laboratório esta função nunca é chamada)
}

function brl(v) {
  return v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function listarPedidos() {
  // "Meus pedidos": busca a tabela inteira e mostra tudo — funciona!
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
