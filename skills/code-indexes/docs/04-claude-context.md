# Claude Context

> Plugin MCP da Zilliz que indexa o código em um banco vetorial e permite buscar trechos por significado, para o agente não carregar pastas inteiras.

| | |
|---|---|
| **Site/repositório** | https://github.com/zilliztech/claude-context |
| **Categoria** | Busca semântica/embeddings |
| **Tipo** | Índice vetorial (embeddings) com divisão de código por AST |
| **Como se conecta** | MCP: `claude mcp add claude-context ... -- npx @zilliz/claude-context-mcp@latest` |
| **Linguagens suportadas** | TypeScript, JavaScript, Python, Java, C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin, Scala e Markdown (outras com divisor de texto genérico) |
| **Preço** | O projeto é grátis; Zilliz Cloud tem plano grátis (5 GB, 2,5 mi de vCUs por mês, até 5 coleções; conferido em 2026-11-24) e a API de embeddings tem custo próprio, que depende do provedor |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Claude Context quebra o código em trechos (por AST, com divisor de reserva), gera embeddings e guarda tudo em um banco vetorial (Zilliz Cloud ou Milvus próprio). O agente pergunta em linguagem natural e recebe os trechos mais parecidos.

O README pede Node.js 20 ou mais, uma chave da OpenAI para o modelo de embedding padrão (também há VoyageAI, Ollama e Gemini) e um banco vetorial.

## Por que usar

- **Busca por significado:** acha código sem saber o nome do símbolo.
- **Base muito grande:** evita carregar diretórios para achar um ponto de partida.
- **Provedores trocáveis**, incluindo Ollama para embedding local.
- **Número do projeto:** o README fala em cerca de 40% menos tokens com a mesma qualidade de recuperação, numa avaliação controlada. É alegação do projeto. A metodologia está em `evaluation/README.md`: 30 instâncias do SWE-bench Verified (dificuldade de 15 a 60 minutos, 2 arquivos modificados), GPT-4o-mini, um agente com read, grep e edit contra o mesmo agente com o Claude Context, 3 execuções por método. Resultado do README: 73.373 tokens médios contra 44.449 (-39,4%), F1 de 0,40 nos dois.

## Quando usar

- Base grande e pouco conhecida, em que o agente não sabe o que procurar.
- Perguntas conceituais ("onde se trata expiração de sessão?").
- Equipe que já tem Milvus ou Zilliz.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base pequena | ❌ Evite | Exige chave de embeddings (OpenAI por padrão) e banco vetorial (README) |
| Base média/grande | ✅ Ótimo | Na pasta `evaluation`, 30 instâncias do SWE-bench Verified: tokens médios de 73.373 para 44.449 (-39,4%) e F1 de 0,40 nos dois, com GPT-4o-mini (evaluation/README.md; avaliação do próprio projeto) |
| Base desconhecida | ✅ Ótimo | O agente pergunta em linguagem natural e recebe os trechos mais parecidos (README) |
| Refatoração com impacto | ❌ Evite | Devolve os trechos mais parecidos; o README não promete exaustividade |
| Linguagem pouco comum | 🟡 Serve | Fora das linguagens listadas, usa divisor de texto genérico (README) |
| Código que não pode sair da máquina | ❌ Evite | No padrão, trechos vão à API de embeddings e ao Zilliz Cloud; o README lista Ollama como provedor de embeddings; o FAQ do repositório (docs/troubleshooting/faq.md) documenta o setup local: Milvus via Docker Compose (`MILVUS_ADDRESS=127.0.0.1:19530`) e Ollama (`EMBEDDING_PROVIDER=Ollama`, `OLLAMA_MODEL=nomic-embed-text`) |
| Base que muda o tempo todo | 🟡 Serve | Exige reindexação; o README anuncia indexação incremental por árvores de Merkle, só dos arquivos alterados |

## Quando é bom

- Funciona com outros agentes além do Claude Code.
- Licença MIT; cerca de 12,7 mil estrelas (12.724 no GitHub em 2026-11-24).

## Quando é ruim

- **Serviços externos e chaves:** OpenAI, Zilliz ou Milvus; mais peças para manter.
- **Privacidade:** o código vai para fora no setup padrão.
- **Custo recorrente** de embeddings e de banco vetorial (Zilliz tem plano grátis; o custo de embeddings depende do provedor e não tem valor fixo).
- **Busca por similaridade:** devolve os trechos mais parecidos, não uma lista completa de usos (o README não promete exaustividade).
- **Tempo de indexação** inicial, que depende do tamanho da base e do provedor de embeddings.
- Sem releases no GitHub; só tags (a mais recente, v0.1.17-rc.0). Último push em 2026-11-24 (conferido em 2026-11-24).

## Como começar

```bash
claude mcp add claude-context \
  -e OPENAI_API_KEY=sk-sua-chave \
  -e MILVUS_ADDRESS=endpoint-publico-do-zilliz-cloud \
  -e MILVUS_TOKEN=chave-do-zilliz-cloud \
  -- npx @zilliz/claude-context-mcp@latest
```

Depois, peça ao Claude para indexar o projeto e confira com `/mcp`. Os nomes exatos das ferramentas não foram confirmados; veja o README.

## Combina com / alternativas

- [ripgrep](11-ripgrep-linha-de-base.md): cobre o texto exato que embeddings erram.
- [CodeGraph](01-codegraph.md): relações exatas, sem serviço externo.
- Alternativa de fora: indexação semântica embutida em editores como Cursor.

## Decisão rápida

- **Use se:** a base é grande, as perguntas são conceituais e a política de privacidade aceita enviar trechos a um provedor.
- **Evite se:** a base é pequena, o código é sigiloso, ou você quer lista completa de usos.
