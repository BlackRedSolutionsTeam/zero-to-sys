# Filas e jobs

> Tudo que é lento, pode falhar ou não precisa responder na hora vai para uma fila e roda num worker separado, com retry, timeout e job idempotente.

| | |
|---|---|
| **Referência** | Documentação oficial do pg-boss, BullMQ, River, Hangfire, Laravel Queues, Celery, Dramatiq, Huey, Django Q2, Spring Framework (Async e Scheduling), Inngest e Trigger.dev; PostgreSQL, SELECT ... FOR UPDATE SKIP LOCKED (postgresql.org/docs); Transactional Outbox, Chris Richardson (microservices.io) |
| **Categoria** | Integrações |
| **Tipo** | Prática de processamento em segundo plano |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go |
| **Verificado em** | 2026-11-24 |

## O que é

Fila é uma lista de tarefas pendentes. Quem pede o trabalho (a API) só anota a tarefa. Outro processo, o **worker**, pega as tarefas uma a uma e executa. Cada tarefa é um **job**.

No sistema de clínica: a API confirma o agendamento e responde em milissegundos. O e-mail de confirmação e o aviso por WhatsApp saem depois, pelo worker.

## Por que usar

- **Resposta rápida:** o usuário não espera o provedor de e-mail.
- **Resiliência:** se o provedor cair, o job tenta de novo em vez de perder o envio.
- **Controle de carga:** o worker processa em ritmo limitado e protege o provedor e o banco.
- **Isolamento:** erro num job não derruba a requisição.

## Quando usar

- Envio de e-mail, WhatsApp ou SMS.
- Relatório ou exportação demorada.
- Receber webhook: guarde, responda 200 e processe na fila (veja [04-webhooks.md](04-webhooks.md)).
- Chamada a integração lenta ou instável.
- Qualquer coisa que precise de retry.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Quase nada roda em segundo plano; um formulário de contato não justifica fila |
| MVP de SaaS | ✅ Ótimo | E-mail e webhook já pedem fila; comece com a fila no próprio Postgres |
| SaaS em crescimento | ✅ Ótimo | Volume, prioridades e painel de falhas ficam essenciais |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios e integrações com sistemas lentos |
| API/integração | ✅ Ótimo | Webhooks e chamadas externas com retry |
| App mobile com backend | ✅ Ótimo | Push, e-mail e processamento de upload fora da requisição |

## Quando é bom

- **Fila no banco (Postgres):** sem serviço novo, e o job entra na mesma transação do dado. Funciona porque o Postgres tem `SELECT ... FOR UPDATE SKIP LOCKED`: vários workers pegam jobs diferentes sem esperar um pelo outro.
- **Job idempotente:** a entrega é **at-least-once** (pelo menos uma vez). Se o worker cair no meio, o job roda de novo. O BullMQ diz isso na documentação e o Hangfire também. Então rodar duas vezes não pode enviar dois e-mails (veja [idempotência e retries](../../api/docs/06-idempotencia-e-retries.md)).
- **Retry com backoff:** esperar mais a cada tentativa (10 s, 1 min, 10 min) dá tempo ao provedor de voltar.
- **Dead-letter:** depois de N falhas, o job vai para uma fila de mortos, onde uma pessoa vê e reprocessa.
- **Timeout por job:** job travado não ocupa o worker para sempre.
- **Concorrência limitada:** poucos jobs ao mesmo tempo contra um provedor com limite de requisições.

## Quando é ruim

- **Fila para tudo:** operação que o usuário precisa ver pronta na hora deve ser síncrona.
- **Job que não é idempotente:** com retry, cobra ou envia em dobro.
- **Fila sem monitoramento:** os jobs falham em silêncio e ninguém vê.
- **Enfileirar dentro de transação sem cuidado:** o worker pode pegar o job antes do commit e não achar o dado.
- **Fila no banco com volume muito alto:** carga de jobs concorre com as consultas do app; nesse ponto avalie Redis ou serviço dedicado.

## Como começar

Opções, todas conferidas na documentação oficial:

