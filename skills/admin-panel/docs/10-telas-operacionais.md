# Telas operacionais

> Cinco telas resolvem a maior parte do dia da equipe: busca global, ficha com linha do tempo, fila de jobs e webhooks com falha, ajuste de cobrança e consulta de logs.

| | |
|---|---|
| **Referência** | Documentação do Stripe sobre webhooks e reenvio de eventos (docs.stripe.com/webhooks, citada de memória e não reaberta nesta data); padrões de fila das skills `integrations` e `operations` |
| **Categoria** | Funcionalidade |
| **Tipo** | Catálogo de telas |
| **Vale para** | SaaS e sistemas com suporte e operação |
| **Verificado em** | 2026-11-25 (referência do Stripe não reaberta nesta data) |

## O que é

As telas que transformam "peça ao dev" em "faça no painel". Layout: [design-systems, doc 03](../../design-systems/docs/03-admin-crud.md). Aqui, o conteúdo e as regras.

## Por que usar

- Cada tela remove um tipo de chamado ao time de desenvolvimento.
- Sem elas, a equipe pede acesso direto ao banco, que é pior.

## Quando usar

- Busca global e ficha do cliente: no MVP do painel.
- Fila, webhooks e cobrança: assim que houver integração e pagamento em produção.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem clientes nem filas |
| MVP de SaaS | ✅ Ótimo | Busca e ficha primeiro |
| SaaS em crescimento | ✅ Ótimo | Todas as telas |
| Sistema interno/corporativo | 🟡 Serve | Fila e logs |
| API/integração | ✅ Ótimo | Webhooks com falha e reenvio |
| App mobile com backend | ✅ Ótimo | Igual ao SaaS |

## As telas

| Tela | O que mostra | Ação |
|---|---|---|
| Busca global | Um campo que acha por nome, e-mail, CPF completo, id, domínio ou número de fatura, com resultado mascarado ([doc 08](08-dados-pessoais-no-painel.md)) | Abrir a ficha |
| Linha do tempo do cliente | Cadastro, logins, mudanças de plano, cobranças, e-mails enviados, erros, chamados, acessos da equipe, tudo em ordem de data | Filtrar por tipo |
| Fila e jobs | Pendentes, em execução, falhos, tentativas, erro e payload sem segredo | Reprocessar um, cancelar, reprocessar lote com limite ([doc 07](07-acoes-perigosas.md)) |
| Webhooks | Eventos recebidos e enviados, status, resposta, número de tentativas | Reprocessar um evento (idempotente) |
| Cobrança | Assinatura, fatura, tentativas de cobrança | Dar crédito, estornar, trocar plano, estender teste, sempre com motivo e limite por papel |
| Logs e saúde | Erros recentes por empresa, status das integrações, versão publicada | Somente leitura; link para a ferramenta de logs |

## Quando é bom

- **Ação com nome** ("Reprocessar webhook"), nunca "editar campo".
- **Link da ficha para a tela de cada evento**, e vice-versa.
- **Idempotência:** reprocessar duas vezes não cobra duas vezes ([integrations, doc 04](../../integrations/docs/04-webhooks.md) e [doc 05](../../integrations/docs/05-filas-e-jobs.md)).
- **Cobrança no provedor de pagamento:** o painel chama a API do provedor e depois grava; não edita o valor direto na tabela ([integrations, doc 01](../../integrations/docs/01-pagamentos.md)).
- **Payload exibido sem segredo:** mascare cabeçalhos e tokens.

## Quando é ruim

- **Reprocessar sem checar o estado atual:** reenviar um webhook de pagamento já aplicado.
- **Ajustar valor na tabela** sem passar pelo provedor: o sistema e o provedor divergem.
- **Busca que varre tudo sem índice:** use índice e paginação ([data, doc 08](../../data/docs/08-indices-e-paginacao.md)).

## Como começar

Reprocessar webhook (TypeScript):

```ts
app.post("/painel/webhooks/:id/reprocessar", exige("webhook.reprocessar"), async (c) => {
  const evento = await db.webhookEvent.findUniqueOrThrow({ where: { id: c.req.param("id") } });
  if (evento.status === "processed") return c.json({ erro: "Evento já processado." }, 409);
  return agir(contexto(c), "webhook.reprocessar", { tipo: "webhook_event", id: evento.id, empresaId: evento.tenantId }, async (tx) => {
    const resultado = await processarEvento(tx, evento);
    return { antes: { status: evento.status }, depois: { status: resultado.status }, valor: resultado };
  });
});
```

Busca global (SQL):

```sql
select id, name, mask_email(email) as email, status
from customers
where email = lower($1)
   or document_hash = encode(digest($1, 'sha256'), 'hex')
   or name ilike $1 || '%'
limit 20;
```

## Combina com / alternativas

- [Auditoria](06-auditoria-do-que-a-equipe-faz.md), [ações perigosas](07-acoes-perigosas.md), [operations, doc 07](../../operations/docs/07-suporte-ao-cliente.md).

## Decisão rápida

- **Use** busca global, ficha com linha do tempo e reprocessar com idempotência.
- **Evite** telas que editam tabela crua e ajuste de cobrança sem passar pelo provedor.
