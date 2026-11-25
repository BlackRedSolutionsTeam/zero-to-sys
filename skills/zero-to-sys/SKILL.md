---
name: zero-to-sys
description: Orquestra a criação de um sistema do zero até produção, decidindo a ordem em que as outras skills deste repositório entram (product, stacks, architecture, data, ia, code-indexes, coding, user-experience, design-systems, design, infra) a partir do contexto do projeto. Use sempre que o usuário pedir para "criar um sistema do zero", "começar um projeto novo", "montar um SaaS/app/site do zero", "por onde eu começo", "monta tudo para mim" ou invocar /zero-to-sys; também quando um projeto existente precisa ser reorganizado de ponta a ponta.
---

# zero-to-sys

Skill principal. Não decide stack, pasta, código, visual nem infra: ela descobre o contexto, define quais skills entram, em que ordem, e o que cada uma entrega para a próxima. Cada decisão técnica é da skill da área.

| Skill | Pasta | Responde |
|---|---|---|
| `product` | [product/](../product/SKILL.md) | O que construir: MVP, fluxos, regras, histórias e backlog |
| `stacks` | [stacks/](../stacks/SKILL.md) | Qual stack completa usar |
| `architecture` | [architecture/](../architecture/SKILL.md) | Como organizar pastas e arquivos |
| `data` | [data/](../data/SKILL.md) | Como modelar tabelas, migrations e isolamento por cliente |
| `ia` | [ia/](../ia/SKILL.md) | Como configurar e usar o agente no projeto |
| `code-indexes` | [code-indexes/](../code-indexes/SKILL.md) | Se e qual índice de código usar |
| `coding` | [coding/](../coding/SKILL.md) | Como escrever o código |
| `user-experience` | [user-experience/](../user-experience/SKILL.md) | Como a experiência muda entre celular, tablet e desktop |
| `design-systems` | [design-systems/](../design-systems/SKILL.md) | Qual layout cada tela deve ter, com exemplo pronto |
| `design` | [design/](../design/SKILL.md) | Quais UI kits e ícones usar |
| `infra` | [infra/](../infra/SKILL.md) | Onde e como pôr em produção |

## Passo 0 — Descobrir o contexto

Antes de disparar qualquer skill, levante estes pontos. Leia primeiro o que já existe na pasta (`package.json`, `*.csproj`, `pyproject.toml`, `go.mod`, `CLAUDE.md`, `AGENTS.md`, `.claude/`, `README`); pergunte ao usuário só o que não der para descobrir, tudo de uma vez.

| Ponto | Por que importa | Exemplos |
|---|---|---|
| Tipo de projeto | Define stack, design e infra | Site de conteúdo, landing, SaaS, painel admin, sistema interno, API, mobile, desktop, CLI |
| Tem interface? | Decide se `design` entra | Web, mobile, nenhuma (API, CLI, worker) |
| O que o time já sabe | Pesa mais que a moda na stack | "Só .NET", "React e Node", "sozinho, sei Python" |
| Porte e prazo | Define o nível da infra e da arquitetura | MVP em semanas, produto em crescimento, corporativo |
| Restrições | Cortam opções antes de escolher | Orçamento zero, nuvem obrigatória (Azure, AWS), dados sensíveis, LGPD, on-premise |
| Projeto novo ou existente | Muda a ordem (ver "Projeto existente") | Pasta vazia, repositório com código |

Se o usuário já decidiu algo (stack, hospedagem, UI kit), registre como fixo e não rediscuta: a skill da área só valida e completa.

### Entender como o cliente quer que o sistema funcione

Os pontos acima dizem como construir. Antes de fixar a stack, entenda também o que o sistema precisa fazer, porque é isso que muda a stack, a arquitetura e a infra. Pergunte só o que ainda for dúvida depois de ler o pedido e o que já existe na pasta: se o pedido já responde, não pergunte.

