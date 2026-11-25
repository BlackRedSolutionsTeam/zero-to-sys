# Permissões e segurança

> Camadas que limitam o que o agente pode fazer: modo de permissão, regras allow/ask/deny, sandbox e cuidado com conteúdo não confiável.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/permission-modes, /permissions, /sandboxing e /security |
| **Categoria** | Segurança e controle |
| **Tipo** | Configuração em `settings.json`, comandos `/permissions` e `/sandbox` |
| **Onde vale** | Claude Code. Os princípios (menor privilégio, isolamento) valem para qualquer agente |
| **Equivalente em outras ferramentas** | Codex: sandbox `read-only`, `workspace-write` e `danger-full-access`; aprovação `on-request`, `never` e `granular`; rede desligada por padrão; flags `--sandbox` e `--ask-for-approval`. Cursor: Run Modes, de uma allowlist ao classificador Auto-review, e sandbox para comandos de terminal (cursor.com/docs/agent/tools/terminal e cursor.com/docs/agent/plan-mode). Copilot CLI: `/allow-all` (`/yolo`) e `/add-dir`; `--allow-tool=TOOL` libera ferramentas sem pedir permissão e `--deny-tool=TOOL` as nega, com padrões `Kind(argumento)`, por exemplo `--allow-tool='shell(git:*)' --deny-tool='shell(git push)'` (referência do Copilot CLI, docs.github.com/copilot, 2026-11-24). Conferido em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Três camadas que se somam:

1. **Modo de permissão.** Confirmados: `default` (alias `manual`), `acceptEdits`, `plan`, `auto`, `dontAsk` e `bypassPermissions`. Troca-se com `Shift+Tab` ou `claude --permission-mode <modo>`. Segundo a documentação, sessões interativas de terminal e VS Code começam em `auto` (versão 2.1.283 ou mais nova); `claude -p` começa em `default`. No modo `auto`, um modelo classificador separado avalia cada ação e bloqueia as arriscadas (como `curl | bash`, deploy em produção, force push). Depois de 3 bloqueios seguidos ou 20 no total, ele pausa e volta a perguntar.
2. **Regras** `allow`, `ask` e `deny` em `permissions`. Regras `deny` valem em todos os modos, inclusive `bypassPermissions`.
3. **Sandbox**, ligada com `/sandbox`: limite do sistema operacional para os comandos de shell (Seatbelt no macOS, bubblewrap no Linux e WSL2). Vem desligada por padrão.

## Por que usar

- **Menor privilégio:** o agente só faz o que precisa naquela tarefa.
- **Menos clique cego:** em modo manual, depois do décimo pedido você aprova sem ler. Bom controle evita isso.
- **Proteção de segredo:** `deny` em `.env` vale mesmo se o modelo errar.
- **Contenção:** a sandbox limita o estrago de um comando ou de uma injeção.

## Quando usar

- Antes de deixar o agente rodar sem você.
- Ao trabalhar com conteúdo de terceiros (páginas, issues, PRs, pacotes).
- Em CI e scripts (`dontAsk` com ferramentas liberadas).

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Trabalho sem supervisão | ✅ Ótimo | `dontAsk` com `allowedTools` e `--max-turns`, em sandbox ou contêiner |
| Base desconhecida ou de terceiros | ✅ Ótimo | Modo `default` ou `plan` até entender o que roda |
| Arquivo que o agente nunca deve ler (`.env`) | ✅ Ótimo | `deny` em `Read(./.env)` vale para a ferramenta Read e para `cat .env` (best-practices) |
| Contêiner descartável | 🟡 Serve | Só aí `bypassPermissions` faz sentido |
| Máquina com credenciais e `bypassPermissions` | ❌ Evite | Aprova tudo que `deny` e `ask` não cobrem |
| Regra de segurança só no `CLAUDE.md` ou na fala | ❌ Evite | Pode se perder ou ser ignorada; use `deny` ou hook |

## Quando é bom

