# Quality gates no CI

> O que barra o PR é um conjunto de checagens automáticas, ordenadas da mais rápida à mais lenta e marcadas como obrigatórias no GitHub.

| | |
|---|---|
| **Referência** | GitHub Docs (Actions, rulesets e "Require status checks to pass before merging", docs.github.com); Playwright, "Continuous Integration" (playwright.dev/docs/ci-intro); "Continuous Delivery" (Jez Humble e David Farley); "Software Engineering at Google" (capítulo sobre testes instáveis) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de integração contínua |
| **Vale para** | GitHub Actions com Node + Postgres (exemplo); a ideia vale para qualquer stack e qualquer CI |
| **Verificado em** | 2026-11-24 |

## O que é

Quality gate (portão de qualidade) é uma checagem automática que precisa passar para o código entrar na `main`. O CI (integração contínua) roda as checagens a cada PR. O GitHub, com status checks obrigatórios, bloqueia o botão de merge enquanto alguma falhar.

## Por que usar

- **Ninguém depende de memória:** "rodei os testes" deixa de ser promessa.
- **Erro barato:** o PR vermelho custa minutos; o erro em produção custa horas.
- **Mesma régua para todos:** pessoa, agente de IA e quem tem pressa passam pelo mesmo portão.

## Quando usar

- Desde o primeiro PR, com o mínimo (lint, typecheck, teste, build).
- Cada gate novo entra quando o risco aparece: e2e quando há fluxo crítico, auditoria quando há dependências.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Lint, build e links quebrados bastam |
| MVP de SaaS | ✅ Ótimo | Poucos gates rápidos evitam quebrar o que já funciona |
| SaaS em crescimento | ✅ Ótimo | Banco limpo, e2e e auditoria protegem um produto com clientes |
| Sistema interno/corporativo | ✅ Ótimo | Exige rastro: quem aprovou e o que passou |
| API/integração | ✅ Ótimo | Teste de contrato e migrations no CI evitam quebrar consumidores |
| App mobile | 🟡 Serve | Testes de unidade no CI; e2e em dispositivo é lento e caro |
| Projeto solo sem PR, commitando direto na main | ❌ Evite | Sem PR não há onde barrar; comece pelo fluxo de PR |

## Quando é bom

- **Ordem do mais rápido ao mais lento:** formatação, lint, typecheck (segundos), testes de unidade, integração com banco, build, e2e. Quem erra o ponto e vírgula não espera o e2e.
- **Jobs em paralelo** quando não dependem um do outro; o PR demora o tempo do mais lento, não a soma.
- **Cache de dependências** (`cache: npm` no setup-node) e do Playwright quando o tempo pesar.
- **Banco limpo no CI:** o job aplica todas as migrations num Postgres novo; pega migration quebrada (veja `skills/data/docs/04-migrations.md`).
- **Cobertura mínima só onde faz sentido:** exija piso em regra de negócio crítica (cálculo, permissão), não um número global. Meta global estimula teste inútil.
- **Tempo-alvo:** feedback do PR em até 10 minutos. Passou disso, divida jobs, use cache ou mova o e2e para o merge.
- **Teste instável (flaky) vira bug:** abra card, corrija ou quarentene com prazo. Repetir até passar esconde o problema.
- **e2e no PR ou no merge:** suíte pequena de fluxos principais roda no PR; suíte grande roda após o merge na `main` e avisa se quebrar.
- **Auditoria de dependências:** `npm audit --audit-level=high --omit=dev` avisa de vulnerabilidade conhecida.

## Quando é ruim

- **Gate lento demais:** pipeline de 30 minutos faz o time juntar PRs enormes.
- **Gate que falha à toa:** instável ensina a clicar em "re-run" sem ler.
- **Auditoria bloqueando por vulnerabilidade sem correção:** bloqueie só severidade alta e tenha como registrar exceção.
- **Meta global de cobertura:** vira corrida por número.
- **Deploy no mesmo workflow dos testes sem ambiente protegido:** para deploy e ambientes, veja `../../infra/docs/07-github-actions.md`.

