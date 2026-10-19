# prof2030-lab — Horizonte Distribuidora

Laboratório de estudo do **Profissional 2030** (INEMA.CLUB, aberto e gratuito): uma empresa **fictícia** de 40 pessoas com **12 falhas de IA plantadas de propósito**, para treinar auditoria, consultoria e adoção segura de IA.

Site: https://inematds.github.io/prof2030-lab/ · Programa: https://eventos.inema.pro/prof2030/

> **Tudo aqui é falso e proposital.** Não há servidor, banco de dados nem dado real. Chaves (`FAKE-EXEMPLO`), CPFs (inválidos), telefones, pessoas e empresas são inventados. Site estático: HTML, CSS e JS puro, sem build.

## Falhas plantadas

| Código | Peça | Falha |
|---|---|---|
| F1 | `pecas/app-pedidos/` | chave de API (falsa) no JavaScript do navegador |
| F2 | `pecas/app-pedidos/` | tabela de pedidos sem RLS |
| F3 | `pecas/app-pedidos/admin.html` | rota de admin sem login |
| F4 | `pecas/app-pedidos/` | dependência velha com vulnerabilidade conhecida no `package.json` |
| F5 | `pecas/agente-whatsapp/` | desconto sem teto |
| F6 | `pecas/agente-whatsapp/` | aceita ordem escondida no texto do cliente (injeção de prompt) |
| F7 | `pecas/agente-whatsapp/` | sem registro nem aprovação humana acima de R$ 5 mil |
| F8 | `pecas/planilha-clientes/` | planilha com CPF e telefone "qualquer pessoa com o link" |
| F9 | `pecas/mcp-email/` | MCP com enviar e apagar e-mail sem aprovação |
| F10 | `pecas/resumo-atendimento/` | conversa de cliente para API estrangeira sem contrato nem base legal |
| F11 | `pecas/painel/` | painel sem linha de base |
| F12 | `inventario.html` | IA na sombra: 4 ferramentas que a TI não conhece |

Respostas completas (onde, por quê, como corrigir, gravidade): `gabarito.html` (com aviso de spoiler).

## Como usar nos cursos

Os cursos Base, Consultor, Auditor, Mentor e Treinador mandam o aluno abrir uma peça, achar a falha pelo código F1–F12 e propor a correção. Os caminhos e códigos são **fixos**: não renomeie peças.

Pessoas fictícias: Carlos Mendes (dono), Patrícia Lima (gerente comercial), Rafael (TI terceirizada), Juliana (atendimento).
