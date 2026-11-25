# Streaming, filas e timeouts na interface

> Chat mostra a resposta aos poucos com streaming; tarefa longa ou em lote vai para uma fila e a tela acompanha o andamento; toda chamada tem timeout e um estado de erro claro.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/build-with-claude/streaming, https://platform.claude.com/docs/en/api/errors, https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events |
| **Categoria** | Interface e arquitetura |
| **Tipo** | Prática de resposta incremental e trabalho assíncrono |
| **Vale para** | Chat, assistentes, geração de texto longo, processamento de documentos; exemplos em TypeScript (Hono) e React |
| **Verificado em** | 2026-11-25 |

## O que é

Um LLM leva de poucos segundos a minutos para terminar uma resposta. A interface escolhe entre três formas:

| Forma | Como funciona | Serve para |
|---|---|---|
| **Streaming** | A API envia a resposta em pedaços (eventos SSE, server-sent events) e o backend repassa ao navegador | Chat e qualquer texto que a pessoa lê enquanto sai |
| **Fila e tarefa em segundo plano** | O pedido vira um job; a tela mostra "processando" e recebe o resultado depois | Documentos grandes, agentes longos, relatórios, lote |
| **Chamada simples** | Espera a resposta inteira | Extração e classificação curtas (poucos segundos, com timeout) |

## Por que usar

- O primeiro token chega em instantes: o usuário vê progresso em vez de um spinner por 20 segundos.
- Requisições HTTP longas caem em proxies e balanceadores; a fila evita isso.
- A API exige streaming (ou uso interno dele) para pedidos com `max_tokens` muito grande, para evitar timeout de HTTP; o SDK oferece `stream.finalMessage()` para receber a mensagem completa sem tratar eventos.

## Quando usar

- **Streaming:** conversa e texto longo visto pelo usuário.
- **Fila:** mais de uns 30 segundos esperados, lote, agente com muitas ferramentas, ou processamento que deve sobreviver a um refresh da página.
- **Chamada simples com timeout:** saída curta usada pelo código.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Chat público com streaming; resto pode ser gerado antes |
| MVP de SaaS | ✅ Ótimo | Streaming de chat e uma fila simples para documentos |
| SaaS em crescimento | ✅ Ótimo | Filas por empresa, retomada e notificação |
| Sistema interno/corporativo | ✅ Ótimo | Processamento de documentos em lote |
| API/integração | ✅ Ótimo | Resposta assíncrona com webhook ou consulta de status |
| App mobile com backend | ✅ Ótimo | SSE ou push; o app não espera uma conexão longa em segundo plano |
| Resposta que precisa estar completa antes de mostrar (JSON) | 🟡 Serve | Sem streaming para o usuário; use fila se demorar |

## Quando é bom

- **Percepção de velocidade:** o primeiro token costuma chegar bem antes do fim da resposta.
- **Botão de parar:** cancelar a requisição interrompe o gasto de tokens de saída que ainda não saíram.
- **Fila com repetição:** falhas do provedor viram nova tentativa, não erro na tela.

## Quando é ruim

- **Streaming de JSON de saída estruturada para o usuário:** JSON parcial não é válido. Para uso pelo código, espere o fim.
- **Proxy que guarda a resposta em buffer** (nginx, alguns CDNs): o streaming chega de uma vez. Desligue o buffer na rota (cabeçalho `X-Accel-Buffering: no` no nginx; skill `nginx`).
- **Conexão presa na função serverless** com limite de tempo curto: use fila ou plataforma com execução longa (skill `infra`).
- **Erro no meio do fluxo sem tratamento:** a API pode enviar um evento `error` (por exemplo `overloaded_error`) depois de começar a responder; a interface precisa mostrar "tente de novo" sem apagar o texto já exibido.
- **Salvar só no fim:** se a conexão cair, a resposta se perde. Salve ao terminar (e opcionalmente em partes).

## Como começar

**Backend com SSE (Hono):**

```ts
import { Hono } from 'hono'
import { streamSSE } from 'hono/streaming'
import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic()
const app = new Hono()

app.post('/chat', async (c) => {
  const { mensagens } = await c.req.json()

  return streamSSE(c, async (sse) => {
    const stream = client.messages.stream({
      model: 'claude-sonnet-5-5',
      max_tokens: 1024,
      system: 'Você é o assistente de uma clínica. Responda em português do Brasil.',
      messages: mensagens
    })

    sse.onAbort(() => stream.abort())

    stream.on('text', (texto) => {
      sse.writeSSE({ event: 'texto', data: JSON.stringify(texto) })
    })

    try {
      const final = await stream.finalMessage()
      await sse.writeSSE({ event: 'fim', data: JSON.stringify(final.usage) })
    } catch {
      await sse.writeSSE({ event: 'erro', data: 'falha_no_provedor' })
    }
  })
})
```