| Tema | O que descobrir | Muda o quê |
|---|---|---|
| Problema e público | Que problema resolve, para quem, quem paga | Escopo do MVP, tom do design |
| Usuários e acessos | Tipos de usuário, login (e-mail, Google, SSO da empresa), papéis e permissões, multiempresa (cada cliente vê só os seus dados) | Auth, modelo de dados, arquitetura |
| Funcionalidades principais | As 3 a 5 coisas que o usuário faz no dia a dia; o fluxo principal, passo a passo | Módulos e pastas, ordem de construção |
| Dados | O que guarda, volume esperado, dados pessoais ou sensíveis, histórico e auditoria | Banco, backup, LGPD, segurança |
| Integrações | Pagamento, e-mail, WhatsApp, ERP, APIs de terceiros, importar planilha | Stack do backend, segredos, MCP |
| Tempo real e tarefas em segundo plano | Notificações, chat, painéis ao vivo, relatórios demorados, rotinas agendadas | Stack, filas, infra |
| Onde o usuário usa | Navegador no computador, celular, app instalado, offline | Web, mobile ou desktop; design |
| Visual | Marca, cores, referências de sites que o cliente gosta | `design` |
| Escala e disponibilidade | Quantos usuários no início e em um ano; o que acontece se ficar fora do ar | Porte da infra |
| Orçamento e operação | Quanto pode gastar por mês, quem vai manter depois | Hospedagem, complexidade aceitável |

Como perguntar:

- **Só o que for dúvida de verdade.** Se a resposta tem um padrão sensato para o tipo de projeto, assuma o padrão e diga qual assumiu, em vez de perguntar.
- **Tudo de uma vez, em no máximo duas rodadas.** Junte as perguntas numa mensagem (ou na ferramenta de perguntas, se houver), agrupadas por tema, cada uma com 2 a 4 opções e a recomendada primeiro. Uma segunda rodada só se a primeira abrir uma dúvida nova.
- **Linguagem do cliente, não do dev.** Pergunte "cada empresa cliente vê só os próprios dados?", não "precisa de multi-tenancy?". Explique o termo técnico quando ele for inevitável.
- **Pergunte o porquê quando a resposta for vaga.** "Precisa de app" pode ser "o usuário usa no celular", e um site responsivo resolve.
- **Feche com um resumo.** Antes da fase 1, mostre em poucas linhas o que entendeu (público, funcionalidades do MVP, integrações, restrições e o que foi assumido) e peça o ok. Esse resumo é o que passa para todas as fases.
- **Dúvida que surgir depois, pergunte na hora.** Se uma fase esbarrar numa decisão que depende do cliente e não há padrão seguro, pare e pergunte em vez de inventar.

## Ordem de disparo — projeto novo

Siga as fases em ordem. Cada fase só começa com a saída da anterior em mãos. Pule a fase quando a condição de "Pule se" valer, e diga ao usuário que pulou e por quê.

| # | Skill | Entra com | Entrega | Pule se |
|---|---|---|---|---|
| 0 | `product` | Resumo aprovado do passo 0 | Escopo do MVP (dentro, fora, depois), fluxo principal, regras de negócio, histórias com critérios de aceite e `BACKLOG.md` em ordem de construção | Site de conteúdo simples: basta a lista de páginas |
| 1 | `stacks` | Contexto, resumo aprovado e escopo da fase 0 | Stack completa: front, back, banco, ORM, auth, testes | A stack já foi decidida e está completa |
| 2 | `architecture` | Stack escolhida, porte | Árvore de pastas, padrão (feature-first, monólito modular, monorepo…), `ARCHITECTURE.md` | Nunca em projeto novo |
| 2b | `data` | Regras de negócio e histórias da fase 0, stack e ORM | Modelo de dados com diagrama, decisão de multiempresa, primeira migration e seed, banco recriável com um comando | Projeto sem banco (site estático, CLI sem estado) |
| 3 | `ia` | Stack, árvore, comandos | `CLAUDE.md`/`AGENTS.md` enxuto, permissões, hooks básicos (format, typecheck no `Stop`) | Nunca: é o que faz as fases seguintes saírem certas |
| 4 | `code-indexes` | Linguagem, tamanho esperado da base | Decisão de índice (ou "ripgrep basta") e a ligação no Claude Code | Base pequena e nova: anote para rever quando crescer |
| 5 | `coding` | Stack, árvore, `CLAUDE.md` | Lint e format configurados, padrão de erros, validação na borda, testes, Conventional Commits | Nunca |
| 6 | `user-experience`, `design-systems`, depois `design` | Tipo de projeto, funcionalidades do resumo, stack de front, marca do cliente | Dispositivo principal e o que muda em cada tamanho (`user-experience`); layout de cada tela e tokens da marca (`design-systems`); UI kit e set de ícones para montá-las (`design`) | Projeto sem interface (API, CLI, worker, biblioteca) |
| 7 | `infra` | Stack, porte, restrições | Hospedagem, banco gerenciado, CI/CD, segredos, observabilidade, backup, segurança base | Só se o usuário disse que é local ou protótipo descartável; mesmo assim, entregue o CI (fase 7 parcial) |

Depois da fase 7, volte à `ia` uma vez: com o projeto rodando, veja os sinais de "Quando criar cada recurso" (skills, subagentes, hooks, MCP) e proponha o que fizer sentido.

