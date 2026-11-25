# Testes de integração com banco

> Teste rota e serviço contra um Postgres de verdade, com as migrations reais, em vez de mockar o ORM.

| | |
|---|---|
| **Referência** | Testcontainers (testcontainers.com e node.testcontainers.org, módulo `@testcontainers/postgresql`); documentação do GitHub Actions (service containers); Vitest (vitest.dev); WebApplicationFactory (Microsoft Learn, "Integration tests in ASP.NET Core"); FastAPI (TestClient); Django (test client); Laravel (HTTP tests); M. Fowler, "TestPyramid" |
| **Categoria** | Qualidade |
| **Tipo** | Prática de teste de integração |
| **Vale para** | Backends com PostgreSQL em TypeScript, .NET, Python, PHP, Go e Java |
| **Verificado em** | 2026-11-24 |

## O que é

Teste de integração junta várias peças reais: a rota, o serviço, o ORM e o banco. Em vez de simular o ORM com um mock (objeto falso que devolve respostas combinadas), você sobe um Postgres de verdade, aplica as migrations do projeto e chama o código como o sistema chama.

Assim o teste pega o que o mock esconde: SQL errado, constraint que falta, tipo de coluna diferente, filtro de empresa esquecido.

## Por que usar

- **Confiança real:** se o teste passa, a consulta funciona no Postgres.
- **Testa as constraints:** `UNIQUE`, `NOT NULL` e chave estrangeira só existem no banco; a constraint também ganha um teste que tenta violá-la.
- **Testa o isolamento multiempresa:** a empresa A não vê os dados da B ([multiempresa](../../data/docs/06-multiempresa.md)).
- **Menos mock:** o teste não quebra quando você refatora o ORM.

## Quando usar

- Regra que depende de consulta, constraint ou transação.
- Critério de aceite com "não permite", "já existe" ou "só vê os seus".

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem banco próprio ou sem regra; o build e o E2E bastam |
| MVP de SaaS | ✅ Ótimo | Poucos testes de integração cobrem os critérios e o isolamento por empresa |
| SaaS em crescimento | ✅ Ótimo | Protege migrations, constraints e o isolamento entre clientes |
| Sistema interno/corporativo | ✅ Ótimo | Regras ficam no banco e na consulta; o mock não pega erro |
| API/integração | ✅ Ótimo | A rota inteira com o banco é o que o cliente da API usa |
| App mobile | 🟡 Serve | Vale no backend dele; o app em si usa testes de componente e E2E |

## Quando é bom

- **Banco real e descartável:** cada execução começa limpa, sem depender de uma máquina.
- **Dados por factory:** cada teste cria só o que precisa.

## Quando é ruim

- **SQLite no lugar do Postgres:** tipos, constraints e funções diferem; o teste passa e produção falha.
- **Subir um banco novo por teste:** lento. Suba um por execução e isole os dados dentro dele.
- **Testar tudo por aqui:** regra pura vai em teste de unidade ([unidade](02-testes-de-unidade.md)), que é mais rápido.

## Como começar

Opções de banco, da mais portátil para a mais simples:

| Opção | Como é | Use quando |
|---|---|---|
| Testcontainers | O próprio teste sobe um Postgres em Docker e o derruba no fim | Padrão: roda igual na máquina e no CI |
| Serviço no GitHub Actions | O CI declara `services: postgres` e passa a URL por variável | CI simples, sem Docker dentro do teste |
| Banco local de teste | Um banco `app_test` no Postgres da máquina | Já tem Postgres local; cuidado para nunca apontar para o banco de desenvolvimento |

Testcontainers por linguagem: `@testcontainers/postgresql` (TypeScript), `Testcontainers.PostgreSql` (.NET), `testcontainers-python`. Os módulos têm a mesma ideia: subir o container e devolver a URL de conexão.

Exemplo em TypeScript (Vitest). Instale `npm install --save-dev @testcontainers/postgresql`. O `setup` sobe o banco uma vez por execução e aplica as migrations reais:

```ts
import { PostgreSqlContainer } from "@testcontainers/postgresql";
import { applyMigrations } from "../src/db/migrate";

export async function setup() {
  const container = await new PostgreSqlContainer("postgres:16").start();
  process.env.DATABASE_URL = container.getConnectionUri();
  await applyMigrations(process.env.DATABASE_URL);
  return async () => {
    await container.stop();
  };
}
```

