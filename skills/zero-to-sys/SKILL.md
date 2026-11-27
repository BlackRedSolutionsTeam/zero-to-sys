---
name: zero-to-sys
description: 'Orquestra a criação de um sistema do zero até produção: descobre o contexto, define as fases e as skills de cada uma, dispara os agentes do plugin em ondas paralelas e conduz o backlog item a item até staging. Use para "criar um sistema do zero", "por onde começo", "monta tudo" ou "implementa a próxima funcionalidade".'
---

# zero-to-sys

Skill principal. Não decide stack, pasta, código, visual nem infra: ela descobre o contexto, define quais skills entram, em que ordem, e o que cada uma entrega para a próxima. Cada decisão técnica é da skill da área.

Cada skill tem um agente especialista dono dela; a lista de skills de cada um está na tabela do arquivo dele em [`agents/`](../../agents/) (resumo no [documento 03](docs/03-especialistas-e-modos.md)). Abra o `SKILL.md` da skill pela ferramenta `Skill` (`zero-to-sys:<skill>`) ou em `skills/<skill>/SKILL.md`.

## Skills sob demanda

Estas skills não têm fase fixa: chame cada uma quando a condição valer.

| Skill | Quando entra |
|---|---|
| `ai-features` | Quando o produto tem chat, assistente, busca semântica, extração ou classificação com LLM |
| `invoicing` | Quando o sistema cobra e precisa emitir nota fiscal |
| `search` | Quando o produto precisa de busca com relevância, filtros e facetas |
| `messaging` | Quando fila do Postgres ou Redis não basta, ou há vídeo e chamadas |
| `performance` | Quando há lentidão, antes de escalar ou de um pico de uso |
| `operations` | Quando o sistema entra no ar e precisa ser operado |
| `maintenance` | Depois do lançamento, em rotina trimestral |
| `local-dev` | Ao montar o repositório e quando alguém novo entra no time |
| `legal` | Antes de abrir o produto ao público |
| `store-targets` | Depois da `product` e da `framia`, antes da `stacks`, sempre que o projeto pode virar app; gera o `docs/STORES.md` |
| `mobile-release` | Quando há app mobile para publicar |
| `desktop-release` | Quando há app desktop para publicar (loja ou download) |
| `admin-panel` | Quando o sistema tem clientes, cobrança ou operação que a equipe precisa gerir sem mexer no banco; entra no backlog como item próprio |

## Paralelismo e especialistas

Quando a ferramenta de agentes estiver disponível (Claude Code como sessão principal, ou Codex), não rode as fases em série: divida em partes e dispare em ondas os agentes do plugin.

| Tema | Documento |
|---|---|
| Limite pela máquina, ondas, fluxo de uma parte, conflitos | [docs/01-paralelismo-e-ondas.md](docs/01-paralelismo-e-ondas.md) |
| Modelo e esforço de cada chamada (Claude Code e Codex) | [docs/02-modelos-e-esforco.md](docs/02-modelos-e-esforco.md) |
| Agentes, modos, pedido e formato de resposta | [docs/03-especialistas-e-modos.md](docs/03-especialistas-e-modos.md) |

## Passo 0 — Descobrir o contexto

Antes de disparar qualquer skill, levante estes pontos. Leia primeiro o que já existe na pasta (`package.json`, `*.csproj`, `pyproject.toml`, `go.mod`, `CLAUDE.md`, `AGENTS.md`, `.claude/`, `README`); pergunte ao usuário só o que não der para descobrir, tudo de uma vez.

