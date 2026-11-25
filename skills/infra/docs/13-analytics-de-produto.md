# Analytics de produto (PostHog, Plausible, Umami e Matomo)

> Medir como as pessoas usam o sistema (quantos agendam, onde desistem, quantas voltam), sem enviar dado pessoal e, se possível, sem cookie.

| | |
|---|---|
| **Site** | https://posthog.com, https://plausible.io, https://umami.is, https://matomo.org, https://marketingplatform.google.com/about/analytics |
| **Categoria** | Operação |
| **Tipo** | Plataformas de analytics de produto e de site (serviço ou autohospedado) |
| **Stack** | Todas têm script para o navegador; PostHog, Matomo e Plausible também aceitam eventos enviados pelo servidor (SDK ou API) |
| **Preço** | PostHog Cloud: grátis até 1 milhão de eventos de analytics por mês, sem cartão (posthog.com/pricing, conferido em 2026-11-24). Umami Cloud: Hobby grátis (100 mil eventos/mês, 1 site, 6 meses de retenção), Pro US$ 20/mês com 1 milhão de eventos (umami.is/pricing, conferido em 2026-11-24). Matomo Cloud: teste de 21 dias. Plausible Cloud é pago: plano Starter a partir de US$ 9/mês (até 10 mil pageviews), com teste de 30 dias sem cartão e sem plano grátis (plausible.io, conferido em 2026-11-24) |
| **Licença** | PostHog: MIT, exceto a pasta `ee/`, que tem licença própria. Plausible CE: AGPLv3 (o script do navegador é MIT). Umami: MIT. Matomo: GPLv3 ou posterior. Google Analytics: serviço proprietário (arquivos LICENSE e READMEs no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Analytics de produto responde "o que as pessoas fazem no sistema?". Cada ação importante vira um **evento** (por exemplo `agendamento_criado`). Com os eventos você monta:

- **Funil:** passos em sequência e quanto cai em cada um (escolheu profissional, escolheu horário, confirmou).
- **Retenção:** quantas pessoas voltam na semana seguinte.
- **Uso por funcionalidade:** o que ninguém abre.

Não é [observabilidade](10-observabilidade.md): ela mostra se o sistema está quebrado; analytics mostra se o produto está sendo usado.

## Por que usar

- **Decidir com dado:** a pergunta "vale construir isso?" ganha resposta.
- **Provar que a meta do MVP foi atingida:** o escopo diz o que precisa acontecer; o evento mostra se aconteceu.
- **Achar o gargalo:** o funil mostra o passo em que a clínica ou o paciente desiste.
- **Cortar o que não é usado,** em vez de manter para sempre.

## Quando usar

- Já no MVP, com poucos eventos ligados às metas do [escopo](../../product/docs/02-escopo-do-mvp.md).
- Antes de mudar uma tela importante, para comparar antes e depois.
- Quando a pergunta do time é "isso funciona?" e ninguém sabe responder.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Plausible ou Umami, sem cookie, mostram visitas e origem |
| MVP de SaaS | ✅ Ótimo | PostHog grátis cobre eventos e funil; poucos eventos bastam |
| SaaS em crescimento | ✅ Ótimo | Funil, retenção e experimentos com os mesmos dados |
| Sistema interno/corporativo | 🟡 Serve | Útil para ver o que a equipe usa; o público é pequeno e conhecido |
| API/integração | 🟡 Serve | Meça uso por cliente no servidor; o navegador não existe |
| App mobile | ✅ Ótimo | PostHog tem SDKs móveis; evento no app mostra o uso real |
| Sistema com dado de saúde | ❌ Evite enviar o dado | Meça a ação, nunca o conteúdo: sem nome, CPF ou motivo da consulta |

## Quando é bom

- **Pouco esforço:** um script ou um SDK e uma função `track`.
- **Sem cookie:** Plausible e Umami se descrevem como sem cookies e sem dado pessoal, o que evita banner de consentimento.
- **Autohospedável:** todas as quatro opções abertas rodam no seu servidor, e os dados ficam com você.
- **Funil e retenção prontos** no PostHog, sem montar consulta SQL.

## Quando é ruim

- **Evento demais:** 200 eventos sem nome claro viram ruído. Comece com 5 a 10.
- **Dado pessoal no evento:** enviar nome, e-mail ou motivo da consulta a um terceiro cria risco jurídico (veja [LGPD](../../security/docs/09-lgpd-na-pratica.md)).
- **Bloqueadores de anúncio** derrubam parte dos eventos do navegador; o evento no servidor não sofre isso.
- **Google Analytics** usa cookies e manda dados a um terceiro; para decidir se pede consentimento, siga o guia da ANPD sobre cookies e a [LGPD](../../security/docs/09-lgpd-na-pratica.md). Não confirmei regra específica do GA4.
- **Autohospedar custa operação:** servidor, atualização e backup são seus.
- **Retenção no plano grátis é limitada** (6 meses no Umami Hobby).

## Como começar

1. Escreva as perguntas do produto (ex.: "quantos pacientes concluem o agendamento?").
2. Para cada pergunta, escolha o evento. Nome padronizado `objeto_ação`, em minúsculas, no passado:

| Evento | Quando dispara | Propriedades permitidas |
|---|---|---|
| `agendamento_criado` | servidor, após gravar no banco | `origem`, `profissional_id`, `antecedencia_dias` |
| `agendamento_cancelado` | servidor, após cancelar | `quem_cancelou` (paciente ou clínica), `antecedencia_horas` |
| `horario_escolhido` | navegador, ao clicar | `profissional_id` |
| `cadastro_concluido` | servidor | `plano` |

3. Centralize o envio em um arquivo. Exemplo no servidor com PostHog (TypeScript):

```ts
import { PostHog } from "posthog-node";

const client = new PostHog(process.env.POSTHOG_KEY!, {
  host: process.env.POSTHOG_HOST,
});

type Evento = "agendamento_criado" | "agendamento_cancelado" | "cadastro_concluido";

export function registrarEvento(
  empresaId: string,
  evento: Evento,
  propriedades: Record<string, string | number | boolean>,
) {
  client.capture({ distinctId: empresaId, event: evento, properties: propriedades });
}
```

4. No navegador, sem cookie nem armazenamento persistente:

```ts
import posthog from "posthog-js";

posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
  api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST,
  persistence: "memory",
});
```

**Servidor ou navegador?** Evento de resultado (agendamento gravado) vai pelo servidor: é exato e bloqueador não derruba. Evento de interação (clicou, abriu a tela) vai pelo navegador.

**Regras fixas:** identifique por id interno (UUID da empresa ou do usuário), nunca por nome, e-mail, CPF ou telefone. Nada de campo livre digitado pelo paciente nem motivo da consulta. Se usar cookie ou identificador persistente, peça consentimento antes de disparar.

Em cada stack: Node usa `posthog-node`; no Python, .NET, Go, PHP e Ruby existem SDKs de servidor do PostHog ou a API HTTP de captura (confira em posthog.com/docs); Plausible e Umami têm API de eventos por HTTP.

## Combina com / alternativas

- [Observabilidade](10-observabilidade.md): erro e lentidão ficam lá; uso fica aqui.
- [Feature flags e rollback](14-feature-flags-e-rollback.md): o PostHog junta flags e analytics, e mede o efeito de cada liberação.
- [Segredos e configuração](09-segredos-e-configuracao.md): a chave do projeto vai em variável de ambiente.
- [Escopo do MVP](../../product/docs/02-escopo-do-mvp.md): cada meta vira um evento.
- [LGPD na prática](../../security/docs/09-lgpd-na-pratica.md): consentimento, base legal e dado de saúde.
- Alternativas: Matomo (completo, GPLv3, mais pesado de hospedar), Google Analytics (gratuito, com cookies e terceiro).

## Decisão rápida

- **Use se:** precisa saber se o produto é usado. Para site, Plausible ou Umami sem cookie; para SaaS, PostHog com eventos `objeto_ação` enviados do servidor e id interno no lugar de dado pessoal.
- **Evite se:** a ideia é mandar nome, CPF ou dado de saúde ao analytics, ou rastrear tudo sem uma pergunta definida.
