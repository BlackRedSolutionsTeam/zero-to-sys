# React Native + Expo (Expo Router)

> Rotas por arquivo dentro de `src/app`, e todo o resto fora dela, porque qualquer arquivo dentro de `app` vira rota.

| | |
|---|---|
| **Referência oficial** | docs.expo.dev/router/basics/core-concepts/; template padrão do Expo (github.com/expo/expo, `templates/expo-template-default`); Redux Style Guide para `features/` |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção de framework (Expo Router) |
| **Vale para** | Apps Expo com Expo Router, em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

O Expo Router cria as telas a partir dos arquivos da pasta `app` (na documentação, `src/app`). O `_layout.tsx` na raiz é renderizado antes de qualquer rota e substitui o papel do `App.jsx`: é onde entram fontes, provedores de tema e splash screen (fonte: docs.expo.dev/router/basics/core-concepts/). O `index.tsx` atende a URL `/`. Pastas entre parênteses, como `(tabs)`, agrupam telas sem entrar na URL.

A documentação alerta: qualquer arquivo que não seja de rota dentro de `src/app` é tratado como rota. Por isso componentes, hooks e constantes ficam fora, em `src/components`, `src/hooks` e `src/constants`.

## Por que usar

- **Navegação por arquivo:** cada arquivo em `src/app` vira uma rota com URL, usável como deep link (docs.expo.dev/router/basics/core-concepts/).
- **Mesma rota em qualquer plataforma:** todas as páginas são acessíveis por URL em iOS, Android e web.

## Quando usar

- App mobile novo em React Native com Expo.
- Quando há compartilhamento de código com um site em React.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App mobile | ✅ Ótimo | Expo Router roda em iOS, Android e web (docs.expo.dev/router) |
| SaaS com app mobile | ✅ Ótimo | O app Expo pode ficar em `apps/mobile` de um monorepo (veja [05](05-monorepo.md)) |
| E-commerce mobile | ✅ Ótimo | Abas por grupo `(tabs)` e rotas dinâmicas por arquivo (docs.expo.dev/router/basics/notation) |
| MVP / protótipo | ✅ Ótimo | `create-expo-app` gera o template padrão com Expo Router (docs.expo.dev/router/installation) |
| Dashboard / painel admin | 🟡 Serve | Expo Router também gera web; use se precisar do app |
| Site / landing page | ❌ Evite | Use [Next.js](06-nextjs.md) ou Astro |
| App com muito código nativo próprio | 🟡 Serve | Código nativo próprio exige development build (docs.expo.dev/develop/development-builds/introduction) |

## Quando é bom

- **Rotas visíveis na árvore de arquivos** (`src/app`).
- **Telas separadas das peças reutilizáveis:** a documentação manda componentes e hooks fora de `src/app`.
- **Grupos `(x)`** agrupam telas sem entrar na URL.

## Quando é ruim

- **Arquivo errado na `app`:** um componente colocado ali vira rota e quebra a navegação.
- **Tela com lógica demais:** o arquivo de rota deve só montar a tela.
- **Layouts aninhados:** cada `_layout.tsx` abre um navegador; planeje a hierarquia.
- **Estrutura fora de `app` fica por sua conta**; a documentação só cita `src/components`, `src/hooks` e `src/constants` como exemplos.

## Como começar

Template padrão do Expo (`templates/expo-template-default` em github.com/expo/expo, conferido em 2026-11-24): `src/app`, `src/components`, `src/hooks`, `src/constants`, `assets/`, `app.json` (reconferido com a árvore do repositório hoje). Grupos `(x)` e a regra de manter o que não é rota fora de `app` vêm da documentação do Expo Router. `features/` segue o Redux Style Guide (https://redux.js.org/style-guide/#structure-files-as-feature-folders-or-ducks).

```
meu-app/
├── src/
│   ├── app/                        # OFICIAL: só rotas
│   │   ├── _layout.tsx             # OFICIAL: raiz, fontes e providers
│   │   ├── index.tsx               # OFICIAL: tela "/"
│   │   ├── (tabs)/                 # OFICIAL: grupo de abas
│   │   │   ├── _layout.tsx         # barra de abas
│   │   │   ├── index.tsx           # aba inicial
│   │   │   └── pedidos.tsx         # aba de pedidos
│   │   └── explore.tsx             # OFICIAL (template padrão): segunda rota
│   ├── features/                   # Redux Style Guide: uma pasta por assunto
│   │   └── orders/
│   │       ├── ordersSlice.ts
│   │       └── Orders.tsx
│   ├── components/                 # OFICIAL (template padrão): peças compartilhadas
│   ├── hooks/                      # OFICIAL (template padrão)
│   └── constants/                  # OFICIAL (template padrão): tema, cores, medidas
├── assets/                         # OFICIAL (template padrão): imagens
├── app.json                        # OFICIAL (template padrão): configuração do Expo
└── package.json
```

Regras de nome e lugar:

- **Em `app/` só rotas e `_layout`.** Nada de componente, hook ou utilitário.
- **Arquivo de rota:** o nome vira a URL; o template usa minúsculas (`explore.tsx`) e `kebab-case` nos componentes (`themed-text.tsx`). Escolha um padrão só.
- **Tela fina:** importa de `features/` e monta.
- **Grupos `(x)`** para abas e fluxos, sem alterar a URL.
- **Teste ao lado do arquivo** em `features/`, nunca em `app/` (viraria rota).

## Combina com / alternativas

- [Feature-first](01-feature-first-colocation.md) para `features/`.
- [Monorepo](05-monorepo.md): `apps/mobile` ao lado de `apps/web`.
- Alternativa: React Navigation puro, sem rotas por arquivo (reactnavigation.org).

## Decisão rápida

- **Use se:** é app mobile em React Native com Expo.
- **Evite se:** o projeto é só web ou usa outra pilha mobile (Flutter, nativo).