| Ponto | Por que importa | Exemplos |
|---|---|---|
| Tipo de projeto | Define stack, design e infra | Site de conteúdo, landing, SaaS, painel admin, sistema interno, API, mobile, desktop, CLI |
| Tem interface? | Decide se `design` entra | Web, mobile, nenhuma (API, CLI, worker) |
| O que o time já sabe | Pesa mais que a moda na stack | "Só .NET", "React e Node", "sozinho, sei Python" |
| Porte e prazo | Define o nível da infra e da arquitetura | MVP em semanas, produto em crescimento, corporativo |
| Onde vai ser publicado | Regras das lojas mudam login, cobrança e pacote (skill `store-targets`) | App Store, Google Play, Microsoft Store, Mac App Store, download no desktop, web |
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
| Domínio | Já tem domínio? Em nome de quem? E-mail com o domínio da empresa? | `domains`, `cloudflare` |
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
- **Feche com um resumo.** Antes da fase 0, mostre em poucas linhas o que entendeu (público, funcionalidades do MVP, integrações, restrições e o que foi assumido) e peça o ok. Esse resumo é o que passa para todas as fases.
- **Dúvida que surgir depois, pergunte na hora.** Se uma fase esbarrar numa decisão que depende do cliente e não há padrão seguro, pare e pergunte em vez de inventar.

## Ordem de disparo — projeto novo

Siga as fases em ordem. Cada fase só começa com a saída da anterior em mãos. Pule a fase quando a condição de "Pule se" valer, e diga ao usuário que pulou e por quê. A fase 1 prototipa o sistema inteiro no Framia e nenhum código é escrito antes dela ser aprovada. As fases 2 a 9 montam a base; a fase 10 constrói as funcionalidades, uma por vez.

| # | Skill | Entra com | Entrega | Pule se |
|---|---|---|---|---|
| 0 | `product` | Resumo aprovado do passo 0 | Escopo do MVP (dentro, fora, depois), fluxo principal, regras de negócio, histórias com critérios de aceite e `BACKLOG.md` em ordem de construção | Site de conteúdo simples: basta a lista de páginas |
| 1 | `framia` | Escopo, fluxo principal, regras de negócio e `BACKLOG.md` da fase 0; marca do cliente | Projeto no Framia aprovado pelo cliente: design system (tokens, temas, componentes), telas com estados e protótipo clicável, fluxos, banco e enums, rotas da API com perfis, requisitos ligados às telas; link do projeto no `README` e OpenAPI alvo no repositório | CLI ou biblioteca, sem tela, banco nem API. Em API ou worker, faça só banco, rotas, fluxos e requisitos |
| 2 | `stacks` | Contexto, resumo aprovado, escopo da fase 0, tamanho real do sistema no protótipo da fase 1 e destinos do `docs/STORES.md` (`store-targets`) | Stack completa: front, back, banco, ORM, auth, testes | A stack já foi decidida e está completa |
| 3 | `architecture` | Stack escolhida, porte | Árvore de pastas, padrão (feature-first, monólito modular, monorepo…), `ARCHITECTURE.md` e, em projeto com tela, `docs/MOTION.md` | Nunca em projeto novo |
| 4 | `data` | Regras de negócio e histórias da fase 0, diagrama do banco da fase 1, stack e ORM | Modelo de dados com diagrama, decisão de multiempresa, primeira migration e seed, banco recriável com um comando | Projeto sem banco (site estático, CLI sem estado) |
| 5 | `ia` | Stack, árvore, comandos | `CLAUDE.md`/`AGENTS.md` enxuto apontando para `BACKLOG.md` e regras, com a linha que aponta para o `docs/MOTION.md` em projeto com tela, permissões, hooks básicos (format, typecheck no `Stop`) | Nunca: é o que faz as fases seguintes saírem certas |
| 6 | `code-indexes` | Linguagem, tamanho esperado da base | Decisão de índice (ou "ripgrep basta") e a ligação no Claude Code | Base pequena e nova: anote para rever quando crescer |
| 7 | `coding`, depois `security` e `quality` | Stack, árvore, `CLAUDE.md`, papéis do produto | Lint e format, padrão de erros, validação na borda, Conventional Commits (`coding`); login, sessão, papéis e permissões base, rate limit e auditoria de dependências (`security`, pule em site sem login); CI com os gates de testes (`quality`) | Nunca em `coding` e `quality` |
| 8 | `user-experience`, `design-systems`, depois `design` | Tipo de projeto, fluxos da fase 0, telas, tokens e componentes aprovados na fase 1, stack de front, marca do cliente | Dispositivo principal, o que muda em cada tamanho e os tokens e padrões de movimento (`user-experience`); layout de cada tela e tokens da marca, os mesmos do protótipo (`design-systems`); UI kit e set de ícones para montá-las, com os componentes do protótipo reescritos nele (`design`) | Projeto sem interface (API, CLI, worker, biblioteca) |
| 9 | `infra`, com `domains` e `cloudflare`; em servidor próprio, `vps` e `nginx` | Stack, porte, restrições, domínio | Hospedagem, banco gerenciado, CI/CD, staging, segredos, observabilidade, backup, segurança base (`infra`); domínio, DNS e e-mail do domínio (`domains`); borda com SSL, cache e WAF (`cloudflare`); VPS preparada e nginx com HTTPS, quando não for PaaS (`vps`, `nginx`) | Só se o usuário disse que é local ou protótipo descartável; mesmo assim, entregue o CI (fase 9 parcial) |
| 10 | Construção (ciclo abaixo) | `BACKLOG.md` e tudo o que as fases 0 a 9 montaram | Cada item do backlog pronto, testado e em staging | Nunca: é aqui que o sistema existe |

