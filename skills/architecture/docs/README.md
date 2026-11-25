# Estrutura de pastas e arquivos

Um documento por padrão ou stack, com a árvore de pastas completa, quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê. Em cada árvore, cada pasta e cada arquivo tem fonte oficial (documentação, template ou app de referência), e a fonte é citada. As convenções foram verificadas nas documentações oficiais em 2026-11-24.

## Padrões que valem para qualquer stack

| Padrão | O que é | Custo | Doc |
|---|---|---|---|
| Feature-first e colocation | Pasta por assunto; teste, estilo e tipo ao lado | Baixo | [01-feature-first-colocation.md](01-feature-first-colocation.md) |
| Vertical slice | Uma pasta por caso de uso | Baixo a médio | [02-vertical-slice.md](02-vertical-slice.md) |
| Camadas, Clean, hexagonal | Domínio no centro, infraestrutura na borda | Alto | [03-camadas-clean-hexagonal.md](03-camadas-clean-hexagonal.md) |
| Monólito modular | Módulos com fronteira, um deploy | Médio | [04-monolito-modular.md](04-monolito-modular.md) |
| Monorepo | Vários apps e pacotes no mesmo repositório | Médio | [05-monorepo.md](05-monorepo.md) |

## Estrutura recomendada por stack

| Stack | Fonte oficial | Doc |
|---|---|---|
| Next.js (App Router) | nextjs.org/docs | [06-nextjs.md](06-nextjs.md) |
| React + Vite (e nota de Astro) | vite.dev, docs.astro.build | [07-react-vite.md](07-react-vite.md) |
| React Native + Expo | docs.expo.dev | [08-react-native-expo.md](08-react-native-expo.md) |
| NestJS, Hono, Fastify | docs.nestjs.com | [09-nestjs-node.md](09-nestjs-node.md) |
| ASP.NET Core | learn.microsoft.com (sem guia de pastas confirmado) | [10-aspnet-core.md](10-aspnet-core.md) |
| FastAPI e Django | fastapi.tiangolo.com, docs.djangoproject.com | [11-python-fastapi-django.md](11-python-fastapi-django.md) |
| Laravel | laravel.com/docs | [12-laravel.md](12-laravel.md) |
| Go | go.dev/doc/modules/layout | [13-go.md](13-go.md) |

## Qual escolher

- **Primeiro a stack:** o framework define parte das pastas. Siga o documento da parte 2.
- **Para o que o framework deixa livre:** [feature-first](01-feature-first-colocation.md). Serve para quase tudo.
- **API com muitos casos de uso:** [vertical slice](02-vertical-slice.md) dentro de cada módulo.
- **Sistema médio ou grande em um deploy:** [monólito modular](04-monolito-modular.md).
- **Domínio rico e sistema longo:** [camadas](03-camadas-clean-hexagonal.md), só nos módulos que precisam.
- **Dois ou mais apps com código comum:** [monorepo](05-monorepo.md).
- **Projeto pequeno ou MVP:** a convenção da stack e poucas pastas; ignore o resto.

## O que saiu da lista e por quê

| Item | Motivo |
|---|---|
| Atomic Design como estrutura de pastas | `atoms/molecules/organisms` vem da metodologia de Brad Frost para criar design systems de interface (atomicdesign.bradfrost.com/chapter-2), não de uma convenção de pastas de framework. Use como vocabulário de design, não de pastas |
| Pastas por tipo em projeto grande (`components/`, `services/`, `models/` globais) | Uma mudança de um assunto fica espalhada por várias pastas, e a busca por assunto não aponta uma pasta (juízo do guia; a base é o Redux Style Guide, que recomenda feature folders em vez de pastas por tipo). Em projeto pequeno o problema aparece menos |
| Microserviços cedo demais | Fowler lista como custos: distribuição (chamadas remotas lentas e sujeitas a falha), consistência eventual e complexidade operacional, que exige equipe de operação madura (martinfowler.com/articles/microservice-trade-offs.html). Comece com [monólito modular](04-monolito-modular.md) |
| "golang-standards/project-layout" como padrão | O nome sugere ser oficial, mas não é padrão do time do Go; o guia oficial é a página do go.dev. O README do repositório diz: "This is NOT an official standard defined by the core Go dev team" (conferido em 2026-11-24) |
| Feature-Sliced Design (FSD) | Metodologia de front com camadas (`app`, `pages`, `widgets`, `features`, `entities`, `shared`). Documentação em feature-sliced.design; este guia fica com [feature-first](01-feature-first-colocation.md), que tem fonte oficial no Redux Style Guide e no Next.js |
| Domain-Driven Design completo | É método de modelagem, não de pastas. O que serve às pastas já está em [monólito modular](04-monolito-modular.md) e [camadas](03-camadas-clean-hexagonal.md) |
| Astro como documento próprio | Estrutura simples (só `src/pages/` é reservada); coube em uma nota no [07](07-react-vite.md) |
| Rails, Spring, Svelte Kit, Nuxt, Flutter | Conferidos nas docs oficiais em 2026-11-24; a estrutura é imposta ou guiada pelo framework, então um documento próprio repetiria a doc. Rails: a seção "Directory Structure" do guia Getting Started lista `app/` (controllers, models, views, helpers, mailers, jobs, assets), `config/` e `db/`. Spring Boot: não exige layout; recomenda a classe principal em um pacote raiz acima das demais, evitar o pacote default e mostra exemplo por feature (`customer/`, `order/`). SvelteKit: `src/lib`, `src/routes`, `static/` e arquivos de raiz fixos. Nuxt: `app/` (components, composables, pages, layouts...), `server/`, `public/`, `shared/`. Flutter: a doc de arquitetura fala em camadas (UI e dados, domínio opcional) e em views, view models, repositórios e serviços, mas não define pastas |
| Nx em detalhe | Citado no [05](05-monorepo.md); conferido em nx.dev em 2026-11-24: cache local, grafo de projetos, geradores (`nx g <plugin>:<gerador>`). Estrutura de pastas em nx.dev/docs/kb/folder-structure: o Nx funciona com qualquer estrutura (as do guia são convenções, não requisitos); layout plano (`packages/`) ou agrupado (`apps/` + `libs/`); o ideal é app fina e a maior parte do código em `libs/`. Licença MIT (LICENSE do repositório nrwl/nx, conferido em 2026-11-24) |
