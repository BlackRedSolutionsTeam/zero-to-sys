# Context7

> Serviço da Upstash que entrega ao agente a documentação atual e os exemplos de código da versão certa de uma biblioteca, em vez de ele adivinhar ou fazer buscas na web.

| | |
|---|---|
| **Site/repositório** | https://github.com/upstash/context7 (painel e chave em context7.com/dashboard) |
| **Categoria** | Documentação de bibliotecas |
| **Tipo** | Busca de documentação hospedada; não indexa o seu código |
| **Como se conecta** | MCP remoto (`https://mcp.context7.com/mcp`) ou `npx ctx7 setup --claude` |
| **Linguagens suportadas** | Não se aplica ao seu código; cobre a documentação de bibliotecas publicadas |
| **Preço** | Chave grátis para limites maiores; plano grátis com 1.000 chamadas de API por mês e só repositórios públicos; Pro a US$ 10 por usuário/mês (conferido em context7.com/plans em 2026-11-24) |
| **Licença** | MIT (servidor MCP); API, motor de análise e de coleta são privados |
| **Verificado em** | 2026-11-24 |

## O que é

O servidor MCP expõe duas ferramentas: `resolve-library-id`, que converte um nome de biblioteca em um identificador, e `query-docs`, que traz trechos de documentação para esse identificador e a pergunta. O agente usa isso antes de escrever código com uma API que pode ter mudado.

Não é índice do seu projeto. Ele cuida da outra metade do problema: a documentação de fora, que o modelo conhece só até a data de treino.

## Por que usar

- **Alvo declarado:** o README diz que LLMs usam informação desatualizada e que o Context7 traz documentação e exemplos atuais e da versão certa ("no hallucinated APIs" é alegação do projeto).
- **Só duas ferramentas MCP** (`resolve-library-id`, `query-docs`).
- Cerca de 65,4 mil estrelas (65.414 no GitHub em 2026-11-24).

## Quando usar

- Biblioteca que muda rápido (frameworks, SDKs, ferramentas de build).
- Versão recente, posterior ao treino do modelo.
- Ao escrever integração com uma API de terceiros.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base desconhecida | ❌ Evite | Busca documentação hospedada de bibliotecas; não indexa o seu código (README) |
| Linguagem/biblioteca pouco comum | 🟡 Serve | A página inicial context7.com não publica o total de bibliotecas (conferido em 2026-11-24) |
| Atualização de versão de biblioteca | ✅ Ótimo | O README diz que LLMs usam informação desatualizada e que o Context7 traz documentação da versão certa |
| Código que não pode sair da máquina | 🟡 Serve | MCP remoto (`https://mcp.context7.com/mcp`): as consultas vão ao serviço (README) |

## Quando é bom

- Resolve um problema que nenhum índice local resolve.
- Instalação em um comando (`npx ctx7 setup`, que exige Node.js 22.13 ou mais, segundo o README).
- Código do servidor MCP aberto.

## Quando é ruim

- **Serviço externo:** as perguntas saem da máquina; política de retenção de dados não descrita na página lida.
- **Depende do catálogo e da qualidade da documentação indexada.**
- **Plano grátis limitado:** 1.000 chamadas de API por mês, e o usuário grátis é bloqueado ao atingir o limite mensal (context7.com/plans, 2026-11-24).
- **A parte importante é privada** (API e motor de coleta): você não controla a versão da documentação servida.
- Economia de tokens: sem número confirmado.

## Como começar

```bash
npx ctx7 setup --claude
```

O comando autentica por OAuth, gera uma chave de API e instala uma skill (ou configura o modo MCP, à escolha). Manual: use a URL `https://mcp.context7.com/mcp` com o cabeçalho `Authorization: Bearer <chave>`; o comando exato de `claude mcp add` não consta na página lida, confira na documentação.

## Combina com / alternativas

- [CodeGraph](01-codegraph.md) e [LSP](02-lsp-claude-code.md): entendem o seu código; o Context7 entende as bibliotecas.
- Alternativa de fora: busca na web do próprio agente, mais lenta e mais ruidosa.
- Sobre MCP em geral e gestão de contexto: veja a skill `ia`.

## Decisão rápida

- **Use se:** o projeto usa bibliotecas novas ou que mudam de versão e o agente erra APIs.
- **Evite se:** o problema é navegar no seu código, ou nada de pergunta pode sair da rede.
