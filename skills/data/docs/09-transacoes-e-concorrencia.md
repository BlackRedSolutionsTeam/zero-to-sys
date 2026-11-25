# Transações e concorrência

> Agrupe escritas relacionadas numa transação curta e proteja os pontos em que duas pessoas disputam o mesmo dado com constraint, trava ou versão.

| | |
|---|---|
| **Referência** | PostgreSQL: Transaction Isolation, Explicit Locking e Exclusion Constraints (postgresql.org/docs/current); "Designing Data-Intensive Applications", Martin Kleppmann (2017); Transactional Outbox, Chris Richardson (microservices.io) |
| **Categoria** | Dados |
| **Tipo** | Prática de integridade e concorrência |
| **Vale para** | PostgreSQL com qualquer ORM (Prisma, Drizzle, EF Core, SQLAlchemy, Django, Eloquent, Spring Data) ou SQL puro |
| **Verificado em** | 2026-11-24 |

## O que é

**Transação** é um grupo de comandos que vale tudo ou nada: se um falha, o banco desfaz os outros (`ROLLBACK`). Se todos passam, o `COMMIT` grava tudo de uma vez.

**Concorrência** é quando várias pessoas mexem no mesmo dado ao mesmo tempo. O caso clássico: dois pacientes clicam no mesmo horário da clínica no mesmo segundo. Sem proteção, os dois conseguem.

## Por que usar

- **Sem dado pela metade:** criar pedido, itens e baixar estoque acontece junto ou não acontece.
- **Sem horário duplicado:** o banco garante, mesmo que a aplicação erre.
- **Menos bug raro:** falha de concorrência só aparece com carga, e é difícil de reproduzir.
- **Integração segura:** o outbox evita evento perdido ou evento de algo que nunca foi gravado.

## Quando usar

- Operação que mexe em mais de uma tabela (pedido + itens + estoque).
- Reservas e agendamentos: horário, mesa, quarto, vaga.
- Saldo, estoque e contadores que várias pessoas alteram.
- Todo evento que precisa avisar outro sistema depois de gravar.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Quase só leitura; o banco já cuida do básico |
| MVP de SaaS | ✅ Ótimo | Transação e unique cobrem 90% dos casos desde o dia 1 |
| SaaS em crescimento | ✅ Ótimo | Concorrência real aparece; exclusion constraint e outbox pagam o custo |
| Sistema interno/corporativo | ✅ Ótimo | Fluxos longos com várias tabelas e várias pessoas editando |
| API/integração | ✅ Ótimo | Retentativas do cliente exigem idempotência e outbox |
| App mobile com backend | ✅ Ótimo | Conexão cai no meio; o servidor não pode deixar dado pela metade |
| Transação aberta durante chamada de pagamento ou e-mail | ❌ Evite | Segura conexão e trava linhas por segundos |

## Quando é bom

- **Atomicidade:** uma falha desfaz tudo e o dado fica consistente.
- **Constraint no banco:** vale para qualquer código que escreva, inclusive scripts e outros serviços.
- **Lock otimista:** não bloqueia ninguém e detecta conflito só quando ele acontece.
- **Outbox:** o evento nasce na mesma transação do dado, então os dois existem ou nenhum existe.

## Quando é ruim

- **Transação longa:** segura locks e conexões, e trava quem espera.
- **Chamada externa dentro dela:** se o pagamento passou e o commit falhou, você cobrou sem registrar.
- **`SERIALIZABLE` em tudo:** mais erros de serialização e mais retentativas.
- **`SELECT ... FOR UPDATE` sem critério:** vira fila e pode gerar deadlock (duas transações esperando uma à outra).
- **Checar e depois inserir na aplicação:** `if (horario livre) insert` falha com duas requisições simultâneas.

## Como começar

**1. Transação curta, sem chamada externa.** Abra, escreva, feche. Pagamento e e-mail ficam fora.