Depois da fase 9, volte à `ia` uma vez: com o projeto rodando, veja os sinais de "Quando criar cada recurso" (skills, subagentes, hooks, MCP) e proponha o que fizer sentido.

### Fase 10 — ciclo por funcionalidade

Para cada item do `BACKLOG.md`, na ordem do backlog, rode os passos abaixo. Um item por vez: o próximo só começa quando o anterior fecha.

| Passo | Skill | O que fazer | Pule se |
|---|---|---|---|
| 1. Critério | `product` (e `framia`) | Releia a história e os critérios de aceite do item; se estiverem vagos, reescreva antes de codar. Leia o requisito do item no Framia (`get_requirement`): telas, estados e rotas desenhados | Nunca |
| 2. Dados | `data` | Tabelas, colunas e constraints que o item pede; migration e seed; checklist de tabela nova | O item não muda o banco |
| 3. Back | `api` (e `coding`; `security` para login e permissões; `integrations` se houver serviço externo) | Rota ou ação no padrão de rotas, erro e lista da API, validação na borda, regras de negócio; OpenAPI e cliente do front regenerados | O item é só de tela |
| 4. Tela | `user-experience` → `design-systems` → `design` | Tela no layout escolhido, com os estados vazio, carregando, erro e sem permissão, e com transição suave em toda troca de tela e de estado (`user-experience`, doc 16) | O item não tem interface |
| 5. Testes | `quality` (estilo do teste em `coding`) | Um teste por critério de aceite, na camada mais barata; o fluxo principal coberto de ponta a ponta quando o item fecha o fluxo | Nunca |
| 6. Pronto | `quality` | Definição de pronto abaixo (detalhada em `quality`, doc 08); PR pequeno com o item; critérios testados marcados no Framia (`check_criteria`) | Nunca |
| 7. Staging | `infra` | Deploy em staging e verificação do critério no ambiente | Projeto sem staging ainda: verifique local e anote |

**Definição de pronto de um item** (detalhes em [quality/docs/08](../quality/docs/08-definition-of-done.md)):

- [ ] Todos os critérios de aceite do item cumpridos e verificados (rodando, não só lendo o código).
- [ ] Um teste automatizado por critério; testes, lint, typecheck e build verdes.
- [ ] Migration revisada e o banco recriado do zero sem erro, se o item mexe no banco.
- [ ] Tela conferida no dispositivo principal e no secundário, se o item tem interface.
- [ ] Fluxo do item clicado de ponta a ponta: toda troca de tela e de estado é suave, nada aparece ou some de uma vez, conforme o `docs/MOTION.md` do projeto.
- [ ] Status do item atualizado no `BACKLOG.md` no mesmo PR; regra nova registrada em `docs/regras-de-negocio.md`.
- [ ] Deploy em staging verificado, quando já houver staging.

