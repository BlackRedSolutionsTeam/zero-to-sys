# Acessibilidade e desempenho automáticos

> Deixe o CI avisar quando uma tela fica inacessível ou lenta, e complete com teste manual o que a máquina não vê.

| | |
|---|---|
| **Referência** | Playwright, "Accessibility testing" (playwright.dev); @axe-core/playwright e axe-core (Deque); Lighthouse CI (googlechrome.github.io/lighthouse-ci); web.dev, "Web Vitals"; WCAG 2.x (W3C) |
| **Categoria** | Qualidade |
| **Tipo** | Prática de verificação automática |
| **Vale para** | Qualquer sistema com tela web, em qualquer backend, porque o teste roda no navegador |
| **Verificado em** | 2026-11-24 |

## O que é

Duas verificações que rodam sozinhas no CI:

- **Acessibilidade:** o axe-core procura problemas conhecidos de WCAG (diretrizes de acessibilidade web do W3C), como imagem sem texto alternativo e contraste baixo. O pacote `@axe-core/playwright` o liga aos testes do Playwright.
- **Desempenho:** o Lighthouse mede a página e dá notas e métricas. O Lighthouse CI (`@lhci/cli`) roda o Lighthouse várias vezes e falha o build se passar do limite.

Core Web Vitals são as três métricas de experiência do Google. Os limites "bom" do web.dev, medidos no percentil 75 dos acessos:

| Métrica | O que mede | Bom |
|---|---|---|
| LCP (Largest Contentful Paint) | Quando o maior conteúdo aparece | 2,5 s ou menos |
| INP (Interaction to Next Paint) | Quanto a página demora a responder a cliques e teclas | 200 ms ou menos |
| CLS (Cumulative Layout Shift) | Quanto o layout pula durante o carregamento | 0,1 ou menos |

## Por que usar

- **Barato:** um teste de poucas linhas por tela.
- **Pega regressão cedo:** um botão sem nome acessível não chega a produção.
- **Número no lugar de opinião:** "a página ficou lenta" vira métrica com limite.

## Quando usar

- Em toda tela principal, junto do teste e2e.
- Em tela nova, antes do PR.
- Para desempenho, nas páginas de entrada (home, login, agendamento).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Páginas públicas, sem login: Lighthouse CI funciona direto e a busca depende de desempenho |
| MVP de SaaS | ✅ Ótimo | Axe nas telas principais custa pouco |
| SaaS em crescimento | ✅ Ótimo | Evita que acessibilidade e velocidade piorem a cada release |
| Sistema interno/corporativo | 🟡 Serve | Axe vale muito; Lighthouse dá mais trabalho atrás de login |
| API/integração | ❌ Evite | Não há tela para medir |
| App mobile | 🟡 Serve | Vale para a versão web; app nativo tem ferramentas próprias das plataformas |

## Quando é bom

- **Axe em estados diferentes:** tela vazia, com erro, com modal aberto.
- **Falha o build:** `violations` precisa ser lista vazia.
- **Limites realistas:** comece com `warn`, suba para `error` quando estabilizar.
- **Várias execuções:** o resultado varia, então use a mediana.

## Quando é ruim

- **Achar que automático basta:** a doc do Playwright diz que o teste automático não detecta todos os tipos de violação de WCAG, e não dá percentual. Não existe número oficial para citar.
- **O que a máquina não pega:** ordem do foco com teclado, se o leitor de tela anuncia algo que faz sentido, texto de link claro, uso real por quem tem deficiência. Faça teste manual com Tab, Enter, Esc e um leitor de tela (VoiceOver, NVDA).
- **Página atrás de login:** o Lighthouse CI abre a página sem sessão e mede a tela de login. É preciso configurar cookies ou script de login.
- **Resultado instável no CI:** máquina compartilhada muda os números; uma execução só engana.
- **Nota como meta:** nota 100 não garante boa experiência para quem usa.

## Como começar

Instalar:

```bash
npm install -D @axe-core/playwright @lhci/cli
```

Teste axe na tela de agendamento. Critério: a tela de agendamento não tem violações de WCAG A e AA detectáveis, nem com o modal de confirmação aberto.

```ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('acessibilidade da tela de agendamento', () => {
  test('sem violações ao abrir a tela', async ({ page }) => {
    await page.goto('/agendar');
    await expect(page.getByRole('heading', { name: 'Agendar consulta' })).toBeVisible();

    const resultado = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(resultado.violations).toEqual([]);
  });

  test('sem violações com o modal de confirmação aberto', async ({ page }) => {
    await page.goto('/agendar');
    await page.getByRole('button', { name: '10/12 às 09:00' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();

    const resultado = await new AxeBuilder({ page })
      .include('[role="dialog"]')
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(resultado.violations).toEqual([]);
  });
});
```

Lighthouse CI (`lighthouserc.js`) com 5 execuções, mediana e limites:

```js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/agendar'],
      numberOfRuns: 5,
      startServerCommand: 'npm run start',
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9, aggregationMethod: 'median' }],
        'categories:accessibility': ['error', { minScore: 0.95, aggregationMethod: 'median' }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500, aggregationMethod: 'median' }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1, aggregationMethod: 'median' }],
      },
    },
    upload: { target: 'temporary-public-storage' },
  },
};
```

Rodar:

```bash
npx lhci autorun
```

O Lighthouse mede em laboratório e não mede INP (a métrica de interação precisa de uso real); no lugar, ele tem o Total Blocking Time como aproximação. Para INP de verdade, use dados de campo.

Para limite de tamanho de arquivos, o LHCI aceita `budgetsFile` apontando para um `budgets.json`, mas ele não pode ser usado junto de `assertions` no mesmo `assert`.

| Em cada stack | O que muda |
|---|---|
| TypeScript, .NET, Python, PHP | Nada nos testes; só o comando que sobe o servidor (`startServerCommand` ou `webServer`) |
| Página atrás de login | Axe: use o `storageState` do doc 05. Lighthouse CI: configure login por script |

## Combina com / alternativas

- `05-ponta-a-ponta-com-playwright.md`: o axe roda dentro dos mesmos testes.
- `07-quality-gates-no-ci.md`: decide se a falha bloqueia o PR.
- Desempenho e rede: `../../user-experience/docs/12-desempenho-e-rede.md`.
- Contraste, foco e tamanho de toque desde o desenho: skill `design-systems` (`../../design-systems/SKILL.md`).
- Alternativas: Pa11y, Accessibility Insights, WebPageTest, PageSpeed Insights (dados de campo).

## Decisão rápida

- **Use se:** o sistema tem telas e você quer barrar regressões simples de acessibilidade e velocidade.
- **Evite se:** a ideia é trocar teste manual de teclado e leitor de tela por ele, ou medir uma tela com login sem configurar a sessão.