## Como começar

Gates que bloqueiam o PR, em ordem:

| Ordem | Gate | Comando (TypeScript) |
|---|---|---|
| 1 | Formatação | `npx prettier --check .` |
| 2 | Lint | `npm run lint` |
| 3 | Typecheck | `npx tsc --noEmit` |
| 4 | Unidade e integração | `npm test` |
| 5 | Migrations no banco limpo | `npm run db:migrate` |
| 6 | Build | `npm run build` |
| 7 | e2e dos fluxos principais | `npx playwright test` |
| 8 | Auditoria | `npm audit --audit-level=high --omit=dev` |

Arquivo `.github/workflows/ci.yml` (Node + Postgres). Confira a versão mais recente de cada action na página dela no GitHub antes de copiar:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npx prettier --check .
      - run: npm run lint
      - run: npm audit --audit-level=high --omit=dev

  typecheck:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_USER: clinica
          POSTGRES_PASSWORD: clinica
          POSTGRES_DB: clinica_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U clinica"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      DATABASE_URL: postgres://clinica:clinica@localhost:5432/clinica_test
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run db:migrate
      - run: npm test
      - run: npm run build

  e2e:
    needs: [lint, typecheck, test]
    runs-on: ubuntu-latest
    timeout-minutes: 20
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_USER: clinica
          POSTGRES_PASSWORD: clinica
          POSTGRES_DB: clinica_e2e
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U clinica"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 10
    env:
      DATABASE_URL: postgres://clinica:clinica@localhost:5432/clinica_e2e
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run db:migrate
      - run: npm run db:seed
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test
      - uses: actions/upload-artifact@v7
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 14
```

Para o e2e subir o app sozinho, use `webServer` no `playwright.config.ts` (veja `05-ponta-a-ponta-com-playwright.md`).

Marcar os gates como obrigatórios: no GitHub, em Settings, Rules, Rulesets, crie um ruleset para a `main`, ative "Require a pull request before merging" e "Require status checks to pass before merging", e adicione `lint`, `typecheck`, `test` e `e2e`. Marque "Require branches to be up to date before merging" para testar o código já combinado com a `main`. O mecanismo antigo, "branch protection rules", ainda existe; os dois podem conviver, então escolha um para não ter regra duplicada.

Em cada stack, só mudam os comandos:

| Stack | Teste | Lint e tipos | Auditoria |
|---|---|---|---|
| TypeScript | `npm test` | `eslint`, `tsc --noEmit` | `npm audit` |
| .NET | `dotnet test` | `dotnet format --verify-no-changes` | `dotnet list package --vulnerable` |
| Python | `pytest` | `ruff check`, `mypy` | `pip-audit` |
| PHP | `vendor/bin/pest` | `pint --test`, `phpstan` | `composer audit` |
| Go | `go test ./...` | `go vet`, `golangci-lint` | `govulncheck ./...` |
| Java | `./mvnw verify` | `checkstyle` | OWASP dependency-check |

## Combina com / alternativas

- `01-piramide-de-testes.md`: define quais testes existem para serem barrados.
- `03-testes-de-integracao-com-banco.md` e `05-ponta-a-ponta-com-playwright.md`: o que roda nos jobs `test` e `e2e`.
- `08-definition-of-done.md`: o gate automático é parte da definição de pronto.
- `../../infra/docs/07-github-actions.md`: deploy, ambientes e segredos.
- `../../coding/docs/09-formatacao-e-lint-automaticos.md`: configuração de lint e format.
- Alternativas ao GitHub Actions: GitLab CI, Azure Pipelines, CircleCI; a ordem dos gates é a mesma.

## Decisão rápida

- **Use se:** o código passa por PR e você quer que "pronto" seja verificável sem confiar em memória.
- **Evite se:** ainda não há testes nem lint; comece criando-os e só então os torne obrigatórios.