- **`deny` é firme:** vale em todos os modos.
- **`auto` reduz prompts:** a documentação o coloca entre o manual e o `bypassPermissions`.
- **Sandbox independe do modelo:** limita arquivos e rede do shell mesmo se o agente errar. Por padrão, escrita só no diretório de trabalho e rede só para domínios permitidos.
- **`/permissions` e `/fewer-permission-prompts`:** auditam as regras e geram uma lista de comandos de leitura para liberar.

## Quando é ruim

- **O classificador do `auto` é julgamento, não regra:** pode errar. A documentação manda pôr os "nunca" em `deny` ou hook.
- **Regra casa chamada, não intenção:** `Read(./.env)` pega `cat .env`, mas não um script que abre o arquivo. Um `deny` de `WebFetch` para um domínio não impede `curl` ao mesmo domínio sem sandbox.
- **Sandbox não cobre tudo:** não cobre as ferramentas Read, Edit, Write, WebFetch e WebSearch (elas seguem as regras), nem hooks, servidores MCP locais, o que você digita com `!` e comandos em `excludedCommands`. Por padrão leitura é ampla (inclui `~/.ssh`). No Windows nativo os comandos rodam sem sandbox; use WSL2.
- **Comandos fora da sandbox:** comandos que casam com `excludedCommands` (por exemplo `docker compose *`) rodam sem sandbox (sandboxing).
- **Injeção de prompt:** texto em página, issue, README ou resposta de MCP pode tentar mandar no agente. Nenhuma proteção é total, diz a própria documentação. Revise comandos, evite mandar conteúdo não confiável direto ao agente e use VM para execução de risco.
- **Aprovar sem ler:** "Yes, and don't ask again" grava a regra no `.claude/settings.local.json` da raiz do repositório e ela vale em todos os worktrees (permissions e worktrees).
- **`autoMode` do projeto é ignorado:** o classificador não lê `autoMode` de `.claude/settings.json` nem de `.claude/settings.local.json` (auto-mode-config). Ao personalizar, mantenha `"$defaults"` nas listas, senão você substitui as regras embutidas.

## Como começar

```json
{
  "permissions": {
    "allow": ["Bash(pnpm tsc --noEmit)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)", "Read(./.env.local)", "Read(./secrets/**)"]
  },
  "sandbox": { "enabled": true }
}
```

```bash
claude --permission-mode plan          # só ler e planejar
/sandbox                               # ligar a sandbox (dentro da sessão)
/permissions                           # auditar regras
claude -p "tarefa" --permission-mode dontAsk --allowedTools "Read,Edit" --max-turns 20
```

Antes de deixar rodando sozinho, as cinco perguntas do guia oficial: sabe o que é "pronto"? Consegue checar o próprio trabalho? O que pode tocar? O que o interrompe (`--max-turns`, `--max-budget-usd`)? Quem aprova o resultado?

## Combina com / alternativas

Combina com:
- [Hooks](08-hooks.md): impõem passos e bloqueios que regra de permissão não expressa.
- [MCP](07-mcp.md): regras por ferramenta de servidor.
- [Paralelismo e worktrees](10-paralelismo-e-orquestracao.md): worktree compartilha o `.git` e as aprovações "don't ask again" com o checkout principal (worktrees, "What worktrees share").

Alternativas:
- Contêiner ou VM para o processo inteiro (guia de dev containers e de ambientes de sandbox da documentação).
- Sessões na nuvem (VM isolada gerenciada, rede limitada por padrão).
- `/security-review` para uma passada de segurança sobre as mudanças do branch.

## Decisão rápida

- **Use se:** o agente vai rodar sem você, mexe em repositório com segredo ou lê conteúdo de terceiros.
- **Evite se:** a ideia é desligar tudo "para ir mais rápido" numa máquina com suas credenciais.

Fontes das recomendações: code.claude.com/docs/en/permission-modes, permissions, sandboxing, security ("Protect against prompt injection") e best-practices ("Let Claude run without you", "Limit access with permission rules and the sandbox").
