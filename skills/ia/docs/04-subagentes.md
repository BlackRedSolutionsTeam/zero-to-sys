# Subagentes

> Agente auxiliar com contexto próprio: recebe uma tarefa, trabalha separado e devolve só um resumo.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/sub-agents |
| **Categoria** | Delegação |
| **Tipo** | Arquivo `.md` com frontmatter em `.claude/agents/` ou `~/.claude/agents/`, além dos embutidos |
| **Onde vale** | Claude Code. Outras ferramentas têm recurso parecido (ver abaixo) |
| **Equivalente em outras ferramentas** | Codex: TOML em `.codex/agents/`. Cursor: Markdown em `.cursor/agents/` (também lê `.claude/agents/`). GitHub Copilot: `.github/agents/<nome>.agent.md`. Conferido em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Subagente é uma instância do modelo com janela de contexto, prompt de sistema, ferramentas e permissões próprios. O agente principal delega quando a tarefa bate com a `description` do subagente, ou você pede. Só o resumo volta para a conversa principal.

Já existem embutidos: `Explore` (leitura rápida para buscar no código), `Plan` (pesquisa no modo de planejamento) e `general-purpose` (todas as ferramentas). Para criar o seu, escreva um arquivo com `name` e `description` (obrigatórios) e, se quiser, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `isolation: worktree`, entre outros. O corpo do arquivo vira o prompt de sistema. Você chama pedindo em linguagem natural, com `@agent-nome` ou iniciando a sessão com `claude --agent nome`.

O subagente não vê a sua conversa nem os arquivos que o agente principal já leu. Ele recebe o prompt que o principal escreveu, os arquivos `CLAUDE.md` e um resumo do estado do git; `Explore` e `Plan` não recebem o `CLAUDE.md` nem o resumo do git (sub-agents, "What loads at startup"). Por padrão, subagentes podem criar subagentes até três níveis, e até 20 rodam ao mesmo tempo.

## Por que usar

- **Tira ruído do contexto:** teste completo ou busca ampla roda fora e volta resumido.
- **Paralelismo:** pesquisas independentes rodam ao mesmo tempo.
- **Revisor sem viés:** a documentação diz que um revisor novo ajuda porque não viu o seu raciocínio (best-practices, "What you can stop doing").
- **Menos poder:** um revisor com `tools: Read, Grep, Glob` não consegue editar, e isso é imposto pelo Claude Code.

## Quando usar

- Busca ampla no código (`Explore`), sem lotar a conversa.
- Revisar a mudança contra uma especificação.
- Tarefas independentes que podem andar juntas.
- Trabalho simples e barato com `model: haiku` (coletar arquivos que importam um módulo).

### Quando o agente deve propor

- **Sinais:** uma tarefa lateral despeja na conversa saída que você não vai mais consultar (gatilho da tabela "Build your setup over time", features-overview); ou a mesma delegação, como revisar contra a especificação, volta a cada feature.
- **O que fazer:** propor o arquivo com `name`, `description`, o conjunto mínimo de `tools` e o prompt que já vinha sendo usado. Com o ok, gravar em `.claude/agents/<nome>.md` (projeto) ou `~/.claude/agents/<nome>.md` (pessoal).
- **Não proponha se:** a delegação é única (use o `Explore` ou o `general-purpose` embutidos), ou o que se repete é um procedimento que precisa do contexto da conversa (isso é [skill](03-skills.md)). Um subagente por papel que se repete, não um por tarefa.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Base desconhecida | ✅ Ótimo | `Explore` mapeia sem encher o seu contexto |
| Revisão do que foi gerado | ✅ Ótimo | Contexto limpo: não é influenciado pelo raciocínio que gerou o código |
| Trabalho em paralelo | ✅ Ótimo | Partes independentes andam juntas (com `isolation: worktree` se editam) |
| Feature grande | 🟡 Serve | Para pesquisa e revisão sim; fases que dividem muito contexto (planejar, implementar, testar) ficam melhor na conversa principal |
| Investigações independentes | ✅ Ótimo | A documentação sugere vários subagentes ao mesmo tempo |
| Tarefa pequena | ❌ Evite | O subagente precisa reunir o contexto de novo e pode ser mais lento |
| Muita conversa e ajuste | ❌ Evite | A documentação manda usar a conversa principal quando há vai e vem frequente |

