# Fila simples x broker

> Fique na fila do Postgres ou do Redis enquanto ela der conta; só adote um broker (RabbitMQ, Kafka, NATS) quando medir um limite real ou precisar de roteamento, vários consumidores ou reprocessamento de histórico.

| | |
|---|---|
| **Referência** | Documentação oficial de PostgreSQL (SKIP LOCKED), RabbitMQ (rabbitmq.com/docs), Apache Kafka (kafka.apache.org/documentation), NATS JetStream (docs.nats.io), BullMQ; Enterprise Integration Patterns (enterpriseintegrationpatterns.com) |
| **Categoria** | Mensageria |
| **Tipo** | Prática de decisão de infraestrutura |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go |
| **Verificado em** | 2026-11-25 |

## O que é

Três famílias resolvem "um processo avisa outro":

- **Fila de tarefas:** cada mensagem é um trabalho que um worker executa uma vez e some. É o caso de [filas e jobs](../../integrations/docs/05-filas-e-jobs.md).
- **Broker de mensagens (RabbitMQ):** recebe, roteia para filas e entrega ao consumidor; a mensagem some depois do ack.
- **Log de eventos (Kafka, NATS JetStream):** guarda os eventos em ordem por um tempo; vários consumidores leem, cada um no seu ritmo, e podem reler o passado.

## Por que usar

- Saber quando o Postgres ou o Redis já bastam evita operar um servidor a mais.
- Saber o que cada broker faz evita escolher pelo nome.

## Quando usar

- A fila do Postgres ou do Redis começou a pesar no banco do app.
- Vários serviços diferentes precisam reagir ao mesmo evento.
- Precisa reler eventos antigos (reprocessar, montar uma visão nova).
- Precisa de roteamento por tipo, prioridade ou padrão de nome.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Não tem o que enfileirar |
| MVP de SaaS | ❌ Evite | pg-boss ou BullMQ resolvem; broker é custo operacional sem retorno |
| SaaS em crescimento | 🟡 Serve | RabbitMQ quando vários serviços consomem; só se a fila do banco virar gargalo |
| Sistema interno/corporativo | 🟡 Serve | Integração entre sistemas pede broker; um único sistema, não |
| API/integração com alto volume | ✅ Ótimo | Milhares de eventos por segundo e vários consumidores |
| App mobile com backend | ❌ Evite | A fila do backend basta |

## Quando é bom

| Necessidade | Escolha |
|---|---|
| Tarefas em segundo plano, até alguns milhares por minuto | Fila no Postgres (pg-boss, River) ou no Redis (BullMQ) |
| Tarefas com roteamento, prioridade e vários serviços | RabbitMQ ([02](./02-rabbitmq.md)) |
| Stream de eventos com histórico e reprocessamento | Kafka ([03](./03-kafka.md)) |
| Mensagens leves e rápidas entre serviços, binário único | NATS (core e JetStream) |
| Só avisar o navegador | SSE ou serviço gerenciado ([tempo real](../../integrations/docs/08-tempo-real-e-notificacoes.md)) |

- **NATS:** o servidor é um binário único. O core NATS entrega só a quem está conectado na hora; o JetStream (conferido em 2026-11-25 em docs.nats.io) acrescenta persistência, replay e entrega at-least-once. A versão mais recente do servidor era a 2.15.3.
- **Serviço gerenciado** tira a operação das suas costas: CloudAMQP para RabbitMQ (plano grátis Little Lemur: 100 filas, 10 mil mensagens enfileiradas e 1 milhão de mensagens por mês; Tough Tiger a US$ 19/mês; dedicado a partir de US$ 50/mês, conferido em 2026-11-25) e Confluent Cloud para Kafka (Basic a partir de US$ 0/mês, com a primeira unidade de computação grátis, conferido em 2026-11-25).

## Quando é ruim

- **Broker no MVP:** mais um serviço para atualizar, monitorar e fazer backup.
- **Kafka como fila de e-mail:** serve, mas é o exagero clássico.
- **Trocar a fila por falta de monitoramento:** se os jobs falham em silêncio, o problema é observabilidade, não a ferramenta.
- **Broker sem dono:** quem opera, atualiza e responde quando enche o disco?
- **Esperar entrega exatamente uma vez:** todos entregam pelo menos uma vez; o consumidor precisa ser idempotente ([idempotência](../../api/docs/06-idempotencia-e-retries.md)).

## Como começar

Teste antes de trocar: meça a fila atual.

```sql
select count(*) filter (where status = 'pending') as pendentes,
       now() - min(run_at) filter (where status = 'pending') as mais_antigo
from job;
```

Sinais para sair da fila do banco:

| Sinal | Ação |
|---|---|
| Idade do job mais antigo cresce mesmo com mais workers | Medir o gargalo; talvez índice, talvez Redis |
| O banco do app sofre com o `UPDATE` da fila | Fila em Redis ou em outro Postgres |
| Três ou mais serviços reagem ao mesmo evento | RabbitMQ ou Kafka |
| Precisa reprocessar os eventos de ontem | Kafka ou JetStream |

Opções de operar o broker: gerenciado (CloudAMQP, Confluent Cloud) ou próprio no Compose da VPS ([skill vps](../../vps/SKILL.md)); a operação está em [infra](../../infra/SKILL.md).

## Combina com / alternativas

- [Filas e jobs](../../integrations/docs/05-filas-e-jobs.md): o ponto de partida.
- [02 RabbitMQ](./02-rabbitmq.md), [03 Kafka](./03-kafka.md) e [04 Outbox](./04-outbox-e-entrega-confiavel.md).
- [Arquitetura](../../architecture/SKILL.md): monólito modular antes de serviços; sem serviços, sem necessidade de broker.

## Decisão rápida

- **Use se:** a fila do banco foi medida e não dá conta, ou vários serviços precisam do mesmo evento.
- **Evite se:** o time é pequeno, o sistema é um monólito e a fila atual ainda responde.
