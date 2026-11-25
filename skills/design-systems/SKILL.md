---
name: design-systems
description: 'Catálogo de layouts por tipo de sistema (dashboard, admin/CRUD, login, landing, e-commerce, kanban, chat, financeiro, agendamento, docs, mobile) com anatomia, tokens e HTML de referência. Use antes de montar uma tela nova ou quando pedirem "como deve ser o layout".'
---

# design-systems

Catálogo de layouts por tipo de sistema. Cada tipo tem um documento em `docs/` (anatomia, medidas, tokens, padrões essenciais, erros comuns) e um exemplo em `examples/` (um HTML autocontido, com tema claro e escuro, que mostra o layout pronto). Esta skill decide a **estrutura e o visual da tela**; os componentes e ícones para montá-la vêm da skill `design`.

## Como usar esta skill

1. **Descubra o tipo de tela** que o pedido envolve e o que o projeto já tem: marca (cores, fonte, logotipo), telas prontas, UI kit instalado. O que já existe no projeto tem prioridade sobre o exemplo.
2. **Escolha o layout pela tabela abaixo.** Um sistema costuma juntar vários: um SaaS tem landing (05), login e configurações (04), dashboard (02) e listas (03).
3. **Leia o documento do tipo** em `docs/` e **abra o exemplo** em `examples/`. Confira "Anatomia do layout", "Componentes e padrões essenciais" e "Quando é ruim".
4. **Leia [docs/01-fundamentos.md](docs/01-fundamentos.md)** se ainda não leu nesta tarefa: as regras de espaçamento, tipografia, cor e estados valem para todos os tipos.
5. **Monte a tela na stack do projeto**, com os componentes da skill `design`. Use o exemplo como referência de estrutura, medidas e hierarquia; não cole o HTML dele no projeto.
6. **Troque os tokens pela marca do cliente** e confira o resultado renderizado, em tela grande e em celular, nos temas claro e escuro.
7. **Explique a escolha ao usuário em uma ou duas frases**: qual layout e por quê.

## Qual layout usar

| O usuário precisa | Layout | Documento | Exemplo |
|---|---|---|---|
| Ver números e acompanhar indicadores | Dashboard de análise | [02](docs/02-dashboard-analytics.md) | [HTML](examples/02-dashboard-analytics.html) |
| Cadastrar, listar, filtrar e editar registros | Painel admin / CRUD | [03](docs/03-admin-crud.md) | [HTML](examples/03-admin-crud.html) |
| Entrar, se cadastrar, configurar a conta | Login, onboarding e configurações | [04](docs/04-auth-onboarding-configuracoes.md) | [HTML](examples/04-auth-onboarding-configuracoes.html) |
| Conhecer e comprar um produto digital | Landing page de SaaS | [05](docs/05-landing-saas.md) | [HTML](examples/05-landing-saas.html) |
| Comprar produtos físicos | E-commerce | [06](docs/06-ecommerce.md) | [HTML](examples/06-ecommerce.html) |
| Mover itens por etapas (vendas, tarefas) | CRM / quadro kanban | [07](docs/07-crm-kanban.md) | [HTML](examples/07-crm-kanban.html) |
| Conversar e atender (mensagens, tickets) | Caixa de entrada / chat | [08](docs/08-inbox-chat.md) | [HTML](examples/08-inbox-chat.html) |
| Ver saldo, pagar, conferir transações | Financeiro | [09](docs/09-financeiro.md) | [HTML](examples/09-financeiro.html) |
| Marcar horário e ver a agenda | Agendamento | [10](docs/10-agendamento.md) | [HTML](examples/10-agendamento.html) |
| Ler e consultar conteúdo técnico ou ajuda | Documentação | [11](docs/11-documentacao.md) | [HTML](examples/11-documentacao.html) |
| Usar no celular, em app instalado | App mobile | [12](docs/12-app-mobile.md) | [HTML](examples/12-app-mobile.html) |
| Qualquer tela: vazio, carregando, erro, sem permissão | Estados de tela | [13](docs/13-estados-de-tela.md) | no próprio doc |
| Site público que precisa aparecer no Google | SEO | [14](docs/14-seo.md) | no próprio doc |

As regras comuns a todos estão em [docs/01-fundamentos.md](docs/01-fundamentos.md).

