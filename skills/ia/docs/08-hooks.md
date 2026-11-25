# Hooks

> Comandos que o Claude Code executa em pontos fixos do ciclo do agente, sem depender de o modelo lembrar.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/hooks e https://code.claude.com/docs/en/hooks-guide |
| **Categoria** | Automação e imposição de regra |
| **Tipo** | Configuração em `settings.json` |
| **Onde vale** | Claude Code. Codex, Cursor e GitHub Copilot têm hooks (conferido em 2026-11-24) |
| **Equivalente em outras ferramentas** | Codex: `hooks.json` ou `[hooks]` no `config.toml`, com `PreToolUse`, `PostToolUse`, `Stop`. Cursor: `.cursor/hooks.json`, com eventos em camelCase (`preToolUse`, `afterFileEdit`, `stop`). Copilot: `.github/hooks/*.json`. Os formatos de JSON diferem do Claude Code |
| **Verificado em** | 2026-11-24 |

## O que é

Hook é um gatilho que o Claude Code (não o modelo) dispara. Fica em `~/.claude/settings.json` (todos os projetos), `.claude/settings.json` (projeto, vai para o git), `.claude/settings.local.json` (projeto, fora do git), nas configurações gerenciadas, em plugins ou no frontmatter de skill e subagente.

Eventos confirmados, entre muitos: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `PreCompact`, `Notification`, `WorktreeCreate`. Tipos de handler: `command` (script de shell, recebe JSON no stdin), `http`, `mcp_tool`, `prompt` e `agent`. O `matcher` filtra por nome de ferramenta (`Bash`, `Edit|Write`, `mcp__servidor__.*`).

Código de saída de um hook `command`: `0` segue em frente; `2` bloqueia nos eventos que podem bloquear (`PreToolUse`, `UserPromptSubmit`, `Stop`) e devolve o stderr ao agente; qualquer outro código é erro que não bloqueia.

## Por que usar

- **Garantia:** acontece toda vez, independente do que o modelo decidiu.
- **Qualidade automática:** formatador depois de editar, typecheck antes de terminar.
- **Proteção:** impedir edição em pasta protegida.
- **Menos peso no `CLAUDE.md`:** a regra sai do texto e vira código.

## Quando usar

- Regra com zero exceção ("nunca editar `migrations/`", "sempre formatar").
- Verificação obrigatória antes de o agente encerrar (`Stop`).
- Reinjetar contexto depois de compactar (`SessionStart` com origem `compact`).
- Notificação quando o agente termina ou pede permissão.

### Quando o agente deve propor

- **Sinais:** uma regra escrita no `CLAUDE.md` foi ignorada (best-practices: se você segue acrescentando ênfase, a linha pertence a um hook); o usuário quer algo executado toda vez sem pedir (features-overview); o usuário disse "nunca" ou "sempre" sobre uma ação que dá para checar por comando.
- **O que fazer:** propor o JSON do hook e explicar em uma frase o que ele roda e quando. Com o ok, gravar em `.claude/settings.json` se a regra é do time, em `.claude/settings.local.json` se é só desta máquina, ou em `~/.claude/settings.json` se vale para todos os projetos da pessoa. Teste o hook uma vez antes de dizer que está pronto.
- **Não proponha se:** a regra precisa de julgamento ou é só preferência (best-practices: apague hooks de preferência e deixe o Claude decidir; isso fica no `CLAUDE.md`). Nunca crie hook sem mostrar o comando, porque ele roda sozinho.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Trabalho sem supervisão | ✅ Ótimo | O hook `Stop` impede encerrar com o typecheck quebrado |
| Feature grande | ✅ Ótimo | A documentação dá como exemplo rodar o ESLint depois de cada edição de arquivo (features-overview) |
| Passo que deve acontecer toda vez | ✅ Ótimo | "You want something to happen every time without asking" (features-overview) |
| Código gerado que não pode tocar certos arquivos | ✅ Ótimo | `PreToolUse` com exit 2 bloqueia |
| Preferência que tem exceções | ❌ Evite | A documentação diz que "preferir exportação nomeada" fica no `CLAUDE.md` |
| Hook que consulta modelo (`prompt`, `agent`) | 🟡 Serve | Outro modelo decide, então não é determinístico |

