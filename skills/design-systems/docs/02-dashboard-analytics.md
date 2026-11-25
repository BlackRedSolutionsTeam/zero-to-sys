# Dashboard analytics

> Painel de SaaS com barra lateral, números-chave no topo, gráficos no meio e uma tabela de itens recentes embaixo: sóbrio, denso e feito para consultar todo dia.

| | |
|---|---|
| **Tipo de sistema** | Painel de análise de dados (SaaS de vendas, produto, marketing, finanças) |
| **Exemplo** | [02-dashboard-analytics.html](../examples/02-dashboard-analytics.html) (marca fictícia Vendara) |
| **Layout base** | Barra lateral fixa + cabeçalho + conteúdo em cartões |
| **Referências reais** | Plausible (https://plausible.io), PostHog (https://posthog.com), Stripe Dashboard (https://docs.stripe.com/dashboard/basics), Linear (https://linear.app). URLs responderam 200 em 2026-11-24 (stripe.com/docs/dashboard redireciona para docs.stripe.com/dashboard/basics); o painel de cada produto fica atrás de login e não é público, só o que os sites e a documentação mostram |
| **Componentes** | shadcn/ui (Card, Table, Tabs, Badge, Sheet para a gaveta, Skeleton, Select, Button), Lucide para ícones, gráficos pelo componente Chart do shadcn, que usa Recharts (ui.shadcn.com/docs/components/chart, 2026-11-24), ou SVG próprio (o exemplo usa SVG) |
| **Verificado em** | 2026-11-24 |

## O que é

Uma tela de resumo. Em uma olhada o usuário vê como o negócio está (KPIs), como evoluiu (gráficos) e o que acabou de acontecer (tabela de itens recentes). Tudo no mesmo período, escolhido num seletor no topo.

## Por que este layout

- A **barra lateral** guarda a navegação sem gastar altura, e o usuário sempre sabe onde está.
- Os **KPIs no topo** respondem "estou bem?" em dois segundos.
- **Gráficos** mostram tendência, que um número solto não mostra.
- A **tabela** leva do resumo ao detalhe: cada linha abre o item.
- A grade de cartões deixa reordenar e adicionar blocos sem refazer a tela.

## Quando usar

- Primeira tela depois do login em produtos de análise, vendas, métricas ou operação.
- Quando o usuário volta todo dia para acompanhar números.
- Quando há poucas métricas principais e um ou dois recortes (tempo, canal).

## Para que tipo de projeto

| Projeto | Encaixe | Por quê |
|---|---|---|
| SaaS de métricas, vendas ou marketing | ✅ Ótimo | É o caso central |
| Painel interno de operação ou diretoria | ✅ Ótimo | Acompanhamento diário, denso e comparativo |
| Painel de admin com muito cadastro | 🟡 Serve | Use como início, mas o trabalho está nas listas e formulários (ver 03-admin-crud.md) |
| App financeiro | 🟡 Serve | Serve para visão geral; extratos e conciliação pedem layout próprio (09-financeiro.md) |
| Landing page | ❌ Evite | Pede narrativa, não densidade (05-landing-saas.md) |
| App mobile | ❌ Evite | Gráficos e tabelas densos funcionam mal em tela pequena; simplifique (12-app-mobile.md) |

## Anatomia do layout

```
+----------+--------------------------------------------------+
| Logo     | Breadcrumb            [ Buscar... ]   [tema]     | 56 px
| Visão    +--------------------------------------------------+
| Pedidos  | Título               [7d|30d|90d] [Exportar]     |
| Clientes | [Painel|Carregando|Vazio|Erro]                   |
| ...      | +-------+ +-------+ +-------+ +-------+          |
|          | | KPI   | | KPI   | | KPI   | | KPI   |          |
| Análises | +-------+ +-------+ +-------+ +-------+          |
| ...      | +---------------------------+ +---------------+  |
|          | | Gráfico de linhas  (2fr)  | | Por canal(1fr)|  |
| Conta    | +---------------------------+ +---------------+  |
| ...      | +----------------------------------------------+ |
| [avatar] | | Tabela de pedidos recentes                   | |
+----------+ +----------------------------------------------+ |
  240 px                  conteúdo, até 1440 px
```

- **Barra lateral:** 240 px, fixa, com grupos de navegação (rótulo de 11 px em caixa alta), item ativo com fundo da marca suave, perfil no rodapé.
- **Cabeçalho:** 56 px, fixo, com breadcrumb, busca (260 px) e botão de tema.
- **Conteúdo:** padding de 24 px, largura máxima de 1440 px, vão de 16 px entre cartões.
- **KPIs:** 4 colunas iguais; cada cartão tem rótulo, valor de 26 px, variação em pílula (seta + cor + sinal) e minigráfico.
- **Gráficos:** linha em 2fr e distribuição em 1fr; legenda no cabeçalho do cartão; ponto destacado com valor.
- **Tabela:** linhas de 48 px, cabeçalho de 36 px com fundo cinza, números à direita, rodapé com contagem e paginação.
- **Tablet (até 1100 px):** KPIs em 2 colunas e gráficos empilhados.
- **Celular (até 860 px):** a barra lateral vira gaveta aberta pelo botão de menu (com fundo escurecido e Esc para fechar); KPIs em 1 coluna até 520 px; a tabela rola dentro do cartão e esconde a coluna menos importante.

## Tokens do exemplo

| Token | Claro | Escuro |
|---|---|---|
| Fundo / superfície / superfície 2 | `#f6f7f9` / `#ffffff` / `#f1f3f6` | `#0d1118` / `#141a24` / `#1a212d` |
| Borda / borda forte | `#e3e7ed` / `#cfd5de` | `#242d3b` / `#334053` |
| Texto / secundário / terciário | `#151b26` / `#4a5565` / `#636e7f` | `#e8ecf2` / `#aab3c2` / `#8893a5` |
| Marca (índigo) / suave | `#4338ca` / `#eceefe` | `#8b93ff` / `#212650` |
| Sucesso / alerta / erro | `#0f7b4f` / `#a15c07` / `#c0322b` | `#4cc38a` / `#e5a94a` / `#f2837c` |
| Séries do gráfico | `#4338ca`, `#0e8aa8`, `#b7791f` | `#8b93ff`, `#45c2dd`, `#e5a94a` |

| Item | Valor |
|---|---|
| Fonte | Inter, com fallback para a pilha do sistema |
| Escala tipográfica | 11 (rótulo de grupo), 12 (legenda), 14 (base), 22 (título), 26 (KPI); 13, 15 e 16 em pontos isolados |
| Raio | 6 px (botão interno), 8 px (campos e botões), 12 px (cartões), 99 px (pílulas) |
| Sombra | `0 1px 2px rgba(21,27,38,.06)` no claro; nenhuma nos cartões no escuro; gaveta do celular: `0 8px 24px` |
| Espaçamento | 4, 8, 12, 16, 24, 32 px |

## Componentes e padrões essenciais

- Seletor de período (grupo segmentado) que atualiza todos os blocos juntos.
- Cartão de KPI: rótulo, valor, variação com seta e cor, minigráfico.
- Gráfico de linhas com período anterior tracejado, eixos legíveis, legenda e descrição acessível (`role="img"` + `aria-label`).
- Barras de distribuição com valor e porcentagem ao lado.
- Tabela com `th scope`, números tabulares à direita, status em pílula com texto e link no identificador.
- Busca global, botão de tema, exportação.
- **Vazio:** ícone, "Nenhum pedido neste período", explicação e ação (conectar canal ou ampliar período).
- **Carregando:** esqueletos com a forma de KPIs, gráfico e tabela, `aria-busy="true"`; sem spinner de tela cheia.
- **Erro:** faixa com `role="alert"`, causa em linguagem simples, "Tentar de novo" e os blocos que carregaram mantidos.

## Quando é bom

- Muitos números que o usuário compara no tempo.
- Uso diário, em tela grande, por quem já conhece os termos.
- Produto com várias áreas além do painel (a barra lateral escala bem).

## Quando é ruim

- Poucos dados: o painel fica vazio e desperdiça espaço.
- Usuário leigo ou só em celular: prefira uma lista de destaques.
- Erros comuns desta tela:
  - KPIs demais, sem prioridade.
  - Gráfico 3D, de pizza com muitas fatias ou com arco-íris de cores.
  - Eixo cortado que exagera a variação; sem unidade ou período.
  - Variação só em vermelho e verde, sem seta nem sinal.
  - Números sem `tabular-nums` ou alinhados à esquerda.
  - Tabela estourando a página no celular.
  - Sem estado vazio, de carregamento e de erro.
  - Tudo com sombra e borda forte; sem hierarquia entre cartões.

## Como começar

1. Abra [o exemplo](../examples/02-dashboard-analytics.html) no navegador e teste os dois temas, a gaveta no celular e as abas de estado.
2. Copie o bloco `:root` e troque `--brand` e os neutros pela marca (confira o contraste AA, WCAG 1.4.3).
3. Troque os dados e os rótulos pelos do seu produto; mantenha 4 KPIs e 2 gráficos como ponto de partida.
4. Monte com os componentes da skill `design`: Card, Table, Tabs, Sheet (gaveta), Skeleton, Badge e ícones Lucide. Para gráficos reais, use o componente Chart do shadcn ou outra biblioteca com as mesmas cores.
5. Regras gerais em [01-fundamentos.md](01-fundamentos.md).

## Combina com / alternativas

- [03-admin-crud.md](03-admin-crud.md): listas e formulários que o painel referencia.
- [09-financeiro.md](09-financeiro.md): variante focada em dinheiro e extratos.
- [07-crm-kanban.md](07-crm-kanban.md): quando o trabalho é mover itens, não só ler números.
- Alternativa: página única de relatório (sem barra lateral) para produto com uma só tela de dados.

## Decisão rápida

- **Use se:** o usuário volta todo dia para acompanhar números e comparar períodos, em tela grande.
- **Evite se:** há poucos dados, o público é leigo ou mobile, ou o trabalho principal é cadastrar e editar.
