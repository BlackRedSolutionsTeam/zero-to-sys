# Integrar com ERP e contabilidade

> Se o cliente já usa ERP, deixe o ERP emitir e o seu sistema mandar a venda; duas fontes emitindo nota é o caminho mais curto para duplicata.

| | |
|---|---|
| **Referência** | https://developer.omie.com.br, https://developer.bling.com.br, https://developers.contaazul.com |
| **Categoria** | Integração |
| **Tipo** | Prática de integração com ERP e sistema contábil |
| **Vale para** | Sistemas que vendem a clientes que usam Omie, Bling ou Conta Azul; backends que enviam vendas e recebem notas |
| **Verificado em** | 2026-11-25 |

## O que é

**ERP** é o sistema de gestão da empresa: estoque, financeiro, faturamento e emissão de nota. **Omie**, **Bling** e **Conta Azul** são os mais comuns em pequenas empresas e têm API para enviar pedidos e consultar notas. Há três arranjos:

| Arranjo | Quem emite | Seu sistema faz |
|---|---|---|
| Emissor próprio ([doc 02](02-emissor-via-api.md)) | Seu sistema pelo emissor | Emite e, se quiser, exporta para o ERP |
| ERP emite | O ERP | Envia a venda e lê a nota |
| Contador faz | O escritório | Exporta XML e relatório |

## Por que usar

- **Uma fonte de verdade fiscal:** o ERP já tem estoque, financeiro e o contador.
- **Menos código fiscal no seu sistema.**
- **Integração com a contabilidade:** o ERP exporta o necessário ao contador.

## Quando usar

- O cliente já tem ERP e não quer trocar.
- O sistema é um front de vendas (loja, agendamento) e o back-office fiscal é do ERP.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Loja virtual de cliente com ERP | ✅ Ótimo | Pedido vai ao ERP, que emite e baixa estoque |
| SaaS vendido a clientes com ERPs diferentes | 🟡 Serve | Cada ERP é uma integração; priorize o mais usado pelos clientes |
| Sistema interno de empresa com ERP | ✅ Ótimo | Substitui digitação |
| Produto próprio sem cliente com ERP | ❌ Evite | Use emissor por API (doc 02) |
| Só exportar para o contador | 🟡 Serve | Exportação de XML e planilha basta |

## Quando é bom

- **Omie:** API de pedidos de venda, ordens de serviço (faturamento para NFS-e), consulta de NF-e e NFS-e emitidas, clientes, produtos e contas a receber; webhooks configurados em Aplicativos.
- **Bling:** API v3 com OAuth 2.0 e erro 429 ao exceder o limite; limites lidos na página oficial em 2026-11-25 (tabela abaixo).
- **Conta Azul:** API em `api-v2.contaazul.com` com consulta de NF-e e NFS-e emitidas, por data, número e id da venda, e busca por chave de acesso. É só consulta de notas já emitidas no ERP, não emissão.

## Quando é ruim

- **Limites de requisição:** a Omie limita por IP, por app e por método; o Bling e a Conta Azul retornam 429. Leia em lote e com espera.
- **Cada ERP tem um modelo de cliente, produto e venda diferente:** mapeie com uma tabela de correspondência, não com a estrutura do seu banco.
- **Nota emitida nos dois lados:** se o ERP emite, o seu sistema não pode emitir a mesma venda.
- **Credenciais de cliente no seu servidor:** cada cliente autoriza com OAuth ou chave dele; trate como segredo (skill `security`).

## Como começar

### Limites e autenticação, conferidos em 2026-11-25

| ERP | Autenticação | Limites e detalhes |
|---|---|---|
| Omie | Chave e segredo do aplicativo, criados em Aplicativos; chamadas em JSON a `https://app.omie.com.br/api/v1/...` | 240 requisições por minuto por IP, app e método, 960 por minuto por IP, 4 simultâneas; apps de teste 60 por minuto; no máximo 100 registros por página; 10 chamadas inválidas iguais bloqueiam por 30 minutos |
| Bling | OAuth 2.0 (authorization code, access token e refresh token), erro 401 para chave inválida | 3 requisições por segundo e 120.000 por dia, por conta Bling (não por endpoint); acima disso, HTTP 429. Bloqueio do IP por 10 minutos com 300 erros em 10 segundos ou 600 requisições em 10 segundos, e por 60 minutos com 20 chamadas a `/oauth/token` em 60 segundos; insistir pode bloquear o IP por tempo indeterminado (developer.bling.com.br/limites, 2026-11-25) |
| Conta Azul | OAuth 2.0 Authorization Code. Troca do código em `POST https://api-v2.contaazul.com/oauth/token` com `Authorization: Basic` (client id e secret em Base64) e corpo `application/x-www-form-urlencoded` (`grant_type`, `code`, `redirect_uri`). Chamadas com `Authorization: Bearer <access_token>`. `access_token` vale 3.600 segundos; o `refresh_token` vale até 2 anos, mas cada renovação emite um novo e invalida o anterior, então grave o novo a cada renovação | 600 chamadas por minuto e até 10 por segundo, por conta conectada; acima disso, HTTP 429. Rotas: `GET /v1/notas-fiscais` (NF-e emitidas), `GET /v1/notas-fiscais-servico` (NFS-e) e `GET /v1/notas-fiscais/{chave}` (arquivo da nota). A própria documentação é inconsistente: a introdução da API de notas diz que só há consulta de NF-e, mas a rota de NFS-e está listada; teste antes de prometer ao cliente |