### Por que essa ordem

- **Stack antes de tudo:** pasta, lint, UI kit e hospedagem dependem dela.
- **Arquitetura antes da IA:** o `CLAUDE.md` cita comandos e convenções que só existem depois da árvore.
- **IA e índice antes do código:** o agente escreve o resto do projeto; configurado cedo, erra menos e gasta menos.
- **Dispositivo antes de layout, layout antes de componente:** dentro da fase 6, `user-experience` define para quais dispositivos projetar e qual é o principal; `design-systems` define a estrutura de cada tela e os tokens; só depois `design` escolhe com o que montar.
- **Coding antes do design:** lint, testes e padrão de erros valem também para os componentes de tela.
- **Infra por último, mas não esquecida:** a escolha de hospedagem pode pedir ajuste no código (variáveis de ambiente, Docker, healthcheck); faça antes do primeiro deploy, não depois.

### Atalhos por tipo de projeto

| Projeto | Fases | Observação |
|---|---|---|
| Site de conteúdo, blog, landing | 1 → 2 → 3 → 5 → 6 → 7 | Pule `code-indexes`; infra costuma ser PaaS ou estático |
| MVP de SaaS | 1 → 2 → 3 → 5 → 6 → 7 → 4 | Índice só quando a base crescer |
| SaaS em crescimento, sistema corporativo | 1 → 2 → 3 → 4 → 5 → 6 → 7 | Todas; arquitetura e infra com mais peso |
| API, worker, CLI | 1 → 2 → 3 → 4 → 5 → 7 | Sem a fase 6 (`user-experience`, `design-systems` e `design`) |
| Mobile, desktop | 1 → 2 → 3 → 5 → 6 → 7 | Infra cobre só o backend e o CI de build |

## Projeto existente

Quando a pasta já tem código, a ordem inverte: primeiro entender, depois mudar.

1. `ia` e `code-indexes`: configure o agente e, em base grande ou desconhecida, o índice, para ler o projeto com menos tokens.
2. `architecture`: compare a estrutura atual com a recomendada para a stack. Proponha a mudança em passos; não mova tudo de uma vez.
3. `coding`: lint, format e testes antes de refatorar.
4. `user-experience`, `design-systems`, `design` e `infra`: só se o pedido cobre essas áreas.
5. `stacks`: só se o usuário quer trocar ou acrescentar uma tecnologia. Não proponha trocar a stack por conta própria.

## Regras de uso

- **Uma skill por vez, na ordem.** Leia o `SKILL.md` da skill da fase e siga o "Como usar" dela; não decida a área por conta própria nesta skill.
- **Passe o contexto adiante.** Ao abrir cada fase, resuma em poucas linhas o que as anteriores decidiram (stack, árvore, comandos). A skill seguinte depende disso.
- **Confirme as decisões grandes.** Mostre e espere o ok antes de: fixar a stack (fase 1), criar a árvore de pastas (fase 2) e qualquer coisa que gere custo ou conta externa (fase 7). O resto segue direto.
- **O que o usuário fixou não se rediscute.** Se uma escolha fixa conflita com a recomendação de uma skill, diga o risco em uma frase e siga a escolha do usuário.
- **Requisitos do cliente guiam cada fase.** Ao escolher entre duas opções numa fase, a que atende melhor ao resumo aprovado no passo 0 ganha da que é só mais popular.
- **Registre as decisões no projeto.** O resumo do passo 0 (o que o sistema faz e para quem) vai no `README`. Stack, padrão de arquitetura e hospedagem vão no `ARCHITECTURE.md` (ou `README`); comandos e armadilhas no `CLAUDE.md`/`AGENTS.md`. Não crie documento de planejamento separado.
- **Não pule a verificação.** Ao fim de cada fase, rode o que der para rodar (instalar, build, lint, teste, abrir a página) antes de passar à próxima.
- **Mostre o progresso.** Diga em uma linha a fase em que está e as que faltam, por exemplo: "Fase 3 de 7 (ia). Faltam: coding, design, infra".

## Quando a lista não cobre

Se o projeto pede uma área sem skill aqui (dados e analytics, pagamentos, compliance específico, app de jogos, hardware), diga isso ao usuário, cubra com a documentação oficial da ferramenta e siga a ordem das fases para o resto.

## Validade dos dados

Esta skill não traz preços, versões nem comandos: eles ficam nas skills de cada área, verificados em 2026-11-24. Confira a linha "Verificado em" de cada documento antes de afirmar algo decisivo.
