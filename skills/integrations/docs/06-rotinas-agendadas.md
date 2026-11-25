# Rotinas agendadas

> Rotina que roda por horário (cron) deve rodar em UTC, uma vez só, ser idempotente e avisar quando não rodar.

| | |
|---|---|
| **Referência** | Documentação oficial do GitHub Actions (evento schedule), Vercel Cron Jobs, Railway Cron, Render Cron Jobs, Cloudflare Workers (limites), Celery (periodic tasks), Laravel (Task Scheduling), Hangfire, Spring (@Scheduled), BullMQ, pg-boss, Healthchecks.io e Sentry Crons; PostgreSQL, Advisory Locks (postgresql.org/docs) |
| **Categoria** | Integrações |
| **Tipo** | Prática de tarefas recorrentes |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go |
| **Verificado em** | 2026-11-24 |

## O que é

Rotina agendada é código que roda sozinho em horário fixo ou em intervalo: "todo dia às 03:00", "a cada 5 minutos". O agendador mais antigo é o **cron**, cuja expressão tem cinco campos (minuto, hora, dia do mês, mês, dia da semana).

No sistema de clínica: lembrar o paciente 24 horas antes da consulta e apagar dados expirados.

## Por que usar

- **Automático:** ninguém precisa lembrar de rodar.
- **Previsível:** o horário está no código, versionado.
- **Separa o tempo do pedido:** o que depende do relógio, e não de uma ação do usuário, tem lugar próprio.

## Quando usar

- Lembrete de consulta, cobrança recorrente, resumo diário.
- Limpeza de dados expirados, token vencido e arquivos temporários.
- Sincronizar com sistema externo que não envia webhook.
- Gerar relatório noturno.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um cron para reconstruir o site ou checar links basta |
| MVP de SaaS | ✅ Ótimo | Lembretes e limpeza já aparecem; o cron do provedor resolve |
| SaaS em crescimento | ✅ Ótimo | Rotinas viram jobs agendados na fila, com lock e alerta |
| Sistema interno/corporativo | ✅ Ótimo | Relatórios e integrações noturnas |
| API/integração | ✅ Ótimo | Reconciliação e sincronização periódica |
| App mobile com backend | 🟡 Serve | O backend roda a rotina; o app só recebe o efeito |
| Rotina que depende de precisão de segundos em plano grátis | ❌ Evite | Planos grátis atrasam ou limitam a frequência |

## Quando é bom

- **UTC no agendador, fuso só na tela:** rode e guarde tudo em UTC e converta para exibir. GitHub Actions, Railway, Render e Celery usam UTC por padrão, e horário de verão pode fazer a rotina rodar duas vezes ou nenhuma (o Laravel avisa isso na documentação e recomenda evitar agendar por fuso quando possível).
- **Rotina idempotente:** rodar duas vezes dá o mesmo resultado que rodar uma.
- **Rotina que só enfileira:** o agendador cria jobs e a [fila](05-filas-e-jobs.md) faz o trabalho, com retry.
- **Lock contra execução dupla:** com duas instâncias do app, as duas disparam a rotina.
- **Alerta de "não rodou":** a falha mais perigosa é a que não faz barulho.

## Quando é ruim

- **Cron em app com várias instâncias, sem lock:** a rotina roda uma vez por instância.
- **Confiar que rodou:** GitHub avisa que as execuções podem atrasar e, sob carga alta, jobs na fila podem ser descartados.
- **Repositório público parado:** o GitHub desativa workflows agendados após 60 dias sem atividade.
- **Rotina longa dentro de função serverless:** o limite de tempo da função corta a execução.
- **Janela por horário de relógio local:** muda duas vezes por ano.

## Como começar

Onde o cron roda, com limites conferidos nas páginas oficiais em 2026-11-24 (confirme antes de depender):

| Opção | Limite no plano grátis ou de entrada | Fuso |
|---|---|---|
| GitHub Actions `schedule` | Intervalo mínimo de 5 minutos; pode atrasar, sobretudo no início da hora | UTC por padrão; aceita `timezone` |
| Vercel Cron | Hobby: uma vez por dia, com precisão por hora (um cron de 01:00 pode rodar entre 01:00 e 01:59); até 100 crons por projeto | Confira na doc |
| Railway cron | Intervalo mínimo de 5 minutos; se a execução anterior ainda roda, a nova é pulada | UTC |
| Render cron | Cobrança mínima de US$ 1 por mês por serviço; uma execução por vez; para após 12 horas | UTC |
| Cloudflare Cron Triggers | Plano Workers Free: 5 por conta | Confira na doc |