Mostre o progresso a cada passo: "Item 3 de 9 (cadastro de pacientes). Passo: dados". Se um item revelar uma regra nova ou um erro no backlog, volte à `product`, ajuste e siga.

### Por que essa ordem

- **Produto antes da stack:** o tamanho do escopo, as integrações e as regras decidem a stack, não o contrário.
- **Protótipo antes da stack e do código:** no Framia, mudar uma tela, uma tabela ou uma rota custa minutos; depois do código, custa retrabalho. O cliente aprova o que vai receber, o design system fica decidido, e o tamanho real do sistema (telas, tabelas, rotas) ajuda a escolher a stack e a infra.
- **Stack antes da estrutura:** pasta, lint, UI kit e hospedagem dependem dela.
- **Dados logo depois da arquitetura:** o modelo sai das regras de negócio e é a parte mais cara de mudar depois; multiempresa, por exemplo, se decide no primeiro dia.
- **Arquitetura antes da IA:** o `CLAUDE.md` cita comandos e convenções que só existem depois da árvore.
- **IA e índice antes do código:** o agente escreve o resto do projeto; configurado cedo, erra menos e gasta menos.
- **Coding antes do design:** lint, testes e padrão de erros valem também para os componentes de tela.
- **Dispositivo antes de layout, layout antes de componente:** dentro da fase 8, `user-experience` define para quais dispositivos projetar; `design-systems`, a estrutura de cada tela; só depois `design` escolhe com o que montar.
- **Infra antes de construir:** staging e CI prontos fazem cada item da fase 10 ser verificado no ambiente real, e não só no fim.
- **No ciclo, dados antes do back e back antes da tela:** a tela consome a API, e a API depende das tabelas. Fazer na ordem evita tela com dado inventado que depois não encaixa.
- **Fatia vertical, um item por vez:** cada item fecha de ponta a ponta antes do próximo; o sistema está sempre funcionando, só que menor.

### Atalhos por tipo de projeto

| Projeto | Fases | Observação |
|---|---|---|
| Site de conteúdo, blog, landing | 0 → 1 → 2 → 3 → 5 → 7 → 8 → 9 → 10 | Fase 0 curta (lista de páginas); na fase 1, só design system e páginas; sem `data` e `code-indexes` |
| MVP de SaaS | 0 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 9 → 10 → 6 | Índice só quando a base crescer |
| SaaS em crescimento, sistema corporativo | 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 | Todas; dados, arquitetura e infra com mais peso |
| API, worker, CLI | 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 9 → 10 | Sem a fase 8; na fase 1, só banco, rotas, fluxos e requisitos (CLI pula a fase 1); no ciclo, sem o passo de tela |
| Mobile, desktop | 0 → 1 → 2 → 3 → 4 → 5 → 7 → 8 → 9 → 10 | Infra cobre o backend e o CI de build |

## Projeto existente

Quando a pasta já tem código, a ordem inverte: primeiro entender, depois mudar.

1. `audit`: diagnostique o projeto (só leitura) para saber o que está bom e o que falta antes de mudar qualquer coisa.
2. `ia` e `code-indexes`: configure o agente e, em base grande ou desconhecida, o índice, para ler o projeto com menos tokens.
3. `product`: se não houver backlog nem regras escritas, levante o que o sistema já faz e o que o pedido acrescenta, e registre.
4. `architecture` e `data`: compare a estrutura e o modelo atuais com o recomendado. Proponha a mudança em passos; não mova tudo de uma vez.
5. `coding` e `quality`: lint, format e testes antes de refatorar.
6. `security`, `integrations`, `user-experience`, `design-systems`, `design` e `infra`: só se o pedido cobre essas áreas ou se a `audit` apontou falha grave de segurança ou de backup.
7. `stacks`: só se o usuário quer trocar ou acrescentar uma tecnologia. Não proponha trocar a stack por conta própria.
8. Funcionalidade nova: se ela traz tela, tabela ou rota nova, prototipe antes no `framia` (numa branch, quando o projeto já existe lá) e espere o ok; depois siga o ciclo da fase 10 para ela.

