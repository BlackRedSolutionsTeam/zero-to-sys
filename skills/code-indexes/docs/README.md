# Indexação de código e economia de tokens

Um documento por ferramenta, explicando o tipo de índice, o que precisa para rodar, se o código sai da máquina, quando ganha e quando perde. Entrou só o que existe, está mantido e tem instalação confirmada. Licenças, comandos e números foram verificados nos repositórios e na documentação oficial em 2026-11-24. Números de economia de tokens são alegações dos próprios projetos, salvo quando o texto diz outra coisa. Cada linha de "Para que tipo de base/tarefa" cita o fato do documento e a fonte dele; "Qual escolher" resume os documentos.

## Grafo de código

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| CodeGraph | Grafo AST em SQLite, uma ferramenta MCP que devolve código, chamadas e impacto | Sim (telemetria anônima desligável) | [01-codegraph.md](01-codegraph.md) |
| codebase-memory-mcp | Grafo local com código, documentos e infraestrutura; 17 ferramentas | Sim | [05-codebase-memory-mcp.md](05-codebase-memory-mcp.md) |
| GitNexus | Grafo com fluxos de execução e renomeação; licença não comercial | Índice sim; recursos remotos opcionais | [06-gitnexus.md](06-gitnexus.md) |

## LSP e símbolos

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| LSP nativo do Claude Code | Ferramenta `LSP` e diagnósticos, via plugins oficiais | Sim | [02-lsp-claude-code.md](02-lsp-claude-code.md) |
| Serena | MCP com navegação e edição por símbolo, sobre LSP | Sim (com LSP) | [03-serena.md](03-serena.md) |

## Busca semântica e embeddings

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| Claude Context | Índice vetorial do código; precisa de banco vetorial e API de embeddings | Não no padrão | [04-claude-context.md](04-claude-context.md) |

## Empacotadores de repositório

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| Repomix | Junta o repositório em um arquivo, com contagem de tokens e compressão | Sim | [07-repomix.md](07-repomix.md) |

## Busca estrutural

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| ast-grep | Busca e reescrita por padrão de AST, via CLI | Sim | [08-ast-grep.md](08-ast-grep.md) |

## Documentação de bibliotecas

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| Context7 | Documentação atual de bibliotecas, servida por MCP remoto | Não | [09-context7.md](09-context7.md) |

## Compressão de saída

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| RTK | Proxy que resume a saída de comandos de shell | Sim | [10-rtk.md](10-rtk.md) |

## Linha de base

| Ferramenta | O que é | Local | Doc |
|---|---|---|---|
| ripgrep | Busca de texto rápida; quando grep já basta | Sim | [11-ripgrep-linha-de-base.md](11-ripgrep-linha-de-base.md) |

## Qual escolher

- **Base pequena ou busca de texto exato:** [ripgrep](11-ripgrep-linha-de-base.md) e leitura direta. Não indexe.
- **Base média ou grande, entender e achar onde mexer:** [CodeGraph](01-codegraph.md). Se tiver infraestrutura no mesmo repositório, olhe [codebase-memory-mcp](05-codebase-memory-mcp.md).
- **Erros de tipo e referências exatas em linguagem tipada:** [LSP nativo](02-lsp-claude-code.md). Edição por símbolo ou linguagem fora do plugin: [Serena](03-serena.md).
- **Perguntas conceituais em base enorme, aceitando serviço externo:** [Claude Context](04-claude-context.md).
- **Migrar um padrão em muitos arquivos:** [ast-grep](08-ast-grep.md).
- **Entregar a base a um modelo fora do Claude Code:** [Repomix](07-repomix.md).
- **Biblioteca nova ou que muda de versão:** [Context7](09-context7.md).
- **Muita saída de comando:** [RTK](10-rtk.md).
- Uma ferramenta de grafo por projeto; combine com LSP e ripgrep, não com outro grafo.

## O que saiu da lista e por quê

| Ferramenta | Motivo |
|---|---|
| Mapa do repositório do aider (repo map) | É técnica de um agente específico, não ferramenta que se liga ao Claude Code. Referência (aider.chat/docs/repomap.html): o aider ordena o mapa com um algoritmo de ranking em grafo, em que cada arquivo é um nó e as arestas são dependências, com orçamento padrão de 1k tokens (`--map-tokens`). A ideia aparece em ferramentas daqui, como o `--compress` do Repomix |
| code-index-mcp | Existe e é MIT, com cerca de 1 mil estrelas e 10 linguagens com AST; mas cobre o mesmo que CodeGraph e codebase-memory-mcp, e o README não traz comando `claude mcp add` (o repositório tem 30 releases, conferido via `gh api` em 2026-11-24) |
| Sourcegraph, Cody e Amp | Sourcegraph: a página de preços (sourcegraph.com/pricing, 2026-11-24) lista só o plano Enterprise, a partir de US$ 16 mil por ano, em nuvem dedicada ou auto-hospedado. Cody: o blog da Sourcegraph informa que os planos Free e Pro deixaram de aceitar novos cadastros em 25/06/2025 e foram encerrados em 23/07/2025 (sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans). Amp (ampcode.com, 2026-11-24): o site o descreve como agente e ambiente de desenvolvimento, com agentes em sandboxes na nuvem ("orbs"), e diz que ele é gratuito quando você usa suas próprias assinaturas e chaves. Ficaram fora por serem agentes e produtos, não ferramentas que se ligam ao Claude Code por MCP |
| Alternativas de grafo de mesmo nome | A busca por "codegraph" retorna dezenas de repositórios homônimos e forks; só o de colbymchenry foi confirmado como o da skill. Cuidado ao pesquisar |
| Servidores MCP de sistema de arquivos e de busca genéricos | Duplicam as ferramentas nativas do Claude Code sem indexar nada: leem arquivos e buscam texto, o que o Claude Code já faz com Read e com busca por `find`/`grep` embutidos no Bash (macOS, Linux, WSL) ou Grep/Glob (Windows), segundo code.claude.com/docs/en/tools-reference |
