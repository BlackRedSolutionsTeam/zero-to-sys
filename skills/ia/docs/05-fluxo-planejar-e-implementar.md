# Fluxo: explorar, planejar, implementar, verificar

> Separar entender, decidir e escrever em etapas, usando o modo de planejamento e uma especificação escrita, para não construir a coisa errada.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/permission-modes (modo de planejamento) e https://code.claude.com/docs/en/best-practices |
| **Categoria** | Método de trabalho |
| **Tipo** | Prática com apoio de recursos do Claude Code (`/plan`, `Shift+Tab`, `SPEC.md`) |
| **Onde vale** | Qualquer agente de código. Os atalhos citados são do Claude Code |
| **Equivalente em outras ferramentas** | Outras ferramentas têm modos de plano ou "ask"; o Cursor tem Plan Mode (conferido em 2026-11-24); o Cursor tem modo Ask, somente leitura, que responde sobre o código sem alterar arquivos (cursor.com/help/ai-features/ask-mode); Codex tem `/plan` (developers.openai.com/codex/cli/slash-commands); os demais não foram conferidos |
| **Verificado em** | 2026-11-24 |

## O que é

O fluxo tem quatro etapas: explorar (ler o código sem mexer), planejar (escrever o que vai mudar), implementar e verificar (rodar algo que dê passou ou falhou).

No Claude Code, o modo de planejamento (`plan`) deixa o agente ler arquivos, rodar comandos de leitura e escrever um plano, sem editar o código até você aprovar. Para entrar: `Shift+Tab` até o modo plan, prefixar um pedido com `/plan` ou iniciar com `claude --permission-mode plan`. Ao final, você escolhe aprovar com modo auto, aprovar revisando as edições, ou continuar planejando. `Ctrl+G` abre o plano no seu editor para você ajustar antes de seguir.

Para o que você ainda não definiu, a documentação sugere pedir uma entrevista: "me entreviste até conseguir escrever a especificação e grave em SPEC.md". Depois, abra uma sessão nova para construir a partir do arquivo.

## Por que usar

- **Revisão antes da edição:** no modo plan o Claude só lê e propõe; as edições ficam bloqueadas até você aprovar o plano.
- **Contexto limpo:** a sessão de construção começa só com a especificação, sem o caminho de ideias descartadas.
- **Escopo:** a documentação diz que o Claude tende a ler o pedido de forma conservadora; peça "seja ambicioso" quando quiser a versão completa.
- **Critério de pronto:** a documentação chama o `SPEC.md` de "written definition of done" e o usa como alvo do revisor.

## Quando usar

- Explorar uma base antes de mudá-la (permission-modes, tabela de modos: "Exploring a codebase before changing it").
- Mudança que você quer revisar antes de ela tocar o disco (common-workflows, "Plan before editing").
- Quando o pedido ainda está vago: use a entrevista (best-practices).

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Base desconhecida | ✅ Ótimo | O modo plan é indicado para explorar antes de mudar (permission-modes) |
| Pedido ainda vago | ✅ Ótimo | A entrevista gera o `SPEC.md` (best-practices) |
| Mudança que você quer revisar antes de editar | ✅ Ótimo | Claude propõe e não edita até você aprovar (common-workflows) |

## Quando é bom

- **Editável:** `Ctrl+G` abre o plano no seu editor antes de o Claude prosseguir (permission-modes).
- **Sobrevive à compactação:** a documentação diz que o plano escrito no modo de planejamento é reinjetado do disco depois de compactar.
- **Aproveita modelos diferentes:** o alias `opusplan` usa Opus para planejar e Sonnet para executar (ver [12](12-modelo-e-esforco.md)).
- **Combina com `/rewind`:** dá para tentar a abordagem ousada e voltar atrás.

## Quando é ruim

- **Aprovar muda o modo:** ao aprovar, a sessão sai do plan mode e começa a editar no modo que a opção escolhida descreve (auto, auto-accept edits ou revisão manual).
- **Rodar comandos no plano:** no modo plan, comandos fora do conjunto de leitura pedem aprovação (ou passam pelo classificador, se o modo auto está disponível). Leia o que está sendo aprovado.

## Como começar

```text
# 1. Explorar e planejar (Shift+Tab até plan, ou /plan antes do pedido)
/plan adicionar limite de requisições na API pública. Leia src/api/ e me diga
como os middlewares estão ligados antes de propor.

# 2. Se o pedido está vago, peça a entrevista
Quero limitar requisições na API pública, mas não pensei direito. Me entreviste
até conseguir escrever a especificação e grave em SPEC.md.

# 3. Sessão nova para implementar
/clear
implemente o SPEC.md. Rode pnpm vitest run src/api e pnpm tsc --noEmit até passar.

# 4. Verificar com outro olhar
use um subagente para revisar a mudança contra o SPEC.md; relate só lacunas de correção
```

## Combina com / alternativas

Combina com:
- [Subagentes](04-subagentes.md): `Explore` na exploração e revisor no fim.
- [Prompt e verificação](11-prompt-e-verificacao.md): a etapa 4 depende de um check que dê passou ou falhou.
- [Gestão de contexto](06-gestao-de-contexto.md): `/clear` entre planejar e implementar.

Alternativas:
- Pedir direto, sem o modo plan: é o padrão do Claude Code; o plan mode é opcional (`Shift+Tab` ou `/plan`).
- `/loop` ou `/goal` para trabalho longo depois do plano (ver [11](11-prompt-e-verificacao.md)).

## Decisão rápida

- **Use se:** você quer explorar antes de mudar, revisar o plano antes das edições ou ainda precisa definir o pedido.
- **Evite se:** nenhum desses motivos se aplica; a documentação não pede plano para toda tarefa.

Fontes das recomendações: code.claude.com/docs/en/permission-modes ("Analyze before you edit with plan mode"), common-workflows ("Plan before editing") e best-practices (entrevista e `SPEC.md`).
