# Custo, cache, limites por usuário e fallback

> Meça os tokens de cada chamada, use cache de prompt e lote onde couber, dê a cada usuário um orçamento e tenha um plano para quando a API falhar ou chegar no limite.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/build-with-claude/prompt-caching, https://platform.claude.com/docs/en/api/rate-limits, https://platform.claude.com/docs/en/api/errors |
| **Categoria** | Custo e confiabilidade |
| **Tipo** | Prática de controle de gasto e resiliência |
| **Vale para** | Qualquer produto com LLM por API; exemplos em TypeScript |
| **Verificado em** | 2026-11-25 |

## O que é

O custo de IA é variável: cresce com o uso. Este doc reúne quatro controles: **medir** (tokens por chamada), **reduzir** (cache de prompt, lote, modelo menor, saída curta), **limitar** (orçamento por usuário e por empresa) e **degradar** (fallback quando o provedor cai ou o limite estoura).

## Por que usar

- Um laço de agente ou um usuário abusivo pode gastar o mês em horas.
- Cache de prompt corta o custo da parte repetida do prompt (instruções, ferramentas, documento fixo) para uma fração.
- O provedor tem limite por minuto e teto mensal; chegar neles sem plano derruba o recurso.

## Quando usar

- Antes do lançamento: conta de custo por usuário ativo.
- Desde o primeiro dia: registro de `usage` por chamada, usuário e recurso.
- Em todo prompt com mais de 512 tokens que se repete entre chamadas.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Chat público atrai abuso; limite e teto são obrigatórios |
| MVP de SaaS | ✅ Ótimo | Margem apertada; cada centavo por usuário conta |
| SaaS em crescimento | ✅ Ótimo | Plano com franquia de IA e cobrança por excedente |
| Sistema interno/corporativo | 🟡 Serve | Volume previsível; foque em medir e em teto |
| API/integração | ✅ Ótimo | Cota por chave de API é parte do contrato |
| App mobile com backend | ✅ Ótimo | Limite no backend, nunca no app |
| Recurso gratuito aberto sem login | ❌ Evite | Sem identidade não há como limitar |

## Quando é bom

- **Cache:** leituras de cache custam uma fração da entrada normal (0,1x na maioria dos modelos; no Sonnet 5.5 e no Opus 5.5 é 0,05x; no Fable 5.2 é 0,025x, conferido em 2026-11-25).
- **Lote:** a Batch API dá 50% de desconto em entrada e saída para o que não precisa de resposta na hora (relatórios, reprocessamento, avaliação).
- **Modelo certo por tarefa:** Haiku 5.5 para classificar, Sonnet 5.5 para responder ([doc 02](02-provedor-e-modelo.md)).
- **Teto duplo:** o seu (orçamento por usuário) e o do Console (limite mensal da organização).

## Quando é ruim

- **Cache em prompt que muda toda vez:** timestamp ou ID no começo do prompt anula o cache. O que muda vai no fim.
- **Cache que não passa do mínimo:** abaixo de 512 tokens (Sonnet 5.5, Opus 5.5, Haiku 5.5, Fable 5.2) não há cache e não há erro; confira `cache_read_input_tokens`. Modelos mais antigos exigem de 1.024 a 4.096.
- **Retentar sem limite:** retry em 429 sem `retry-after` e sem teto vira tempestade.
- **Fallback silencioso e ruim:** trocar para um modelo pior sem avisar pode quebrar o esquema de saída.
- **Chave única para tudo:** sem separar ambientes e recursos, ninguém sabe quem gastou.

## Como começar

**1. Medir.** Toda resposta traz `usage`. Total de entrada = `input_tokens` + `cache_creation_input_tokens` + `cache_read_input_tokens`. Guarde por chamada:

```ts
const PRECO_POR_MILHAO = {
  'claude-haiku-5-5': { entrada: 0.1, saida: 0.5, leituraCache: 0.01 },
  'claude-sonnet-5-5': { entrada: 2, saida: 10, leituraCache: 0.1 }
}

export function custoEmDolar(modelo: keyof typeof PRECO_POR_MILHAO, usage: Anthropic.Usage) {
  const p = PRECO_POR_MILHAO[modelo]
  const leitura = usage.cache_read_input_tokens ?? 0
  const escrita = usage.cache_creation_input_tokens ?? 0
  return (
    (usage.input_tokens * p.entrada + escrita * p.entrada * 1.25 + leitura * p.leituraCache + usage.output_tokens * p.saida) /
    1_000_000
  )
}
```

(A escrita no cache de 5 minutos custa 1,25x a entrada; a de 1 hora, 2x. O Haiku 5.5 cobra preços maiores quando o prompt passa de 100 mil tokens: [doc 02](02-provedor-e-modelo.md).) Salve `usuario_id`, `empresa_id`, `recurso`, modelo, tokens e custo em uma tabela e some por mês.

