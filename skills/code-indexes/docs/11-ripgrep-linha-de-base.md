# ripgrep (linha de base)

> Busca de texto por expressão regular, muito rápida, que respeita o .gitignore; a linha de base contra a qual todo índice precisa se justificar.

| | |
|---|---|
| **Site/repositório** | https://github.com/BurntSushi/ripgrep |
| **Categoria** | Linha de base (texto) |
| **Tipo** | Busca de texto por linha; sem índice |
| **Como se conecta** | CLI `rg`; no Windows o Claude Code traz a ferramenta nativa Grep, baseada em ripgrep; no macOS, Linux e WSL o `grep` do Bash roda um `ugrep` embutido (code.claude.com/docs/en/tools-reference) |
| **Linguagens suportadas** | Qualquer arquivo de texto |
| **Preço** | Grátis |
| **Licença** | MIT ou Unlicense (escolha do usuário) |
| **Verificado em** | 2026-11-24 |

## O que é

`rg padrão` percorre a pasta atual de forma recursiva, ignora o que o `.gitignore` ignora, além de arquivos ocultos e binários (`-uuu` desliga isso). Não guarda índice: cada busca lê os arquivos de novo, o que é rápido o bastante na maioria das bases.

Este documento existe para dizer quando indexar é desperdício. Nesses casos, grep mais leitura direta do arquivo já resolve.

## Por que usar

- **Zero configuração, zero estado, zero contexto de ferramenta.**
- **Sempre atual:** não há índice para ficar velho.
- **Exato:** acha a string, o log, a chave de config.
- Números do próprio projeto: no kernel Linux, 0,082 s contra 0,273 s do git grep (i9-12900K). São medidas do autor em hardware e corpus específicos, e o README admite casos em que a vantagem some.

## Quando usar

- Base pequena ou média, até onde a busca continua instantânea.
- Texto exato: mensagem de erro, nome de variável de ambiente, rota, chave de i18n.
- Arquivos que índices de código não cobrem (configuração, docs, SQL, YAML).
- Primeiro passo antes de decidir se vale indexar.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base pequena | ✅ Ótimo | Não guarda índice: cada busca lê os arquivos de novo, rápido o bastante na maioria das bases (README) |
| Monorepo grande | 🟡 Serve | No kernel Linux, 0,082 s contra 0,273 s do git grep (README, i9-12900K) |
| Refatoração com impacto | ❌ Evite | É busca de texto por linha, sem índice (README) |
| Busca por texto exato | ✅ Ótimo | Acha a string, o log, a chave de config (README) |
| Linguagem pouco comum | ✅ Ótimo | Lê qualquer arquivo de texto (README) |
| Arquivos de configuração e docs | ✅ Ótimo | Percorre qualquer arquivo de texto, inclusive o que os índices de símbolo não cobrem (README) |

## Quando é bom

- Zero configuração, ignora o que o `.gitignore` ignora (README).
- Cerca de 70,3 mil estrelas (70.286 no GitHub em 2026-11-24); última versão 16.0.0, de 2026-11-22.

## Quando é ruim

- **Não entende código:** `parse` no comentário e `parse` na função são o mesmo resultado.
- **Muitas voltas em base grande:** cada pergunta vira busca, leitura e nova busca.
- **Saída longa** se o padrão for amplo; limite com `-l`, `-c` ou `-m`.
- **Não vê despacho dinâmico, renomeações nem herança.**
- Sem número de tokens economizados: ele não economiza, é a referência.

## Como começar

```bash
brew install ripgrep       # macOS; Debian/Ubuntu: sudo apt-get install ripgrep
rg -n "createSession" src/ # busca com número de linha
rg -l "TODO" -g '*.ts'     # só os nomes de arquivo, filtrando por glob
```

Não há servidor a ligar. O Claude Code já faz busca de texto pelas ferramentas nativas (veja o início deste documento); instale o `rg` só se quiser usá-lo pelo Bash, e confirme que está no PATH.

## Combina com / alternativas

- [CodeGraph](01-codegraph.md), [Serena](03-serena.md), [LSP](02-lsp-claude-code.md): entram quando o texto não basta.
- [ast-grep](08-ast-grep.md): quando a forma do código importa mais que o texto.
- Alternativas de fora: `git grep` (git-scm.com/docs/git-grep), ugrep (github.com/Genivia/ugrep).

## Decisão rápida

- **Use se:** a base é pequena ou a busca é de texto exato.
- **Evite como única ferramenta se:** a base é grande, a tarefa é de impacto ou a pergunta é de arquitetura.
