# Modelo e esforço por chamada

> Única tabela de modelos do plugin. Os agentes dizem só a categoria; o nome do modelo sai daqui.

| | |
|---|---|
| **Categoria** | Orquestração |
| **Vale para** | Claude Code e Codex |
| **Verificado em** | 2026-11-25 (`codex debug models`) |

| Categoria | Quando | Claude Code | Codex | Esforço |
|---|---|---|---|---|
| Decisão difícil | Stack, arquitetura, modelo de dados, auth, LGPD, julgamento de plano | `opus` | `gpt-6.2-astra` | `high` (`xhigh` em projeto grande) |
| Implementar | Funcionalidade, tela, integração, testes | `sonnet` | `gpt-6.2-sol` | `medium` |
| Mecânica | Renomear, gerar seed, ajustar texto, listar arquivos, conferir links | `haiku` | `gpt-6-luna` | `low` |

- **Falhou duas vezes:** suba um nível de modelo ou de esforço.
- **`max`** (e `ultra` no Codex) só quando o usuário pedir.
- **Claude Code:** passe `model` e `effort` na chamada do agente.
- **Codex:** passe o modelo e o `model_reasoning_effort` ao criar o subagente, se a ferramenta aceitar; senão vale `[agents] default_subagent_model` e `default_subagent_reasoning_effort` do `config.toml`.
- **Nomes do Codex mudam:** confira com `codex debug models` e use o equivalente atual (o mais capaz, o padrão para código, o rápido e barato).
- Diga no plano o modelo e o esforço de cada chamada.
