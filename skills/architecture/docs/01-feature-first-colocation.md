# Organizar por funcionalidade e colocation

> Agrupar os arquivos pelo assunto do negócio (pedidos, usuários, pagamentos) e deixar teste, estilo e tipo ao lado do código que usam, em vez de separar tudo por tipo técnico.

| | |
|---|---|
| **Referência oficial** | Redux Style Guide (redux.js.org/style-guide, conferido em 2026-11-24) e Next.js: "Colocation" e "Split project files by feature or route" (nextjs.org/docs/app/getting-started/project-structure). O Next.js documenta a divisão por feature como uma das estratégias; o restante do documento aplica essa estratégia a qualquer stack |
| **Categoria** | Parte 1 — Padrões que valem para qualquer stack |
| **Tipo** | Padrão de organização de pastas |
| **Vale para** | Qualquer linguagem e framework com módulos ou pacotes |
| **Verificado em** | 2026-11-24 |

## O que é

Há dois jeitos de dividir um projeto. Por tipo: `components/`, `hooks/`, `services/`, `models/`, cada pasta com arquivos de todos os assuntos. Por funcionalidade (feature): `orders/`, `users/`, `billing/`, cada pasta com o que aquele assunto precisa.

Colocation é a regra que acompanha: o que muda junto fica junto. O teste de `OrderList` fica ao lado de `OrderList`, junto do estilo e do tipo. Na documentação do Next.js, a página só vira rota se tiver `page` ou `route`, e o resto da pasta "pode ser colocado com segurança". A documentação diz que o Next.js não impõe uma organização; a escolha é do time.

## Por que usar

- **Manutenção:** o Redux Style Guide diz que colocar a lógica de uma feature em um só lugar "typically makes it easier to maintain that code" e recomenda a pasta por feature para a maioria dos apps (redux.js.org/style-guide).
- **Achar rápido:** o assunto da tarefa diz a pasta. "Corrigir o cancelamento de pedido" começa em `orders/`. É consequência direta da pasta por assunto, não um dado medido.
- **Colocation segura no Next.js:** arquivos de projeto podem ficar dentro das pastas de rota sem virar rota (nextjs.org/docs/app/getting-started/project-structure).

## Quando usar

- Projeto com vários assuntos distintos.
- Projetos que vão crescer ou ter mais de uma pessoa.
- Front-end React, Vue ou Svelte, back-end Node, Python, .NET ou PHP.
- Como base antes de vertical slice ([02](02-vertical-slice.md)) ou monólito modular ([04](04-monolito-modular.md)).

## Para que tipo de projeto

A tabela é recomendação deste guia, derivada de duas fontes: o Redux Style Guide recomenda feature folders para a maioria dos apps, e o Next.js documenta "Split project files by feature or route" como uma estratégia. As linhas de projeto pequeno não têm fonte oficial e não são afirmação das docs.

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site estático | 🟡 Serve | Poucos assuntos; `components/` e `sections/` bastam |
| SaaS / app web | ✅ Ótimo | Muitos assuntos que crescem juntos: o caso central |
| Dashboard / painel admin | ✅ Ótimo | Cada tela e relatório vira uma feature |
| API / back-end | ✅ Ótimo | Um módulo por assunto, com rota, serviço e teste juntos |
| App mobile | ✅ Ótimo | Telas e lógica por feature |
| Biblioteca pequena | 🟡 Serve | Costuma ter um assunto só |
| Script ou ferramenta de uma tarefa | ❌ Evite | Pasta por feature é cerimônia para 3 arquivos |
| Projeto pequeno que nunca vai crescer | 🟡 Serve | Poucos assuntos; a estrutura por tipo ainda é legível |

## Quando é bom

- **Lógica da feature junta:** o Redux Style Guide recomenda o "feature folder" (todos os arquivos da feature na mesma pasta).
- **Colocation permitida:** o Next.js documenta que arquivos podem ficar ao lado das rotas.
- **Fronteira verificável:** a regra "feature não importa de feature" pode ser checada por lint (ferramenta do time; sem recurso oficial único).

## Quando é ruim

- **Código compartilhado sem dono:** o que serve a duas features vai para `common/` e essa pasta vira lixeira se não houver critério (veja a regra no [SKILL.md](../SKILL.md)).
- **Feature mal recortada:** pasta `utils` ou `common` dentro de cada feature é sinal de recorte ruim.
- **Mistura de dois critérios:** metade por tipo, metade por feature deixa todos sem saber onde pôr.
- **Dependência circular:** `orders` importa `users` que importa `orders`. Resolva com uma interface ou um evento, ou una as duas.
- **Convenção do framework:** onde o framework manda por tipo (por exemplo `app/Models` no Laravel), respeite e use feature dentro do que for livre.

## Como começar

Exemplo em TypeScript (React), na árvore do Redux Style Guide, "Structure Files as Feature Folders with Single-File Logic" (https://redux.js.org/style-guide/#structure-files-as-feature-folders-with-single-file-logic, conferido em 2026-11-24): `app/` (configuração do app inteiro), `common/` (hooks, componentes genéricos e utilitários) e `features/` (uma pasta por assunto). A documentação do Next.js ("Colocation") confirma que colocation é permitida.

```
src/
├── index.tsx                  # entrada: renderiza a árvore de componentes
├── app/                       # configuração do app inteiro
│   ├── store.ts
│   └── App.tsx
├── common/                    # hooks, componentes genéricos, utilitários
└── features/                  # contém todas as pastas de feature
    └── orders/                # uma feature
        ├── ordersSlice.ts     # lógica (reducer e ações) da feature
        └── Orders.tsx         # componente da feature
```

Regras de nome e lugar:

- **Pasta:** nome do domínio, em minúsculas, no plural quando for coleção (`orders`).
- **Arquivo:** um padrão por projeto. React: `PascalCase.tsx` para componente, `camelCase.ts` para o resto; ou `kebab-case` em tudo. Escolha um e fixe no AGENTS.md.
- **Teste:** `nome.test.ts` ao lado, ou `__tests__/` na mesma pasta. Testes de ponta a ponta ficam em `e2e/` na raiz.
- **Regra de promoção:** começou dentro da feature. Só mova para `common/` quando uma segunda feature precisar.
- **Importação:** uma feature importa de outra só pelo `index.ts`, nunca por caminho interno.

## Combina com / alternativas

- [Vertical slice](02-vertical-slice.md): leva a ideia ao nível de caso de uso.
- [Monólito modular](04-monolito-modular.md): feature com fronteira forçada.
- [Next.js](06-nextjs.md), [React + Vite](07-react-vite.md): aplicam o padrão com as regras de cada um.
- Alternativa: pastas por tipo (veja "O que saiu da lista" no [README](README.md)).

## Decisão rápida

- **Use se:** o projeto tem vários assuntos de negócio e vai crescer.
- **Evite se:** é um script ou um site de 5 páginas; ou se o framework já impõe uma estrutura fixa que cobre o caso.
