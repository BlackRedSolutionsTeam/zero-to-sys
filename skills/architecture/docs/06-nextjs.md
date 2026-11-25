# Next.js (App Router)

> Convenções de arquivo do App Router: a pasta define a rota, `page` a expõe e o resto fica ao lado, sem virar rota.

| | |
|---|---|
| **Referência oficial** | nextjs.org/docs/app/getting-started/project-structure (página atualizada em 2026-07-21) |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção de framework |
| **Vale para** | Next.js com App Router, em TypeScript ou JavaScript |
| **Verificado em** | 2026-11-24 |

## O que é

No App Router, pastas dentro de `app/` definem segmentos de URL. Arquivos especiais definem o que cada segmento faz: `layout`, `page`, `loading`, `error`, `not-found`, `route`, `template`, `default`. Uma rota só é pública se tiver `page` ou `route`.

A documentação diz que o Next.js é "unopinionated" sobre onde pôr o resto do código e mostra três estratégias: arquivos fora de `app`, arquivos em pastas de topo dentro de `app` ou divisão por feature ou rota. A recomendação é escolher uma e manter. Também existem pastas privadas `_pasta` (fora do roteamento), grupos `(grupo)` (fora da URL) e slots `@pasta` (rotas paralelas).

## Por que usar

- **Roteamento pelo sistema de arquivos:** a pasta diz a URL.
- **Colocation segura:** uma rota só é pública com `page` ou `route`, então outros arquivos ao lado não viram rota (nextjs.org/docs/app/getting-started/project-structure).
- **Layouts aninhados e grupos** sem mudar a URL.
- **Pasta `src/` opcional** separa código de configuração.

## Quando usar

- Projetos Next.js que usam o App Router.
- Apps com áreas distintas (marketing, loja, admin), via route groups.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS / app web | ✅ Ótimo | Route groups com layouts próprios e Server Actions (nextjs.org/docs/app/guides/authentication) |
| E-commerce / áreas distintas | ✅ Ótimo | A página de estrutura mostra `(marketing)` e `(shop)` com root layouts distintos |
| API pura | 🟡 Serve | `route` define endpoints, mas o foco do framework é a interface |
| App mobile | ❌ Evite | Next.js é web; use [Expo](08-react-native-expo.md) |

Outros tipos (blog, painel, landing): a documentação oficial não trata esses casos.

## Quando é bom

- **Convenção oficial clara** para rota, erro, carregamento e metadata.
- **Liberdade no resto:** a documentação diz que o Next.js é "unopinionated" sobre onde pôr os demais arquivos.
- **Guia oficial de organização** com exemplos de grupos e layouts.

## Quando é ruim

- **Nome reservado:** arquivo `page.tsx` ou `route.ts` em pasta de componente a transforma em rota. Não use esses nomes fora de rota.
- **Mistura de estratégias:** a documentação recomenda escolher uma e manter.
- **Lógica de negócio dentro de `page.tsx`:** escolha deste documento; a página só monta e a regra fica na feature.

## Como começar

Estratégia recomendada aqui: `app/` só para rotas e código por feature em `src/features` (escolha deste documento, uma das três mostradas na documentação). O que é convenção oficial está marcado.

```
meu-app/
├── src/
│   ├── app/                           # OFICIAL: roteamento
│   │   ├── layout.tsx                 # OFICIAL: layout raiz (html e body)
│   │   ├── page.tsx                   # OFICIAL: rota "/"
│   │   ├── global-error.tsx           # OFICIAL: erro global
│   │   ├── (marketing)/               # OFICIAL: grupo, não entra na URL
│   │   │   └── sobre/page.tsx         # rota "/sobre"
│   │   ├── (app)/                     # grupo da área logada
│   │   │   ├── layout.tsx             # layout só da área logada
│   │   │   └── pedidos/
│   │   │       ├── page.tsx           # "/pedidos": só monta a tela
│   │   │       ├── loading.tsx        # OFICIAL: skeleton
│   │   │       ├── [id]/page.tsx      # OFICIAL: rota dinâmica
│   │   │       └── _components/       # OFICIAL: pasta privada, só desta rota
│   │   └── api/health/route.ts        # OFICIAL: endpoint
│   ├── features/                      # OFICIAL: estratégia "Split project files by feature or route" (nextjs.org/docs/app/getting-started/project-structure)
│   │   └── orders/
│   │       ├── components/
│   │       ├── actions.ts             # server actions de pedidos
│   │       ├── queries.ts             # leitura de dados
│   │       └── types.ts
│   ├── components/ui/                 # OFICIAL: alias padrão do shadcn/ui em components.json (ui.shadcn.com/docs/components-json)
│   └── lib/                           # OFICIAL: alias `lib` do shadcn/ui e estratégia "Store project files outside of app" do Next.js
├── public/                            # OFICIAL: arquivos estáticos
├── proxy.ts                           # OFICIAL: proxy de requisições (ver nota)
├── next.config.ts
├── .env.local                         # OFICIAL: fora do git
└── tsconfig.json
```

Regras de nome e lugar:

- **Arquivos especiais em minúsculas** com o nome exato (`page`, `layout`, `loading`).
- **Pastas de rota:** minúsculas, `kebab-case`; dinâmica em `[colchetes]`.
- **Componentes:** `PascalCase.tsx`: o React exige nome de componente com inicial maiúscula e usa arquivos como `Gallery.js` nos exemplos (react.dev/learn/importing-and-exporting-components).
- **`page.tsx` fino:** busca dados, chama a feature, devolve a tela.
- **Pasta privada `_x`:** para o que é só daquela rota.
- **Nota:** a documentação lista `proxy.ts` como arquivo de raiz. Em versões antigas era `middleware.ts`; confira a versão do projeto.

## Combina com / alternativas

- [Feature-first](01-feature-first-colocation.md) para a pasta `features/`.
- [Monorepo](05-monorepo.md) quando o site divide pacotes com outros apps.
- Alternativa: [React + Vite](07-react-vite.md) (SPA).

## Decisão rápida

- **Use se:** o projeto é Next.js com App Router; mantenha `app/` só para rotas e a lógica por feature.
- **Evite se:** o projeto é um app mobile.