## Regras de uso

- **Uma skill por vez, na ordem.** Leia o `SKILL.md` da skill da fase e siga o "Como usar" dela; não decida a área por conta própria nesta skill.
- **Passe o contexto adiante.** Ao abrir cada fase, resuma em poucas linhas o que as anteriores decidiram (escopo, stack, árvore, modelo de dados, comandos). A skill seguinte depende disso.
- **Confirme as decisões grandes.** Mostre e espere o ok antes de: fechar o escopo do MVP (fase 0), criar o projeto no Framia e dar o protótipo por aprovado (fase 1), fixar a stack (fase 2), criar a árvore de pastas (fase 3), aplicar o modelo de dados (fase 4) e qualquer coisa que gere custo ou conta externa (fase 9). O resto segue direto.
- **O que o usuário fixou não se rediscute.** Se uma escolha fixa conflita com a recomendação de uma skill, diga o risco em uma frase e siga a escolha do usuário.
- **Requisitos do cliente guiam cada fase.** Ao escolher entre duas opções numa fase, a que atende melhor ao escopo aprovado na fase 0 ganha da que é só mais popular.
- **Registre as decisões no projeto.** O que o sistema faz e para quem vai no `README`; backlog e critérios no `BACKLOG.md`; regras em `docs/regras-de-negocio.md`; stack, padrão de arquitetura, modelo de dados e hospedagem no `ARCHITECTURE.md` (ou `README`); padrão de movimento e transições no `docs/MOTION.md` (projeto com tela); comandos e armadilhas no `CLAUDE.md`/`AGENTS.md`. Não crie documento de planejamento separado.
- **Interface suave é princípio do plugin.** Todo sistema com tela sai com transição curta em cada troca de tela e de estado (abrir, fechar, carregar, salvar, navegar), do protótipo ao código. Tela que joga o conteúdo de uma vez não está pronta. Vale do gesto mais simples (pressionar um botão) ao mais avançado (arrastar, deslizar, pinça). As regras estão em `user-experience`, [documento 16](../user-experience/docs/16-movimento-e-transicoes.md); todo pedido de tela lista essa skill, o especialista de interface julga o movimento de cada tela entregue, o projeto nasce com o `docs/MOTION.md` (fase 3, modelo no documento 16), e na fase 5 o `CLAUDE.md`/`AGENTS.md` aponta para ele, para valer também nas sessões sem o plugin. Em projeto existente, o arquivo é criado na primeira tarefa com tela.
- **Não pule a verificação.** Ao fim de cada fase e de cada item, rode o que der para rodar (instalar, build, lint, teste, abrir a página) antes de passar adiante.
- **Mostre o progresso.** Diga em uma linha a fase em que está e as que faltam, por exemplo: "Fase 5 de 10 (ia). Faltam: coding, design, infra, construção". Na fase 10, diga o item e o passo.

## Quando a lista não cobre

Se o projeto pede uma área sem skill aqui (analytics, pagamentos, compliance específico, app de jogos, hardware), diga isso ao usuário, cubra com a documentação oficial da ferramenta e siga a ordem das fases para o resto.

## Validade dos dados

Esta skill não traz preços, versões nem comandos: eles ficam nas skills de cada área, verificados entre 2026-11-24 e 2026-11-26. Confira a linha "Verificado em" de cada documento antes de afirmar algo decisivo.
