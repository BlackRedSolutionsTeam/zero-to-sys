# code-indexes

Skill para o Claude Code que escolhe como o agente lê e navega o código de um projeto: grafo de código, LSP, busca semântica, empacotadores, busca estrutural, documentação de bibliotecas e compressão de saída. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por ferramenta ([docs/](docs/)), explicando o tipo de índice, o que precisa para rodar, se o código sai da máquina, quando ganha e quando perde.

## Ferramentas cobertas

Só entrou o que existe, está mantido, tem instalação confirmada e resolve um problema real do agente de código. Há também um documento de linha de base, para os casos em que indexar é desperdício.

| Ferramenta | Papel | Documento |
|---|---|---|
| CodeGraph | Grafo local em SQLite, responde com código, chamadas e impacto | [docs/01-codegraph.md](docs/01-codegraph.md) |
| LSP nativo do Claude Code | Definição, referências e diagnósticos exatos | [docs/02-lsp-claude-code.md](docs/02-lsp-claude-code.md) |
| Serena | Navegação e edição por símbolo, via LSP | [docs/03-serena.md](docs/03-serena.md) |
| Claude Context | Busca semântica por embeddings | [docs/04-claude-context.md](docs/04-claude-context.md) |
| codebase-memory-mcp | Grafo local com código e infraestrutura | [docs/05-codebase-memory-mcp.md](docs/05-codebase-memory-mcp.md) |
| GitNexus | Grafo com fluxos de execução (licença não comercial) | [docs/06-gitnexus.md](docs/06-gitnexus.md) |
| Repomix | Empacota o repositório em um arquivo | [docs/07-repomix.md](docs/07-repomix.md) |
| ast-grep | Busca e reescrita por estrutura de código | [docs/08-ast-grep.md](docs/08-ast-grep.md) |
| Context7 | Documentação atual de bibliotecas | [docs/09-context7.md](docs/09-context7.md) |
| RTK | Compressão da saída de comandos | [docs/10-rtk.md](docs/10-rtk.md) |
| ripgrep | Linha de base: quando grep já basta | [docs/11-ripgrep-linha-de-base.md](docs/11-ripgrep-linha-de-base.md) |

O [docs/README.md](docs/README.md) tem o índice por tipo, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/code-indexes ~/.claude/skills/code-indexes
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é entender uma base grande, indexar código, reduzir leituras ou gastos de contexto, ou escolher um MCP de código. Também dá para chamar direto com `/code-indexes`. Exemplos:

- "Esse monorepo é enorme, como o agente acha as coisas mais rápido?"
- "Qual MCP de código eu uso para refatorar com segurança?"
- "/code-indexes o agente está gastando muito contexto com grep neste projeto."

Com a skill carregada, o Claude:

1. mede a base (tamanho, linguagens, monorepo) e a tarefa, e vê o que já está instalado;
2. testa a linha de base: em base pequena, fica com grep e leitura direta;
3. escolhe a ferramenta pela tabela do [SKILL.md](SKILL.md);
4. lê o documento da ferramenta antes de instalar e confere licença e privacidade;
5. liga a ferramenta e confere o custo de contexto com `/context`;
6. explica a escolha em uma ou duas frases.

## Estrutura

```
code-indexes/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md             índice, "Qual escolher" e o que saiu da lista
    ├── 01-codegraph.md
    ├── 02-lsp-claude-code.md
    ├── 03-serena.md
    ├── 04-claude-context.md
    ├── 05-codebase-memory-mcp.md
    ├── 06-gitnexus.md
    ├── 07-repomix.md
    ├── 08-ast-grep.md
    ├── 09-context7.md
    ├── 10-rtk.md
    └── 11-ripgrep-linha-de-base.md
```

## Como manter

- **Adicionar uma ferramenta:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua a ferramenta nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover uma ferramenta:** apague o documento, tire-a das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** licenças, comandos e números foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar. Números de economia de tokens são alegações dos projetos; só troque por medição com fonte.
