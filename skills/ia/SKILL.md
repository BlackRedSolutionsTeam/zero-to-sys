---
name: ia
description: 'Orienta o trabalho com agentes de IA de código: CLAUDE.md e AGENTS.md, memória, skills, subagentes, modo de planejamento, contexto, MCP, hooks, permissões, worktrees, modelo e esforço. Use ao configurar um projeto para IA ou quando perguntarem "como configuro o Claude Code".'
---

# ia

Guia de decisão para usar agentes de IA de código da melhor forma, com foco no Claude Code. Cada recurso tem um documento em `docs/` com quando usar, como se encaixa em cada tipo de tarefa, pontos fortes, limitações, comandos e decisão rápida.

## Como usar esta skill

1. **Descubra a situação** antes de recomendar qualquer recurso: tamanho da tarefa (pequena, feature grande, bug difícil, base desconhecida, tarefa repetitiva, trabalho em paralelo), se alguém acompanha a execução e o que o projeto já tem (`CLAUDE.md`, `AGENTS.md`, `.claude/`, `.mcp.json`, hooks). O que já está configurado tem prioridade sobre esta lista.
2. **Escolha os recursos pela tabela abaixo.** Comece pelo mais simples: a documentação manda ir adicionando extensões conforme os gatilhos aparecem (features-overview, "Build your setup over time").
3. **Leia o documento de cada recurso escolhido** em `docs/` antes de configurar. Confira principalmente "Encaixe por tipo de tarefa", "Quando é ruim" e "Como começar".
4. **Aplique pelos comandos de "Como começar"** do documento. Confira na documentação oficial (code.claude.com/docs) se o Claude Code instalado for de outra versão.
5. **Aplique as regras de uso** desta skill.
6. **Ao fim da tarefa, veja se apareceu algum sinal de "Quando criar cada recurso"** e, se sim, proponha a criação.
7. **Explique a escolha ao usuário em uma ou duas frases**: qual recurso e por que, para aquela situação.

## Qual usar

| Situação | Comece por | Acrescente se precisar |
|---|---|---|
| Tarefa que você já sabe descrever | Pedido específico com comando de teste ([11](docs/11-prompt-e-verificacao.md)) | Modo de planejamento só se quiser revisar antes de editar ([05](docs/05-fluxo-planejar-e-implementar.md)) |
| Feature grande | Modo de planejamento e `SPEC.md` ([05](docs/05-fluxo-planejar-e-implementar.md)), sessão nova para implementar | Subagente revisor ([04](docs/04-subagentes.md)), hook `Stop` com o typecheck ([08](docs/08-hooks.md)) |
| Bug difícil | Teste que reproduz a falha, depois a correção ([11](docs/11-prompt-e-verificacao.md)); esforço maior ([12](docs/12-modelo-e-esforco.md)) | `/rewind` para descartar beco sem saída ([06](docs/06-gestao-de-contexto.md)); hipóteses em paralelo ([10](docs/10-paralelismo-e-orquestracao.md)) |
| Base desconhecida | Modo de planejamento e subagente `Explore` ([05](docs/05-fluxo-planejar-e-implementar.md), [04](docs/04-subagentes.md)) | `/init` e `CLAUDE.md` enxuto ([01](docs/01-claude-md-agents-md.md)) |
| Tarefa repetitiva | Skill ([03](docs/03-skills.md)) | Hook para o passo fixo ([08](docs/08-hooks.md)); `claude -p` em script ([11](docs/11-prompt-e-verificacao.md)) |
| Trabalho em paralelo | Worktrees ([10](docs/10-paralelismo-e-orquestracao.md)) | `/batch` para mudança mecânica; agent teams (experimental), começando por pesquisa e revisão |
| Rodar sem supervisão | Permissões, sandbox e limite de turnos ([09](docs/09-permissoes-e-seguranca.md)) | `/goal` ou hook `Stop` ([11](docs/11-prompt-e-verificacao.md)); PR aprovado por pessoa |
| Precisa de dado de outro sistema (card, erro, design) | CLI do serviço, se existir | Servidor MCP ([07](docs/07-mcp.md)) |
| O agente repete o mesmo erro | Linha no `CLAUDE.md` ([01](docs/01-claude-md-agents-md.md)) | Regra sem exceção vira hook ([08](docs/08-hooks.md)) |
| Sessão lenta ou cara | `/clear`, `/compact` com foco, `/usage` ([06](docs/06-gestao-de-contexto.md)) | Modelo e esforço ([12](docs/12-modelo-e-esforco.md)) |
| Lembrar preferências entre sessões | Memória automática ([02](docs/02-memoria-automatica.md)) | `CLAUDE.md` para o que é do time |

