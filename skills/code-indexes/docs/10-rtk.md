# RTK (Rust Token Killer)

> Proxy de linha de comando, em um binário Rust, que reescreve comandos de shell do agente e devolve uma saída resumida, para gastar menos tokens com logs de git, testes e listagens.

| | |
|---|---|
| **Site/repositório** | https://github.com/rtk-ai/rtk |
| **Categoria** | Compressão de saída de comandos |
| **Tipo** | Filtros de saída por comando; não indexa o código |
| **Como se conecta** | Hook de shell: `rtk init -g`, depois reiniciar o Claude Code |
| **Linguagens suportadas** | Não se aplica; cobre mais de 100 comandos (git, gh, cargo, npm, pnpm, pytest, go test, jest, vitest, tsc, eslint, docker, kubectl, terraform e outros) |
| **Preço** | Grátis para uso em produção |
| **Licença** | CLI `rtk` em Apache-2.0; `rtk-engine` e `rtk-proxy` em BUSL-1.1; edição `rtk-oss` só Apache-2.0 |
| **Verificado em** | 2026-11-24 |

## O que é

Quando o agente roda `git status`, o hook troca por `rtk git status`, que devolve um resumo mais curto. As ferramentas nativas `Read`, `Grep` e `Glob` passam sem mudança por padrão. Se um filtro falha, volta a saída bruta; `rtk bypass` roda o comando sem filtro. O painel `rtk gain` mostra a economia.

Atenção: existe outro pacote chamado "rtk" no crates.io; o README manda conferir com `rtk gain`.

## Por que usar

- **Ataca outra fonte de gasto:** saída de comandos, que índices de código não tocam.
- **Funciona com qualquer linguagem**, porque filtra comandos, não código.
- **Sem MCP e sem custo de definições de ferramenta.**
- **Falha de forma segura:** volta ao bruto.
- Números do projeto: "até 90% menos saída de comandos", e 93,3% na demonstração do README (cargo test 94,2%, ls 82,3%). São alegações do projeto; os tokens são estimados por bytes/4. O README avisa que cortar 90% da saída de comandos não corta 90% do custo, e cita 20,2% de redução do custo total para o melhor pipeline listado, no benchmark do autor do pipeline.

## Quando usar

- Sessões com muito `git`, teste, build e lint.
- Ciclo de testes com saída longa.
- Qualquer linguagem, junto a um índice de código.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | Demonstração do README: 93,3% menos saída, `cargo test` 94,2% (alegação do projeto) |
| Busca por texto exato | ❌ Evite | `Read`, `Grep` e `Glob` nativos passam sem filtro por padrão (README), e `grep`/`rg` pelo Bash são resumidos |
| Linguagem pouco comum | 🟡 Serve | Cobre mais de 100 comandos, por comando e não por linguagem (README) |
| Depuração de falha que precisa do log inteiro | ❌ Evite | `rtk bypass` roda o comando sem filtro (README) |
| Código que não pode sair da máquina | ✅ Ótimo | Sem telemetria por padrão; só liga com `rtk telemetry enable` (README) |

## Quando é bom

- Instalação por Homebrew (`brew install rtk`) ou winget (`winget install rtk-ai.rtk`).
- Suporta 18 agentes (Claude Code, Copilot, Cursor, Gemini CLI, Codex e outros).
- 87.723 estrelas no GitHub em 2026-11-24 e 2.948 commits no ramo `develop`.

## Quando é ruim

- **Resumo pode ocultar o erro** de que você precisa; confira antes de confiar.
- **Licença mista:** o binário `rtk` traz o `rtk-engine` em BUSL-1.1; o uso em produção é gratuito, mas oferecer o RTK como produto ou serviço comercial a terceiros exige contato com os mantenedores (README, "Editions and licence").
- **Reescreve comandos por hook**, o que muda o que o agente vê; entenda o que está sendo filtrado.
- **Issues abertas:** 950 (busca na API do GitHub em 2026-11-24).
- Versão atual: v1.2.1, de 2026-11-19 (conferido no GitHub em 2026-11-24).

## Como começar

```bash
brew install rtk          # macOS/Linux; no Windows: winget install rtk-ai.rtk
rtk init -g               # instala o hook; reinicie o Claude Code
rtk gain                  # confirma que é o rtk certo e mostra a economia
```

## Combina com / alternativas

- [CodeGraph](01-codegraph.md), [LSP](02-lsp-claude-code.md): cuidam da leitura do código; o RTK cuida da saída dos comandos.
- Hooks e gestão de contexto em geral: veja a skill `ia`.

## Decisão rápida

- **Use se:** o agente roda muitos comandos com saída longa e você quer cortar esse gasto.
- **Evite se:** você depende do log bruto para depurar, ou a licença BUSL de partes do pacote é problema.
