# Paralelismo e ondas

> Divida a tarefa em partes, dispare juntas todas as que não dependem de outra e limite a quantidade pela máquina.

| | |
|---|---|
| **Categoria** | Orquestração |
| **Vale para** | Claude Code como sessão principal (`claude --agent zero-to-sys:zero-to-sys`) e Codex |
| **Verificado em** | 2026-11-25 |

## Limite pela máquina

- Meça no começo: `sysctl -n hw.ncpu` e `sysctl -n hw.memsize` no macOS; `nproc` e `free -g` no Linux.
- Até metade dos núcleos de agentes ao mesmo tempo, no mínimo 2 e no máximo 10.
- Com menos de 8 GB de memória livre, no máximo 3.
- Agente que só lê e pensa pesa pouco. Agente que roda build, testes ou containers conta como dois.

## Ondas

1. **Monte o grafo:** liste as partes, o agente de cada uma e do que cada parte depende. Mostre em poucas linhas antes de disparar.
2. **Dispare a onda:** todas as partes sem dependência pendente saem juntas, numa única mensagem com várias chamadas de agente, até o limite.
3. **Próxima onda:** quando uma volta, dispare o que ficou livre. Nunca espere em série o que pode correr junto.
4. **Longo e independente** roda em segundo plano enquanto o resto segue.

## Fluxo de uma parte

especialista planeja → especialistas afetados julgam (juntos) → `zero-to-sys-executor` implementa → `zero-to-sys-qualidade` julga o diff.

Exemplo: o `arquiteto` planeja o banco; `seguranca` e `integracoes` julgam ao mesmo tempo; o executor aplica; `qualidade` revisa.

## Sem conflito

- Dois executores só rodam juntos se mexem em arquivos diferentes.
- Com risco de conflito, use worktree em cada um (`isolation: "worktree"` no Claude Code) e junte depois, ou ponha em série.

## Progresso

Uma linha por onda: "Onda 2 de 4: executor em agendamento e em login, qualidade julgando o banco".