## Quando é bom

- **Determinístico:** hooks `command`, `http` e `mcp_tool` rodam sempre. Com `onFailure: "block"` bloqueiam também se o hook quebrar.
- **Peça ao agente:** "escreva um hook que bloqueie edição na pasta de migrations", e `/hooks` mostra o resultado.
- **Escopo compartilhável:** no `.claude/settings.json` vale para o time.

## Quando é ruim

- **Hook demais:** a documentação diz que cada hook e regra `deny` vai disparar sem querer alguma vez e que alguém precisa mantê-lo; mantenha o conjunto pequeno (best-practices).
- **Hooks de repositório rodam código na máquina de quem clonar:** hooks em frontmatter de subagente de projeto só rodam depois de você aceitar o diálogo de confiança da pasta (hooks, "Workspace trust").
- **Depende de ferramentas:** os exemplos oficiais usam `jq`; sem ele o script falha.
- **Loop de `Stop`:** se o hook bloquear oito vezes seguidas sem chamada de ferramenta, o Claude Code encerra mesmo assim (limite configurável por `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`).
- **`PostToolUse` não desfaz:** a ferramenta já rodou; o exit 2 só mostra o erro ao agente.
- **Caminhos em worktree:** `${CLAUDE_PROJECT_DIR}` continua apontando para a raiz original; o diretório do worktree vem no campo `cwd` do JSON de entrada.
- **Formato (conferido em 2026-11-24):** o JSON de entrada traz `session_id`, `cwd`, `permission_mode`, `hook_event_name`, `tool_name` e `tool_input`. Para bloquear no `PreToolUse`, ou saia com código 2 (o stderr vira o motivo) ou imprima no stdout, com saída 0, `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"..."}}` (`allow`, `deny`, `ask` ou `defer`). Outro código de saída não bloqueia. A referência tem 33 eventos e detalhes por evento (`updatedInput` e demais): consulte-a antes de escrever um hook além dos exemplos abaixo.

## Como começar

Formatar depois de cada edição, em `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "f=$(jq -r '.tool_input.file_path') && npx prettier --write --ignore-unknown \"$f\"" }
        ]
      }
    ]
  }
}
```

Não deixar o agente terminar com o typecheck quebrado:

```json
{
  "hooks": {
    "Stop": [
      { "hooks": [ { "type": "command", "command": "pnpm tsc --noEmit 1>&2 || exit 2" } ] }
    ]
  }
}
```

Bloquear um comando (script chamado por `PreToolUse` com `matcher: "Bash"`):

```bash
#!/bin/bash
command=$(jq -r '.tool_input.command')
if [[ "$command" == rm* ]]; then echo "Bloqueado: rm" >&2; exit 2; fi
exit 0
```

## Combina com / alternativas

Combina com:
- [Permissões e segurança](09-permissoes-e-seguranca.md): hooks e regras `deny` formam a camada determinística.
- [Prompt e verificação](11-prompt-e-verificacao.md): `Stop` torna o check obrigatório.
- [Skills](03-skills.md): a skill descreve o passo, o hook garante.

Alternativas:
- Linha no `CLAUDE.md`: o agente segue quase sempre, mas pode decidir que não se aplica.
- Regra `deny` em `permissions`: para impedir leitura ou edição de caminhos, sem escrever script.
- CI e proteção de branch: a última barreira, fora do agente.

## Decisão rápida

- **Use se:** a regra não pode ter exceção ou o passo precisa acontecer sempre.
- **Evite se:** é preferência, ou se você já tem tantos hooks que ninguém sabe o que cada um faz.

Fontes das recomendações: code.claude.com/docs/en/best-practices ("Enforce the rules that can't have exceptions"), features-overview e hooks-guide.
