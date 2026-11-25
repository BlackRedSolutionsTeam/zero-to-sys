# Stacks

Um documento por stack, explicando a composição inteira, quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê. A lista ficou só com o que passa em três critérios: maturidade real, manutenção ativa e documentação oficial completa. Versões, comandos e licenças foram verificados nos sites oficiais em 2026-11-24. As datas de versão vêm do GitHub (releases) e do npm. Cada documento cita as fontes de suas afirmações.

## Web

| Stack | O que é | Grátis | Doc |
|---|---|---|---|
| Astro | Sites de conteúdo com pouco JavaScript | Sim, open source | [01-astro-conteudo.md](01-astro-conteudo.md) |
| Next.js | SaaS full-stack em TypeScript com Postgres, Drizzle e Better Auth | Sim, open source | [02-nextjs-saas.md](02-nextjs-saas.md) |
| React Router / TanStack Start | Full-stack React sobre Vite | Sim, open source | [03-react-router-tanstack-start.md](03-react-router-tanstack-start.md) |
| React + Vite + API | SPA com backend separado | Sim, open source | [04-spa-vite-api.md](04-spa-vite-api.md) |

## Backend e API

| Stack | O que é | Grátis | Doc |
|---|---|---|---|
| Node (Hono, Fastify, NestJS) | API em TypeScript | Sim, open source | [05-node-api.md](05-node-api.md) |
| Python (FastAPI, Django) | API, dados, IA e sistemas com admin | Sim, open source | [06-python-fastapi-django.md](06-python-fastapi-django.md) |
| .NET (ASP.NET Core) | Sistema corporativo em C# | Sim (Visual Studio tem a edição Community grátis e as edições Professional e Enterprise pagas; visualstudio.microsoft.com/vs/compare) | [07-dotnet-aspnet-core.md](07-dotnet-aspnet-core.md) |
| Java (Spring Boot) | Sistema corporativo e regulado | Sim (existe suporte comercial pago; spring.io/support) | [08-java-spring-boot.md](08-java-spring-boot.md) |
| Laravel e Rails | Framework web completo (monólito) | Sim (o Laravel é MIT; serviços como o Forge têm plano pago; forge.laravel.com/pricing) | [09-laravel-rails.md](09-laravel-rails.md) |
| Go | API, serviços de rede e CLI | Sim, open source | [10-go-api.md](10-go-api.md) |

## Apps

| Stack | O que é | Grátis | Doc |
|---|---|---|---|
| Mobile (Expo, Flutter, nativo) | Apps de celular | Frameworks sim; o Apple Developer Program custa 99 USD por ano (developer.apple.com/programs/enroll) | [11-mobile.md](11-mobile.md) |
| Desktop (Tauri, Electron) | Apps de computador | Sim; assinar para macOS pede o Apple Developer Program, pago (v2.tauri.app/distribute/sign/macos e electronjs.org/docs/latest/tutorial/code-signing) | [12-desktop.md](12-desktop.md) |

## Qual escolher

