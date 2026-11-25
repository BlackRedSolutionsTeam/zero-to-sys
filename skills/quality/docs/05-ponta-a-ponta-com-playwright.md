# Ponta a ponta com Playwright

> Teste de ponta a ponta só para os fluxos principais do produto, pelo navegador, com localizadores por papel e dados próprios em cada teste.

| | |
|---|---|
| **Referência** | Playwright (playwright.dev): Installation, Test configuration, Locators, Auto-waiting, Authentication, Best Practices, Trace viewer; Maestro (maestro.mobile.dev); Detox (wix.github.io/Detox) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de verificação |
| **Vale para** | Qualquer backend (.NET, Python, PHP, Node, Go, Java), porque o teste roda pelo navegador; mobile nativo usa Maestro ou Detox |
| **Verificado em** | 2026-11-24 |

## O que é

Teste ponta a ponta (e2e, de "end to end") abre o sistema de verdade num navegador, clica, digita e confere o que aparece. Passa por tela, API e banco juntos.

Playwright é a ferramenta da Microsoft para isso. Ela controla Chromium, Firefox e WebKit. Como só conversa com o navegador, não importa em que linguagem o backend foi escrito.

Os fluxos a testar vêm do documento de fluxos e jornadas da skill `product` (`../../product/docs/03-fluxos-e-jornadas.md`): o caminho feliz de cada jornada principal, não cada tela.

## Por que usar

- **Pega o que os outros testes não pegam:** botão escondido, rota quebrada, front e back que não se entendem.
- **Confiança para publicar:** se o fluxo que dá dinheiro passa, o resto é risco menor.

## Quando usar

- Em cada fluxo principal da jornada (ex.: paciente agenda consulta).
- Depois que a funcionalidade passou nos testes de unidade e integração.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um teste do formulário de contato e da navegação já basta |
| MVP de SaaS | ✅ Ótimo | Poucos fluxos (cadastro, uso principal, pagamento) dão muita segurança |
| SaaS em crescimento | ✅ Ótimo | Protege os fluxos que geram receita a cada deploy |
| Sistema interno/corporativo | ✅ Ótimo | Fluxos longos com vários perfis; o teste substitui o roteiro manual |
| API/integração | ❌ Evite | Sem tela, use teste de API e de contrato (`04-testes-de-api-e-contrato.md`) |
| App mobile | 🟡 Serve | Playwright cobre a versão web; para app nativo use Maestro ou Detox |

## Quando é bom

- **Poucos testes, só os fluxos principais:** cada um conta uma jornada inteira.
- **Localizadores por papel e texto:** `getByRole` e `getByLabel` quebram menos que CSS e ainda provam que a tela é acessível.
- **Dados próprios:** cada teste cria o que precisa e não depende de ordem.
- **Login uma vez:** o estado de login é salvo e reaproveitado.

## Quando é ruim

- **Testar tudo por e2e:** é lento e frágil. Regra de negócio fica na unidade, rota na integração.
- **Esperar tempo fixo (`waitForTimeout`):** deixa o teste lento e ainda instável.
- **Depender de dado deixado por outro teste:** muda a ordem e quebra.
- **Seletor CSS colado no layout:** qualquer ajuste visual quebra o teste.

## Como começar

Instalar (cria config, pasta `tests` e baixa os navegadores):

```bash
npm init playwright@latest
```

`playwright.config.ts` com servidor local, URL por variável, desktop, celular e login em um projeto de setup:

```ts
import { defineConfig, devices } from '@playwright/test';

const baseURL = process.env.BASE_URL ?? 'http://localhost:3000';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL,
    trace: 'on-first-retry',
  },
  webServer: process.env.BASE_URL
    ? undefined
    : {
        command: 'npm run start',
        url: baseURL,
        reuseExistingServer: !process.env.CI,
      },
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'desktop',
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/paciente.json' },
      dependencies: ['setup'],
    },
    {
      name: 'mobile',
      use: { ...devices['Pixel 7'], storageState: 'playwright/.auth/paciente.json' },
      dependencies: ['setup'],
    },
  ],
});
```

Login uma vez (`e2e/auth.setup.ts`). Coloque `playwright/.auth` no `.gitignore`: o arquivo guarda cookies.

```ts
import { test as setup } from '@playwright/test';

setup('login do paciente', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('E-mail').fill(process.env.E2E_EMAIL!);
  await page.getByLabel('Senha').fill(process.env.E2E_SENHA!);
  await page.getByRole('button', { name: 'Entrar' }).click();
  await page.waitForURL('/agenda');
  await page.context().storageState({ path: 'playwright/.auth/paciente.json' });
});
```

Critério de aceite virando teste. Dado um profissional com horário livre, quando o paciente escolhe o horário e confirma, então vê a consulta em "Meus agendamentos":

```ts
import { test, expect } from '@playwright/test';

test('paciente agenda consulta de ponta a ponta', async ({ page, request }) => {
  const horario = await request.post('/api/test/horarios', {
    data: { profissional: 'Dra. Ana Lima', inicio: '2026-12-10T09:00' },
  });
  const { id } = await horario.json();

  await page.goto('/agendar');
  await page.getByRole('combobox', { name: 'Profissional' }).selectOption('Dra. Ana Lima');
  await page.getByRole('button', { name: '10/12 às 09:00' }).click();
  await page.getByRole('button', { name: 'Confirmar agendamento' }).click();

  await expect(page.getByRole('status')).toHaveText('Consulta agendada');
  await page.goto('/meus-agendamentos');
  await expect(page.getByRole('listitem').filter({ hasText: 'Dra. Ana Lima' })).toBeVisible();

  await request.delete(`/api/test/horarios/${id}`);
});
```

A rota `/api/test/...` existe só em ambiente de teste e usa os seeds da skill `data` (`../../data/docs/05-seeds-e-dados-de-teste.md`).

Rodar no CI e no staging (o mesmo teste, outra URL):

```bash
npx playwright test
BASE_URL=https://staging.clinica.example npx playwright test --project=desktop
```

| Em cada stack | O que muda |
|---|---|
| TypeScript (Next, React) | `webServer` sobe `npm run start` |
| .NET, Python, PHP | `webServer` sobe `dotnet run`, `uvicorn` ou `php artisan serve`; ou use `BASE_URL` de um ambiente já no ar |
| Mobile nativo | Maestro (fluxos em YAML) ou Detox (React Native), não Playwright |

Como combater teste instável: nada de `waitForTimeout`, use `expect(...).toBeVisible()` (verificação que tenta de novo até passar), `retries` só no CI e abra o trace da falha para achar a causa.

## Combina com / alternativas

- `01-piramide-de-testes.md`: e2e é o topo, poucos testes.
- `04-testes-de-api-e-contrato.md`: o que não precisa de tela fica na API.
- `06-acessibilidade-e-desempenho-automaticos.md`: reaproveita as mesmas páginas e o mesmo Playwright.
- `07-quality-gates-no-ci.md` e a skill `infra` (`../../infra/docs/07-github-actions.md`): rodar no pipeline.
- Alternativas: Cypress, Selenium, Maestro e Detox para mobile nativo.

## Decisão rápida

- **Use se:** o sistema tem tela e há fluxos que não podem quebrar sem ninguém perceber.
- **Evite se:** o projeto é só API, ou se você quer cobrir regra de negócio com e2e (use unidade).
