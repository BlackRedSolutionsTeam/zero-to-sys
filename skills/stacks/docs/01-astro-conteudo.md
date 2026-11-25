# Astro (site de conteúdo)

> Stack para sites de conteúdo, institucionais e blogs: Astro gera HTML estático com pouco JavaScript, e o conteúdo vem de Markdown/MDX ou de um CMS.

| | |
|---|---|
| **Site** | https://astro.build |
| **Categoria** | Área 1 — Site de conteúdo, institucional e blog |
| **Tipo** | Stack completa (framework de sites + conteúdo em arquivos ou CMS) |
| **Stack/composição** | Astro, TypeScript, Markdown/MDX com content collections, Tailwind CSS; CMS headless opcional; sem banco no caso padrão; testes: Playwright (listado entre as ferramentas de teste suportadas, docs.astro.build/en/guides/testing); formulários por serviço externo ou endpoint em modo servidor |
| **Preço** | Grátis (nenhum plano pago do framework encontrado nas páginas lidas) |
| **Licença** | MIT (LICENSE no repositório e registro npm, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Astro é um framework para sites em que o conteúdo é o centro. Por padrão, as páginas são pré-renderizadas como HTML estático no build (fonte: docs.astro.build/en/guides/on-demand-rendering). O JavaScript entra só nos componentes interativos, chamados "ilhas" (fonte: docs.astro.build/en/concepts/islands).

O conteúdo fica em arquivos Markdown ou MDX dentro do repositório, com schema opcional para validar cada entrada (content collections), ou vem de um CMS, banco ou API por loaders (fonte: docs.astro.build/en/guides/content-collections). Componentes React, Preact, Svelte, Vue, Solid e outros são suportados, mas não são obrigatórios (fonte: docs.astro.build/en/concepts/why-astro).

A documentação oficial pede Node.js v22.23.4 ou superior, e diz que versões ímpares como a v23 não são suportadas (docs.astro.build/en/install-and-setup). A versão atual do Astro no npm é a 7.4.13 (conferido em 2026-11-24), que exige Node `>=22.23.4`.

## Por que usar

- **Menos JavaScript no cliente:** "Zero JS, by default" (fonte: docs.astro.build/en/concepts/why-astro).
- **Conteúdo tipado:** content collections dão validação e tipos TypeScript para o conteúdo (fonte: docs.astro.build/en/guides/content-collections).
- **Páginas estáticas por padrão:** rotas são pré-renderizadas no build; renderização sob demanda é opcional, com adaptador (fonte: docs.astro.build/en/guides/on-demand-rendering). Hospedagem é da skill infra.
- **Aceita os componentes do framework que o time já conhece:** React, Preact, Svelte, Vue, Solid (fonte: docs.astro.build/en/concepts/why-astro).

## Quando usar

- Blog, documentação, site institucional, portfólio, landing page (a documentação cita marketing, publicação, documentação, blogs, portfólios, landing pages e e-commerce; fonte: docs.astro.build/en/concepts/why-astro).
- Site em que quem edita o conteúdo é o dev ou usa um CMS headless.
- Projeto em que SEO e velocidade de carregamento são prioridade: a própria documentação posiciona o Astro para sites que carregam rápido e têm bom SEO (fonte: docs.astro.build/en/concepts/why-astro).
- Site que precisa de uma ou duas áreas interativas (busca, formulário, calculadora).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Blog / documentação | ✅ Ótimo | Content collections e MDX (docs.astro.build/en/guides/content-collections); blogs e documentação estão entre os casos citados em why-astro |
| Site institucional / landing page | ✅ Ótimo | Sites de marketing e landing pages são casos citados em docs.astro.build/en/concepts/why-astro |
| Portfólio | ✅ Ótimo | Portfólio é caso citado em docs.astro.build/en/concepts/why-astro |
| E-commerce | 🟡 Serve | A documentação cita e-commerce entre os usos (why-astro); conta de usuário exige modo servidor e uma biblioteca de autenticação (docs.astro.build/en/guides/authentication) |
| MVP / protótipo | 🟡 Serve | Serve para página de validação (landing page); se o MVP é um app, veja as linhas de SaaS e dashboard |
| SaaS / app web | ❌ Evite | A documentação diz que o Astro foi desenhado para sites de conteúdo, e que outros frameworks são feitos para apps (why-astro): use [Next.js](02-nextjs-saas.md) ou [React Router/TanStack Start](03-react-router-tanstack-start.md) |
| Dashboard / painel admin | ❌ Evite | A documentação cita dashboards com login como caso de frameworks de aplicação, não do Astro (docs.astro.build/en/concepts/why-astro) |
| Sistema interno corporativo | ❌ Evite | Auth e banco vêm de bibliotecas e serviços externos (docs.astro.build/en/guides/authentication e /guides/backend); frameworks de aplicação cobrem isso melhor (why-astro) |
| Tempo real | ❌ Evite | Sem recurso oficial de tempo real encontrado na documentação lida; use backend à parte |
| App mobile | ❌ Evite | O Astro é um framework web (docs.astro.build/en/concepts/why-astro); para app de celular veja [Expo ou Flutter](11-mobile.md) |

## Quando é bom

- **Entrega leve:** a maior parte da página é HTML estático, com ilhas de JavaScript onde há interatividade (docs.astro.build/en/concepts/islands).
- **Conteúdo no repositório:** coleções locais leem Markdown, MDX, Markdoc, YAML, TOML e JSON (docs.astro.build/en/guides/content-collections); por ficarem no repositório, o Git versiona o conteúdo.
- **Várias bibliotecas de UI:** React, Preact, Svelte, Vue e Solid convivem no mesmo projeto (docs.astro.build/en/concepts/why-astro).
- **Integração com CMS:** há guias oficiais por CMS (docs.astro.build/en/guides/cms).

## Quando é ruim

- **Edição por não técnicos:** conteúdo local fica em arquivos do repositório; sem CMS, quem edita precisa mexer neles (docs.astro.build/en/guides/content-collections).
- **Muita interatividade:** a documentação coloca os frameworks de aplicação como a escolha para dashboards e apps complexos (docs.astro.build/en/concepts/why-astro).
- **Dados do usuário:** páginas por visitante exigem renderização sob demanda, com adaptador (docs.astro.build/en/guides/on-demand-rendering); login usa bibliotecas externas (docs.astro.build/en/guides/authentication).
- **Build estático:** por padrão as páginas são geradas no build; para renderizar rotas a cada visita, use renderização sob demanda (docs.astro.build/en/guides/on-demand-rendering).
- **Estado compartilhado entre ilhas:** exige uma biblioteca à parte; a receita oficial usa Nano Stores (docs.astro.build/en/recipes/sharing-state-islands).

## Como começar

Comando da documentação oficial (docs.astro.build/en/install-and-setup):

```bash
npm create astro@latest
```

Também existem `pnpm create astro@latest` e `yarn create astro`. O assistente guia a criação e permite escolher um template inicial (fonte: docs.astro.build/en/install-and-setup). Para componentes, veja a skill design (HyperUI). Estrutura de pastas é da skill architecture.

## Combina com / alternativas

- Conteúdo: Markdown/MDX no repositório, ou um CMS headless (guias oficiais em docs.astro.build/en/guides/cms).
- Estilo: Tailwind CSS (docs.astro.build/en/guides/styling) e [HyperUI](../../design/docs/04-hyperui.md).
- Hospedagem: skill infra.
- Quando a página vira app: migre a parte dinâmica para [Next.js](02-nextjs-saas.md) ou use uma API separada ([SPA + API](04-spa-vite-api.md)).
- Alternativas de fora: Eleventy (11ty.dev), Hugo (gohugo.io), WordPress (wordpress.org).

## Decisão rápida

- **Use se:** o site é majoritariamente conteúdo e velocidade e SEO importam (why-astro).
- **Evite se:** o projeto é um app com login, painel e muito estado, ou quem edita o conteúdo não pode mexer em Git e você não terá CMS.
