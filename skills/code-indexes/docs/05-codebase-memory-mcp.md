# codebase-memory-mcp

> Servidor MCP local, em C, que monta um grafo de conhecimento persistente do repositório (código, documentos e infraestrutura) e o consulta por busca, caminhos de chamada e arquitetura.

| | |
|---|---|
| **Site/repositório** | https://github.com/DeusData/codebase-memory-mcp |
| **Categoria** | Grafo de código |
| **Tipo** | Grafo AST (tree-sitter) em SQLite, com resolução de tipos híbrida com LSP em algumas linguagens |
| **Como se conecta** | MCP; plugin do Claude Code ou entrada manual em `~/.claude.json` |
| **Linguagens suportadas** | 164 gramáticas tree-sitter; resolução de tipos para Python, TS/JS, PHP, C#, Go, C, C++, Java, Kotlin, Rust e Perl; também Dockerfile, Kubernetes, Helm, Terraform, Ansible e CI |
| **Preço** | Grátis |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Um binário nativo que indexa o repositório e guarda o grafo em SQLite na sua máquina. Expõe 17 ferramentas MCP, entre elas `search_graph`, `search_code`, `trace_path`, `detect_changes`, `get_architecture`, `index_repository` e `check_index_coverage`. Há uma interface de navegador opcional (CBM Lens), em beta.

Diferente de grafos só de código, ele também indexa infraestrutura (Kubernetes, Terraform, CI) e documentos (Markdown, PDF com texto).

## Por que usar

- **Local:** o README diz que não precisa de serviço, de chave de API, e que não coleta telemetria.
- **Cobre infraestrutura e documentos** além do código.
- **Muitas linguagens** e instalação por vários canais (npm, PyPI, Homebrew, Scoop e outros).
- **Números do projeto:** um preprint no arXiv, escrito pelo próprio projeto, com 31 repositórios, relata cerca de 10 vezes menos tokens e 2,1 vezes menos chamadas contra exploração arquivo a arquivo. É alegação do projeto (arXiv 2603.27277); o resumo do artigo informa também qualidade de resposta de 83% contra 92% do agente que explora arquivos.

## Quando usar

- Base com código e infraestrutura juntos (monorepo com Terraform, Helm, CI).
- Perguntas de arquitetura e rastreio de chamadas.
- Quando se quer índice local sem chave e sem telemetria.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | Ferramentas `search_graph`, `search_code` e `trace_path` (README) |
| Monorepo grande | ✅ Ótimo | O README cita o kernel Linux indexado em cerca de 3 minutos (Apple M3 Pro, medida do projeto) |
| Base desconhecida | ✅ Ótimo | `get_architecture` dá uma visão inicial (README) |
| Refatoração com impacto | ✅ Ótimo | `detect_changes` e `trace_path` (README) |
| Pergunta de arquitetura | ✅ Ótimo | Ferramenta própria, `get_architecture` (README) |
| Busca por texto exato | 🟡 Serve | Há `search_code` entre as 17 ferramentas (README) |
| Linguagem pouco comum | ✅ Ótimo | 164 gramáticas tree-sitter (README) |
| Código que não pode sair da máquina | ✅ Ótimo | Local, sem telemetria, segundo o README |
| Quem quer poucas ferramentas listadas | 🟡 Serve | São 17 ferramentas MCP (README); o Claude Code adia as definições de ferramentas MCP por padrão (code.claude.com/docs/en/mcp, "Scale with MCP tool search") |

## Quando é bom

- Visão de arquitetura pronta e cobertura de infraestrutura.
- Releases com checksums e SLSA 3 citados no README.
- Comunidade grande (cerca de 49,1 mil estrelas na leitura do README).

## Quando é ruim

- **17 ferramentas MCP** (README). No Claude Code, as definições ficam adiadas por padrão: só nomes e instruções do servidor carregam no início (code.claude.com/docs/en/mcp, "Scale with MCP tool search"); meça com `/context`.
- **Issues abertas:** 509 (busca na API do GitHub em 2026-11-24); partes em beta ou experimentais segundo o README (CBM Lens v0.0.1 beta, Smart CI).
- **Windows:** o README cita falso positivo do Defender nos binários.
- Análise estática: mesmos pontos cegos de DI e reflexão.
- Última versão: v0.12.1, de 2026-10-16 (conferido na API de releases do GitHub em 2026-11-24).

## Como começar

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

Como plugin do Claude Code:

```
claude plugin marketplace add DeusData/codebase-memory-mcp
claude plugin install codebase-memory@codebase-memory
```

O plugin registra só o servidor MCP, sem skills nem hooks. Confira com `/mcp` (devem aparecer 17 ferramentas).

## Combina com / alternativas

- [CodeGraph](01-codegraph.md): uma só ferramenta listada por padrão.
- [GitNexus](06-gitnexus.md): grafo com fluxos de execução, licença não comercial.
- [LSP nativo](02-lsp-claude-code.md) para tipos exatos.

## Decisão rápida

- **Use se:** quer grafo local com infraestrutura e arquitetura incluídas, e aceita 17 ferramentas MCP.
- **Evite se:** quer uma única ferramenta listada (CodeGraph), ou não quer partes em beta no fluxo.
