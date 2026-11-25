# Avaliação e regressão de prompt

> Monte um conjunto de casos com a resposta certa, rode-o a cada mudança de prompt, modelo ou esquema e bloqueie a mudança que piora a nota, como um teste automatizado qualquer.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/test-and-evaluate/develop-tests, https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| **Categoria** | Qualidade |
| **Tipo** | Prática de avaliação (evals) de recursos com LLM |
| **Vale para** | Extração, classificação, resumo, RAG e agentes; exemplos em TypeScript com Vitest |
| **Verificado em** | 2026-11-25 |

## O que é

Avaliação (eval) é um conjunto de entradas com a saída esperada mais um código que dá nota. Serve para três perguntas: o recurso funciona? A mudança piorou algo? Um modelo menor e mais barato dá conta? Testes comuns (skill `quality`) esperam resultado exato; aqui o resultado varia, então você mede uma taxa de acerto.

## Por que usar

- Sem medir, trocar uma palavra no prompt melhora um caso e quebra três sem ninguém ver.
- É a única forma segura de baixar de modelo para cortar custo ([doc 02](02-provedor-e-modelo.md)).
- Aprovar o modelo novo quando o antigo for aposentado deixa de ser aposta.

## Quando usar

- Antes de lançar qualquer recurso com LLM.
- A cada mudança de prompt, modelo, esquema, ferramenta ou parâmetro de busca do RAG.
- Depois de cada erro real em produção: o caso vira teste.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Amostra pequena para resumos e etiquetas |
| MVP de SaaS | ✅ Ótimo | 30 a 50 casos já pegam a maioria das regressões |
| SaaS em crescimento | ✅ Ótimo | Roda no CI e acompanha a qualidade por versão |
| Sistema interno/corporativo | ✅ Ótimo | Prova de qualidade para a área de negócio |
| API/integração | ✅ Ótimo | Contrato de saída verificável |
| App mobile com backend | ✅ Ótimo | Mudar o backend não exige nova versão do app |
| Recurso com ação irreversível | ✅ Ótimo | Obrigatório, incluindo casos de ataque |

## Quando é bom

- **Casos reais:** tirados de produção ou de pedidos de usuários (sem dados pessoais, ou anonimizados), espelhando a distribuição de uso.
- **Nota por código** sempre que possível: igualdade exata, campos do JSON, presença da citação correta, ferramenta escolhida.
- **Volume com sinal médio** vale mais que poucos casos perfeitos; a documentação dá exemplos de 50 a 1.000 casos.
- **Conjunto separado:** uma parte para ajustar o prompt, outra (retida) para medir de verdade.

## Quando é ruim

- **Casos só do caminho feliz:** inclua entrada vazia, texto enorme, erros de digitação, ambiguidade, gíria, outra língua e tentativas de ataque (doc 07).
- **Juiz LLM sem calibração:** o modelo que dá a nota tem viés a favor de si mesmo. Use um modelo diferente do avaliado, peça resposta restrita ("só um número", "só sim ou não"), defina cada ponto da escala e rejeite saída inesperada do juiz.
- **Rodar só na máquina de alguém:** sem CI, a avaliação é esquecida.
- **Custo ignorado:** 200 casos no Opus 5.5 a cada commit pesam; rode o conjunto pequeno no PR e o completo à noite, ou use a Batch API (50% de desconto, conferido em 2026-11-25).

## Como começar

**Formato dos casos** (`avaliacao/extracao.json`):

```json
[
  {
    "id": "whatsapp-001",
    "entrada": "Oi, queria marcar pediatria pro meu filho na sexta, é urgente",
    "esperado": { "especialidade": "pediatria", "urgente": true }
  },
  {
    "id": "whatsapp-014",
    "entrada": "bom dia",
    "esperado": { "especialidade": "outra", "urgente": false }
  }
]
```

**Rodador com nota por código:**

```ts
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { extrairAgendamento } from '../src/ia/extrair-agendamento'

const casos = JSON.parse(readFileSync('avaliacao/extracao.json', 'utf-8'))
const NOTA_MINIMA = 0.92

describe('extração de agendamento', () => {
  it(`acerta pelo menos ${NOTA_MINIMA * 100}% dos casos`, async () => {
    const resultados = await Promise.all(
      casos.map(async (caso: { id: string; entrada: string; esperado: Record<string, unknown> }) => {
        const obtido = await extrairAgendamento(caso.entrada)
        const acertou = Object.entries(caso.esperado).every(([campo, valor]) => obtido?.[campo as keyof typeof obtido] === valor)
        return { id: caso.id, acertou }
      })
    )
    const falhas = resultados.filter((r) => !r.acertou).map((r) => r.id)
    const nota = 1 - falhas.length / resultados.length
    console.log({ nota, falhas })
    expect(nota).toBeGreaterThanOrEqual(NOTA_MINIMA)
  }, 120_000)
})
```

**Regressão de prompt:**

1. Prompts ficam no repositório, versionados (arquivo `prompts/extracao.md` ou constante), nunca só num painel.
2. O pull request que muda prompt, modelo ou esquema roda a avaliação no CI ([quality gates](../../quality/docs/07-quality-gates-no-ci.md)).
3. A nota mínima fica no código; subir a nota exige revisão.
4. Guarde o resultado de cada rodada (nota, versão do prompt, ID do modelo, custo em tokens) para comparar.
5. Para RAG, meça a **recuperação** separada da **resposta**: o trecho certo está entre os 8 devolvidos? A resposta o cita?
6. Para agentes, meça a ferramenta escolhida, os argumentos e o número de passos.

**Juiz LLM** (para tom e completude, onde não há resposta exata): peça uma nota de 1 a 5 com a escala definida, em saída estruturada, usando um modelo diferente do avaliado; confira à mão uma amostra do juiz antes de confiar nele.

**Em produção:** registre amostras de entradas e saídas (sem dados pessoais), ofereça "útil / não útil" ao usuário e traga os casos ruins para o conjunto. Observabilidade geral: [skill infra](../../infra/docs/10-observabilidade.md).

## Combina com / alternativas

- [Prompts e saída estruturada](03-prompts-saida-estruturada-e-validacao.md): o esquema torna a nota por código possível.
- Pirâmide de testes e CI: skill `quality`.
- Alternativas: Promptfoo, Braintrust, LangSmith, Langfuse (código aberto) e o painel de avaliação do Console da Anthropic.

## Decisão rápida

- **Use se:** o recurso vai para produção ou o prompt vai mudar mais de uma vez: 30 a 50 casos, nota por código e CI.
- **Evite se:** a saída é só um rascunho livre que um humano sempre reescreve; aí a amostragem manual basta.