| Opção | Onde guarda | Notas |
|---|---|---|
| pg-boss (Node) | Postgres | Requer Node 22.12+ e Postgres 13+; retry com backoff exponencial, dead letter, agendamento cron, criação de job em transação |
| Graphile Worker (Node) | Postgres | Fila para Node e Postgres; retries com backoff exponencial (padrão de 25 tentativas em cerca de três dias), agendamento estilo cron e `SKIP LOCKED` |
| River (Go, também outras linguagens) | Postgres ou SQLite | Enfileira em transação; retries, jobs únicos, jobs periódicos |
| BullMQ (Node) | Redis 6.2+ (ou Postgres 13+) | Retry com backoff, job schedulers com cron; at-least-once |
| Inngest | Serviço | Plano grátis: 50.000 execuções por mês e 5 passos simultâneos |
| Trigger.dev | Serviço | Plano grátis: US$ 5 de crédito de computação por mês, 20 execuções simultâneas |

Preços e limites mudam; confirme na página oficial antes de decidir.

Exemplo principal com pg-boss: lembrete de agendamento.

```ts
import { PgBoss } from "pg-boss";

export const boss = new PgBoss(process.env.DATABASE_URL!);

export async function startQueue() {
  await boss.start();
  await boss.createQueue("send-reminder");
}

export async function enqueueReminder(appointmentId: string) {
  await boss.send("send-reminder", { appointmentId });
}
```

Worker (processo separado do servidor web):

```ts
import { boss, startQueue } from "./queue";
import { sendReminder } from "./reminders";

await startQueue();

await boss.work("send-reminder", async ([job]) => {
  await sendReminder(job.data.appointmentId);
});
```

Idempotência dentro do job: marque o envio antes de repetir.

```ts
export async function sendReminder(appointmentId: string) {
  const claimed = await db.query(
    "update appointment set reminder_sent_at = now() where id = $1 and reminder_sent_at is null returning id",
    [appointmentId],
  );
  if (claimed.rowCount === 0) return;
  await email.send(await buildReminder(appointmentId));
}
```

Se o envio falhar depois de marcar, o lembrete se perde. Para não perder, grave o estado só depois de enviar e use a chave de idempotência do provedor, quando ele oferecer.

Fila feita à mão no Postgres, quando não quiser biblioteca:

```sql
with next_job as (
  select id from job
  where status = 'pending' and run_at <= now()
  order by run_at
  limit 1
  for update skip locked
)
update job set status = 'running', started_at = now()
from next_job where job.id = next_job.id
returning job.*;
```

**Outbox:** quando o job precisa existir se, e somente se, o dado foi gravado, grave uma linha na tabela `outbox` na mesma transação. Um processo lê as pendentes e as publica. Detalhes em [transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md). Bibliotecas que enfileiram na mesma transação (pg-boss, River) fazem o papel do outbox.

**Worker como processo separado:** rode o worker como outro serviço, com o mesmo código e outro comando de início. Hospedagem em [PaaS](../../infra/docs/01-paas.md).

**Observabilidade:** meça tamanho da fila, idade do job mais antigo, taxa de falha e o conteúdo da fila de mortos. Alerte quando o job mais antigo passar de um limite (por exemplo, 10 minutos).

**Em cada stack:**

| Stack | Ferramenta |
|---|---|
| Node | pg-boss, Graphile Worker, BullMQ |
| Python | Celery, Dramatiq (Redis ou RabbitMQ), Huey (Redis, Postgres, SQLite), Django Q2 (inclui o banco via ORM) |
| .NET | Hangfire (armazena em SQL Server ou Redis; licença LGPLv3; painel embutido) |
| Java | Spring `@Async` (executor em memória, sem persistência) e Quartz para agendamento |
| Laravel | Laravel Queues (drivers database, redis, sqs); Horizon para Redis; `ShouldBeUnique`, `afterCommit` |
| Go | River |

`@Async` do Spring roda no mesmo processo: se o app reiniciar, o que estava na memória se perde. Para job que não pode se perder, use fila persistente.

## Combina com / alternativas

- [06-rotinas-agendadas.md](06-rotinas-agendadas.md): jobs repetidos no tempo.
- [04-webhooks.md](04-webhooks.md): receber e processar depois.
- [02-email-transacional.md](02-email-transacional.md) e [03-whatsapp-e-sms.md](03-whatsapp-e-sms.md): os envios que mais passam pela fila.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md) e [transações e outbox](../../data/docs/09-transacoes-e-concorrencia.md).
- [PaaS](../../infra/docs/01-paas.md): onde rodar o worker.

## Decisão rápida

- **Use se:** a tarefa é lenta, falha com frequência ou pode esperar alguns segundos; comece pela fila no Postgres e só vá para Redis ou serviço quando medir a necessidade.
- **Evite se:** o usuário precisa do resultado na mesma resposta, ou se o job não puder ser idempotente e não houver como protegê-lo.
