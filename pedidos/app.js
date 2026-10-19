// app.js — "Pedidos Horizonte" (gerado por vibe coding num fim de semana)
// ARQUIVO DE LABORATÓRIO: nenhuma página carrega este arquivo. É só para leitura.
// Os endereços terminam em .invalid e não existem. As chaves são falsas.

const API_URL = "https://banco.horizonte-lab.invalid/rest/v1";
const CHAVE_PUBLICA = "pk-FALSO-LAB-publica-0000"; // chave falsa de laboratório (pública: ok no navegador SE houver RLS)
const CHAVE_SERVICO = "sk-FALSO-LAB-service-role-0000-NAO-E-REAL"; // chave falsa de laboratório — secreta, NÃO podia estar aqui
const CHAVE_PAGAMENTO = "sk-FALSO-LAB-pagamento-0000-NAO-E-REAL"; // chave falsa de laboratório — secreta, NÃO podia estar aqui

const TABELA_PRECOS = { "CX-AGUA-500": 18.9, "CX-REFRI-2L": 54.0, "FARDO-ARROZ-5KG": 129.5 };

// Monta o pedido no navegador
function fecharPedido(itens, cupom) {
  let total = 0;
  for (const item of itens) {
    total += TABELA_PRECOS[item.sku] * item.qtd;
  }
  let desconto = cupom === "HORIZONTE10" ? 0.10 : 0;
  if (window.descontoExtra) desconto = window.descontoExtra; // "atalho para testes"
  const pedido = {
    cliente_id: sessionStorage.getItem("cliente_id"),
    itens,
    desconto,
    total: total * (1 - desconto) // o servidor grava este total como veio
  };
  return gravar("pedidos", pedido, CHAVE_SERVICO);
}

// Grava direto no banco usando a chave de serviço
function gravar(tabela, dados, chave) {
  return fetch(`${API_URL}/${tabela}`, {
    method: "POST",
    headers: { "apikey": chave, "Authorization": `Bearer ${chave}`, "Content-Type": "application/json" },
    body: JSON.stringify(dados)
  });
}

// "Proteção" do admin: só esconde o botão para quem não é da equipe
function abrirAdmin() {
  const ehEquipe = localStorage.getItem("equipe") === "sim";
  document.querySelector("#btn-admin").style.display = ehEquipe ? "block" : "none";
  // a página /admin.html continua abrindo para qualquer um que digitar o endereço
}
