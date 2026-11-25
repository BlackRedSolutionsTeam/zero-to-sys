# Prompts, saída estruturada e validação na borda

> Escreva o prompt como uma instrução clara com exemplos, peça a resposta em JSON com esquema e valide o resultado no código antes de usar: a saída do modelo é entrada não confiável.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/build-with-claude/structured-outputs, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices, https://zod.dev |
| **Categoria** | Integração com LLM |
| **Tipo** | Prática de prompt e contrato de saída |
| **Vale para** | Extração, classificação, resumo e qualquer chamada cuja resposta o código vai ler; exemplos em TypeScript com Zod |
| **Verificado em** | 2026-11-25 |

## O que é

Três camadas:

1. **Prompt:** instruções para o modelo, separadas em papel (`system`) e tarefa (mensagem do usuário).
2. **Saída estruturada:** em vez de texto livre, o modelo devolve JSON que segue um esquema (JSON Schema). A API Messages aceita o esquema em `output_config.format` com `type: "json_schema"`, e a resposta vem como JSON válido no bloco de texto.
3. **Validação na borda:** o código confere o JSON de novo (tipos, regras de negócio) antes de salvar ou agir. Borda é o ponto onde dado externo entra no seu sistema; a resposta do LLM é dado externo.

## Por que usar

- Texto livre exige regex frágil para ler; JSON com esquema vira objeto tipado.
- O esquema vale como contrato: o modelo não inventa campos nem esquece obrigatórios.
- A validação pega o que o esquema não cobre (data no passado, médico que não existe).

## Quando usar

- Toda vez que o código, e não uma pessoa, lê a resposta.
- Extração de campos, classificação, decisões de roteamento.
- Chamadas de ferramenta, com `strict: true` na definição da ferramenta ([doc 05](05-ferramentas-e-agentes-no-produto.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Resumos e etiquetas geradas em lote |
| MVP de SaaS | ✅ Ótimo | Extração e classificação com poucas linhas |
| SaaS em crescimento | ✅ Ótimo | Contrato estável entre IA e o resto do sistema |
| Sistema interno/corporativo | ✅ Ótimo | Transforma e-mail e PDF em registros |
| API/integração | ✅ Ótimo | Normaliza entrada suja em campos conhecidos |
| App mobile com backend | ✅ Ótimo | O app recebe só JSON já validado |
| Chat aberto sem ação no sistema | 🟡 Serve | Texto livre basta; valide só o que virar ação |

## Quando é bom

- **Esquema pequeno e plano:** poucos campos, nomes claros, `enum` para valores fixos.
- **Exemplos no prompt:** dois ou três casos reais mostram o formato melhor que uma descrição longa.
- **Validação com mensagem de erro**, para reenviar o erro ao modelo e tentar de novo uma vez.

## Quando é ruim

- **Confiar cegamente no JSON:** o esquema garante formato, não verdade. Uma data válida pode estar errada.
- **Esquema grande e aninhado:** erros e latência aumentam. Divida em duas chamadas.
- **Restrições que o esquema não aceita:** a API recusa com erro 400 `minimum`, `maximum`, `minLength`, `maxLength`, `oneOf` (use `anyOf`), esquemas recursivos e `additionalProperties` diferente de `false`. Valide esses limites no código.
- **Mudar o esquema com frequência:** a primeira chamada com esquema novo é mais lenta (compilação da gramática) e trocar o formato invalida o cache de prompt.
- **Prompt como lugar de segredo ou regra de segurança:** quem controla a entrada pode tentar extrair ou contornar (doc 07).

## Como começar

**Estrutura do prompt** (regras que funcionam em qualquer modelo):

| Parte | O que pôr |
|---|---|
| Papel e contexto | Quem o modelo é e para quê (uma ou duas frases) |
| Tarefa | O que fazer, em passos curtos, dizendo o que fazer em vez do que não fazer |
| Dados | Entre etiquetas como `<mensagem>...</mensagem>`, separados das instruções |
| Exemplos | 2 a 3, cobrindo um caso difícil |
| Formato | O esquema; diga o que fazer quando faltar dado (`null`, não inventar) |

**Extração com Zod e o SDK** (Zod 3.25 ou mais novo):

```ts
import Anthropic from '@anthropic-ai/sdk'
import { zodOutputFormat } from '@anthropic-ai/sdk/helpers/zod'
import { z } from 'zod'

const Agendamento = z.object({
  paciente: z.string(),
  especialidade: z.enum(['clinica_geral', 'pediatria', 'dermatologia', 'outra']),
  data_desejada: z.string().nullable(),
  urgente: z.boolean()
})

const client = new Anthropic()

export async function extrairAgendamento(mensagem: string) {
  const resposta = await client.messages.parse({
    model: 'claude-haiku-5-5',
    max_tokens: 512,
    system: 'Extraia o pedido de agendamento. Use null quando a data não estiver na mensagem; não invente.',
    messages: [{ role: 'user', content: `<mensagem>${mensagem}</mensagem>` }],
    output_config: { format: zodOutputFormat(Agendamento) }
  })
  return resposta.parsed_output
}
```

**Validação de negócio depois do esquema:**

```ts
const dados = await extrairAgendamento(textoDoWhatsapp)

if (!dados) throw new ErroDeExtracao('sem_resposta')

if (dados.data_desejada && new Date(dados.data_desejada) < new Date()) {
  throw new ErroDeExtracao('data_no_passado')
}

if (!(await medicoExiste(dados.especialidade))) {
  throw new ErroDeExtracao('especialidade_sem_medico')
}
```

**Sem o helper do SDK:** envie o esquema em `output_config.format` e faça `JSON.parse` do texto da resposta, depois `Agendamento.safeParse`. Em Python, `client.messages.parse` com `output_format=` e Pydantic.

**Regras de operação:**

- Fixe o ID do modelo (`claude-haiku-5-5`) e versione o prompt no repositório, como código.
- Limite `max_tokens` ao tamanho esperado; resposta cortada (`stop_reason: "max_tokens"`) é JSON incompleto.
- Trate `stop_reason: "refusal"` como falha controlada, não como resposta vazia.
- Em falha de validação: tente de novo uma vez com o erro anexado; na segunda falha, devolva ao usuário um caminho manual (formulário).
- Nunca interpole a saída do modelo em SQL, HTML ou comando de shell sem tratar ([OWASP no código](../../security/docs/05-owasp-no-codigo.md)).
- Os modelos atuais pensam de forma adaptativa; para extração simples, o `effort` menor reduz custo e latência (doc 02).

## Combina com / alternativas

- [Avaliação](06-avaliacao-e-regressao-de-prompt.md): o conjunto de testes prova que o prompt e o esquema funcionam.
- [Guardrails e injeção](07-guardrails-injecao-e-lgpd.md): o texto do usuário dentro do prompt é entrada hostil.
- Validação de dados em geral: skill `coding` e skill `api`.
- Alternativas: chamada de ferramenta com `strict: true` (mesmo efeito, via ferramenta), bibliotecas como Instructor (Python), Vercel AI SDK com `generateObject`, Pydantic AI.

## Decisão rápida

- **Use se:** o código vai ler a resposta: esquema na API mais Zod ou Pydantic no código.
- **Evite se:** a resposta é só para uma pessoa ler; aí texto livre basta.
