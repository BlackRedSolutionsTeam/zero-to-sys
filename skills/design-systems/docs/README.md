# Layouts por tipo de sistema

Um documento por tipo de sistema, com a anatomia do layout, medidas, tokens, padrões essenciais, quando é bom e quando é ruim. Cada um tem um exemplo pronto em [../examples/](../examples/), com o mesmo número. As referências reais foram conferidas em 2026-11-24.

## Base

| Documento | O que é |
|---|---|
| [01-fundamentos.md](01-fundamentos.md) | Espaçamento, tipografia, cor, tokens, estados, responsividade e acessibilidade. Vale para todos os tipos |

## Telas de trabalho (o usuário passa o dia nelas)

| Layout | Estrutura | Direção visual do exemplo | Doc | Exemplo |
|---|---|---|---|---|
| Dashboard de análise | Barra lateral + KPIs, gráficos e tabela | Sóbria e densa, neutros frios, azul-índigo | [02](02-dashboard-analytics.md) | [HTML](../examples/02-dashboard-analytics.html) |
| Painel admin / CRUD | Barra lateral + tabela com filtros + formulário em painel | Compacta e neutra, cinzas quentes, verde-petróleo | [03](03-admin-crud.md) | [HTML](../examples/03-admin-crud.html) |
| CRM / kanban | Colunas de etapas + painel de detalhe | Escura, bordas finas, violeta discreto | [07](07-crm-kanban.md) | [HTML](../examples/07-crm-kanban.html) |
| Caixa de entrada / chat | Três colunas: lista, conversa, contexto | Clara e limpa, neutros frios, verde | [08](08-inbox-chat.md) | [HTML](../examples/08-inbox-chat.html) |
| Financeiro | Navegação no topo + saldo, fluxo e transações | Sóbria, muito espaço, verde-escuro | [09](09-financeiro.md) | [HTML](../examples/09-financeiro.html) |
| Agendamento | Grade semanal de horários + painel de marcação | Suave e amigável, tons pastel | [10](10-agendamento.md) | [HTML](../examples/10-agendamento.html) |

## Telas de borda (todo sistema tem)

| Layout | Estrutura | Direção visual do exemplo | Doc | Exemplo |
|---|---|---|---|---|
| Login, onboarding e configurações | Tela dividida, passos, seções com navegação lateral | Clara e acolhedora, laranja-coral | [04](04-auth-onboarding-configuracoes.md) | [HTML](../examples/04-auth-onboarding-configuracoes.html) |

## Telas públicas (vendem ou informam)

| Layout | Estrutura | Direção visual do exemplo | Doc | Exemplo |
|---|---|---|---|---|
| Landing page de SaaS | Seções empilhadas: hero, recursos, preços, FAQ | Escura e editorial, tipografia grande | [05](05-landing-saas.md) | [HTML](../examples/05-landing-saas.html) |
| E-commerce | Vitrine em grade, página de produto, carrinho lateral | Clara e quente, terracota, título serifado | [06](06-ecommerce.md) | [HTML](../examples/06-ecommerce.html) |
| Documentação | Navegação em árvore, coluna de leitura, índice | Tipográfica e calma, azul-cobalto | [11](11-documentacao.md) | [HTML](../examples/11-documentacao.html) |

## Mobile

| Layout | Estrutura | Direção visual do exemplo | Doc | Exemplo |
|---|---|---|---|---|
| App mobile | Abas inferiores, listas, folha inferior | Viva e tátil, cantos bem arredondados | [12](12-app-mobile.md) | [HTML](../examples/12-app-mobile.html) |

## Qual escolher

- **A tela responde "como estamos?":** [dashboard](02-dashboard-analytics.md). Se o usuário vai agir em cada linha, não é dashboard, é [CRUD](03-admin-crud.md).
- **A tela é uma lista de registros para manter:** [CRUD](03-admin-crud.md). É o layout mais usado em sistema interno; comece por ele.
- **Os itens passam por etapas:** [kanban](07-crm-kanban.md). Se o trabalho for editar muitos registros em lista, volte para a tabela do [CRUD](03-admin-crud.md).
- **O trabalho é responder pessoas:** [caixa de entrada](08-inbox-chat.md).
- **O centro é dinheiro:** [financeiro](09-financeiro.md).
- **O centro é o tempo:** [agendamento](10-agendamento.md).
- **É a porta de entrada do produto:** [landing](05-landing-saas.md) para vender, [login e onboarding](04-auth-onboarding-configuracoes.md) para entrar.
- **Vende produto físico:** [e-commerce](06-ecommerce.md).
- **É para ler:** [documentação](11-documentacao.md).
- **É app instalado no celular:** [app mobile](12-app-mobile.md). Sistema web usado no celular continua nos layouts acima, na versão responsiva.

Sempre junto: [fundamentos](01-fundamentos.md).

## O que ficou fora e por quê

| Layout | Motivo |
|---|---|
| Site institucional e blog | A estrutura é a da [landing](05-landing-saas.md) com menos seções, mais a coluna de leitura da [documentação](11-documentacao.md) |
| Portfólio | Depende de direção de arte própria; um exemplo genérico ajudaria pouco |
| Editor visual (canvas, design, fluxograma) | Interação muito específica de cada produto; não cabe num exemplo estático |
| Mapa e rastreamento | Depende de biblioteca de mapas e de dados reais |
| Rede social e feed | Padrão conhecido, mas pouco pedido em sistemas de negócio |
| Player de mídia e streaming | Caso específico, com regras próprias de conteúdo |
| Painel de TV / monitoramento em parede | Variante do [dashboard](02-dashboard-analytics.md) com fonte maior e sem interação |
| Formulário longo em etapas (wizard) | Coberto em parte pelo onboarding em [04](04-auth-onboarding-configuracoes.md) |
| E-mail transacional | Tem restrições próprias de HTML de e-mail; fora do escopo de telas |
