# ast-grep

> Ferramenta de linha de comando, em Rust, para buscar, checar e reescrever código por estrutura sintática (AST), não por texto.

| | |
|---|---|
| **Site/repositório** | https://github.com/ast-grep/ast-grep |
| **Categoria** | Busca estrutural (AST) |
| **Tipo** | Busca e reescrita por padrão de AST (tree-sitter); sem índice persistente |
| **Como se conecta** | CLI (`ast-grep` ou `sg`) chamada pelo agente via Bash; MCP experimental (ast-grep/ast-grep-mcp); skill para Claude Code no repositório ast-grep/agent-skill (ast-grep.github.io/advanced/prompting, conferido em 2026-11-24) |
| **Linguagens suportadas** | Embutidas: Bash, C, C++, C#, CSS, Elixir, Go, Haskell, HCL, HTML, Java, JavaScript, JSON, Kotlin, Lua, Markdown, Nix, PHP, Python, Ruby, Rust, Scala, Solidity, Swift, TypeScript, TSX, YAML, Zig (ast-grep.github.io/reference/languages); outras via linguagem customizada |
| **Preço** | Grátis |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Você escreve um padrão que parece código, com variáveis como `$A`, e o ast-grep acha todos os trechos com a mesma estrutura sintática (README). Também reescreve. O exemplo do README troca `$A && $A()` por `$A?.()`:

```bash
ast-grep -p '$A && $A()' -l ts -r '$A?.()'
```

Também serve como linter por regras. Roda na hora, sem indexar.

## Por que usar

- **Casa estrutura, não texto:** a documentação mostra que `console.log(123)` dentro de comentário não casa com o padrão (ast-grep.github.io/guide/pattern-syntax).
- **Reescrita e lint em larga escala:** o README cita "massive scale code manipulation".
- **Sem índice persistente** (README).
- **É um comando do shell, não um MCP:** não adiciona servidor ao Claude Code.

## Quando usar

- Migração de API ou padrão de código em muitos arquivos.
- Achar todos os usos de uma forma de código ("todo `useEffect` sem lista de dependências").
- Regras de lint específicas do projeto.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | Roda na hora, sem indexar; núcleo compilado, com parsing tree-sitter e vários núcleos (README) |
| Monorepo grande | ✅ Ótimo | O README cita "massive scale code manipulation" |
| Refatoração com impacto | 🟡 Serve | Casa por estrutura sintática (ast-grep.github.io/guide/pattern-syntax) |
| Busca por texto exato | ❌ Evite | `console.log(123)` dentro de comentário não casa com o padrão (ast-grep.github.io/guide/pattern-syntax) |
| Linguagem pouco comum | 🟡 Serve | Lista de linguagens embutidas; outras via linguagem customizada (ast-grep.github.io/reference/languages) |
| Migração de padrão em lote | ✅ Ótimo | O exemplo do README troca `$A && $A()` por `$A?.()` |
| Código que não pode sair da máquina | ✅ Ótimo | CLI chamada pelo Bash, sem servidor (README) |

## Quando é bom

- Escrito em linguagem compilada, com parsing tree-sitter e vários núcleos (README).
- Padrões escritos como código comum (README).
- Cerca de 16,7 mil estrelas (16.688 no GitHub em 2026-11-24); última versão 0.51.3, de 2026-11-16.

## Quando é ruim

- **Sem semântica:** não resolve tipos, imports nem herança; "esta chamada é desta função" é por forma.
- **Curva dos padrões:** variáveis, restrições e regras exigem prática.
- **O agente precisa ser instruído:** a documentação diz que, com a skill instalada, o Claude decide por consulta se a usa, e que um prompt em AGENTS.md só funciona se o modelo conhecer a ferramenta (ast-grep.github.io/advanced/prompting).
- Requer Node.js 20+ pela via npm.
- O servidor MCP (`ast-grep/ast-grep-mcp`, MIT, mantido na organização do projeto) se descreve como experimental (conferido em 2026-11-24).

## Como começar

```bash
npm install --global @ast-grep/cli
# ou: brew install ast-grep
# ou: pip install ast-grep-cli
# ou: cargo install ast-grep --locked
```

Não há servidor a ligar: o Claude chama o binário pelo Bash. Para a skill oficial, a documentação indica `npx skills add ast-grep/agent-skill` ou, dentro do Claude Code, `/plugin marketplace add ast-grep/agent-skill`. Outra opção documentada é uma instrução em AGENTS.md ou CLAUDE.md para usar `ast-grep --lang <linguagem> -p '<padrão>'` em buscas sintáticas.

## Combina com / alternativas

- [ripgrep](11-ripgrep-linha-de-base.md): texto; ast-grep: forma.
- [LSP nativo](02-lsp-claude-code.md): semântica e renomeação.
- Alternativas de fora: Comby (comby.dev), Semgrep (semgrep.dev).

## Decisão rápida

- **Use se:** precisa achar ou reescrever um padrão de código em muitos arquivos.
- **Evite se:** a tarefa é entender um sistema novo ou buscar texto literal.
