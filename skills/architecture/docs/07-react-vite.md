# React + Vite (SPA por features)

> App de página única em React organizado por funcionalidade, com `index.html` na raiz e uma pasta por assunto dentro de `src/`.

| | |
|---|---|
| **Referência oficial** | vite.dev/guide: só define `index.html` na raiz como ponto de entrada e não prescreve pastas de `src/` (conferido). React: a documentação antiga (legacy.reactjs.org, FAQ de estrutura) diz que o React não tem opinião sobre pastas; o resto segue o template oficial `create-vite` `template-react-ts` (github.com/vitejs/vite, `packages/create-vite`): `index.html`, `public/` e `src/` com `main.tsx`, `App.tsx` e `assets/`. `app/`, `common/` e `features/` seguem o Redux Style Guide (https://redux.js.org/style-guide/#structure-files-as-feature-folders-or-ducks, conferido em 2026-11-24). Astro: docs.astro.build/en/basics/project-structure/ |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Template oficial create-vite e Redux Style Guide |
| **Vale para** | React + Vite em TypeScript; a mesma ideia serve a Vue e Svelte |
| **Verificado em** | 2026-11-24 |

## O que é

O Vite trata o `index.html` como código-fonte, na raiz do projeto, e não dentro de `public/`. Fora isso, ele não impõe pastas. O React também não: a própria documentação do React diz que não há opinião sobre estrutura de arquivos.

Por isso a organização é decisão do time. Uma opção documentada: `src/features/` com uma pasta por assunto, `src/common/` para o que serve a mais de uma feature e `src/app/` para a configuração do app inteiro (Redux Style Guide, conferido em 2026-11-24).

Nota sobre Astro: a documentação do Astro reserva só `src/pages/` (obrigatória, cada arquivo vira rota). `src/components/`, `src/layouts/` e `src/styles/` são convenção, não obrigação; `public/` guarda arquivos sem processamento. A estrutura por feature do quadro abaixo vale também para as ilhas React de um projeto Astro.

## Por que usar

- **Sem pastas impostas:** o Vite só exige o `index.html` na raiz (vite.dev/guide) e o React não opina sobre estrutura, então a pasta segue o domínio.
- **Pasta por feature:** o Redux Style Guide recomenda organizar por feature (redux.js.org/style-guide).

## Quando usar

- SPA atrás de login: painel, dashboard, app interno.
- Projeto sem necessidade de SEO ou renderização no servidor (o `template-react-ts` gera só `index.html` e `src/main.tsx`, sem servidor).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Dashboard / painel admin | ✅ Ótimo | Não há SSR no template create-vite; a pasta por feature separa as telas |
| Sistema interno corporativo | ✅ Ótimo | Sem servidor no template; pastas por feature organizam muitas telas |
| SaaS / app web | ✅ Ótimo | Astro documenta ilhas React (docs.astro.build); a área logada pode ser SPA |
| MVP / protótipo | ✅ Ótimo | `npm create vite` gera o template pronto (vite.dev/guide) |
| Landing page / site de marketing | 🟡 Serve | O template não tem SSR; o HTML inicial vem sem o conteúdo |
| Blog / conteúdo | ❌ Evite | Astro tem `src/pages/` por arquivo (docs.astro.build/en/basics/project-structure/); veja também [Next.js](06-nextjs.md) |
| E-commerce | 🟡 Serve | O template não tem SSR; para SEO veja [Next.js](06-nextjs.md) |

## Quando é bom

- **Estrutura que acompanha o negócio**, não o framework (Redux Style Guide).
- **Poucas regras impostas:** só `index.html` na raiz (vite.dev/guide).
- **Variáveis `VITE_`** são as únicas expostas ao cliente (vite.dev/guide/env-and-mode).

## Quando é ruim

- **Nada impõe pastas:** nem Vite nem React definem estrutura; adote feature-first desde o início.
- **Roteamento fica por sua conta:** o template não traz roteador; escolha uma biblioteca e siga a estrutura dela.
- **Sem SSR:** páginas públicas dependem de JavaScript para aparecer.
- **Importação cruzada:** feature importando interno de outra. O ESLint tem a regra `no-restricted-imports` para proibir caminhos de importação (eslint.org/docs/latest/rules/no-restricted-imports). O Vite recomenda evitar barrel files, que carregam mais arquivos que o necessário (vite.dev/guide/performance).

## Como começar

Template create-vite: `index.html` na raiz, `public/`, `src/main.tsx`, `src/App.tsx`, `src/assets/`, `src/index.css`, `src/App.css`, `vite.config.ts`, `tsconfig.json`. `app/`, `common/` e `features/` vêm do Redux Style Guide (conferido em 2026-11-24).

```
meu-app/
├── index.html                    # create-vite: entrada, na raiz
├── public/                       # create-vite: arquivos copiados sem processar
├── src/
│   ├── main.tsx                  # create-vite: ponto de entrada
│   ├── App.tsx                   # create-vite: componente raiz
│   ├── index.css, App.css        # create-vite: estilos
│   ├── assets/                   # create-vite: imagens importadas
│   ├── app/                      # Redux: configuração do app inteiro (store)
│   ├── common/                   # Redux: hooks, componentes genéricos, utilitários
│   └── features/                 # Redux: uma pasta por assunto
│       └── orders/
│           ├── ordersSlice.ts
│           └── Orders.tsx
├── vite.config.ts                # create-vite
└── tsconfig.json                 # create-vite
```

Regras de nome e lugar:

- **Componente:** `PascalCase.tsx`. Hook: `useAlgo.ts`. Demais: `camelCase.ts` ou `kebab-case.ts`, um padrão só.
- **Apelido de importação:** `@/features/orders` configurado no tsconfig e no Vite evita `../../..`.
- **Testes e estilos** ao lado do arquivo ([01](01-feature-first-colocation.md)).
- **Variáveis de ambiente:** `.env` na raiz; no Vite só as prefixadas com `VITE_` chegam ao cliente (vite.dev/guide/env-and-mode, conferido em 2026-11-24).

## Combina com / alternativas

- [Feature-first](01-feature-first-colocation.md) é a base.
- [Next.js](06-nextjs.md): quando precisar de SSR e SEO.
- [Monorepo](05-monorepo.md): o app vira `apps/web`.
- Alternativa para conteúdo: Astro, com `src/pages/` obrigatória.

## Decisão rápida

- **Use se:** é uma SPA sem necessidade de SEO e o time quer liberdade.
- **Evite se:** o site é público e depende de busca, ou o time não vai manter a disciplina de pastas.
