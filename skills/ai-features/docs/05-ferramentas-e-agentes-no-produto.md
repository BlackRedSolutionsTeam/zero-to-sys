# Ferramentas e agentes dentro do produto

> Dê ao modelo ferramentas pequenas e bem descritas que chamam o seu código, limite o que cada uma pode fazer e peça confirmação humana antes de qualquer ação que escreva, gaste ou apague.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview, https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner, https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls |
| **Categoria** | Integração com LLM |
| **Tipo** | Prática de uso de ferramentas (tool use) e agentes |
| **Vale para** | Assistente que consulta e age no sistema (agendar, buscar pedido, emitir segunda via); exemplos em TypeScript |
| **Verificado em** | 2026-11-25 |

## O que é

**Ferramenta (tool)** é uma função sua que o modelo pode pedir para executar. Você descreve nome, finalidade e parâmetros (JSON Schema); o modelo responde com `stop_reason: "tool_use"` e os argumentos; **seu código** executa e devolve o resultado em um bloco `tool_result`; o modelo continua. O modelo nunca executa nada sozinho.

**Agente** é esse laço repetido até a tarefa acabar. O SDK tem um *tool runner* que roda o laço por você (em beta na conferência); para aprovação humana, registro próprio ou execução condicional, escreva o laço manualmente.

Exemplo dos docs: assistente da clínica com `buscar_horarios`, `agendar_consulta` e `cancelar_consulta`.

## Por que usar

- O modelo entende o pedido em linguagem natural e o seu código continua dono das regras.
- Dá acesso a dados atuais sem pôr tudo no prompt.
- Uma ferramenta bem escrita é reaproveitada em vários fluxos.

## Quando usar