- **Site de conteúdo, blog, institucional:** [Astro](01-astro-conteudo.md): a documentação o posiciona para sites de conteúdo, com islands e content collections (docs.astro.build/en/concepts/why-astro).
- **SaaS ou app web com time de JavaScript:** [Next.js](02-nextjs-saas.md), com Server Actions, Route Handlers e guia de autenticação (nextjs.org/docs/app/guides/authentication); [React Router](https://reactrouter.com) ou [TanStack Start](https://tanstack.com/start/latest) como alternativas full-stack em React.
- **Backend atendendo web, mobile e integrações:** [SPA + API](04-spa-vite-api.md), com a API em [Node](05-node-api.md), [.NET](07-dotnet-aspnet-core.md), [Java](08-java-spring-boot.md), [Laravel](09-laravel-rails.md) ou [Go](10-go-api.md).
- **Dados, IA, automação:** [Python](06-python-fastapi-django.md); o doc cita as fontes de FastAPI (fastapi.tiangolo.com) e Django.
- **Sistema interno ou corporativo:** a stack da empresa. Sem padrão, [Django](06-python-fastapi-django.md), que traz o admin como app incluído (docs.djangoproject.com/en/stable/ref/contrib/admin), ou [Laravel](09-laravel-rails.md), com starter kits oficiais (laravel.com/docs/starter-kits). [.NET](07-dotnet-aspnet-core.md) e [Java](08-java-spring-boot.md) quando a empresa já usa essas plataformas.
- **E-commerce próprio:** [Next.js](02-nextjs-saas.md) ou [Laravel](09-laravel-rails.md); nenhum dos dois traz módulo oficial de e-commerce, veja os documentos.
- **Tempo real:** [Go](10-go-api.md) (concorrência na linguagem; go.dev/doc) ou [Node](05-node-api.md); com Laravel há o Reverb (laravel.com/docs/reverb) e com .NET o SignalR (learn.microsoft.com/en-us/aspnet/core/signalr/introduction).
- **CLI e ferramentas:** [Go](10-go-api.md) (fonte do uso em CLI: [documento 10](10-go-api.md)).
- **Mobile:** [Expo](11-mobile.md) com time de React (Expo é feito sobre React Native; docs.expo.dev); [Flutter](https://flutter.dev) para um código único em várias plataformas.
- **Desktop:** [Tauri](12-desktop.md), que aceita qualquer frontend web (tauri.app); [Electron](https://www.electronjs.org) para apps com JavaScript, HTML e CSS.
- **Em qualquer caso:** a linguagem que o time já domina e a stack que já existe no projeto vêm antes desta lista.

Hospedagem e deploy são da skill infra; UI kits e ícones, da skill design; estrutura de pastas, da skill architecture.

## O que saiu da lista e por quê

| Stack | Motivo |
|---|---|
| Remix v2 | Tem guia de migração para o React Router v7 (reactrouter.com/upgrading/remix); vale o [documento 03](03-react-router-tanstack-start.md). O repositório remix-run/remix hoje publica o Remix 3.3.0 (2026-11-19, via GitHub), um framework novo, fora do escopo desta lista |
| SvelteKit e Nuxt | Ativos (SvelteKit com commits em 2026-11-24, Nuxt v4.7.0 em 2026-11-23, via GitHub). Ficam fora pelo escopo da lista, que tem um documento por área: o full-stack em TypeScript já está coberto por [Next.js](02-nextjs-saas.md) e [React Router / TanStack Start](03-react-router-tanstack-start.md) |
| Rust (Axum e similares) | Ativo (Rust 1.100.0 em 2026-11-12; Axum 0.8.9 em 2026-04-14, via GitHub). Fica fora pelo escopo da lista: API e CLI compiladas já estão cobertas por [Go](10-go-api.md) |
| Elixir / Phoenix | Ativo (Phoenix v1.8.17 em 2026-11-20, via GitHub). Fica fora pelo escopo da lista: tempo real já está coberto por [Go](10-go-api.md) e [Node](05-node-api.md) |
| Express puro | Mantido (Express 5, v5.3.0 em 2026-10-09, via GitHub). Fica fora pelo escopo da lista: o [documento 05](05-node-api.md) cobre Hono, Fastify e NestJS. Quem já tem Express pode manter |
| Rails como documento próprio | Entrou junto com o Laravel em [09](09-laravel-rails.md), por ser da mesma categoria (framework web completo); as fontes de cada um estão lá |
| Supabase, Firebase e outros BaaS | São serviços hospedados, não stacks de código; ficam para a skill infra |
| Stacks MERN e MEAN como nome | São siglas de combinações de peças; as peças estão nos documentos 02 a 05 |
| Kotlin Multiplatform e .NET MAUI | Ativos (Compose Multiplatform v1.12.2 em 2026-10-15; .NET MAUI 11.0.10 em 2026-11-11, via GitHub). Ficam fora pelo escopo da lista: o mobile multiplataforma já está coberto por Expo e Flutter no [documento 11](11-mobile.md) |
| Blazor como front principal | Fica fora do escopo da lista, que usa React no front; citado no [documento 07](07-dotnet-aspnet-core.md) como opção |
| Plataformas low-code e de e-commerce prontas (Shopify, WooCommerce) | São produtos, não stacks de código; comparar planos pagos foge do escopo |
| WordPress | É um CMS (wordpress.org), não uma stack de código. O [blog de segurança oficial](https://wordpress.org/news/category/security/) publicou as versões 7.1.3 (2026-10-06), 7.1.4 (2026-10-28) e 7.1.5 (2026-11-18). Para conteúdo em código use [Astro](01-astro-conteudo.md) |
