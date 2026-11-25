# Outbox e entrega confiável entre serviços

> Para nunca gravar o dado sem publicar o evento (nem o contrário), grave o evento numa tabela `outbox` na mesma transação do dado e deixe outro processo publicá-lo; do outro lado, o consumidor ignora duplicatas.

| | |
|---|---|
| **Referência** | https://microservices.io/patterns/data/transactional-outbox.html, https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html, https://www.postgresql.org/docs/current/sql-select.html, https://debezium.io/releases/ |
| **Categoria** | Mensageria |
| **Tipo** | Padrão de entrega confiável |
| **Vale para** | Qualquer stack com banco relacional e broker |
| **Verificado em** | 2026-11-25 |

## O que é

Gravar no banco e publicar no broker são duas operações. Se uma funciona e a outra falha, o sistema fica inconsistente: pedido salvo sem evento, ou evento sem pedido (dual write).

- **Outbox (saída):** o evento vira uma linha numa tabela do mesmo banco, na mesma transação do dado. Um **relay** lê as linhas pendentes e publica no broker.
- **Inbox (entrada):** o consumidor guarda o id de cada mensagem processada e ignora as repetidas.

Resultado: entrega **at-least-once** no broker e efeito **uma vez** no consumidor.

## Por que usar

- Elimina a inconsistência entre banco e broker.
- Se o broker cair, os eventos esperam na tabela.
- Funciona com qualquer broker.

## Quando usar

- Serviço que grava no banco e avisa outros ([02](./02-rabbitmq.md) ou [03](./03-kafka.md)).
- Qualquer fluxo em que perder um evento custa dinheiro.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem eventos |
| MVP de SaaS | 🟡 Serve | Se a fila é a do próprio Postgres (pg-boss), ela já é o outbox |
| SaaS em crescimento | ✅ Ótimo | Quando entra broker, entra outbox |
| Sistema interno/corporativo | ✅ Ótimo | Integração entre sistemas sem perda |
| API/integração | ✅ Ótimo | Garante o webhook ou o evento |
| App mobile com backend | 🟡 Serve | Só com vários serviços |

## Quando é bom

- Evento e dado nascem juntos ou não nascem.
- Relay simples (consulta periódica) ou CDC com Debezium, que lê o log do banco.
- Debezium: a versão estável mais recente era a 3.7.1.Final (novembro de 2026); exige Kafka Connect 3.1 ou superior (conferido em 2026-11-25). Tem o Outbox Event Router, que roteia as linhas da tabela para topics.

## Quando é ruim

- **Tabela outbox sem limpeza:** cresce sem fim; apague as publicadas.
- **Relay sem lock:** duas instâncias publicam a mesma linha; use `FOR UPDATE SKIP LOCKED`.
- **Esperar ordem global:** a ordem vale por entidade (chave de partição).
- **Consumidor não idempotente:** at-least-once repete mensagens.
- **Usar com um único app e uma fila no próprio banco:** a fila já está na mesma transação.

## Como começar

Tabelas:

```sql
create table outbox (
  id uuid primary key default gen_random_uuid(),
  aggregate_id text not null,
  type text not null,
  payload jsonb not null,
  created_at timestamptz not null default now(),
  published_at timestamptz
);

create index outbox_pending_idx on outbox (created_at) where published_at is null;

create table inbox (
  message_id text primary key,
  processed_at timestamptz not null default now()
);
```

Gravar o dado e o evento na mesma transação:

```ts
await db.transaction(async (tx) => {
  const pedido = await tx.insert(pedidos).values(dados).returning();
  await tx.insert(outbox).values({
    aggregateId: pedido.id,
    type: "pedido.criado",
    payload: { id: pedido.id, total: pedido.total },
  });
});
```

Relay que publica em lotes:

```ts
export async function publicarPendentes() {
  await db.transaction(async (tx) => {
    const linhas = await tx.execute(sql`
      select * from outbox
      where published_at is null
      order by created_at
      limit 100
      for update skip locked
    `);
    for (const linha of linhas) {
      await broker.publish(linha.type, linha.aggregate_id, linha.payload, linha.id);
    }
    await tx.execute(sql`
      update outbox set published_at = now()
      where id = any(${linhas.map((l) => l.id)})
    `);
  });
}
```

Consumidor com inbox:

```ts
export async function tratar(messageId: string, evento: Evento) {
  await db.transaction(async (tx) => {
    const novo = await tx.execute(sql`
      insert into inbox (message_id) values (${messageId})
      on conflict do nothing returning message_id
    `);
    if (novo.length === 0) return;
    await aplicar(tx, evento);
  });
}
```

- Mande o `id` da linha como id da mensagem: é a chave da inbox.
- Rode o relay a cada poucos segundos; limpe `published_at` antigos com uma rotina ([rotinas agendadas](../../integrations/docs/06-rotinas-agendadas.md)).
- Com Kafka e volume alto, troque o relay por Debezium.
- Meça a idade da linha pendente mais antiga e alerte.

## Combina com / alternativas

- [Filas e jobs](../../integrations/docs/05-filas-e-jobs.md): pg-boss e River enfileiram na mesma transação, fazendo o papel do outbox.
- [Transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md) e [idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).
- [Arquitetura](../../architecture/SKILL.md): onde ficam as fronteiras entre serviços.
- Alternativa: sagas, quando o fluxo atravessa vários serviços e precisa de compensação.

## Decisão rápida

- **Use se:** um serviço grava no banco e publica num broker, e o evento não pode se perder.
- **Evite se:** a fila já vive no mesmo banco da transação.