Fontes lidas em 2026-11-25: developer.bling.com.br/limites e developers.contaazul.com (autenticação, troca do código, renovação, chamadas, perguntas frequentes e erros comuns). Não lidos: a URL da tela de autorização e os escopos da Conta Azul, e o fluxo OAuth do Bling além dos limites; copie-os do portal do desenvolvedor de cada um ao montar o aplicativo.

### Endpoints úteis da Omie

| O que | Endereço |
|---|---|
| Cliente | `https://app.omie.com.br/api/v1/geral/clientes/` |
| Pedido de venda (produto) | `https://app.omie.com.br/api/v1/produtos/pedido/` |
| Faturamento do pedido | `https://app.omie.com.br/api/v1/produtos/pedidovendafat/` |
| Ordem de serviço | `https://app.omie.com.br/api/v1/servicos/os/` |
| NF-e emitidas | `https://app.omie.com.br/api/v1/produtos/nfconsultar/` |
| NFS-e emitidas | `https://app.omie.com.br/api/v1/servicos/nfse/` |
| PDF e XML | `https://app.omie.com.br/api/v1/produtos/dfedocs/` |

### Fluxo recomendado

1. O pagamento é aprovado no seu sistema ([doc 05](05-fluxo-pagamento-emissao-webhook.md)).
2. Um job envia o cliente (se novo) e o pedido ao ERP e grava o id externo.
3. O ERP fatura e emite a nota.
4. Webhook do ERP, ou consulta periódica, traz a nota; o job baixa XML e PDF e guarda uma cópia ([doc 07](07-guarda-de-xml-e-lgpd.md)).

```ts
export async function enviarVendaParaOmie(pedido: Pedido) {
  const resposta = await fetch("https://app.omie.com.br/api/v1/produtos/pedido/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      call: "IncluirPedido",
      app_key: process.env.OMIE_APP_KEY,
      app_secret: process.env.OMIE_APP_SECRET,
      param: [montarPedidoOmie(pedido)],
    }),
  });

  if (!resposta.ok) throw new Error(`Omie respondeu ${resposta.status}`);
  const corpo = await resposta.json();
  await pedidos.gravarIdExterno(pedido.id, "omie", String(corpo.codigo_pedido));
}
```

O formato `call`, `app_key`, `app_secret` e `param` segue o padrão JSON das APIs da Omie; confira o nome do método e os campos de `montarPedidoOmie` na página do serviço "Pedidos de Venda". A chave `pedido.id` vira idempotência: se o id externo já existe, não envie de novo.

### Mapa e erros

- **Tabela de correspondência:** `id_externo_cliente`, `id_externo_produto` e `sistema` (omie, bling, contaazul) por registro.
- **Falha do ERP:** retry com espera na fila; erro de validação vai para fila de revisão, não para loop (skill `integrations`, doc 05).
- **Rotina de conciliação:** compare pedidos pagos sem nota há mais de 1 dia e alerte.

### Contabilidade

Escritório contábil normalmente pede o XML do mês e o relatório de vendas. Gere um ZIP mensal dos XML guardados ([doc 07](07-guarda-de-xml-e-lgpd.md)) e uma planilha de vendas ([planilhas](../../integrations/docs/09-importar-e-exportar-planilhas.md)). Muitos ERPs dão acesso direto ao contador, o que dispensa envio manual.

## Decisão rápida

| Situação | Escolha |
|---|---|
| Cliente usa ERP | O ERP emite; você envia a venda |
| Ninguém usa ERP | Emissor por API (doc 02) |
| Quer só ajudar o contador | ZIP de XML e planilha mensal |
| Vários ERPs possíveis | Adaptador por ERP atrás de uma interface única; comece pelo que seus clientes usam |
| Dúvida de quem emite | Uma só fonte por venda, registrada no pedido |
