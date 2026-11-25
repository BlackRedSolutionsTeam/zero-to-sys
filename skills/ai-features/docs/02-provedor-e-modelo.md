# Escolher provedor e modelo

> Comece pela API de um provedor grande, escolha o menor modelo que passa no seu conjunto de testes e calcule o custo por uso antes de lançar.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/about-claude/models/overview, https://platform.claude.com/docs/en/about-claude/pricing, https://platform.claude.com/docs/en/api/rate-limits, https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data |
| **Categoria** | Decisão técnica |
| **Tipo** | Escolha de provedor, modelo e plano de custo |
| **Vale para** | Qualquer produto que chame um LLM por API; exemplos com a API da Anthropic (Claude) |
| **Verificado em** | 2026-11-25 |

## O que é

Você escolhe duas coisas: o **provedor** (quem hospeda o modelo e cobra) e o **modelo** (qual cérebro usar para cada tarefa). O preço é por **token** (pedaço de texto, algo como três quartos de uma palavra em inglês; em português um pouco menos), cobrado separado para entrada (o que você envia) e saída (o que o modelo escreve). A saída custa várias vezes mais que a entrada.

## Modelos Claude atuais

Conferido em 2026-11-25 em `platform.claude.com`. Preços em dólar por milhão de tokens (MTok).

| Modelo (ID da API) | Entrada | Saída | Para quê | Latência |
|---|---|---|---|---|
| `claude-haiku-5-5` | US$ 0,10 (prompt até 100 mil tokens) | US$ 0,50 | Classificação, extração, roteamento, alto volume | Mais rápida |
| `claude-sonnet-5-5` | US$ 2 | US$ 10 | Padrão da maioria dos recursos: chat, RAG, agentes simples | Rápida |
| `claude-opus-5-5` | US$ 4 | US$ 20 | Agentes longos, raciocínio mais difícil, trabalho de conhecimento | Moderada |
| `claude-fable-5-2` | US$ 8 | US$ 40 | Raciocínio mais exigente, tarefas longas; só se o Opus 5.5 não passa nos testes | Moderada |

- Todos têm janela de contexto de 1 milhão de tokens e saída máxima de 128 mil tokens, aceitam texto e imagem e têm uso de ferramentas.
- O Haiku 5.5 cobra mais quando o prompt passa de 100 mil tokens: US$ 0,50 de entrada e US$ 2,50 de saída.
- Todo ID é um instantâneo fixo: o comportamento não muda sem você trocar o ID.
- Aposentadoria prevista (compromisso da Anthropic): Haiku 5.5 e Sonnet 5.5 não antes de outubro e setembro de 2027; Opus 5.5 não antes de setembro de 2027; Fable 5.2 não antes de novembro de 2027. Ponha o ID numa variável de ambiente para trocar sem deploy.
- O tokenizador dos modelos recentes gera cerca de 30% mais tokens para o mesmo texto que o dos modelos antigos; estime custo com a contagem de tokens da API, não com tabelas antigas.

## Custo de uma conversa

Chat de clínica com 2.000 tokens de entrada (instruções, contexto e pergunta) e 500 de saída:

| Modelo | Conta | Custo por resposta |
|---|---|---|
| Haiku 5.5 | 2.000 × 0,10 + 500 × 0,50 por milhão | US$ 0,00045 |
| Sonnet 5.5 | 2.000 × 2 + 500 × 10 por milhão | US$ 0,009 |
| Opus 5.5 | 2.000 × 4 + 500 × 20 por milhão | US$ 0,018 |
| Fable 5.2 | 2.000 × 8 + 500 × 40 por milhão | US$ 0,036 |

Mil conversas por dia no Sonnet 5.5 dão cerca de US$ 9 por dia. Descontos no [doc 08](08-custo-cache-limites-e-fallback.md): cache de prompt e lote (Batch API) com 50% de desconto.

## Como escolher o modelo

1. Monte o conjunto de testes ([doc 06](06-avaliacao-e-regressao-de-prompt.md)).
2. Rode no **Haiku 5.5**. Se passa, fique nele.
3. Se não passa, suba para o **Sonnet 5.5**, depois **Opus 5.5**, e só então **Fable 5.2**.
4. Uma tarefa pode usar modelos diferentes: Haiku para classificar a intenção, Sonnet para responder.

O nível de esforço (parâmetro `effort`) também muda custo e qualidade: o padrão é `high` no Fable 5.2 e no Sonnet 5.5 e `medium` no Opus 5.5 e no Haiku 5.5. Teste o nível menor antes de subir de modelo.

## Escolher o provedor