```sql
BEGIN;
INSERT INTO orders (id, customer_id, total_cents) VALUES ($1, $2, $3);
INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $4, 2);
UPDATE products SET stock = stock - 2 WHERE id = $4 AND stock >= 2;
INSERT INTO outbox (id, topic, payload) VALUES ($5, 'order.created', '{"order_id": "..."}');
COMMIT;
```

Se o `UPDATE` não afetar nenhuma linha, não há estoque: faça `ROLLBACK`.

**2. Isolamento.** Define o que uma transação enxerga das outras. No Postgres:

- **Read Committed** (padrão): cada comando vê o que já foi confirmado. Serve para a maioria.
- **Repeatable Read:** a transação vê uma foto fixa do banco. Use em relatórios que fazem várias consultas e precisam de números coerentes.
- **Serializable:** o resultado é como se as transações rodassem uma por vez. Use quando a regra depende de ler vários registros e decidir, e não dá para expressar com constraint. Prepare-se para erro de serialização.

**3. Dois usuários no mesmo horário.** Três soluções, da mais simples à mais geral:

```sql
CREATE UNIQUE INDEX uq_appointments_slot ON appointments (doctor_id, starts_at) WHERE status <> 'cancelled';
```

Para faixas de horário que podem se sobrepor (consulta de 30 e de 60 minutos), use exclusion constraint. Ela precisa da extensão `btree_gist`:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE appointments ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (doctor_id WITH =, tstzrange(starts_at, ends_at) WITH &&)
  WHERE (status <> 'cancelled');
```

O segundo insert falha com erro de violação; trate e responda "horário indisponível". Terceira opção, travar a linha antes de decidir:

```sql
BEGIN;
SELECT id FROM doctors WHERE id = $1 FOR UPDATE;
COMMIT;
```

**4. Lock otimista.** Coluna `version`; o `UPDATE` só vale se a versão ainda for a que você leu.

```sql
UPDATE products SET price_cents = $1, version = version + 1 WHERE id = $2 AND version = $3;
```

Zero linhas afetadas significa que alguém mudou antes: recarregue e avise a pessoa.

| ORM | Como fazer |
|---|---|
| EF Core | `[ConcurrencyCheck]` ou `IsRowVersion()`; lança `DbUpdateConcurrencyException` |
| Prisma | `updateMany({ where: { id, version } })` e confira o `count`; trava com `$queryRaw` + `FOR UPDATE` |
| Drizzle | `update().where(and(eq(id), eq(version)))` e confira as linhas; `.for('update')` no select |
| SQLAlchemy | `version_id_col` no mapper; `with_for_update()` |
| Django | `select_for_update()` dentro de `transaction.atomic()`; `UPDATE` filtrado por versão |
| Eloquent | `lockForUpdate()` dentro de `DB::transaction()` |

**5. Outbox.** Grave o evento numa tabela `outbox` na mesma transação. Um processo separado lê as linhas pendentes, publica (fila, webhook, e-mail) e marca como enviadas. Pode enviar duas vezes, então quem recebe precisa ignorar repetidos (idempotência).

**6. Retry.** Erro de serialização (`SQLSTATE 40001`) e deadlock (`40P01`) pedem repetir a transação inteira, com limite de tentativas e pequena espera.

## Combina com / alternativas

- [03-chaves-e-ids.md](03-chaves-e-ids.md): chave de idempotência e unique.
- [06-multiempresa.md](06-multiempresa.md): inclua o id da empresa nas constraints.
- [07-auditoria-historico-soft-delete.md](07-auditoria-historico-soft-delete.md): o registro de auditoria entra na mesma transação.
- [08-indices-e-paginacao.md](08-indices-e-paginacao.md): a constraint cria índice.
- Alternativas: fila com um único consumidor (serializa por desenho) ou lock distribuído (Redis), mais frágil que constraint no banco.

## Decisão rápida

- **Use se:** a operação toca mais de uma tabela, ou duas pessoas podem disputar o mesmo recurso.
- **Evite se:** a ideia é abrir transação ao redor de chamada externa; use outbox. Evite também `SERIALIZABLE` por padrão.
