# Migrations

> Toda mudança no banco vira um arquivo versionado no Git, aplicado em ordem, e mudanças em tabela grande são feitas em etapas para não travar o sistema.

| | |
|---|---|
| **Referência** | "Evolutionary Database Design" (Martin Fowler e Pramod Sadalage); "Refactoring Databases" (Scott Ambler e Pramod Sadalage, 2006); PostgreSQL, ALTER TABLE e CREATE INDEX CONCURRENTLY (postgresql.org/docs); documentação oficial do Prisma, Drizzle, EF Core, Alembic, Django, Laravel, golang-migrate e Flyway |
| **Categoria** | Dados |
| **Tipo** | Prática de evolução do banco |
| **Vale para** | PostgreSQL com Prisma, Drizzle, EF Core, Alembic, Django, Laravel, golang-migrate, Flyway |
| **Verificado em** | 2026-11-24 |

## O que é

Migration é um arquivo que descreve uma mudança no esquema do banco (criar tabela, adicionar coluna, criar índice). As migrations rodam em ordem e o banco guarda quais já foram aplicadas. Assim, todo ambiente (seu computador, teste, produção) chega ao mesmo esquema.

Fowler e Sadalage chamam isso de projeto evolutivo de banco: o esquema muda em passos pequenos, junto com o código.

## Por que usar

- **Reprodutível:** um banco novo se monta rodando as migrations.
- **Revisável:** a mudança aparece no PR como qualquer código.
- **Seguro:** em vez de alterar produção na mão, o mesmo arquivo roda em todo ambiente.

## Quando usar

- Em qualquer mudança de esquema, sem exceção, desde o primeiro dia.
- Ao trocar dados em massa que o código novo exige (backfill).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas mudanças; ainda vale versionar |
| MVP de SaaS | ✅ Ótimo | O esquema muda toda semana; sem migration, ambientes divergem |
| SaaS em crescimento | ✅ Ótimo | Tabelas grandes exigem expand and contract |
| Sistema interno/corporativo | ✅ Ótimo | Vários ambientes e auditoria de mudanças |
| API/integração | ✅ Ótimo | Esquema e contrato evoluem juntos |
| App mobile com backend | ✅ Ótimo | Versões antigas do app seguem usando o esquema antigo por um tempo |
| Qualquer um, editando o banco de produção na mão | ❌ Evite | Sem rastro, sem repetição, sem revisão |

## Quando é bom

- **Uma migration por mudança:** fácil de revisar e de desfazer.
- **Versionada no Git:** o histórico do esquema acompanha o do código.
- **Nunca editar migration já aplicada:** quem já rodou não roda de novo. Corrija com uma migration nova.
- **Rodar no CI/deploy antes do app novo:** o esquema novo precisa existir quando o código novo subir.
- **Reversível quando possível:** tenha o caminho de volta (`down`), mas lembre que apagar coluna não devolve os dados. Backup é a rede de segurança real.
- **Revisar o SQL gerado pelo ORM:** o gerador automático pode escolher apagar e recriar uma coluna em vez de renomear.

## Quando é ruim

- **Migration que trava tabela grande:** `alter table` com bloqueio longo para as escritas.
- **Misturar mudança de esquema e backfill pesado** na mesma transação.
- **Editar migration antiga** que já rodou em produção.
- **Confiar cegamente no autogenerate:** ele não entende a intenção (renomear vira apagar e criar).
- **Migration irreversível sem aviso:** ninguém sabe que não volta.
- **Alguns bancos e ferramentas:** nem toda ferramenta faz `down` real; veja a documentação da sua.

## Como começar

Mudança sem travar, em etapas (expand and contract: primeiro expandir o esquema, depois contrair removendo o antigo). Exemplo: adicionar `phone` obrigatório em `customer`.

```sql
alter table customer add column phone text;
```

Faça o backfill em lotes, repetindo até não atualizar nenhuma linha:

```sql
update customer
set phone = ''
where id in (
  select id from customer where phone is null limit 5000
);
```

Depois que o app novo grava sempre o telefone:

```sql
alter table customer add constraint customer_phone_not_null check (phone is not null) not valid;
alter table customer validate constraint customer_phone_not_null;
alter table customer alter column phone set not null;
alter table customer drop constraint customer_phone_not_null;
```

O `validate constraint` não bloqueia escritas. O Postgres reaproveita a constraint já validada para aplicar o `set not null` sem reler a tabela toda (consulte a doc de ALTER TABLE da sua versão).

Índice sem bloquear escrita:

```sql
create index concurrently idx_appointment_scheduled_at on appointment (scheduled_at);
```

`create index concurrently` não pode rodar dentro de transação. Configure a ferramenta para rodar essa migration sem transação.

Renomear coluna em duas etapas, sem derrubar o app que está no ar:

1. Crie a coluna nova, grave nas duas e faça backfill. Deploy do app lendo a nova.
2. Quando nada mais lê a antiga, apague-a em outra migration.

Ferramenta por stack:

| Stack | Gerar | Aplicar |
|---|---|---|
| Prisma | `prisma migrate dev --name add_phone` | `prisma migrate deploy` (CI/produção) |
| Drizzle | `drizzle-kit generate` | `drizzle-kit migrate` |
| EF Core (.NET) | `dotnet ef migrations add AddPhone` | `dotnet ef database update` |
| SQLAlchemy + Alembic | `alembic revision --autogenerate -m "add phone"` | `alembic upgrade head` |
| Django | `python manage.py makemigrations` | `python manage.py migrate` |
| Laravel | `php artisan make:migration add_phone_to_customer` | `php artisan migrate` |
| Go (golang-migrate) | `migrate create -ext sql -dir migrations add_phone` | `migrate -path migrations -database "$DATABASE_URL" up` |
| Java (Flyway) | arquivo `V2__add_phone.sql` | `flyway migrate` |

No deploy, rode o comando de aplicar como passo do pipeline, antes de subir a versão nova do app.

## Combina com / alternativas

- [01-modelagem-de-entidades.md](01-modelagem-de-entidades.md): o modelo que as migrations constroem.
- [03-chaves-e-ids.md](03-chaves-e-ids.md): trocar tipo de PK depois dá muito trabalho.
- [05-seeds-e-dados-de-teste.md](05-seeds-e-dados-de-teste.md): dados iniciais ficam separados do esquema.
- [08-indices-e-paginacao.md](08-indices-e-paginacao.md): criação de índices em tabela grande.
- Skill `infra`: backup antes de mudança destrutiva (`skills/infra/docs/11-backup-e-recuperacao.md`).
- Alternativa: SQL puro versionado (Flyway, golang-migrate) quando o ORM gera SQL que você não controla.
- Leitura: "Refactoring Databases" (Ambler e Sadalage) traz um catálogo de refatorações de esquema com a transição em etapas.

## Decisão rápida

- **Use se:** o banco tem mais de um ambiente ou mais de uma pessoa mexendo. Ou seja, quase sempre.
- **Evite se:** a ideia é alterar produção na mão, editar migration já aplicada ou rodar `alter table` pesado em horário de pico sem etapas.