| Opção | Quando serve | Cuidado |
|---|---|---|
| API direta da Anthropic | Padrão: recursos novos primeiro, preço de tabela | Cobrança em dólar com cartão |
| Mesmos modelos via Amazon Bedrock, Google Cloud ou Microsoft Foundry | A empresa já tem contrato, créditos ou exigência de residência de dados | Preço e limites próprios; regional pode ter acréscimo de 10% |
| Modelo aberto hospedado por você (Llama, Qwen, Mistral) | Dado que não pode sair da empresa; volume enorme e estável | Você opera GPU, atualização e segurança; quase nunca compensa no início |
| Outros provedores de API (OpenAI, Google) | Já usa no sistema; comparação com seus testes | Mantenha uma camada fina para trocar (doc 05) |

Para residência de dados na API direta existe o parâmetro `inference_geo: "us"`, com multiplicador de 1,1 sobre todos os preços. Não há processamento no Brasil: confira com o jurídico se a LGPD exige contrato ou cláusulas (doc 07).

## Limites e privacidade

- **Limites por nível (tier):** conferidos em 2026-11-25, no nível Start o Sonnet 5.5, o Opus 5.5 e o Haiku 5.5 têm 4.000 requisições por minuto, 2.000.000 de tokens de entrada por minuto e 400.000 de saída por minuto; o Fable 5.2 tem 500.000 de entrada e 100.000 de saída. Organização nova pode começar no nível Evaluation, com limites menores.
- **Teto de gasto mensal por nível:** US$ 500 (Start), US$ 1.000 (Build) e US$ 200.000 (Scale). Ao chegar no teto, a API devolve 429 sem `retry-after` até o dia 1 do mês seguinte (`enforced_spend_limit_reached`). Defina também o seu próprio limite no Console, abaixo do teto.
- **Cache de entrada não conta no limite de tokens de entrada**, o que aumenta a vazão.
- **Retenção:** a Anthropic informa apagar entradas e saídas de seus servidores em até 30 dias, com exceções (contrato de retenção zero, política de uso, lei). Conteúdo sinalizado por violação pode ser guardado por mais tempo. Dados pessoais: doc 07.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Haiku 5.5 para resumos e busca barata |
| MVP de SaaS | ✅ Ótimo | API direta, Sonnet 5.5 de padrão, Haiku 5.5 onde passar |
| SaaS em crescimento | ✅ Ótimo | Vários modelos por tarefa, cache e limites por usuário |
| Sistema interno/corporativo | ✅ Ótimo | Bedrock ou Foundry se a empresa já tem contrato |
| API/integração | ✅ Ótimo | Haiku 5.5 para normalizar entrada em alto volume |
| App mobile com backend | ✅ Ótimo | Backend chama a API; a chave nunca vai no app |
| Dado que não pode sair do país ou da empresa | ❌ Evite API pública | Modelo hospedado por você ou contrato específico |

## Quando é bom

- **API:** zero infraestrutura, pagamento por uso, modelos sempre atualizados.
- **Vários tamanhos:** troca de modelo é trocar uma string.
- **Preço previsível:** tabela pública, calculável antes do lançamento.

## Quando é ruim

- **Depender de um provedor só** sem plano de queda (doc 08, fallback).
- **Usar o maior modelo para tudo:** custo até 80 vezes maior que o Haiku 5.5 na saída, sem ganho em tarefas simples.
- **Chave de API no front-end ou no app:** qualquer pessoa extrai e gasta seu saldo. A chamada sempre sai do backend.
- **Ignorar o tier:** o limite de requisições do nível Start pode ser pequeno para um lançamento; peça aumento antes.

## Como começar

```bash
npm install @anthropic-ai/sdk
export ANTHROPIC_API_KEY=sk-ant-...
```

```ts
import Anthropic from '@anthropic-ai/sdk'

const client = new Anthropic()

const resposta = await client.messages.create({
  model: process.env.MODELO_PADRAO ?? 'claude-sonnet-5-5',
  max_tokens: 1024,
  system: 'Você é o assistente de uma clínica. Responda em português do Brasil, de forma curta.',
  messages: [{ role: 'user', content: 'Qual o horário de funcionamento?' }]
})

console.log(resposta.content, resposta.usage)
```

Guarde a chave como segredo ([segredos](../../infra/docs/09-segredos-e-configuracao.md)), uma por ambiente, e registre `usage` de cada chamada para acompanhar o custo (doc 08). SDKs e stacks: skill `stacks`. Para o tamanho do prompt antes de enviar existe o endpoint de contagem de tokens da API.

## Combina com / alternativas

- [Prompts e saída estruturada](03-prompts-saida-estruturada-e-validacao.md) e [custo e cache](08-custo-cache-limites-e-fallback.md).
- Embeddings: a Anthropic não tem modelo próprio e indica a Voyage AI; veja o [doc 04](04-rag-chunking-embeddings-pgvector.md).
- Alternativas: OpenAI, Google Gemini, modelos abertos via Ollama ou vLLM, gateways que unificam provedores.

## Decisão rápida

- **Use se:** quer começar rápido: API direta, `claude-sonnet-5-5` de padrão e `claude-haiku-5-5` para o que for simples.
- **Evite se:** a ideia é um modelo único e grande para tudo, ou chave de API fora do backend.