Antes de abrir o fluxo, valide sessão, orçamento e limite do usuário ([doc 08](08-custo-cache-limites-e-fallback.md)); depois do `fim`, registre `usage` e custo.

**Interface (React):**

```tsx
import { useState } from 'react'

export function useChat() {
  const [texto, setTexto] = useState('')
  const [estado, setEstado] = useState<'ocioso' | 'respondendo' | 'erro'>('ocioso')
  const [controle, setControle] = useState<AbortController | null>(null)

  async function enviar(mensagens: { role: string; content: string }[]) {
    const abortar = new AbortController()
    setControle(abortar)
    setTexto('')
    setEstado('respondendo')
    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagens }),
        signal: abortar.signal
      })
      if (!res.ok || !res.body) throw new Error('falha')
      const leitor = res.body.pipeThrough(new TextDecoderStream()).getReader()
      let buffer = ''
      while (true) {
        const { done, value } = await leitor.read()
        if (done) break
        buffer += value
        const eventos = buffer.split('\n\n')
        buffer = eventos.pop() ?? ''
        for (const evento of eventos) {
          const [linhaEvento, linhaDados] = evento.split('\n')
          const nome = linhaEvento.replace('event: ', '')
          const dados = linhaDados.replace('data: ', '')
          if (nome === 'texto') setTexto((anterior) => anterior + JSON.parse(dados))
          if (nome === 'erro') setEstado('erro')
        }
      }
      setEstado((atual) => (atual === 'erro' ? atual : 'ocioso'))
    } catch (erro) {
      if ((erro as Error).name !== 'AbortError') setEstado('erro')
    }
  }

  return { texto, estado, enviar, parar: () => controle?.abort() }
}
```

Para navegador, `EventSource` só aceita GET; para POST com corpo, use `fetch` como acima. Detalhes de tempo real e SSE: [tempo real e notificações](../../integrations/docs/08-tempo-real-e-notificacoes.md).

**Fila para tarefas longas:**

1. A rota cria um registro `tarefa_ia` (`pendente`) e responde `202` com o `id`.
2. Um worker consome o job, chama o modelo (com streaming interno se `max_tokens` for grande), grava o resultado e muda o estado para `concluida` ou `falhou`.
3. A tela consulta o estado a cada poucos segundos ou recebe por SSE; ao terminar, mostra o resultado ou notifica por e-mail.
4. O job é **idempotente** (mesmo `id`, mesmo resultado) e tem número máximo de tentativas. Mecânica de filas, repetição e dead letter: [filas e jobs](../../integrations/docs/05-filas-e-jobs.md).
5. Para volume sem urgência (milhares de documentos), use a Batch API: 50% de desconto e limites próprios (conferido em 2026-11-25: até 100 mil pedidos por lote); o resultado chega depois.

**Timeouts, de dentro para fora:**

| Camada | Valor inicial | Por quê |
|---|---|---|
| Chamada curta (extração, classificação) | 30 s, com 2 tentativas | Evita travar a requisição do usuário |
| Streaming | Sem prazo total; prazo para o primeiro token (10 a 15 s) e para silêncio entre eventos | A resposta pode demorar, o silêncio não |
| Proxy e balanceador | Acima do tempo de resposta mais longo, sem buffer na rota de streaming | Evita cortar a conexão no meio |
| Job na fila | 5 a 15 min por tentativa | Tarefas longas com agentes |
| Interface | Botão de parar sempre visível e mensagem após 60 s sem progresso | O usuário não fica sem saída |

**Estados da interface:** vazio, digitando, respondendo (com parar), erro com "tentar de novo", limite atingido (com o motivo e o próximo horário), IA indisponível (com alternativa manual). Acessibilidade: região `aria-live="polite"` para o texto que chega, sem anunciar cada palavra (skill `user-experience`).

## Combina com / alternativas

- [Custo e fallback](08-custo-cache-limites-e-fallback.md): erros 429 e 5xx, retry e teto de gasto.
- Infra e tempo limite de funções: skill `infra`; proxy: skill `nginx`.
- Alternativas: WebSocket (mais pesado, só se precisar de duas vias), Vercel AI SDK (`useChat` e `streamText`) para streaming pronto em React e Next.js, polling simples para tarefas curtas.

## Decisão rápida

- **Use se:** o usuário lê a resposta enquanto ela sai: SSE com botão de parar; se passa de 30 segundos, fila com estado da tarefa.
- **Evite se:** a saída é um JSON para o código: espere o fim; e nunca deixe uma chamada sem timeout.