**2. Cache de prompt.** Ponha o que não muda (instruções, ferramentas, documento fixo) no começo e marque `cache_control`:

```ts
const resposta = await client.messages.create({
  model: 'claude-sonnet-5-5',
  max_tokens: 1024,
  cache_control: { type: 'ephemeral' },
  system: MANUAL_DA_CLINICA,
  messages: [{ role: 'user', content: pergunta }]
})
```

Cache padrão dura 5 minutos e renova a cada leitura; `{ type: 'ephemeral', ttl: '1h' }` dura 1 hora (escrita a 2x). A escrita de 5 minutos compensa a partir da primeira leitura; a de 1 hora, a partir da segunda. A ordem é ferramentas, depois `system`, depois mensagens: mudar um nível invalida os seguintes (trocar ferramentas ou `tool_choice` invalida muito). Pode-se usar até 4 pontos de corte explícitos se o cache automático não bastar.

**3. Limites por usuário.** Contador no Redis ou no Postgres por usuário e por dia:

| Controle | Valor inicial |
|---|---|
| Mensagens por usuário | 30 por hora, 200 por dia no plano gratuito |
| Tamanho da entrada | 4.000 caracteres por mensagem |
| `max_tokens` por resposta | O menor que atende o recurso |
| Orçamento por empresa | Franquia mensal em dólar, com aviso em 80% e bloqueio em 100% |
| Passos de agente | Máximo de 6 por pedido ([doc 05](05-ferramentas-e-agentes-no-produto.md)) |
| Limite mensal no Console | Abaixo do teto do tier, para não parar o produto inteiro |

Mecânica de rate limit, `429` e `Retry-After` do **seu** sistema: [rate limit](../../security/docs/06-rate-limit.md).

**4. Erros do provedor e fallback.** O SDK refaz automaticamente algumas falhas; ajuste e trate o resto:

| Situação | Ação |
|---|---|
| `429` com `retry-after` | Esperar esse tempo, com limite de tentativas; uma fila suaviza picos |
| `429` com `error_code: "enforced_spend_limit_reached"` (sem `retry-after`) | Não retentar; recurso em modo reduzido até o dia 1; alerta para a equipe |
| `429` com `ramp_limit_exceeded` | Subir o tráfego em degraus, não de uma vez |
| `529` ou `overloaded_error`, `5xx` | Retry com espera crescente; depois fallback |
| Timeout | Fallback e mensagem clara ao usuário |
| Bloqueio por orçamento do usuário | Mensagem com o próximo reinício e opção de plano maior |

```ts
const MODELOS = ['claude-sonnet-5-5', 'claude-haiku-5-5']

export async function responderComFallback(params: Omit<Anthropic.MessageCreateParamsNonStreaming, 'model'>) {
  let ultimoErro: unknown
  for (const model of MODELOS) {
    try {
      return await client.messages.create({ ...params, model }, { timeout: 30_000, maxRetries: 2 })
    } catch (erro) {
      ultimoErro = erro
      if (erro instanceof Anthropic.APIError && erro.status && erro.status < 500 && erro.status !== 429) throw erro
    }
  }
  throw ultimoErro
}
```

Degrau final do fallback: sem IA. O recurso vira formulário, busca comum ou "fale com o atendente". O sistema precisa funcionar sem o LLM ([doc 01](01-quando-ia-vale-a-pena.md)). Teste o fallback desligando a chave em homologação.

**5. Outros ganhos:** respostas curtas (`max_tokens` e instrução de brevidade), menos resultados do RAG (8 em vez de 20), `effort` menor em tarefa simples, contagem de tokens antes de enviar entradas enormes, cache semântico de perguntas idênticas (guarde a resposta do FAQ no seu banco).

**6. Acompanhar:** painel com custo por dia, por recurso e por empresa, taxa de acerto do cache e alerta quando o gasto do dia passa de 2x a média ([observabilidade](../../infra/docs/10-observabilidade.md)). O Console também mostra uso e taxa de cache.

## Combina com / alternativas

- [Streaming e filas](09-streaming-filas-e-timeouts.md): fila para lote e picos.
- Cobrança por excedente: skill `integrations` ([pagamentos](../../integrations/docs/01-pagamentos.md)).
- Alternativas: gateways de LLM com orçamento e fallback (LiteLLM, Portkey, Cloudflare AI Gateway), contrato com desconto de volume (a Anthropic negocia para alto volume).

## Decisão rápida

- **Use se:** o recurso tem usuários reais: registro de `usage`, cache no prompt fixo, orçamento por usuário e fallback sem IA.
- **Evite se:** a ideia é lançar sem teto de gasto, com a chave direto no front-end ou sem plano para a API falhar.