| Tipo de projeto | Layouts que costuma juntar |
|---|---|
| SaaS B2B | 05 (site), 04 (entrada e conta), 02 (início), 03 (listas e cadastros) |
| Sistema interno / ERP | 04, 03 como base, 02 para a visão geral |
| CRM, gestão de projetos, helpdesk | 04, 07 ou 08 como tela principal, 03 para cadastros, 02 para relatórios |
| Loja virtual | 06 para o cliente, 03 e 02 para o painel do lojista |
| Fintech, conta digital | 05, 04, 09 como tela principal |
| Clínica, salão, serviços | 10 como tela principal, 03 para cadastros, 04 |
| Produto para desenvolvedores | 05, 11, 02 |
| App de celular | 12, com 04 adaptado para as telas de entrada |

## Checklist de toda tela montada a partir de um layout

- [ ] O layout foi escolhido pela ação principal da tela, e o motivo está registrado (conferir na conversa ou no PR).
- [ ] Cores, tipografia, espaçamento e raio estão em tokens, sem valor solto no CSS (`grep -rnE '#[0-9a-fA-F]{3,6}' src`).
- [ ] A tela usa os tokens da marca do projeto, não os do exemplo (`diff` entre os tokens do projeto e os do exemplo).
- [ ] A tela tem os estados vazio, carregando e erro (`grep -rniE 'empty|loading|error' src`).
- [ ] Abaixo de 600 px a barra lateral, a tabela e as colunas viram o que o documento diz (abrir a 360 px).
- [ ] O contraste atinge AA e o foco é visível (Lighthouse de acessibilidade ou `axe`).
- [ ] Alvos de toque têm pelo menos 44 pt e a informação não depende só de cor (inspecionar a tela).
- [ ] A tela foi aberta e olhada em tema claro e escuro (captura de tela das duas).
- [ ] Nenhum visual, nome ou logotipo de produto existente foi copiado (comparar com a referência).

## Regras de uso

- **O layout segue a tarefa do usuário, não a moda.** Escolha pela ação principal da tela (ver, cadastrar, mover, conversar, comprar), não pelo que está bonito no exemplo.
- **A marca do cliente ganha do exemplo.** Cores, fonte e raio do exemplo são ponto de partida. Se o projeto já tem tokens, use os dele e mantenha só a estrutura.
- **Exemplo é referência, não código de produção.** O HTML é puro para abrir em qualquer lugar. No projeto, monte com os componentes da stack (skill `design`) e os tokens no sistema de tema dela.
- **Tokens antes de telas.** Defina cores, tipografia, espaçamento e raio em variáveis uma vez, e use só elas. Valor solto no meio do CSS é o que quebra a consistência.
- **Um sistema, uma direção visual.** Os exemplos têm direções diferentes de propósito. Dentro de um mesmo produto, todas as telas usam os mesmos tokens, mesmo vindo de layouts diferentes.
- **Toda tela tem estados.** Vazio, carregando e erro fazem parte do layout. Tela que só funciona com dados perfeitos não está pronta.
- **Celular não é opcional.** Cada documento diz o que a barra lateral, a tabela e as colunas viram em tela estreita. Confira abaixo de 600 px (breakpoint compact do Material 3, m3.material.io/foundations/layout/breakpoints/overview, 2026-11-24), por exemplo em 360 px.
- **Acessibilidade é parte do visual.** Contraste AA (WCAG 1.4.3), foco visível (MDN `:focus-visible`), alvo de toque de 44 pt no iOS (Apple HIG, Accessibility, 2026-11-24; o piso do WCAG 2.5.8 é 24 px) e informação que não depende só de cor (Apple HIG, Accessibility).
- **Não copie produto existente.** As referências reais dos documentos servem para estudar princípios. Não reproduza o visual, o nome nem o logotipo de nenhuma delas.
- **Confira renderizado.** Não diga que a tela está pronta sem abrir e olhar, em claro e escuro.

## Quando a lista não cobre

Se a tela pedida não se encaixa em nenhum dos onze tipos (editor visual, mapa, player de mídia, jogo, painel de TV, formulário longo de várias etapas), diga isso ao usuário, aplique os [fundamentos](docs/01-fundamentos.md) e monte a partir do tipo mais próximo. O `docs/README.md` registra o que ficou fora, com o motivo.

## Validade dos dados

As referências reais citadas nos documentos foram conferidas em 2026-11-24. Sites mudam de visual: trate-as como ponto de estudo, não como garantia de que ainda estão como descrito.
