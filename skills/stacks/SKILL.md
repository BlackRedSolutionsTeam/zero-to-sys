---
name: stacks
description: Escolhe a stack completa (frontend, backend, banco, ORM, auth, testes) para cada tipo de projeto, usando só ferramentas gratuitas (Astro, Next.js, React Router/TanStack Start, React + Vite com API separada, Node com Hono/Fastify/NestJS, Python com FastAPI/Django, .NET, Java com Spring Boot, Laravel/Rails, Go, Expo/Flutter, Tauri/Electron). Use sempre que for começar um sistema do zero ou decidir tecnologia — "qual stack usar", "com o que eu faço esse sistema", "qual backend", "qual framework", "vale Next ou Laravel", "qual linguagem para esta API", "como montar um SaaS, e-commerce, app mobile, sistema interno ou site", "criar o projeto".
---

# stacks

Guia de decisão para escolher a stack de um sistema novo. Cada documento em `docs/` descreve uma stack completa: composição inteira (frontend, backend, banco, ORM, auth, testes), para que tipo de projeto funciona melhor, onde é ruim e como criar o projeto.

## Como usar esta skill

1. **Descubra o que já existe e o que o time sabe** antes de escolher qualquer coisa: veja o repositório (`package.json`, `.csproj`, `pom.xml`, `composer.json`, `pyproject.toml`, `go.mod`), pergunte a linguagem que o time domina e se a empresa já tem padrão. O que já está no projeto tem prioridade sobre esta lista.
2. **Identifique o tipo de projeto**: conteúdo, SaaS, API, sistema interno, mobile, desktop, tempo real, dados/IA, e-commerce, CLI.
3. **Escolha a stack pela tabela abaixo.**
4. **Leia o documento da stack escolhida** em `docs/` antes de criar qualquer coisa. Confira principalmente "Para que tipo de projeto", "Quando é ruim" e "Como começar".
5. **Crie o projeto pelos comandos de "Como começar"** do documento. Confira a versão atual na documentação oficial antes de rodar.
6. **Explique a escolha ao usuário em duas ou três frases**: qual stack, por que serve a esse projeto e qual o principal ponto fraco.

## Qual stack usar

| Projeto | Stack recomendada | Alternativa |
|---|---|---|
| Site de conteúdo, blog, institucional, landing | [Astro](docs/01-astro-conteudo.md) (docs.astro.build/en/concepts/why-astro) | Next.js se o site vai virar app |
| SaaS ou app web, time de JavaScript | [Next.js + Postgres + Drizzle + Better Auth](docs/02-nextjs-saas.md) (guia de autenticação: nextjs.org/docs/app/guides/authentication) | [React Router ou TanStack Start](docs/03-react-router-tanstack-start.md) |
| App com muita interação e estado na URL | [TanStack Start ou React Router](docs/03-react-router-tanstack-start.md) | Next.js |
| Front web com backend que atende vários clientes | [SPA React + Vite e API separada](docs/04-spa-vite-api.md) | Next.js se só há web |
| API enxuta, BFF, tempo real em TypeScript | [Node com Hono ou Fastify](docs/05-node-api.md) | NestJS, se quiser módulos e injeção de dependência (docs.nestjs.com) |
| Dados, IA, automação | [Python com FastAPI](docs/06-python-fastapi-django.md) | Django se há cadastro e admin |
| Sistema interno com cadastros e admin, equipe pequena | [Django](docs/06-python-fastapi-django.md) (admin incluído no framework: docs.djangoproject.com/en/stable/ref/contrib/admin) | [Laravel](docs/09-laravel-rails.md), Rails |
| Sistema corporativo em empresa Microsoft | [.NET (ASP.NET Core)](docs/07-dotnet-aspnet-core.md) | Java Spring Boot |
| Sistema corporativo ou regulado em empresa Java | [Java com Spring Boot](docs/08-java-spring-boot.md) | .NET |
| API, serviço de rede, CLI (concorrência na linguagem: go.dev/doc) | [Go](docs/10-go-api.md) | Node (API) |
| E-commerce próprio | [Next.js](docs/02-nextjs-saas.md) ou [Laravel](docs/09-laravel-rails.md); nenhum dos dois traz módulo oficial de e-commerce, veja os documentos | .NET ou Java, se a empresa já usa |
| Tempo real (chat, notificações, streaming) | [Go](docs/10-go-api.md) ou [Node](docs/05-node-api.md) | Laravel com Reverb (laravel.com/docs/reverb) |
| App mobile, time de React | [Expo (React Native)](docs/11-mobile.md) (docs.expo.dev) | Flutter |
| App mobile com um código só para várias plataformas | [Flutter](docs/11-mobile.md) (flutter.dev) | Expo |
| Desktop com tecnologia web | [Tauri](docs/12-desktop.md) (aceita qualquer frontend web: tauri.app) | Electron |
| MVP para validar ideia | A stack que o time já domina; senão Next.js ou Laravel | Astro se for só uma página |

