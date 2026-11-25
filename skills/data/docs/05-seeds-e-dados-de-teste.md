# Seeds e dados de teste

> Separe os dados que o sistema precisa para existir, os dados falsos para desenvolver e os dados criados por cada teste, e recrie tudo com um único comando.

| | |
|---|---|
| **Referência** | Documentação oficial: Prisma (Seeding), EF Core (Data Seeding), Django (fixtures e `loaddata`), Laravel (Database Seeding e Factories), Faker (faker.readthedocs.io), @faker-js/faker (fakerjs.dev), Testcontainers (testcontainers.com), PostgreSQL (`INSERT ... ON CONFLICT`) |
| **Categoria** | Dados |
| **Tipo** | Prática de carga inicial e de dados de teste |
| **Vale para** | PostgreSQL com Prisma, Drizzle, EF Core, SQLAlchemy, Django, Eloquent, Go e Spring |
| **Verificado em** | 2026-11-24 |

## O que é

Seed (semente) é um script que coloca dados no banco depois das migrations. Existem três tipos, e misturar os três é a causa mais comum de bagunça:

- **Seed de referência:** dados que o sistema precisa para funcionar, em qualquer ambiente. Papéis de acesso, status de agendamento, planos, estados e cidades. Vai para produção.
- **Seed de desenvolvimento:** dados falsos e realistas para ver a tela cheia: 50 pacientes, 200 consultas. Nunca vai para produção.
- **Dados de teste:** criados dentro de cada teste por factories (funções que montam uma linha válida) ou fixtures (arquivos de dados prontos). Cada teste cria o que precisa.

## Por que usar

- **Ambiente novo em minutos:** quem entra no time roda um comando e vê o sistema funcionando.
- **Telas realistas:** lista vazia esconde problema de layout e de paginação.
- **Testes independentes:** cada teste cria seus dados e não quebra o do colega.
- **Produção previsível:** status e papéis nascem iguais em todo ambiente.

## Quando usar

- Seed de referência: sempre que o código depende de uma linha fixa (papel `admin`, status `agendada`).
- Seed de desenvolvimento: assim que existir a primeira tela de listagem.
- Factories: desde o primeiro teste que precisa de dados.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas tabelas; um seed de categorias e alguns posts bastam |
| MVP de SaaS | ✅ Ótimo | Papéis, planos e uma empresa de demonstração aceleram a demo |
| SaaS em crescimento | ✅ Ótimo | Volume falso grande revela consultas lentas antes dos clientes |
| Sistema interno/corporativo | ✅ Ótimo | Tabelas de domínio (cargos, filiais) são seed de referência |
| API/integração | ✅ Ótimo | Factories deixam os testes de contrato curtos e legíveis |
| App mobile com backend | ✅ Ótimo | O app precisa de conta de teste e dados para a loja de apps revisar |
| Cópia de produção para desenvolver | ❌ Evite | Traz dado pessoal para o notebook e viola a LGPD |

## Quando é bom

- **Idempotente:** rodar duas vezes dá o mesmo resultado, sem duplicar.
- **Determinístico:** com a mesma semente do gerador, os dados falsos saem iguais.
- **Versionado:** o seed fica no Git, junto do código.
- **Separado por ambiente:** referência em todos, desenvolvimento só local.

## Quando é ruim

- **Seed de referência dentro da migration de estrutura:** dificulta mudar um valor depois.
- **Dados falsos em produção** por rodar o seed errado. Proteja o seed de desenvolvimento com checagem de ambiente.
- **Teste que depende de dado do seed:** quebra quando alguém muda o seed. Use factory.
- **Dump de produção em desenvolvimento:** vaza CPF, e-mail e telefone. Se for inevitável, anonimize antes de sair do servidor.

## Como começar

**1. Seed de referência idempotente (Postgres).** O `ON CONFLICT DO NOTHING` ignora a linha que já existe. Use `DO UPDATE` quando o valor puder mudar.

```sql
insert into appointment_statuses (code, label) values
  ('scheduled', 'Agendada'),
  ('confirmed', 'Confirmada'),
  ('done', 'Realizada'),
  ('canceled', 'Cancelada')
on conflict (code) do update set label = excluded.label;
```

