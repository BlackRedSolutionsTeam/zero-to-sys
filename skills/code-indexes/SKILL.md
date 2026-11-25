---
name: code-indexes
description: Escolhe a ferramenta de indexação de código ou de economia de tokens para o Claude Code entender uma base com menos leituras (CodeGraph, LSP nativo, Serena, Claude Context, codebase-memory-mcp, GitNexus, Repomix, ast-grep, Context7, RTK, ripgrep). Use quando o agente gasta muitas chamadas de grep e leitura, quando a base é grande ou desconhecida, antes de uma refatoração com impacto, para responder perguntas de arquitetura, ao pedir "indexar o código", "economizar tokens", "reduzir contexto", "qual MCP de código usar", "mapa do repositório" ou "entender esse projeto".
---

# code-indexes

Guia de decisão para escolher como o agente lê e navega o código: grafo, LSP, embeddings, empacotador, busca estrutural, documentação de bibliotecas e compressão de saída. Cada ferramenta tem um documento em `docs/` com o tipo de índice, o que precisa para rodar, se o código sai da máquina, quando ganha e quando perde.

## Como usar esta skill

1. **Meça a base e a tarefa antes de escolher:** número aproximado de arquivos, linguagens, se é monorepo, se o código pode sair da máquina e qual é a pergunta (entender, achar texto, refatorar, migrar padrão, usar biblioteca). Veja o que já está instalado em `/mcp` e `/plugin`; o que já está ligado tem prioridade.
2. **Comece pela linha de base.** Em base pequena, grep e leitura direta bastam (doc 11). Só indexe se o agente estiver gastando muitas voltas.
3. **Escolha pela tabela abaixo.**
4. **Leia o documento de cada ferramenta escolhida** antes de instalar, principalmente "Para que tipo de base/tarefa", "Quando é ruim" e "Como começar".
5. **Instale pelos comandos do documento.** Confira a versão na documentação oficial antes de rodar.
6. **Confira o custo:** depois de ligar um MCP, veja `/context` para saber quanto de contexto ele usa.
7. **Explique a escolha ao usuário em uma ou duas frases.**

## Qual ferramenta usar

| Base / pergunta | Ferramenta |
|---|---|
| Base pequena (cabe na cabeça), qualquer pergunta | ripgrep e leitura direta (11); nada de índice |
| Texto exato: erro, variável de ambiente, rota, config | ripgrep (11) |
| Base média ou grande, entender fluxo e achar onde mexer | CodeGraph (01); alternativas: codebase-memory-mcp (05) |
| Monorepo grande com código e infraestrutura | codebase-memory-mcp (05) ou CodeGraph (01) |
| Base desconhecida, pergunta em linguagem natural, sem nome de símbolo | CodeGraph (01); Claude Context (04) se aceitar serviço externo |
| Linguagem tipada, erros de tipo após cada edição, referências exatas | LSP nativo do Claude Code (02) |
| Edição e renomeação por símbolo, linguagem fora do LSP nativo | Serena (03) |
| Refatoração com impacto | CodeGraph (01) para o raio de impacto, LSP (02) para referências exatas |
| Migração de padrão em muitos arquivos | ast-grep (08) |
| Entregar a base inteira (ou comprimida) a um modelo, revisar repositório externo | Repomix (07) |
| Usar biblioteca nova ou que mudou de versão | Context7 (09) |
| Sessões com muito git, teste e build de saída longa | RTK (10) |
| Código sigiloso | Só ferramentas locais: 01, 02, 03, 05, 07, 08, 10, 11 |
| Projeto de empresa ou comercial | Evite GitNexus (06): licença não comercial |

| Ferramenta | Documento | Tipo |
|---|---|---|
| CodeGraph | [docs/01-codegraph.md](docs/01-codegraph.md) | Grafo AST em SQLite, MCP |
| LSP nativo do Claude Code | [docs/02-lsp-claude-code.md](docs/02-lsp-claude-code.md) | Servidor de linguagem, plugin |
| Serena | [docs/03-serena.md](docs/03-serena.md) | LSP com edição simbólica, MCP |
| Claude Context | [docs/04-claude-context.md](docs/04-claude-context.md) | Embeddings, banco vetorial, MCP |
| codebase-memory-mcp | [docs/05-codebase-memory-mcp.md](docs/05-codebase-memory-mcp.md) | Grafo AST com infraestrutura, MCP |
| GitNexus | [docs/06-gitnexus.md](docs/06-gitnexus.md) | Grafo com fluxos, licença não comercial |
| Repomix | [docs/07-repomix.md](docs/07-repomix.md) | Empacotador de repositório |
| ast-grep | [docs/08-ast-grep.md](docs/08-ast-grep.md) | Busca e reescrita estrutural, CLI |
| Context7 | [docs/09-context7.md](docs/09-context7.md) | Documentação de bibliotecas, serviço |
| RTK | [docs/10-rtk.md](docs/10-rtk.md) | Compressão da saída de comandos |
| ripgrep | [docs/11-ripgrep-linha-de-base.md](docs/11-ripgrep-linha-de-base.md) | Linha de base, texto |

## Regras de uso

- **Grep primeiro em base pequena.** Indexar uma base que cabe no contexto só cria peça para manter.
- **Um índice de código por projeto.** CodeGraph, codebase-memory-mcp e GitNexus fazem trabalho parecido; ligar dois duplica ferramentas (os três expõem consulta de chamadas e impacto: docs 01, 05 e 06).
- **LSP nativo ou Serena para a mesma linguagem, não os dois.**
- **Meça o custo** com `/context` depois de ligar qualquer MCP. Por padrão o Claude Code adia as definições das ferramentas MCP (tool search): só nomes e instruções do servidor carregam no início (code.claude.com/docs/en/mcp, "Scale with MCP tool search"); `ENABLE_TOOL_SEARCH=false` carrega tudo.
- **Número de economia só com fonte.** As cifras dos projetos (porcentagem de tokens) são alegações deles, feitas em cenários próprios. Não prometa o mesmo resultado ao usuário.
- **Privacidade primeiro.** Confirme se o código sai da máquina (embeddings, serviços hospedados, telemetria) antes de ligar. Claude Context e Context7 usam serviços externos no padrão.
- **Licença antes de adotar.** GitNexus é não comercial; Serena é GPL-3.0; RTK tem partes em BUSL-1.1.
- **Índice não substitui leitura.** Antes de editar, leia o trecho que o índice devolveu; análise estática não vê injeção de dependência, reflexão nem despacho dinâmico.
- **Grafo não acha texto.** Strings, configs e docs ficam com ripgrep.
- **Não deixe ferramenta alterar o repositório sem avisar.** `npx gitnexus analyze` escreve `AGENTS.md` e `CLAUDE.md`; use `--index-only`.
- **Fronteira com a skill `ia`:** subagentes, MCP em geral, hooks e gestão de contexto são da skill `ia`. Aqui só entra o que indexa ou comprime código e saída.

## Quando a lista não cobre

Se a necessidade está fora destas onze ferramentas (busca em vários repositórios hospedados, análise de segurança, indexação de bancos de dados), diga isso ao usuário em vez de forçar uma delas. O `docs/README.md` registra o que foi avaliado e saiu, com o motivo.

## Validade dos dados

Licenças, comandos, linguagens e números dos documentos foram verificados em 2026-11-24, nos repositórios e na documentação oficial. A tabela de escolha e as regras acima resumem os fatos citados em cada documento de `docs/`, que trazem a fonte. Este setor muda rápido: antes de afirmar versão, licença ou preço ao usuário, confira no repositório se a informação for decisiva.
