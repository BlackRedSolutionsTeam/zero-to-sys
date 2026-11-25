# LSP nativo do Claude Code

> Ferramenta `LSP` do próprio Claude Code, ativada por plugins de inteligência de código: dá ao agente definição, referências e diagnósticos de tipo vindos do mesmo servidor de linguagem do editor.

| | |
|---|---|
| **Site/repositório** | https://code.claude.com/docs/en/plugins/code-intelligence (plugins em github.com/anthropics/claude-plugins-official) |
| **Categoria** | LSP/símbolos |
| **Tipo** | Servidor de linguagem (LSP), consulta ao vivo, sem índice próprio |
| **Como se conecta** | Plugin: `/plugin install <plugin>@claude-plugins-official`, mais o binário do servidor na máquina |
| **Linguagens suportadas** | C/C++, C#, Go, Java, Kotlin, Liquid, Lua, PHP, Python, Ruby, Rust, Swift, TypeScript/JavaScript (plugins oficiais); outras via `.lsp.json` |
| **Preço** | Grátis (o plugin; o servidor de linguagem depende de cada projeto) |
| **Licença** | Apache-2.0 (repositório anthropics/claude-plugins-official, via `gh api` em 2026-11-24; o `liquid-lsp` é da Shopify, no repositório Shopify/liquid-skills, que não declara licença: `gh api repos/Shopify/liquid-skills/license` devolve 404 em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Um plugin de inteligência de código diz ao Claude Code qual comando inicia o servidor de linguagem e quais extensões ele cobre. O plugin não traz o servidor: você instala o binário (por exemplo `gopls`, `rust-analyzer`, `typescript-language-server`).

Com o servidor rodando, o Claude ganha duas coisas. Primeiro, diagnósticos depois de cada edição (erros de tipo, import faltando), sem rodar o compilador. Segundo, uma ferramenta `LSP`, somente leitura, que segundo a documentação faz: ir à definição, achar referências, tipo na posição, listar símbolos do arquivo, buscar símbolo no workspace, achar implementações e traçar hierarquia de chamadas.

## Por que usar

- **Exatidão:** resolve símbolos como o compilador resolve, não por texto.
- **Erros pegos na hora**, antes do build.
- **Nada sai da máquina** por causa do plugin; o servidor roda local.
- **Sem custo de banco ou indexação própria** e sem MCP extra.

## Quando usar

- Projeto tipado (TypeScript, Go, Rust, Java, C#) onde erros de tipo são comuns após edição.
- Renomear ou achar todos os usos de um símbolo com precisão.
- Qualquer projeto em que já existe um servidor de linguagem estável.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | Navegação por símbolo vinda do servidor de linguagem; memória alta enquanto ele indexa (documentação do Claude Code) |
| Monorepo grande | 🟡 Serve | A documentação de troubleshooting cita falsos positivos de import não resolvido em monorepo |
| Refatoração com impacto | ✅ Ótimo | A ferramenta `LSP` faz referências e hierarquia de chamadas (code.claude.com/docs/en/tools-reference) |
| Pergunta de arquitetura | ❌ Evite | A ferramenta `LSP` cobre definição, referências, tipo, símbolos, implementações e hierarquia de chamadas, sem consulta de fluxo (tools-reference) |
| Busca por texto exato | ❌ Evite | As consultas da ferramenta são por símbolo (tools-reference) |
| Linguagem pouco comum | 🟡 Serve | Outras linguagens entram via `.lsp.json`, se houver servidor (documentação de plugins de inteligência de código) |
| Sessão em nuvem do Claude Code | ❌ Evite | Os servidores de plugin não iniciam em sessões na nuvem (documentação do Claude Code) |
| Código que não pode sair da máquina | ✅ Ótimo | O servidor de linguagem roda local (documentação de plugins de inteligência de código) |

## Quando é bom

- **Diagnósticos e navegação por símbolo vindos do servidor de linguagem**, como no editor (documentação do Claude Code).
- **Diagnósticos automáticos** após cada Edit ou Write.
- **Instalação em dois passos** (binário e plugin), e o Claude Code oferece o plugin quando acha o binário no PATH (uma vez por sessão).
- **Mantido pela Anthropic** (todos os plugins da tabela, exceto o de Liquid, que é da Shopify).

## Quando é ruim

- **Instalar o binário é com você**, e ele precisa estar no PATH do shell que abriu o `claude`.
- **Memória alta** enquanto o servidor indexa o projeto, conforme a documentação.
- **Só terminal:** não funciona em sessões na nuvem.
- **Consulta por símbolo:** a ferramenta `LSP` faz definição, referências, tipo, símbolos do arquivo, símbolo no workspace, implementações e hierarquia de chamadas; não há consulta de fluxo pronta.
- **Falsos positivos de import não resolvido em monorepo**, segundo a documentação de troubleshooting.
- Número de tokens economizados: não há medição oficial confirmada.

## Como começar

```bash
npm install -g typescript-language-server typescript   # exemplo para TypeScript
which typescript-language-server                        # confirme no PATH
```

Dentro do Claude Code:

```
/plugin install typescript-lsp@claude-plugins-official
```

Para outros idiomas, troque pelo plugin da tabela da documentação (`gopls-lsp`, `pyright-lsp`, `rust-analyzer-lsp` etc.). Para checar: peça um erro de tipo e veja a linha "Found N new diagnostic issues"; se faltar, abra `/plugin` e a aba Errors.

## Combina com / alternativas

- [CodeGraph](01-codegraph.md): visão ampla e fluxo; o LSP dá a precisão.
- [Serena](03-serena.md): mesma base (LSP), mas como MCP com edição simbólica e suporte a mais linguagens.
- [ast-grep](08-ast-grep.md): reescrita estrutural em massa.

## Decisão rápida

- **Use se:** a linguagem tem servidor maduro e você quer navegação exata e diagnósticos após edição.
- **Evite se:** trabalha em sessão na nuvem, ou quer explicar a arquitetura inteira em uma pergunta.