Registre em `vitest.config.ts` com `test: { globalSetup: ["./test/global-setup.ts"] }`. Aqui `applyMigrations` é o comando de migration do seu projeto (Prisma, Drizzle, Flyway...).

Isolamento entre testes: limpe as tabelas antes de cada teste.

```ts
import { beforeEach } from "vitest";
import { db } from "../src/db/client";

beforeEach(async () => {
  await db.execute("TRUNCATE agendamentos, pacientes, profissionais, empresas RESTART IDENTITY CASCADE");
});
```

Estratégias de isolamento:

| Estratégia | Como | Trade-off |
|---|---|---|
| `TRUNCATE` entre testes | Esvazia as tabelas antes de cada teste | Simples; um pouco mais lento |
| Transação com rollback | Abre transação no início, desfaz no fim | Rápido; não serve se o código testado abre a própria transação |
| Banco por worker | Cada processo paralelo usa o seu banco | Permite rodar em paralelo; mais configuração |

Factories (funções que criam dados válidos com valores padrão):

```ts
export async function criarEmpresa(dados = {}) {
  return db.empresas.create({ nome: "Clínica Aurora", ...dados });
}

export async function criarPaciente(empresaId: string, dados = {}) {
  return db.pacientes.create({ empresaId, nome: "Maria Souza", ...dados });
}
```

Critério de aceite: **Dado** que a Dra. Ana tem consulta às 09:00, **quando** a recepção agenda outro paciente às 09:00, **então** o sistema recusa. Vira este teste, chamando a rota inteira em processo (`app.request` do Hono):

```ts
it("não permite agendar dois pacientes no mesmo horário", async () => {
  const empresa = await criarEmpresa();
  const ana = await criarProfissional(empresa.id, { nome: "Dra. Ana" });
  const maria = await criarPaciente(empresa.id);
  const joao = await criarPaciente(empresa.id, { nome: "João Lima" });
  const inicio = "2026-12-01T09:00:00-03:00";

  await post(empresa, "/agendamentos", { profissionalId: ana.id, pacienteId: maria.id, inicio });
  const res = await post(empresa, "/agendamentos", { profissionalId: ana.id, pacienteId: joao.id, inicio });

  expect(res.status).toBe(409);
  expect(await contar("agendamentos", empresa.id)).toBe(1);
});
```

Teste de isolamento multiempresa: a empresa B não enxerga o paciente da A.

```ts
it("não lista pacientes de outra empresa", async () => {
  const a = await criarEmpresa();
  const b = await criarEmpresa({ nome: "Clínica Horizonte" });
  await criarPaciente(a.id);

  const res = await get(b, "/pacientes");

  expect(await res.json()).toEqual({ itens: [] });
});
```

Rota HTTP inteira em processo, em cada stack:

| Stack | Ferramenta |
|---|---|
| TypeScript (Express, Fastify, Nest) | `supertest` |
| TypeScript (Hono) | `app.request()` |
| .NET | `WebApplicationFactory` com `HttpClient` |
| Python (FastAPI) | `TestClient` |
| Python (Django) | test client e `pytest-django` |
| PHP (Laravel) | HTTP tests (`$this->postJson`) |

No GitHub Actions, sem Testcontainers, declare `services: postgres` com a imagem `postgres:16`, `POSTGRES_PASSWORD` e um `--health-cmd pg_isready`, e passe a `DATABASE_URL` por `env`. Pipeline completo em [GitHub Actions](../../infra/docs/07-github-actions.md).

## Combina com / alternativas

- [Pirâmide de testes](01-piramide-de-testes.md): integração é a faixa do meio.
- [Testes de unidade](02-testes-de-unidade.md): regra pura, sem banco.
- [Testes de API e contrato](04-testes-de-api-e-contrato.md): a mesma rota, vista pelo cliente.
- [Seeds e dados de teste](../../data/docs/05-seeds-e-dados-de-teste.md) e [multiempresa](../../data/docs/06-multiempresa.md).
- [Como escrever testes legíveis](../../coding/docs/08-testes.md).

## Decisão rápida

- **Use se:** o critério depende de consulta, constraint, transação ou do isolamento entre empresas.
- **Evite se:** a regra é uma função pura (use unidade) ou o projeto não tem banco.