## Quando é bom

- **Resultado enxuto:** só o resumo entra na conversa.
- **Escopo travado por arquivo:** ferramentas e modelo definidos no frontmatter, versionados no git.
- **Modelo mais barato onde cabe:** `model: haiku` para tarefa simples.
- **Mesmo arquivo serve a times de agentes:** a definição pode ser reaproveitada em agent teams (ver [10](10-paralelismo-e-orquestracao.md)).

## Quando é ruim

- **Custa tokens:** cada subagente faz as próprias requisições e conta no mesmo uso. A documentação de boas práticas avisa isso.
- **Perde detalhe na passagem:** ele só sabe o que está no prompt de delegação, e você só recebe o resumo. O que não foi escrito no pedido não existe para ele.
- **Pode ser mais lento:** precisa reconstruir o contexto que a conversa já tinha.
- **Não melhora a resposta:** a documentação diz que entregar a mesma tarefa a um subagente não dá resposta melhor. O ganho é paralelismo e olhar novo, não inteligência extra.
- **Descrições demais:** se a soma das `description` (sem contar os embutidos) passar de 15.000 tokens, o Claude Code avisa na partida. Descrição curta, detalhe no corpo.
- **Ferramentas removidas:** subagentes não têm `AskUserQuestion` nem `EnterPlanMode`; em segundo plano perdem ainda mais ferramentas (sub-agents, "Available tools").
- **Herda o modo de permissão:** se a sessão está em `bypassPermissions`, `acceptEdits` ou `auto`, o subagente usa esse modo mesmo com `permissionMode` próprio.

## Como começar

Arquivo `.claude/agents/reviewer.md`, como no guia oficial de boas práticas:

```markdown
---
name: reviewer
description: Revisa os arquivos alterados contra a especificação. Use depois de implementar, antes do PR.
tools: Read, Grep, Glob
---
Você revisa código que não escreveu. Compare os arquivos alterados com a
especificação, confira se cada requisito foi feito e se os casos de borda
têm teste, e relate só as lacunas que afetam a correção. Ignore estilo.
```

Uso:

```text
peça ao reviewer para comparar o rate limiter com o SPEC.md
```

O "ignore estilo" importa: a documentação avisa que um revisor sempre acha algo, e corrigir tudo gera camadas e testes desnecessários.

## Combina com / alternativas

Combina com:
- [Fluxo explorar, planejar, implementar](05-fluxo-planejar-e-implementar.md): `Explore` na primeira fase.
- [Modelo e esforço](12-modelo-e-esforco.md): `model` e `effort` por subagente.
- [Paralelismo e worktrees](10-paralelismo-e-orquestracao.md): `isolation: worktree`.

Alternativas:
- Conversa principal com `/clear` entre tarefas: mais simples quando há vai e vem.
- `/btw`: pergunta rápida sobre o contexto atual sem criar histórico.
- Skill com `context: fork`: mesmo isolamento, com instruções empacotadas.

## Decisão rápida

- **Use se:** a tarefa gera muita saída, é independente de outras ou precisa de um revisor que não viu o código ser escrito.
- **Evite se:** a tarefa é pequena, exige ajustes seus a cada passo ou depende de detalhes que você não conseguiria escrever no pedido.

Fontes das recomendações: code.claude.com/docs/en/sub-agents ("Choose between subagents and main conversation"), best-practices ("Know what subagents cost", "What you can stop doing") e features-overview ("Skill vs Subagent").
