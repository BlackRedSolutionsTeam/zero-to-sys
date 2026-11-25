# RabbitMQ

> Broker de filas com roteamento flexível: o produtor publica numa exchange, a exchange manda para filas, e consumidores confirmam (ack) cada mensagem.

| | |
|---|---|
| **Referência** | https://www.rabbitmq.com/docs, https://www.rabbitmq.com/docs/quorum-queues, https://www.rabbitmq.com/docs/dlx, https://www.rabbitmq.com/docs/confirms, https://www.cloudamqp.com/plans.html |
| **Categoria** | Mensageria |
| **Tipo** | Ferramenta de broker de mensagens |
| **Vale para** | Node (amqplib), Python (pika, aio-pika), .NET, Java (Spring AMQP), Laravel e Go |
| **Verificado em** | 2026-11-25 |

## O que é

- **Producer** publica numa **exchange**, não direto na fila.
- A exchange aplica **bindings** (regras) e entrega a uma ou mais **queues**.
- O **consumer** lê da fila e responde **ack** (feito) ou **nack/reject** (falhou).

Tipos de exchange: `direct` (chave exata), `topic` (padrão, como `pedido.*.criado`), `fanout` (todas as filas) e `headers`.

Versão mais recente conferida em 2026-11-25: 4.4.1 (GitHub, lançada em 16 de novembro).

## Por que usar

- Roteamento por tipo de evento sem código no produtor.
- Retentativa e fila de mortos nativas.
- Protocolo maduro, com cliente em todas as linguagens.

## Quando usar

- Vários serviços, cada um com sua fila, recebendo cópias do mesmo evento.
- Tarefas com prioridades e filas separadas por tipo.
- Integração com sistema legado que fala AMQP.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem uso |
| MVP de SaaS | ❌ Evite | Fila no Postgres basta |
| SaaS em crescimento | ✅ Ótimo | Vários workers e serviços com roteamento |
| Sistema interno/corporativo | ✅ Ótimo | Integra sistemas diferentes |
| API/integração | ✅ Ótimo | Absorve picos e protege o sistema de trás |
| App mobile com backend | 🟡 Serve | Só se o backend já for de vários serviços |

## Quando é bom

Conferido em rabbitmq.com/docs/quorum-queues em 2026-11-25:

- **Quorum queue** é a escolha padrão para fila replicada e durável (Raft): o publisher confirm só vem depois de replicar para a maioria dos nós.
- **Limite de entregas:** o padrão é 20 desde a 4.0; ao passar do limite, a mensagem é descartada ou vai para a dead-letter exchange, se houver.
- **Dead-letter at-least-once:** exige `dead-letter-strategy=at-least-once`, `overflow=reject-publish` e uma DLX configurada.
- **Classic queue:** filas temporárias, exclusivas ou com muita criação e remoção.
- **Streams:** leitura repetível, fanout grande e backlog muito longo.

## Quando é ruim

- **Fila que enche sem consumidor:** a memória e o disco sobem até o alarme travar os produtores.
- **Mensagem grande:** guarde o arquivo no storage e mande só o id.
- **Nack com requeue em loop:** o mesmo erro volta para sempre; use `reject` e deixe o limite de entregas agir.
- **Cluster de um nó em produção crítica:** é um ponto único de falha.
- **Ordem global:** só há ordem dentro de uma fila com um consumidor.

## Como começar

Subir local:

```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

Painel em `http://localhost:15672`. Usuário e senha padrão do contêiner (`guest`/`guest`) só aceitam conexão local: troque em produção.

Fila com retentativa e fila de mortos (Node, amqplib):

```ts
import amqp from "amqplib";

const conn = await amqp.connect(process.env.AMQP_URL!);
const ch = await conn.createChannel();

await ch.assertExchange("pedidos", "topic", { durable: true });
await ch.assertExchange("pedidos.mortos", "fanout", { durable: true });
await ch.assertQueue("pedidos.mortos.fila", { durable: true, arguments: { "x-queue-type": "quorum" } });
await ch.bindQueue("pedidos.mortos.fila", "pedidos.mortos", "");

await ch.assertQueue("pedidos.cobranca", {
  durable: true,
  arguments: {
    "x-queue-type": "quorum",
    "x-dead-letter-exchange": "pedidos.mortos",
    "x-delivery-limit": 5,
  },
});
await ch.bindQueue("pedidos.cobranca", "pedidos", "pedido.criado");

ch.prefetch(10);
await ch.consume("pedidos.cobranca", async (msg) => {
  if (!msg) return;
  try {
    await cobrar(JSON.parse(msg.content.toString()));
    ch.ack(msg);
  } catch {
    ch.reject(msg, true);
  }
});
```

Publicar com confirmação:

```ts
const confirmCh = await conn.createConfirmChannel();
confirmCh.publish("pedidos", "pedido.criado", Buffer.from(JSON.stringify({ id })), { persistent: true });
await confirmCh.waitForConfirms();
```

Regras do dia a dia:

- Ack manual sempre; `prefetch` limita quantas mensagens cada consumidor segura.
- Mensagem `persistent` em fila durável.
- Consumidor idempotente: a entrega é pelo menos uma vez.
- Alerta de tamanho da fila e de idade da mensagem mais antiga.
- Monitoramento e backup em [infra](../../infra/SKILL.md); definições (filas, exchanges, usuários) exportáveis pelo painel de gerenciamento.

Gerenciado: CloudAMQP tem plano grátis (Little Lemur, 1 milhão de mensagens por mês, 20 conexões), Tough Tiger a US$ 19/mês e plano dedicado a partir de US$ 50/mês (conferido em 2026-11-25).

## Combina com / alternativas

- [01 Fila simples x broker](./01-fila-simples-x-broker.md): antes de escolher.
- [04 Outbox](./04-outbox-e-entrega-confiavel.md): publicar sem perder o evento.
- [Filas e jobs](../../integrations/docs/05-filas-e-jobs.md): alternativa no Postgres.
- Alternativas: [Kafka](./03-kafka.md) para histórico; NATS JetStream para algo mais leve.

## Decisão rápida

- **Use se:** vários serviços recebem eventos com roteamento, e você tem quem opere o broker (ou paga o gerenciado).
- **Evite se:** só um app envia tarefas a um worker.