- A resposta depende de dados ou ações do sistema (agenda, pedidos, estoque).
- O número de passos varia conforme o pedido.
- **Antes de criar um agente, pergunte se um fluxo fixo basta:** uma chamada, depois código, depois outra chamada. Fluxo fixo é mais barato, rápido e fácil de testar ([doc 01](01-quando-ia-vale-a-pena.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Raramente precisa de ações |
| MVP de SaaS | ✅ Ótimo | Assistente que consulta e age em poucas ferramentas |
| SaaS em crescimento | ✅ Ótimo | Automatiza suporte e tarefas repetitivas por empresa |
| Sistema interno/corporativo | ✅ Ótimo | Consulta e rotinas por linguagem natural, com permissões do usuário |
| API/integração | 🟡 Serve | Prefira fluxos fixos; agente só se a entrada for imprevisível |
| App mobile com backend | ✅ Ótimo | O backend roda as ferramentas; o app só mostra |
| Ação irreversível sem revisão (pagar, apagar em massa) | ❌ Evite | Exija confirmação humana |

## Quando é bom

- **Ferramentas pequenas:** uma finalidade, parâmetros poucos e tipados, nome em verbo (`buscar_horarios`).
- **Descrição clara:** diga o que faz, quando usar e o formato do retorno; é o que o modelo lê.
- **`strict: true`** na definição valida nome e argumentos contra o esquema.
- **Menor privilégio:** a ferramenta roda com as permissões do usuário logado, não de um administrador.
- **Resultados enxutos:** devolva só os campos úteis; resultado grande custa token e confunde.

## Quando é ruim

- **Muitas ferramentas** (dezenas): o modelo escolhe pior e o prompt fica caro (cada ferramenta consome tokens; só a camada de uso de ferramentas já soma cerca de 286 tokens no Sonnet 5.5, conferido em 2026-11-25). Agrupe ou carregue por contexto.
- **Laço sem limite:** custo e tempo sem teto. Defina número máximo de passos, orçamento de tokens e tempo.
- **Ferramenta que escreve sem confirmar:** o modelo pode errar ou ser enganado por texto malicioso (doc 07).
- **Autorização dentro do prompt:** "só peça cancelamento do próprio paciente" no texto não protege; valide no código da ferramenta.
- **Erro engolido:** devolva o erro ao modelo em `tool_result` com `is_error: true` para ele se corrigir.

## Como começar

**Ferramenta com tool runner e Zod** (SDK TypeScript):

```ts
import Anthropic from '@anthropic-ai/sdk'
import { betaZodTool } from '@anthropic-ai/sdk/helpers/beta/zod'
import { z } from 'zod'

const client = new Anthropic()

export function ferramentasDoPaciente(pacienteId: number) {
  const buscarHorarios = betaZodTool({
    name: 'buscar_horarios',
    description: 'Lista horários livres de uma especialidade em uma data. Retorna até 10 horários no formato ISO.',
    inputSchema: z.object({
      especialidade: z.enum(['clinica_geral', 'pediatria', 'dermatologia']),
      data: z.string().describe('Data no formato AAAA-MM-DD')
    }),
    run: async ({ especialidade, data }) => {
      const horarios = await agenda.livres(especialidade, data)
      return JSON.stringify(horarios.slice(0, 10))
    }
  })

  const solicitarAgendamento = betaZodTool({
    name: 'solicitar_agendamento',
    description: 'Registra um pedido de agendamento para o paciente logado. Fica pendente até a confirmação dele na tela.',
    inputSchema: z.object({ horario: z.string() }),
    run: async ({ horario }) => {
      const pedido = await agenda.criarPendente(pacienteId, horario)
      return JSON.stringify({ pedido_id: pedido.id, status: 'pendente_de_confirmacao' })
    }
  })

  return [buscarHorarios, solicitarAgendamento]
}

export async function assistente(pacienteId: number, pergunta: string) {
  return client.beta.messages.toolRunner({
    model: 'claude-sonnet-5-5',
    max_tokens: 1024,
    max_iterations: 6,
    system: 'Você ajuda pacientes a marcar consultas. Nunca confirme um agendamento: peça que o paciente confirme na tela.',
    tools: ferramentasDoPaciente(pacienteId),
    messages: [{ role: 'user', content: pergunta }]
  })
}
```

Pontos de projeto:

- `pacienteId` vem da sessão, não do modelo: o modelo não pode escolher de quem é o agendamento.
- A ferramenta que escreve cria um pedido **pendente**; a confirmação é um botão na interface, clicado pelo usuário.
- `max_iterations` limita o laço.

**Laço manual** (quando precisa de aprovação, registro ou orçamento): chame `client.messages.create` com `tools`; enquanto `stop_reason === 'tool_use'`, execute cada bloco `tool_use`, responda com um `tool_result` (mesmo `tool_use_id`) e chame de novo. Conte tokens e passos a cada volta e pare ao passar do limite.

**Ferramentas prontas do provedor (server tools):** busca na web (US$ 10 por mil buscas, conferido em 2026-11-25), busca de página (web fetch, sem custo extra além dos tokens) e execução de código (cobrada por tempo, com horas grátis por mês). São executadas pela Anthropic; confira custo e dados que saem.

**Protocolos e SDKs de agentes:** MCP serve para conectar ferramentas externas padronizadas; o Claude Agent SDK e o Claude Managed Agents (sessão hospedada, tokens mais US$ 0,08 por hora de execução) servem para agentes longos com arquivos e shell. Para um recurso dentro de um SaaS, chamadas de API com ferramentas próprias costumam bastar.

**Segurança das ferramentas** (detalhes no [doc 07](07-guardrails-injecao-e-lgpd.md)):

| Risco | Medida |
|---|---|
| Argumento inventado ou malicioso | Valide com Zod e regra de negócio dentro da ferramenta |
| Ação em nome de outro usuário | Identidade vem da sessão, nunca dos argumentos |
| Ação destrutiva ou financeira | Pendente mais confirmação humana |
| Laço infinito | `max_iterations`, orçamento de tokens, tempo máximo |
| Conteúdo de terceiros com instruções | Devolva em `tool_result`, com a origem identificada |

## Combina com / alternativas

- [Saída estruturada](03-prompts-saida-estruturada-e-validacao.md) e [avaliação](06-avaliacao-e-regressao-de-prompt.md): avalie também a escolha da ferramenta e dos argumentos.
- Fila para tarefas longas do agente: skill `integrations` ([filas e jobs](../../integrations/docs/05-filas-e-jobs.md)).
- Permissões: skill `security` ([papéis e permissões](../../security/docs/04-papeis-e-permissoes.md)).
- Alternativas: fluxo fixo com chamadas encadeadas, Vercel AI SDK, LangGraph, Mastra, Claude Agent SDK.

## Decisão rápida

- **Use se:** o pedido depende de dados ou ações do sistema e o número de passos varia: poucas ferramentas, identidade da sessão, ação de escrita pendente de confirmação.
- **Evite se:** um fluxo fixo de duas chamadas resolve, ou a ação é irreversível e sem revisão humana.