A coluna `code` precisa ter índice único para o `ON CONFLICT` funcionar.

**2. Dados falsos em português do Brasil.**

```ts
import { fakerPT_BR as faker } from '@faker-js/faker'

faker.seed(42)

const patients = Array.from({ length: 50 }, () => ({
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
}))
```

```python
from faker import Faker

fake = Faker("pt_BR")
Faker.seed(42)
name = fake.name()
cpf = fake.cpf()
```

O Faker do Python tem `cpf()` e `cnpj()` no locale `pt_BR`. Os números são válidos no formato, mas fictícios.

**3. Um comando para recriar o banco local.** Coloque no `package.json`, `Makefile` ou `justfile` e documente no README.

```json
{
  "scripts": {
    "db:reset": "prisma migrate reset --force && prisma db seed"
  }
}
```

`prisma migrate reset` apaga o banco e aplica as migrations. Até o Prisma 6 ele também rodava o seed; no Prisma 7 o seed automático foi removido, então rode `prisma db seed` em seguida.

**4. Banco de teste isolado.** Duas opções:

- **Transação com rollback:** cada teste abre uma transação e desfaz no fim. É rápido, mas não serve para testar código que usa transação própria.
- **Testcontainers:** sobe um Postgres real em Docker por execução e descarta no fim. É mais lento e mais fiel. Nunca aponte teste para o banco de desenvolvimento.

**5. Como fazer seed em cada ORM**

| ORM / ferramenta | Seed de referência e de desenvolvimento | Dados de teste |
|---|---|---|
| Prisma | `prisma/seed.ts` registrado em `prisma db seed` (no Prisma 6 ou anterior, roda também no `migrate reset`) | Funções factory próprias + Faker |
| Drizzle | Script TypeScript com `insert ... onConflictDoNothing()`; pacote `drizzle-seed` para dados falsos | Funções factory próprias |
| EF Core | `HasData` no modelo (vira migration) ou `UseSeeding` / `UseAsyncSeeding` no `DbContextOptions` (EF Core 9) | Bogus (gerador de dados falsos para .NET) e Testcontainers |
| SQLAlchemy + Alembic | Script Python com `insert ... on_conflict_do_nothing` (dialeto PostgreSQL) | Fixtures do pytest + Faker ou factory_boy |
| Django ORM | Fixtures JSON e `manage.py loaddata`; ou comando próprio em `management/commands` | Fixtures do pytest-django + factory_boy |
| Eloquent (Laravel) | Classes em `database/seeders`, rodadas por `php artisan db:seed` | `Model::factory()->create()` |
| Go (sqlc / golang-migrate) | Arquivo `.sql` com `ON CONFLICT` ou programa em `cmd/seed` | Funções helper + Testcontainers for Go |
| Spring Data + Flyway | Migration repetível (`R__`) para referência; `CommandLineRunner` no perfil `dev` | Testcontainers e builders de teste |

Comando de recriação por stack:

| Stack | Comando |
|---|---|
| Prisma | `prisma migrate reset` e depois `prisma db seed` |
| EF Core | `dotnet ef database drop` e depois `dotnet ef database update` |
| Django | `manage.py flush` e depois `migrate` e `loaddata` |
| Laravel | `php artisan migrate:fresh --seed` |

Confira o `HasData`: ele exige chave primária explícita e gera migration a cada mudança, então serve só para dado fixo e pequeno.

## Combina com / alternativas

- [04-migrations.md](04-migrations.md): o seed roda depois da migration.
- [06-multiempresa.md](06-multiempresa.md): o seed de desenvolvimento cria pelo menos duas empresas.
- [10-dados-pessoais-e-lgpd.md](10-dados-pessoais-e-lgpd.md): regras para anonimizar dados reais.
- Alternativa: restaurar um dump anonimizado de produção quando o volume real importa.
- Skill `infra`: backup e recuperação (`skills/infra/docs/11-backup-e-recuperacao.md`).

## Decisão rápida

- **Use se:** o sistema tem tabelas de domínio fixas, telas de listagem ou testes que precisam de dados.
- **Evite se:** a ideia é copiar produção para desenvolver sem anonimizar, ou pôr dados falsos em produção.
