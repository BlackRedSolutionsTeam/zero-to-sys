# Agentes de IA de código

Um documento por recurso, explicando quando usar, como se encaixa em cada tipo de tarefa, quando é bom, quando é ruim e por quê. O foco é o Claude Code; onde há equivalente em outras ferramentas, o documento cita a fonte. Nomes de comandos, caminhos e comportamentos foram verificados na documentação oficial em 2026-11-24.

## Configuração do projeto

| Recurso | O que é | Doc |
|---|---|---|
| CLAUDE.md e AGENTS.md | Arquivo de instruções lido em toda sessão | [01-claude-md-agents-md.md](01-claude-md-agents-md.md) |
| Memória automática | Notas que o agente guarda entre sessões | [02-memoria-automatica.md](02-memoria-automatica.md) |
| Skills | Procedimentos reutilizáveis, carregados sob demanda | [03-skills.md](03-skills.md) |
| MCP | Servidores que ligam o agente a sistemas externos | [07-mcp.md](07-mcp.md) |
| Hooks | Comandos impostos pelo Claude Code em pontos fixos | [08-hooks.md](08-hooks.md) |

## Trabalho com o agente

| Recurso | O que é | Doc |
|---|---|---|
| Fluxo planejar e implementar | Explorar, planejar, implementar, verificar | [05-fluxo-planejar-e-implementar.md](05-fluxo-planejar-e-implementar.md) |
| Prompt e verificação | Pedido específico, check de passou ou falhou e revisão | [11-prompt-e-verificacao.md](11-prompt-e-verificacao.md) |
| Gestão de contexto | `/clear`, `/compact`, `/rewind`, `/context` | [06-gestao-de-contexto.md](06-gestao-de-contexto.md) |
| Modelo e esforço | Qual modelo e quanto raciocínio por tarefa | [12-modelo-e-esforco.md](12-modelo-e-esforco.md) |

## Escala e segurança

| Recurso | O que é | Doc |
|---|---|---|
| Subagentes | Delegação com contexto próprio | [04-subagentes.md](04-subagentes.md) |
| Paralelismo e orquestração | Worktrees, `/batch`, agent teams | [10-paralelismo-e-orquestracao.md](10-paralelismo-e-orquestracao.md) |
| Permissões e segurança | Modos, regras, sandbox, injeção de prompt | [09-permissoes-e-seguranca.md](09-permissoes-e-seguranca.md) |

## Qual escolher

- **Base desconhecida ou pedido vago:** modo de planejamento e `SPEC.md` ([05](05-fluxo-planejar-e-implementar.md)), com `Explore` ([04](04-subagentes.md)) para ler o código.
- **Bug difícil:** teste que reproduz a falha ([11](11-prompt-e-verificacao.md)), esforço maior ([12](12-modelo-e-esforco.md)) e `/rewind` ([06](06-gestao-de-contexto.md)).
- **Tarefa repetitiva:** skill ([03](03-skills.md)); se o passo não pode falhar, hook ([08](08-hooks.md)).
- **Trabalho em paralelo:** worktrees ([10](10-paralelismo-e-orquestracao.md)).
- **Sem supervisão:** permissões e sandbox ([09](09-permissoes-e-seguranca.md)), limite de turnos e check obrigatório.
- **Regra que sempre vale:** `CLAUDE.md` se admite exceção, hook ou `deny` se não admite.
- **Dados de outro sistema:** CLI se existir, MCP se não ([07](07-mcp.md)).

## O que saiu da lista e por quê

| Tópico | Motivo |
|---|---|
| Revisão de código gerado por IA (documento próprio) | Entrou em [11](11-prompt-e-verificacao.md): o conteúdo útil é o check, o revisor sem viés e o `/code-review`, que não rende um documento à parte |
| Agent teams (documento próprio) | Experimentais e desligados por padrão; entram em [10](10-paralelismo-e-orquestracao.md) com as limitações |
| Plugins | Empacotam skills, subagentes, hooks e MCP; é distribuição, não um recurso novo (conferido em code.claude.com/docs/en/plugins em 2026-11-24: um plugin é um diretório com skills, agentes, hooks, servidores MCP ou módulo de hooks, instalado como uma unidade a partir de um marketplace) |
| Agent SDK | A documentação o descreve como "Claude Code as a library" para construir agentes (code.claude.com/docs/en/agent-sdk/overview), não como recurso de uso do Claude Code |
| Rotinas na nuvem, `/loop` e `/schedule` | `/loop` e as tarefas agendadas rodam prompts repetidos dentro da sessão (code.claude.com/docs/en/scheduled-tasks); só citados em [11](11-prompt-e-verificacao.md). Rotinas na nuvem e `/schedule` não foram verificados a fundo |
| Estilos de saída e personalização de interface | Estilos de saída definem papel, tom e formato da resposta (code.claude.com/docs/en/output-styles); não entram no fluxo de trabalho tratado aqui |
| Indexação de código e economia de token (codegraph etc.) | Pertence à skill `code-indexes` |
| Regras e formatos de outras ferramentas (Cursor, Copilot, Codex) | Só o `AGENTS.md` foi tratado aqui (agents.md); a documentação de cada ferramenta descreve os próprios formatos |

Fontes do "Qual escolher": code.claude.com/docs/en/features-overview ("Match features to your goal", "Build your setup over time"), best-practices, permission-modes e common-workflows.