Agendador dentro do framework ou da fila:

| Stack | Como |
|---|---|
| Node | pg-boss (agendamento por cron) ou BullMQ (job schedulers com cron ou intervalo) |
| Python | Celery beat (UTC por padrão, `timezone` configurável; rode só uma instância do beat), Huey `periodic_task`, Django Q2 |
| .NET | Hangfire `RecurringJob.AddOrUpdate("id", ..., cron)` |
| Java | Spring `@Scheduled(cron = "...", zone = "UTC")`; Quartz para persistência |
| Laravel | `Schedule::job(...)` em `routes/console.php`, com um cron chamando `schedule:run` a cada minuto; `withoutOverlapping`, `onOneServer` |
| Go | River (jobs periódicos) |

Exemplo com pg-boss: lembrete 24 horas antes. A rotina roda a cada 15 minutos e enfileira os agendamentos que entram na janela.

```ts
await boss.createQueue("enqueue-reminders");
await boss.schedule("enqueue-reminders", "*/15 * * * *");

await boss.work("enqueue-reminders", async () => {
  const due = await db.query(
    `select id from appointment
     where status = 'confirmed'
       and reminder_sent_at is null
       and starts_at between now() + interval '23 hours 45 minutes' and now() + interval '24 hours'`,
  );
  for (const row of due.rows) {
    await boss.send("send-reminder", { appointmentId: row.id });
  }
});
```

Evitar rodar duas vezes com lock do Postgres. `pg_try_advisory_xact_lock` não espera: devolve `false` se outra sessão já tem o lock, e o lock se solta no fim da transação.

```sql
begin;
select pg_try_advisory_xact_lock(hashtext('cleanup-expired'));
commit;
```

```ts
export async function runExclusive(name: string, work: () => Promise<void>) {
  const client = await pool.connect();
  try {
    await client.query("begin");
    const { rows } = await client.query(
      "select pg_try_advisory_xact_lock(hashtext($1)) as locked",
      [name],
    );
    if (rows[0].locked) await work();
    await client.query("commit");
  } catch (error) {
    await client.query("rollback");
    throw error;
  } finally {
    client.release();
  }
}
```

Limpeza de dados expirados (prazo definido em [dados pessoais e LGPD](../../data/docs/10-dados-pessoais-e-lgpd.md)):

```sql
delete from password_reset_token where expires_at < now() - interval '1 day';
```

Apague em lotes se a tabela for grande, como na doc de [migrations](../../data/docs/04-migrations.md).

**Alerta de "não rodou":** a rotina avisa um monitor quando termina; se o aviso não chegar no prazo, o monitor alerta.

- Healthchecks.io: o plano Hobbyist é grátis e monitora 20 jobs (conferido na página de preços).
- Sentry Crons: monitora rotinas recorrentes e alerta sobre erros e timeouts; confira na documentação oficial o que o seu plano inclui.
- Laravel: `pingOnSuccess` e `pingOnFailure` chamam uma URL de monitor.

```ts
await runExclusive("enqueue-reminders", enqueueReminders);
await fetch(process.env.HEALTHCHECK_URL!);
```

## Combina com / alternativas

- [05-filas-e-jobs.md](05-filas-e-jobs.md): a rotina só enfileira e a fila executa.
- [02-email-transacional.md](02-email-transacional.md) e [03-whatsapp-e-sms.md](03-whatsapp-e-sms.md): canais do lembrete.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).
- [Transações e concorrência](../../data/docs/09-transacoes-e-concorrencia.md): locks.
- [Dados pessoais e LGPD](../../data/docs/10-dados-pessoais-e-lgpd.md): prazo de retenção.
- [PaaS](../../infra/docs/01-paas.md): cron e worker no provedor.

## Decisão rápida

- **Use se:** o trabalho depende do relógio; use o cron do provedor para tarefa simples e agendamento na fila quando já houver worker.
- **Evite se:** a tarefa nasce de uma ação do usuário (use job na fila) ou se a rotina não tiver lock, idempotência e alerta de falha.