| Recurso | Documento | Papel |
|---|---|---|
| CLAUDE.md e AGENTS.md | [docs/01-claude-md-agents-md.md](docs/01-claude-md-agents-md.md) | Instruções persistentes do projeto |
| Memória automática | [docs/02-memoria-automatica.md](docs/02-memoria-automatica.md) | Notas que o agente guarda entre sessões |
| Skills | [docs/03-skills.md](docs/03-skills.md) | Procedimentos reutilizáveis carregados sob demanda |
| Subagentes | [docs/04-subagentes.md](docs/04-subagentes.md) | Delegação com contexto próprio |
| Fluxo planejar e implementar | [docs/05-fluxo-planejar-e-implementar.md](docs/05-fluxo-planejar-e-implementar.md) | Explorar, planejar, implementar, verificar |
| Gestão de contexto | [docs/06-gestao-de-contexto.md](docs/06-gestao-de-contexto.md) | `/clear`, `/compact`, `/rewind`, `/context` |
| MCP | [docs/07-mcp.md](docs/07-mcp.md) | Ligação com sistemas externos |
| Hooks | [docs/08-hooks.md](docs/08-hooks.md) | Regras e passos impostos pelo Claude Code |
| Permissões e segurança | [docs/09-permissoes-e-seguranca.md](docs/09-permissoes-e-seguranca.md) | Modos, regras, sandbox, injeção de prompt |
| Paralelismo e orquestração | [docs/10-paralelismo-e-orquestracao.md](docs/10-paralelismo-e-orquestracao.md) | Worktrees, `/batch`, agent teams |
| Prompt e verificação | [docs/11-prompt-e-verificacao.md](docs/11-prompt-e-verificacao.md) | Pedido específico, check de passou ou falhou, revisão |
| Modelo e esforço | [docs/12-modelo-e-esforco.md](docs/12-modelo-e-esforco.md) | Escolha de modelo e `/effort` por tarefa |

## Quando criar cada recurso

A tabela acima diz o que usar. Esta diz quando o agente deve, por conta própria, propor a criação de um recurso para o projeto. Fique atento a estes sinais durante o trabalho e proponha ao fim da tarefa, não no meio dela.

| Sinal durante o trabalho | O que criar | Onde gravar |
|---|---|---|
| O usuário corrigiu a mesma coisa duas vezes, ou o agente errou um comando e descobriu o certo | Linha no `CLAUDE.md` ([01](docs/01-claude-md-agents-md.md)) | `CLAUDE.md` da raiz; `AGENTS.md` se o time usa mais de uma ferramenta |
| Preferência de uma pessoa só, que não é regra do time | Memória automática ([02](docs/02-memoria-automatica.md)) | O agente grava sozinho, em `~/.claude/projects/<projeto>/memory/` |
| O mesmo procedimento de vários passos foi colado ou explicado pela terceira vez | Skill ([03](docs/03-skills.md)) | `.claude/skills/<nome>/SKILL.md`; `~/.claude/skills/` se é pessoal |
| Uma tarefa lateral despeja na conversa saída que você não vai mais consultar | Subagente ([04](docs/04-subagentes.md)) | `.claude/agents/<nome>.md`; `~/.claude/agents/` se é pessoal |
| O agente pediu mais de uma vez para o usuário colar dados de um sistema externo, e não há CLI | Servidor MCP ([07](docs/07-mcp.md)) | `.mcp.json` (`--scope project`); `--scope user` se é pessoal |
| Uma regra do `CLAUDE.md` foi ignorada, ou o usuário disse "sempre" ou "nunca" sobre algo que um comando confere | Hook ([08](docs/08-hooks.md)) | `.claude/settings.json`; `.claude/settings.local.json` se é só desta máquina |

Como propor:

- **Proponha, não crie em silêncio.** Mostre o conteúdo pronto (a linha, o arquivo da skill, o JSON do hook, o comando `claude mcp add`) e diga em uma frase qual sinal levou à proposta. Grave depois do ok. A exceção é a memória automática, que o agente grava sozinho.
- **MCP e hook sempre passam pelo usuário.** O primeiro dá acesso a um sistema externo e o segundo roda comandos sozinho.
- **Espere o gatilho.** A documentação indica CLAUDE.md quando o erro se repete duas vezes e skill na terceira vez que você cola o mesmo procedimento (features-overview). Descrição de skill entra em toda requisição, então skill criada à toa custa contexto.
- **Um gatilho por recurso.** Os sinais da tabela vêm de "Build your setup over time" (features-overview): CLAUDE.md, skill, MCP, subagente e hook têm cada um o seu.
- **Antes de criar, veja se já existe.** Confira `.claude/skills/`, `.claude/agents/`, `.claude/settings.json` e `.mcp.json`. Atualizar o que existe é melhor que duplicar.
- **Projeto ou pessoal:** o que é do time vai em arquivo versionado no repositório; o que é hábito de uma pessoa vai em `~/.claude/`.

## Checklist de todo projeto configurado para agente de IA

- [ ] Existe CLAUDE.md ou AGENTS.md curto, com menos de 200 linhas (`wc -l CLAUDE.md AGENTS.md`).
- [ ] O arquivo de instruções não descreve arquitetura nem árvore de pastas (`grep -n 'src/' CLAUDE.md`).
- [ ] O arquivo traz os comandos de teste, lint e build que o agente deve rodar (`grep -nE 'test|lint|build' CLAUDE.md`).
- [ ] O que não admite exceção está em hook, regra `deny` ou CI, não só em texto (`cat .claude/settings.json`).
- [ ] Os MCPs ligados são só os usados e confiáveis (`claude mcp list`, `/context`).
- [ ] O modo `bypassPermissions` não está habilitado fora de contêiner descartável (`grep -rn 'bypassPermissions' .claude`).
- [ ] Segredos e `.env` estão fora do alcance do agente por regra `deny` (`grep -n 'deny' .claude/settings.json`).
- [ ] Cada skill ou subagente criado resolve um sinal real de repetição e tem descrição que diz quando usar (`ls .claude/skills .claude/agents`).
- [ ] A tarefa tem um jeito de conferir (teste, typecheck, build ou captura de tela) e o agente apresentou a evidência (rodar o comando).

## Regras de uso

- **Simples primeiro.** Plano, subagente, worktree e agent team custam tokens ou coordenação (best-practices, sub-agents, agent-teams); só entram quando a tarefa pede.
- **Sempre dê um jeito de o agente conferir o trabalho** (teste, typecheck, build, captura de tela) e peça a evidência, não só "pronto".
- **`CLAUDE.md` curto e só com o que o agente não descobre lendo o código.** Menos de 200 linhas. Não descreva arquitetura nem árvore de pastas.
- **O que não admite exceção não fica em texto.** `CLAUDE.md`, skill e pedido são lidos pelo modelo e podem ser ignorados. Use hook, regra `deny` ou CI.
- **Subagente custa tokens e perde detalhe na passagem.** Use para saída grande, trabalho independente ou revisão sem viés, não para "ter resposta melhor".
- **MCP põe nomes e instruções no contexto mesmo sem uso.** Desligue o que não usa, prefira CLI quando existir e confie no servidor antes de ligar (best-practices, mcp).
- **Menor privilégio e nunca `bypassPermissions` fora de contêiner descartável.** Conteúdo de terceiros (páginas, issues, pacotes) pode conter injeção de prompt.
- **Uma tarefa por sessão.** `/clear` ao trocar de assunto; depois de duas correções falhas, sessão nova com pedido melhor.
- **Revise o que o agente propõe:** a documentação de segurança põe essa revisão sob sua responsabilidade (security, "User responsibility").
- **Não invente comando ou opção.** Use só o que está na documentação oficial; na dúvida, confira com `/help`.

## Quando a lista não cobre

Se o pedido está fora destes doze recursos (por exemplo, criar um agente com o Agent SDK, integração em CI com GitHub Actions, rotinas na nuvem, ferramentas de outros fornecedores além do `AGENTS.md`), diga isso ao usuário e consulte a documentação oficial. Indexação de código e economia de token por ferramentas externas ficam na skill `code-indexes`. O `docs/README.md` registra o que foi avaliado e saiu da lista, com o motivo.

## Validade dos dados

Nomes de comandos, caminhos e comportamentos foram verificados na documentação oficial em 2026-11-24, e o Claude Code muda rápido (versões, modelos, padrões de permissão). Antes de afirmar algo decisivo ao usuário, confira na documentação (code.claude.com/docs) ou com `claude --version` e `/help`.
