# GitNexus

> Motor de inteligência de código que indexa o repositório em um grafo (símbolos, chamadas, dependências e fluxos de execução) e o expõe por MCP, CLI e um explorador web.

| | |
|---|---|
| **Site/repositório** | https://github.com/abhigyanpatwari/GitNexus |
| **Categoria** | Grafo de código |
| **Tipo** | Grafo AST com fluxos de execução; embeddings opcionais |
| **Como se conecta** | MCP; `npx gitnexus analyze` e `npx gitnexus setup` |
| **Linguagens suportadas** | C, C++, C#, COBOL, Dart, Go, Java, JavaScript, Kotlin, Objective-C, PHP, Python, Ruby, Rust, Swift, TypeScript, Vue, Zig (R experimental) |
| **Preço** | Grátis para uso não comercial; licença comercial por contato (akonlabs.com) |
| **Licença** | PolyForm Noncommercial 1.0.0 |
| **Verificado em** | 2026-11-24 |

## O que é

O comando `npx gitnexus analyze`, na raiz do repositório, constrói o índice, instala skills do agente, registra hooks do Claude Code e escreve `AGENTS.md` e `CLAUDE.md` (a opção `--index-only` pula essa integração). As ferramentas MCP listadas: `query`, `context`, `impact`, `trace`, `detect_changes` e `rename`.

O índice é local e sem LLM. Embeddings remotos, geração de wiki e chat usam provedores que você configura, e aí o código pode sair da máquina.

## Por que usar

- **Fluxos de execução** além de chamadas simples.
- **`rename` semântico** e `detect_changes` para revisar o efeito de um diff.
- **Servidor compartilhável:** `gitnexus mcp --http --port 3111` atende vários agentes.
- Cerca de 48,8 mil estrelas na leitura do README.

## Quando usar

- Uso pessoal, estudo, pesquisa ou código aberto.
- Refatoração em base média ou grande com renomeação.
- Quando se quer explorar o grafo visualmente.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | Ferramentas `impact` e `detect_changes` (README) |
| Base desconhecida | ✅ Ótimo | `query` e `context` (README) |
| Refatoração com impacto | ✅ Ótimo | `impact`, `detect_changes` e `rename` (README) |
| Pergunta de arquitetura | ✅ Ótimo | O README descreve fluxos de execução no grafo |
| Linguagem pouco comum | 🟡 Serve | A página diz que o suporte varia por construção da linguagem (README) |
| Projeto comercial/empresa | ❌ Evite | Licença PolyForm Noncommercial 1.0.0; uso comercial exige licença paga (README, akonlabs.com) |
| Código que não pode sair da máquina | 🟡 Serve | O índice é local; embeddings remotos, wiki e chat usam provedores configurados, e o código pode sair (README) |

## Quando é bom

- Conjunto de ferramentas focado em impacto e renomeação.
- Integração automática com Claude Code por hooks e skills.
- Aceita linguagens menos comuns (COBOL, Zig, Dart).

## Quando é ruim

- **Licença PolyForm Noncommercial:** proíbe uso comercial sem licença. Para trabalho de empresa, é o principal motivo de descarte.
- **`analyze` altera o repositório:** escreve `AGENTS.md`, `CLAUDE.md`, skills e hooks; use `--index-only` se não quiser isso.
- **Exige Node.js 22.18+ (22.x) ou 24.11+.**
- Recursos de empresa (revisão de PR, wiki automática, multi-repositório) são alegação do projeto, sem comprovação na página.
- O próprio README manda checar ambiguidade, frescor do índice e limites de cobertura.
- Custo em tokens e economia: sem número confirmado.

## Como começar

```bash
cd seu-projeto
npx gitnexus analyze --index-only   # só o índice, sem mexer em AGENTS.md/CLAUDE.md
npx gitnexus setup                  # detecta o Claude Code e registra o MCP
```

Instalação global: `npm install -g gitnexus`. Confira com `/mcp`.

## Combina com / alternativas

- [CodeGraph](01-codegraph.md) e [codebase-memory-mcp](05-codebase-memory-mcp.md): mesma ideia com licença MIT.
- [LSP nativo](02-lsp-claude-code.md): tipos exatos.

## Decisão rápida

- **Use se:** o uso é não comercial e você quer fluxos de execução e renomeação semântica.
- **Evite se:** o projeto é de empresa ou cliente (licença), ou você não quer que o comando altere arquivos do repositório.
