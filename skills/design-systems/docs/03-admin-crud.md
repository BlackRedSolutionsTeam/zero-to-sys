# Painel admin / CRUD

> Lista densa e rápida de ler, com busca, filtros e ações em lote, e o formulário de criar e editar num painel lateral que abre sem tirar a pessoa da lista.

| | |
|---|---|
| **Tipo de sistema** | Painel administrativo, sistema interno, back-office (contratos, estoque, cadastros, usuários) |
| **Exemplo** | [03-admin-crud.html](../examples/03-admin-crud.html) |
| **Layout base** | Barra lateral fixa + barra superior fina + conteúdo com tabela; formulário em drawer à direita |
| **Referências reais** | Linear (https://linear.app), Stripe (https://stripe.com), Shopify (https://www.shopify.com), Airtable (https://www.airtable.com) e Attio (https://attio.com). Os URLs responderam 200 em 2026-11-24; as telas internas exigem login e não foram abertas, então o doc não descreve o design delas |
| **Componentes** | shadcn/ui: Table, Sheet (drawer), Input, Select, Checkbox, Badge, Tabs, Pagination, Dropdown Menu, Skeleton, Toast (aviso) (lista em ui.shadcn.com/docs/components, 2026-11-24). Lucide para ícones. TanStack Table para ordenação e seleção, se for React |
| **Verificado em** | 2026-11-24 |

## O que é

É a tela de trabalho de quem cadastra, confere e corrige dados o dia todo. A tela principal é uma lista: tabela com uma linha por registro, busca no topo, filtros, seleção de várias linhas para agir em lote e paginação. Criar e editar acontecem num painel lateral (drawer) que desliza por cima da lista, então o contexto não se perde.

O exemplo (marca fictícia Lastro, gestão de contratos) mostra a lista completa, o drawer com validação visível e quatro estados da lista: com dados, carregando, vazio e erro.

## Por que este layout

- **Densidade:** a pessoa vê muitas linhas sem rolar. Linhas de 44 px e texto de 14 px.
- **Contexto preservado:** o drawer deixa a lista visível atrás. Quem edita o 5º registro não perde o lugar nem o filtro.
- **Menos telas:** uma rota (`/contratos`) cobre listar, criar e editar. Menos navegação, menos código.
- **Ações no lugar certo:** a barra de lote aparece só quando há seleção, e a ação principal fica sempre no canto superior direito.
- **Tom de ferramenta:** cinzas quentes e uma cor de marca só para o que é clicável ou selecionado deixam a atenção nos dados.

## Quando usar

- A pessoa repete a mesma tarefa de cadastro e conferência muitas vezes por dia.
- O registro tem poucos campos (cabe em um drawer com rolagem).
- Há muitos registros e a busca e o filtro são mais usados que a navegação.
- Existem ações em lote: arquivar, exportar, excluir, trocar responsável.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Sistema interno (contratos, estoque, RH) | ✅ Ótimo | É o caso central: cadastro e conferência em volume |
| Back-office de e-commerce ou SaaS | ✅ Ótimo | Pedidos, clientes e usuários seguem o mesmo padrão |
| Gestão de usuários e permissões | ✅ Ótimo | Lista com filtro por perfil e edição rápida |
| CRM simples (lista de contatos) | 🟡 Serve | Funciona, mas pipeline pede kanban (ver 07) |
| Dashboard de métricas | 🟡 Serve | Use a tabela como apoio, não como tela principal (ver 02) |
| Cadastro com formulário muito longo (muitos campos, várias etapas) | ❌ Evite | O drawer fica apertado; use página inteira com seções |
| App para o cliente final | ❌ Evite | Tabela densa assusta quem não é do ofício |
| Site de conteúdo ou marketing | ❌ Evite | Não há dados para listar |

## Anatomia do layout

```
┌────────┬──────────────────────────────────────────┐
│ Marca  │ Topo: migalhas · busca global · tema     │ 48 px
│        ├──────────────────────────────────────────┤
│ Menu   │ Título + subtítulo      [Exportar][Novo] │
│ lateral│ ┌─────┬─────┬─────┬─────┐ resumo (4 cards)│
│ 232 px │ └─────┴─────┴─────┴─────┘                │
│        │ ┌──────────────────────────────────────┐ │
│        │ │ Abas de status                       │ │
│ Perfil │ │ Busca · Filtros                      │ │
│        │ │ [barra de lote: 3 selecionados ...]  │ │
│        │ │ ☐ Contrato  Categoria  Valor  Status │ │
│        │ │ ☐ linhas de 44 px ...                │ │
│        │ │ 1–8 de 248             ‹ 1 2 3 … ›   │ │
│        │ └──────────────────────────────────────┘ │
└────────┴──────────────────────────────┬───────────┤
                                        │ Drawer    │
                                        │ 440 px    │
                                        └───────────┘
```

- **Barra lateral:** 232 px, fixa, itens de 32 px, rótulos de grupo em maiúsculas pequenas. Perfil do usuário no rodapé.
- **Barra superior:** 48 px, fixa ao rolar, com migalhas à esquerda e tema à direita.
- **Conteúdo:** padding de 20 px no topo, 24 px nas laterais e 32 px embaixo, largura máxima de 1280 px. Resumo em grade de 4 colunas com 12 px de espaço.
- **Tabela:** cabeçalho de 36 px (fixo), linhas de 44 px, células com 12 px de padding lateral. Números alinhados à direita e tabulares.
- **Barra de lote:** substitui visualmente a faixa de filtros (aparece abaixo dela) só com 1 ou mais linhas marcadas.
- **Drawer:** 440 px, cabeçalho de 49 px (12 px de padding, título de 24 px de linha e borda de 1 px), corpo rolável, rodapé fixo com Cancelar e Salvar. Fundo escurecido, Esc fecha, foco volta ao botão que abriu.
- **Tablet (até 1023 px):** resumo vira 2 colunas; a tabela rola dentro do próprio contêiner.
- **Celular (até 860 px):** a barra lateral vira gaveta aberta pelo ícone de menu; o drawer ocupa a largura toda da tela quando ela tem menos de 440 px; filtros secundários são ocultados (`hide-m`); até 520 px, o formulário vira 1 coluna e o botão "Novo" ocupa a largura toda.

## Tokens do exemplo

| Token | Claro | Escuro |
|---|---|---|
| Fundo da página | `#f6f5f3` | `#151413` |
| Superfície (cards, tabela) | `#ffffff` | `#1d1c1a` |
| Borda | `#e4e1db` | `#34312d` |
| Texto / texto secundário | `#1f1d1a` / `#645f57` | `#ecebe8` / `#a8a298` |
| Marca (verde-petróleo) | `#0f766e` (texto sobre ela `#ffffff`) | `#3cc4b4` (texto sobre ela `#06201d`) |
| Marca suave (seleção) | `#e1f0ee` | `#16312e` |
| Status ok / atenção / erro | `#166534` / `#8a4b00` / `#b42318` | `#6fd58f` / `#f2b45a` / `#ff8f84` |

| Item | Valor |
|---|---|
| Fonte | Inter, com pilha do sistema como fallback |
| Escala tipográfica | 11 (rótulo de grupo) · 12 (apoio, cabeçalho de tabela) · 13 (migalhas, nome do perfil) · 14 (corpo) · 15 (marca, título de estado) · 16 (título de drawer) · 20 (título de página e números do resumo; 17 no celular) |
| Raio | 6 px (controles), 10 px (cards e tabela), 11 px (chips) |
| Sombra | `0 1px 2px` bem leve nos cards; sombra forte só no drawer |
| Espaçamento | escala de 4/8 px: 4, 8, 12, 16, 24, 32 |

## Componentes e padrões essenciais

- **Tabela:** cabeçalho fixo, ordenação por coluna, primeira coluna com o identificador em destaque e dado secundário embaixo, última coluna com ação da linha.
- **Busca e filtros:** campo de busca com ícone, filtros em selects, abas de status com contador. Mostre os filtros ativos e um "limpar".
- **Seleção em lote:** caixa de seleção por linha e no cabeçalho (com estado indeterminado). A barra de lote mostra "N selecionados" e as ações.
- **Status:** etiqueta com ponto e texto, nunca só cor.
- **Paginação:** "1–8 de 248" e páginas; deixe a quantidade por página escolhível se o volume for grande.
- **Drawer de formulário:** campos agrupados por título, obrigatórios marcados com asterisco, dica abaixo do campo, mensagem de erro no lugar da dica, foco no primeiro campo com erro ao salvar, aviso rápido ao concluir.
- **Estado vazio:** ícone, título que diz o que falta, uma frase e o botão da ação principal.
- **Estado carregando:** linhas fantasma (skeleton) com a altura real das linhas, para a página não pular.
- **Estado de erro:** mensagem sem culpar a pessoa, diz que os dados estão salvos e oferece "Tentar novamente".
- **Ação destrutiva:** pede confirmação e usa a cor de erro só nela.

## Quando é bom

- Quem trabalha na tela todo dia ganha velocidade: a lista fica ao fundo e nada precisa recarregar.
- Pouca navegação: um módulo inteiro cabe em uma rota.
- Fácil de crescer e bom para teclado: novas colunas entram sem mudar a estrutura, Esc fecha o drawer.

## Quando é ruim

- **Formulário grande demais:** tem muitos campos ou etapas, o drawer vira rolagem sem fim. Use página inteira.
- **Muitas colunas no celular:** tabela larga sem plano. Deixe rolar dentro do contêiner ou vire cartões.
- **Erros comuns:**
  - Validar só no envio e mostrar o erro em um aviso que some. O erro tem de ficar junto do campo.
  - Mensagem genérica ("campo inválido"). Diga o formato esperado.
  - Perder o filtro e a página ao salvar. Mantenha na URL.
  - Mostrar status só com cor.
  - Linhas altas demais, que escondem dados (o exemplo usa 44 px).
  - Excluir sem confirmar, ou confirmar tudo, o que ensina a clicar sem ler.
  - Estado vazio em branco ou carregando sem indicação.

## Como começar

1. Abra [03-admin-crud.html](../examples/03-admin-crud.html) no navegador. Teste o botão "Novo contrato", salve com campos vazios para ver a validação, marque linhas para ver a barra de lote, e use o seletor de estado da lista.
2. Copie as variáveis CSS do `:root` (claro e escuro) para o projeto.
3. Troque a cor de marca (`--brand`, `--brand-soft`) e confira o contraste do texto sobre ela (mínimo 4,5:1 para texto normal, WCAG 1.4.3, w3.org/WAI/WCAG22/Understanding/contrast-minimum, 2026-11-24).
4. Monte com a skill design: shadcn/ui (Table, Sheet, Input, Select, Checkbox, Badge, Tabs, Skeleton) e ícones Lucide. Veja `design/docs/01-shadcn-ui.md` e `design/docs/05-lucide.md`.
5. Troque os dados fictícios pelos do seu domínio e ajuste as colunas.

## Combina com / alternativas

- Fundamentos de espaçamento e tipografia: [01-fundamentos.md](01-fundamentos.md)
- Cartões de resumo e gráficos acima da lista: [02-dashboard-analytics.md](02-dashboard-analytics.md)
- Login e configurações do mesmo sistema: [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md)
- Lista de pessoas com funil: [07-crm-kanban.md](07-crm-kanban.md)
- Lista de lançamentos e valores: [09-financeiro.md](09-financeiro.md)

## Decisão rápida

**Use se:** a equipe cadastra e confere muitos registros por dia, o registro tem poucos campos e há ações em lote.

**Evite se:** o formulário é longo ou em etapas, o público é o cliente final, ou a tela principal deveria ser um gráfico ou um quadro kanban.
