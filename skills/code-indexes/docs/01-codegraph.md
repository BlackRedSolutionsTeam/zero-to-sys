# CodeGraph

> Servidor MCP que mantém um grafo de conhecimento do código em SQLite (símbolos, arestas e arquivos) e responde com o código-fonte dos símbolos, o caminho de chamadas e o raio de impacto, em vez de o agente fazer grep e ler arquivos.

| | |
|---|---|
| **Site/repositório** | https://github.com/colbymchenry/codegraph |
| **Categoria** | Grafo de código |
| **Tipo** | Índice AST/grafo (parser nativo em Rust, segundo o README) |
| **Como se conecta** | MCP (`codegraph serve --mcp`), instalado por `codegraph install` |
| **Linguagens suportadas** | Cerca de 35 (TypeScript, JavaScript, Python, Go, Rust, Java, C#, PHP, Ruby, C/C++, Swift, Kotlin, Scala, Dart, Vue, Svelte, Terraform, Solidity e outras) |
| **Preço** | Grátis |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

CodeGraph indexa o projeto uma vez e guarda símbolos, chamadas e dependências em um banco SQLite local, dentro da pasta do projeto. Um observador de arquivos mantém o índice atualizado (o README fala em re-sincronizar um arquivo salvo em menos de um segundo, com debounce padrão de 2 segundos).

Por padrão o servidor MCP expõe uma única ferramenta, `codegraph_explore`. Ela aceita uma pergunta em linguagem natural ou nomes de símbolos e devolve o código-fonte numerado dos símbolos relevantes, o caminho de chamadas entre eles e um resumo do que depende deles. Outras ferramentas (`codegraph_node`, `codegraph_search`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files`, `codegraph_status`) podem ser religadas pela variável `CODEGRAPH_MCP_TOOLS`.

## Por que usar

- **Menos voltas:** uma chamada devolve código, relações e impacto, no lugar de uma sequência de grep e leituras.
- **Uma só ferramenta listada por padrão** (`codegraph_explore`), segundo o README; as outras ficam fora da lista.
- **Local:** o README afirma que nenhum dado sai da máquina e que não há chave de API.
- **Cobre muitas linguagens** (cerca de 35 na lista do README), com extração estrutural e resolução cross-file para todas.

## Quando usar

- Base média ou grande onde o agente gasta muitas chamadas só para se localizar.
- Perguntas de "como X funciona" e "o que quebra se eu mudar Y".
- Antes de editar: ver quem chama o símbolo e o que ele afeta.
- Projetos em que se quer o mesmo índice para Claude Code, Codex, Cursor e Gemini.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | O projeto mediu 88% menos chamadas de ferramenta e 62% menos tokens em sete repositórios abertos; é alegação do autor (README) |
| Monorepo grande | ✅ Ótimo | O README cita o kernel Linux (~70 mil arquivos) indexado em menos de 12 min num VPS de 2 núcleos |
| Base desconhecida | ✅ Ótimo | `codegraph_explore` aceita pergunta em linguagem natural e devolve código, caminho de chamadas e dependentes (README) |
| Refatoração com impacto | ✅ Ótimo | A mesma resposta traz o resumo do que depende dos símbolos (README, `codegraph_explore`) |
| Busca por texto exato | ❌ Evite | Indexa símbolos, chamadas e dependências, não texto livre (README) |
| Linguagem pouco comum | 🟡 Serve | Cobertura de cross-file varia por linguagem (Liquid 73,8% e Pascal/Delphi 77,4% no README); confira a sua |
| Código com injeção de dependência/reflexão | 🟡 Serve | O README atribui o resíduo de cobertura a despacho dinâmico, reflexão/DI e entradas por convenção de framework |
| Código que não pode sair da máquina | ✅ Ótimo | O README afirma que nenhum dado sai da máquina; há telemetria anônima ligada por padrão, que se desliga (README) |

## Quando é bom

- **Instalação guiada** e índice com atualização automática.
- **Resposta única e já com código**, o que reduz leituras de arquivo.
- **Números publicados com método:** o projeto roda Claude Opus 4.8 em sete repositórios abertos, com e sem CodeGraph, mediana de 4 execuções por braço, e informa 88% menos chamadas de ferramenta, 62% menos tokens e 44% mais barato. Isso é alegação do próprio projeto, medida pelo autor. No Django o ganho foi de só 13% de custo.
- **Comunidade grande** (cerca de 78,6 mil estrelas na leitura do README, 78.620 no GitHub em 2026-11-24).

## Quando é ruim

- **Pontos cegos da análise estática:** despacho dinâmico, reflexão, contêineres de DI e entradas por convenção de framework. O README mede a cobertura de cross-file por linguagem em repositórios de referência, de 73,8% (Liquid) a 100% (Python, PHP, Ruby, Svelte), e diz que o resíduo é fronteira de análise estática (despacho dinâmico, reflexão/DI, entradas por convenção de framework).
- **Arquivos acima de 1 MB são ignorados.**
- **Resultados podem ficar defasados** na janela do debounce, e a saída nem sempre avisa.
- **Mais contexto residente:** o README diz que fica cerca de 80% mais contexto de recuperação ao fim da sessão (67 mil contra 18 mil tokens no VS Code). O custo é trocado por menos chamadas.
- **Um escritor MCP por projeto**; em WSL2 com projeto em `/mnt/` ou em rede, o banco pode falhar.
- **Telemetria anônima de uso ligada por padrão**; desligue com `codegraph telemetry off`, `CODEGRAPH_TELEMETRY=0` ou `DO_NOT_TRACK=1`.
- Última versão: v1.6.4, de 2026-11-20 (conferido em 2026-11-24); use `codegraph upgrade`.

## Como começar

```bash
npm i -g @colbymchenry/codegraph
# ou: curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
codegraph install        # escolha Claude Code; grava o MCP em ~/.claude.json
cd seu-projeto
codegraph init           # constrói o índice (a sincronização automática vem ligada)
```

Ligação manual: em `~/.claude.json`, em `mcpServers`, comando `codegraph` com args `["serve", "--mcp"]`. Confira com `/mcp` no Claude Code.

## Combina com / alternativas

- [LSP nativo do Claude Code](02-lsp-claude-code.md): tipos e diagnósticos exatos; o grafo dá a visão ampla.
- [ripgrep](11-ripgrep-linha-de-base.md): texto exato e configs, que o grafo não indexa.
- Alternativas parecidas: [codebase-memory-mcp](05-codebase-memory-mcp.md) e [GitNexus](06-gitnexus.md).

## Decisão rápida

- **Use se:** a base é média ou grande, o agente se perde em grep e leitura, e você quer um índice local sem chave de API.
- **Evite se:** a base é minúscula, o trabalho é busca de texto literal, ou você precisa de resolução semântica exata de tipos (use LSP).
