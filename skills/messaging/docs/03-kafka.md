# Kafka

> Log distribuído de eventos: os eventos ficam guardados por um tempo, em partições ordenadas, e cada grupo de consumidores lê no seu ritmo e pode reler o passado.

| | |
|---|---|
| **Referência** | https://kafka.apache.org/documentation, https://kafka.apache.org/community/downloads/, https://www.confluent.io/confluent-cloud/pricing/ |
| **Categoria** | Mensageria |
| **Tipo** | Ferramenta de streaming de eventos |
| **Vale para** | Java, Node (kafkajs), Python, .NET e Go |
| **Verificado em** | 2026-11-25 |

## O que é

- **Topic:** categoria de eventos (`pedidos`).
- **Partição:** pedaço do topic; a ordem só é garantida dentro de uma partição. Eventos com a mesma **chave** (como o id do pedido) caem na mesma partição.
- **Consumer group:** consumidores que dividem as partições; cada partição vai para um consumidor do grupo. Grupos diferentes leem o mesmo evento de forma independente.
- **Offset:** a posição de leitura. O evento não some ao ser lido; sai por tempo ou tamanho de retenção.

Versões conferidas em 2026-11-25 em kafka.apache.org: 4.4.0 (22 de outubro de 2026) e 4.3.2 (23 de outubro). Desde a 4.0 o Kafka roda sem ZooKeeper, no modo KRaft.

## Por que usar

- Alto volume com vários consumidores independentes.
- Reprocessar o histórico (corrigir um bug e reler os eventos).
- Base para CDC (captura de mudanças do banco) e pipelines de dados.

## Quando usar

- Dezenas de milhares de eventos por segundo.
- Vários times consumindo o mesmo fluxo.
- Evento é o registro oficial (auditoria, event sourcing).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem uso |
| MVP de SaaS | ❌ Evite | Exagero: operação pesada para pouco volume |
| SaaS em crescimento | 🟡 Serve | Só com vários consumidores e volume que o Postgres não segura |
| Sistema interno/corporativo | 🟡 Serve | Integração de dados entre áreas |
| API/integração com alto volume | ✅ Ótimo | Telemetria, cliques, pagamentos em escala |
| App mobile com backend | ❌ Evite | O backend não precisa |

## Quando é bom

- **Retenção configurável:** o evento fica lá; um consumidor novo começa do início.
- **Escala por partição:** mais partições, mais consumidores em paralelo.
- **Durabilidade:** replicação por partição; com fator de replicação 3 e `min.insync.replicas=2`, mais `acks=all` no produtor, sobrevive à queda de um broker.
- **Ecossistema:** Kafka Connect e Debezium para ligar bancos a topics ([04](./04-outbox-e-entrega-confiavel.md)).

## Quando é ruim

- **Exagero para fila de tarefas:** não há retry por mensagem, prioridade nem atraso nativos.
- **Operação:** versões, discos, rebalanceamento, monitoramento de lag; pede gente com experiência.
- **Poucas mensagens:** custo fixo alto para pouco ganho.
- **Ordem global:** só por partição; escolha a chave com cuidado.
- **Mensagem venenosa:** um evento que sempre falha trava a partição do consumidor se você não tratar (fila de mortos feita à mão).

## Como começar

Subir local (imagem oficial, modo KRaft, um nó):

```bash
docker run -d --name kafka -p 9092:9092 apache/kafka:latest
```

Em produção, fixe a versão da imagem em vez de `latest`.

Criar um topic e publicar com chave (Node, kafkajs):

```ts
import { Kafka } from "kafkajs";

const kafka = new Kafka({ clientId: "api", brokers: [process.env.KAFKA_BROKER!] });
const producer = kafka.producer({ idempotent: true });
await producer.connect();

await producer.send({
  topic: "pedidos",
  acks: -1,
  messages: [{ key: pedido.id, value: JSON.stringify({ tipo: "pedido.criado", id: pedido.id }) }],
});
```

Consumidor em grupo:

```ts
const consumer = kafka.consumer({ groupId: "cobranca" });
await consumer.connect();
await consumer.subscribe({ topic: "pedidos", fromBeginning: false });

await consumer.run({
  eachMessage: async ({ message }) => {
    const evento = JSON.parse(message.value!.toString());
    await processar(evento);
  },
});
```

Regras do dia a dia:

- Chave pelo id da entidade, para manter a ordem dela.
- Consumidor idempotente: o commit do offset acontece depois do processamento, então um reinício repete mensagens.
- Número de partições definido com folga: aumentar depois muda o destino das chaves.
- Alerta no **lag** (quanto o grupo está atrás).
- Kafka gerenciado: Confluent Cloud, cluster Basic a partir de US$ 0/mês (primeira unidade de computação grátis; depois US$ 0,14 por unidade-hora; US$ 0,05 por GB trafegado e US$ 0,08 por GB-mês guardado; conferido em 2026-11-25). Serviços compatíveis com o protocolo existem, mas confira preço e compatibilidade antes.

## Combina com / alternativas

- [01 Fila simples x broker](./01-fila-simples-x-broker.md) e [02 RabbitMQ](./02-rabbitmq.md): alternativas mais leves.
- [04 Outbox](./04-outbox-e-entrega-confiavel.md): como publicar eventos do banco sem perdê-los.
- [Arquitetura](../../architecture/SKILL.md): eventos entre serviços só depois de separar serviços de verdade.
- [Infra](../../infra/SKILL.md): operar e monitorar.

## Decisão rápida

- **Use se:** o volume é alto, vários consumidores precisam do mesmo fluxo e o histórico precisa ser relido.
- **Evite se:** o que você quer é uma fila de tarefas ou o time não tem quem opere.