| Stack | Documento | Papel |
|---|---|---|
| Astro | [docs/01-astro-conteudo.md](docs/01-astro-conteudo.md) | Sites de conteúdo, institucionais e blogs |
| Next.js | [docs/02-nextjs-saas.md](docs/02-nextjs-saas.md) | SaaS e app web full-stack em TypeScript |
| React Router / TanStack Start | [docs/03-react-router-tanstack-start.md](docs/03-react-router-tanstack-start.md) | Full-stack React sobre Vite |
| React + Vite + API | [docs/04-spa-vite-api.md](docs/04-spa-vite-api.md) | SPA com backend separado |
| Node (Hono, Fastify, NestJS) | [docs/05-node-api.md](docs/05-node-api.md) | APIs e tempo real em TypeScript |
| Python (FastAPI, Django) | [docs/06-python-fastapi-django.md](docs/06-python-fastapi-django.md) | Dados, IA e sistemas com admin |
| .NET | [docs/07-dotnet-aspnet-core.md](docs/07-dotnet-aspnet-core.md) | Sistema corporativo e interno |
| Java Spring Boot | [docs/08-java-spring-boot.md](docs/08-java-spring-boot.md) | Sistema corporativo e regulado |
| Laravel e Rails | [docs/09-laravel-rails.md](docs/09-laravel-rails.md) | Framework web completo (monólito) |
| Go | [docs/10-go-api.md](docs/10-go-api.md) | APIs, serviços de rede e CLI |
| Mobile (Expo, Flutter, nativo) | [docs/11-mobile.md](docs/11-mobile.md) | Apps de celular |
| Desktop (Tauri, Electron) | [docs/12-desktop.md](docs/12-desktop.md) | Apps de computador |

## Checklist de toda stack escolhida

- [ ] A stack está registrada com o motivo no README ou no AGENTS.md (`grep -niE 'stack' README.md AGENTS.md`).
- [ ] O time sabe operar a linguagem e o framework, ou o risco foi dito ao usuário (conferir na conversa).
- [ ] Front, back, banco, ORM, auth e testes têm uma escolha cada, sem duas ferramentas para o mesmo papel (`cat package.json`).
- [ ] Há uma linguagem só, ou o motivo para separar está escrito (`ls`).
- [ ] Todas as ferramentas escolhidas são gratuitas (conferir a licença e o preço na fonte do documento).
- [ ] A versão e o comando de criação foram conferidos na fonte oficial (`pnpm view <pacote> version`).
- [ ] O projeto foi criado pelo comando oficial e abre em desenvolvimento (`pnpm dev`).
- [ ] Lint, typecheck e testes rodam no projeto novo (`pnpm lint && pnpm test`).
- [ ] O que já existia no projeto foi mantido, sem proposta de reescrita (`git diff --stat`).

## Regras de uso

- **O que o time já sabe pesa mais que a moda.** Uma stack mediana que o time domina entrega mais que a melhor stack que ninguém conhece. Só recomende trocar de linguagem com motivo claro.
- **O que já existe no projeto vem primeiro.** Não proponha reescrever; estenda a stack atual e diga o que ficou de fora.
- **Maturidade e comunidade importam.** Prefira o que tem anos de produção, releases regulares e documentação oficial completa. Ferramenta nova (Better Auth, Drizzle, TanStack Start) é aceitável quando o time aceita o risco; diga isso ao usuário. O Drizzle, por exemplo, usa a tag `rc` na documentação de início (orm.drizzle.team/docs/get-started/postgresql-new).
- **Facilidade de contratar.** Pergunte quem vai manter o sistema e confira o mercado local antes de escolher uma linguagem que o time não conhece.
- **Uma linguagem a menos é um custo a menos.** Só separe front e back, ou crie um serviço em outra linguagem, quando houver um motivo (outros clientes, dados e IA, desempenho).
- **Comece simples.** Monólito primeiro; microserviços só com time e problema que os justifiquem.
- **Só o que é grátis.** Não sugira plano pago de framework ou serviço sem o usuário pedir. Hospedagem e deploy são da skill infra.
- **Versões mudam rápido.** Antes de afirmar uma versão, comando ou licença ao usuário, confira na fonte citada no documento.
- **Limites com outras skills.** UI kits e ícones são da skill design. Estrutura de pastas e camadas de cada stack são da skill architecture. Não repita o que elas já resolvem.

## Quando a lista não cobre

Se o projeto pede algo fora destas stacks (Rust, Elixir/Phoenix, SvelteKit, Nuxt, Kotlin Multiplatform, plataformas de e-commerce prontas, plataformas low-code), diga isso ao usuário em vez de forçar uma delas. O `docs/README.md` registra o que foi avaliado e saiu da lista, com o motivo.

## Validade dos dados

Versões, comandos e licenças dos documentos foram verificados em 2026-11-24, e cada documento diz o que não pôde ser confirmado. Antes de afirmar uma versão ou licença ao usuário, confira no site oficial se a informação for decisiva.
