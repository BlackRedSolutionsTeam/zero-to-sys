# Repomix

> Empacota o repositório inteiro em um único arquivo (XML, Markdown, JSON ou texto) pronto para um modelo, com contagem de tokens, modo de compressão e varredura de segredos.

| | |
|---|---|
| **Site/repositório** | https://github.com/yamadashy/repomix |
| **Categoria** | Empacotador de repositório |
| **Tipo** | Empacotamento em arquivo único; compressão opcional por tree-sitter (experimental); sem índice persistente |
| **Como se conecta** | CLI (`npx repomix@latest`) ou MCP (`claude mcp add repomix -- npx -y repomix --mcp`) |
| **Linguagens suportadas** | Qualquer texto; a compressão (tree-sitter) tem consultas para C, C#, C++, CSS, Dart, Go, Java, JavaScript, PHP, Python, Ruby, Rust, Solidity, Swift, TypeScript e Vue (conferido no código em 2026-11-24) |
| **Preço** | Grátis |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Repomix lê o repositório (respeitando as regras de exclusão), junta os arquivos em um só e mostra quantos tokens o resultado tem, por arquivo e no total. O padrão de codificação é o `o200k_base`; `cl100k_base` também existe.

A opção `--compress` usa tree-sitter para manter classes, funções e interfaces e tirar o corpo das implementações; a página a chama de experimental. Uma verificação com Secretlint deixa de fora arquivos com formato de credencial conhecido. O modo MCP expõe `pack_codebase`, `pack_remote_repository` e `grep_repomix_output`, e a opção `--sandbox` limita os arquivos a um diretório.

## Por que usar

- **Uma entrega só** para colar em um chat ou passar a um modelo de contexto longo.
- **Orçamento visível:** `--token-count-tree` mostra onde estão os tokens e `--token-budget` falha se passar do limite.
- **Repositório remoto sem clonar:** `repomix --remote dono/repo`.
- **Sem serviço, sem chave.**
- Número do projeto: as descrições das ferramentas MCP dizem "cerca de 70% menos tokens" com a compressão. É alegação do projeto, sem método na página.

## Quando usar

- Base pequena ou média que cabe no contexto e a pergunta é ampla.
- Revisão ou resumo de um repositório externo.
- Entregar o código a um modelo fora do Claude Code (chat web, API).
- Descobrir o que pesa no contexto (`--token-count-tree`).

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base pequena | ✅ Ótimo | Junta os arquivos em um só e mostra os tokens por arquivo e no total (README) |
| Base média/grande | 🟡 Serve | `--compress` mantém classes, funções e interfaces e tira o corpo; a página a chama de experimental (README) |
| Monorepo grande | ❌ Evite | Gera arquivo único, sem índice persistente; `--split-output` divide o arquivo (README) |
| Refatoração com impacto | ❌ Evite | Empacota o texto; não monta grafo de chamadas (README, tipo da ferramenta) |
| Linguagem pouco comum | ✅ Ótimo | Empacota qualquer texto; só a compressão depende de consultas tree-sitter (código do repositório, 2026-11-24) |
| Revisão de repositório de terceiros | ✅ Ótimo | `repomix --remote dono/repo` evita clonar (README) |
| Código que não pode sair da máquina | 🟡 Serve | Sem serviço e sem chave (README); `--sandbox` limita os arquivos do modo MCP a um diretório |

## Quando é bom

- Roda com `npx repomix@latest`, sem instalação prévia, e sem índice persistente (README).
- Cerca de 29,4 mil estrelas (29.422 no GitHub em 2026-11-24) e 4.932 commits no ramo padrão.

## Quando é ruim

- **Despejo, não consulta:** o arquivo inteiro entra no contexto de uma vez; não há busca incremental.
- **Fica velho:** o pacote é uma foto; refaça após mudanças.
- **`--compress` é experimental** e perde as implementações.
- **A varredura de segredos não é garantia:** revise o que vai para fora.
- Última versão: v1.19.0, de 2026-11-08 (conferido no GitHub em 2026-11-24).

## Como começar

```bash
npx repomix@latest                      # gera repomix-output.xml na pasta atual
npx repomix@latest --compress           # só estrutura (experimental)
npx repomix@latest --token-count-tree   # onde estão os tokens
```

Ligação ao Claude Code:

```bash
claude mcp add repomix -- npx -y repomix --mcp
```

## Combina com / alternativas

- [ripgrep](11-ripgrep-linha-de-base.md): para achar um ponto antes de empacotar só a pasta certa.
- [CodeGraph](01-codegraph.md): quando a base é grande demais para empacotar.
- Técnica parecida: o mapa do repositório do aider (veja "O que saiu da lista").

## Decisão rápida

- **Use se:** a base cabe no contexto (ou comprimida cabe) e você quer entregá-la inteira a um modelo.
- **Evite se:** a base é grande e a pergunta é pontual; consulte por grafo ou grep.
