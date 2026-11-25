# React Router e TanStack Start (full-stack React sem a mágica do Next)

> Duas alternativas ao Next.js para apps React com servidor: React Router em modo framework e TanStack Start, com Postgres, Drizzle e Better Auth.

| | |
|---|---|
| **Site** | https://reactrouter.com e https://tanstack.com/start |
| **Categoria** | Área 2 — SaaS e app web full-stack em TypeScript (alternativa) |
| **Tipo** | Stack completa opinativa |
| **Stack/composição** | Frontend: React, Tailwind, shadcn/ui. Servidor: loaders e actions (React Router) ou server functions (TanStack Start), sobre Vite. Banco: PostgreSQL. ORM: Drizzle. Auth: Better Auth. Testes: Vitest e Playwright |
| **Preço** | Grátis (open source) |
| **Licença** | MIT (React Router e TanStack Router/Start; LICENSE nos repositórios e registro npm, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

React Router v7 traz o que havia no Remix para dentro do React Router, no "modo framework" (fonte: remix.run/blog/react-router-v7). Ele tem loaders para carregar dados e actions para formulários (fonte: reactrouter.com/start/framework/data-loading e /actions). TanStack Start é um framework React full-stack movido pelo TanStack Router, com SSR, streaming e server functions (fonte: tanstack.com/start/latest/docs/framework/react/overview).

A página oficial do TanStack Start lida na verificação diz que ele é estável; quem veio de uma release candidate segue um guia de migração. No npm, `@tanstack/react-start` está na 1.169.7 (conferido em 2026-11-24). A instalação do shadcn/ui lista React Router e TanStack Start entre os frameworks aceitos (fonte: ui.shadcn.com/docs/installation).

O React Router em modo framework usa Vite (template oficial, repositório remix-run/react-router-templates). O TanStack Start roda com Vite ou Rsbuild (fonte: página Overview do TanStack Start).

## Por que usar

- **Mutações por actions ou server functions:** no React Router, rotas têm actions e fetchers; no TanStack Start, server functions tipadas com GET ou POST (fonte: tanstack.com/start/latest/docs/framework/react/comparison).
- **Roteador tipado (TanStack Start):** o TanStack Router é descrito como roteador type-safe, com rotas aninhadas, search params e carregamento de dados (fonte: página Overview do TanStack Start).
- **Hospedagem à escolha:** a página Overview do TanStack Start diz que ele publica no provedor ou runtime que você quiser.
- **Mesma base de React** do Next.js: componentes e bibliotecas valem para os dois.

## Quando usar

- Time que quer React full-stack com roteamento aninhado e loaders/actions (React Router) ou server functions (TanStack Start).
- App com estado na URL (search params), em que o TanStack Router tipa a busca (fonte: página Overview do TanStack Start).
- Projeto que vai rodar no provedor ou runtime que o time escolher (fonte: página Overview do TanStack Start).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS / app web | ✅ Ótimo | Loaders, actions (React Router) e server functions (TanStack Start) cobrem dados e mutações |
| Dashboard / painel admin | ✅ Ótimo | TanStack Router tipa search params e carrega dados por rota |
| MVP / protótipo | ✅ Ótimo | Os dois têm CLI de criação (`create-react-router`, `@tanstack/cli`) |
| Sistema interno corporativo | 🟡 Serve | Sem recurso oficial específico para esse caso; avalie caso a caso |
| E-commerce | 🟡 Serve | Sem recurso oficial específico para loja; avalie caso a caso |
| Site institucional / blog | ❌ Evite | O foco aqui é app; para conteúdo veja [Astro](01-astro-conteudo.md) |
| API pura | ❌ Evite | Foco é app com tela; para API veja [Node API](05-node-api.md) |
| Tempo real | ❌ Evite | A documentação dos dois não descreve WebSocket nem SSE; use um serviço à parte, veja [Node API](05-node-api.md) |
| App mobile | ❌ Evite | É web; veja [mobile](11-mobile.md) |

## Quando é bom

- **Formulário com action:** no React Router, o formulário envia para uma action e os loaders revalidam os dados (fonte: reactrouter.com/start/framework/actions).
- **Vite:** o React Router em modo framework e o TanStack Start (com Vite ou Rsbuild) usam o Vite.
- **Rotas tipadas (TanStack Start):** roteador type-safe (fonte: página Overview do TanStack Start).
- **Modos do React Router:** além do modo framework, há os modos data e declarative (biblioteca) (fonte: reactrouter.com/start/modes), e o modo framework aceita SPA com `ssr: false` (fonte: reactrouter.com/how-to/spa).

## Quando é ruim

- **Recursos embutidos:** o Next.js documenta otimização de imagem (`next/image`) e ISR como recursos do próprio framework (nextjs.org/docs/app/api-reference/components/image e nextjs.org/docs/app/guides/incremental-static-regeneration, 2026-11-24). Se o projeto precisa disso, confira o equivalente na documentação do React Router e do TanStack Start antes de escolher.
- **React Server Components:** no TanStack Start são experimentais e opt-in; no React Router, integração instável; no Next.js são o modelo central (fonte: tanstack.com/start/latest/docs/framework/react/comparison, verificada em 2026-11-24).
- **Revalidação após deploy (ISR):** no TanStack Start depende de cache HTTP e configuração do provedor; no React Router, de cabeçalhos HTTP e da infraestrutura (mesma fonte).
- **Duas opções:** são frameworks diferentes; escolha um por projeto.

## Como começar

React Router (comando da documentação oficial):

```bash
npx create-react-router@latest my-react-router-app
```

TanStack Start: o guia oficial de início (tanstack.com/start/latest/docs/framework/react/getting-started, conferido em 2026-11-24) indica `npx @tanstack/cli@latest create`. O shadcn/ui aceita o template `start` (`pnpm dlx shadcn@latest init -t start`) e `react-router`. Banco e auth: mesmos comandos de Drizzle e Better Auth do [documento do Next.js](02-nextjs-saas.md).

## Combina com / alternativas

- [Next.js](02-nextjs-saas.md): o Next.js documenta recursos embutidos como `next/image` e ISR (links em "Quando é ruim").
- [SPA + API](04-spa-vite-api.md): quando o backend é separado.
- Alternativas de fora: SvelteKit (svelte.dev) e Nuxt (nuxt.com).

## Decisão rápida

- **Use se:** quer React full-stack com loaders/actions ou server functions, rotas tipadas (TanStack Start) e escolha livre de hospedagem.
- **Evite se:** precisa de recurso que só o Next.js documenta (como `next/image` ou RSC como modelo central), ou o projeto é só conteúdo.
