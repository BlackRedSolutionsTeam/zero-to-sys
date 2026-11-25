# Tabelas e dados densos

> Uma tabela de 8 colunas cabe no desktop, não no celular. Em tela pequena, troque a forma dos dados em vez de encolher a tabela.

| | |
|---|---|
| **Tema** | Tabelas, listas de dados, filtros, paginação e gráficos por dispositivo |
| **Vale para** | Web responsiva, PWA, app nativo (listas em vez de tabelas) |
| **Referências oficiais** | NN/g, tabelas de dados: https://www.nngroup.com/articles/data-tables/ · NN/g, filtros: https://www.nngroup.com/articles/filter-categories-values/ · NN/g, rolagem infinita x paginação: https://www.nngroup.com/articles/infinite-scrolling-tips/ · web.dev, layouts responsivos: https://web.dev/learn/design · WCAG 2.2, reflow 1.4.10: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html |
| **Verificado em** | 2026-11-24 |

## O que é

É como apresentar muitos registros com várias colunas: pedidos, clientes, estoque, métricas. No desktop a tabela mostra tudo e permite comparar. No celular a largura estreita (o WCAG 1.4.10 parte de 320 CSS px) não comporta isso, então se usa lista de cartões, colunas prioritárias, rolagem horizontal ou linha expansível.

## Por que importa

- Tabela encolhida vira texto ilegível; tabela que rola de lado sem pista esconde colunas.
- Dados são a razão de ser de dashboards e sistemas internos; se o usuário não os lê, o sistema falha.
- O WCAG 2.2 (1.4.10, reflow) pede conteúdo utilizável em 320 px de largura sem rolagem em duas direções; tabelas de dados e grades são exceção prevista, mas cada célula ainda precisa caber (WCAG, Understanding 1.4.10, w3.org/WAI/WCAG22/Understanding/reflow.html, 2026-11-24).

## Quando aplicar

- Sempre que uma lista tiver mais de 3 ou 4 colunas ou ações por linha.
- Ao desenhar filtros, busca e ordenação.
- Ao escolher entre paginação e rolagem infinita.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Forma dos dados | Lista de cartões ou linhas de 2 a 3 informações | Tabela com colunas prioritárias, ou lista + detalhe | Tabela completa |
| Colunas | 2 a 3 prioritárias; o resto na linha expandida ou no detalhe | 4 a 6; esconder as secundárias | Todas; escolha de colunas visíveis |
| Rolagem horizontal | Só se comparar for essencial; primeira coluna fixa e indício visual de corte | Menos necessária | Quando a tabela é larga: coluna de identificação e de ações fixas |
| Ordenação | Seletor "Ordenar por" | Cabeçalho clicável ou seletor | Clique no cabeçalho, seta indicando sentido |
| Seleção em lote | Modo seleção (segurar ou botão "Selecionar") + barra de ações | Caixas de seleção | Caixa por linha + "selecionar tudo" + barra de ações |
| Ações por linha | Toque na linha abre o detalhe; menu "..." | Menu "..." ou ícones | Ícones ao pairar e no foco; menu "..."; clique na linha |
| Filtros | Posição sem norma oficial; ver NN/g, filtros | Idem | Idem |
| Paginação | Rolagem infinita com "carregar mais" ou paginação curta | Idem | Paginação numerada, com total e tamanho da página |
| Densidade | Confortável (linhas altas, alvo de toque de 44 pt a 48 dp) | Padrão | Compacta (sem número oficial para a altura de linha) |
| Gráficos | Um por vez, simplificado, rótulos diretos | 2 colunas | Painel de vários gráficos |

## Para que tipo de projeto

| Tipo de projeto | Solução | Por quê |
|---|---|---|
| Landing page | Baixa | Quase não há dados densos; tabela de preços vira cartões |
| E-commerce | Média | Pedidos e comparação de produtos: cartões no celular, tabela no desktop |
| SaaS | Alta | Listas de registros com filtros em todo produto |
| Dashboard | Alta | Tabelas e gráficos são o núcleo; priorize as colunas |
| Sistema interno | Alta | Tabela densa, lote e teclado no desktop; versão simples no celular |
| App de campo | Média | Lista de cartões grandes com status; tabela rara |
| Blog/conteúdo | Baixa | Tabelas pontuais: rolagem horizontal dentro do bloco |

## Regras práticas

- Escolha a saída pelo uso: **cartões** para ler e agir sobre um item; **colunas prioritárias** quando 2 a 3 campos bastam; **rolagem horizontal com primeira coluna fixa** para comparar valores; **linha expansível** para detalhe sem trocar de tela.
- Texto alinhado à esquerda, números à direita com fonte de algarismos tabulares (`font-variant-numeric: tabular-nums`).
- Cabeçalho fixo (`position: sticky`) ao rolar; linhas com alvo de toque de 44 pt (Apple HIG, Accessibility) a 48 dp (Android, support.google.com/accessibility/android/answer/7101858) no celular (ver [07](07-toque-mouse-teclado.md)).
- Em tabela, mantenha `<table>`, `<th scope>` e `<caption>` semânticos; ao virar cartões, use lista e mantenha o nome do campo junto do valor (NN/g e WCAG 1.3.1).
- Filtros: não há norma oficial sobre onde colocá-los por aparelho; veja a organização de categorias e valores em NN/g, nngroup.com/articles/filter-categories-values.
- Paginação x rolagem infinita (NN/g, nngroup.com/articles/infinite-scrolling-tips, 2026-11-24): a paginação dá pontos de referência para achar um item de novo; a rolagem infinita serve a navegação sem tarefa definida, pode impedir o acesso ao rodapé e perde a posição se não a guardar. Para tarefas de busca e comparação, o NN/g desaconselha a rolagem infinita. Para sistema de trabalho, prefira paginação ou "carregar mais".
- Gráfico no celular: um tipo simples, poucos rótulos, legenda direta, toque mostra o valor; mantenha uma tabela ou resumo em texto como alternativa acessível. Veja a skill `dataviz`, se disponível.
- Estado vazio, carregando (esqueleto) e erro desenhados em cada forma.

## Erros comuns

- **Tabela do desktop espremida no celular.** Corrija: cartões ou colunas prioritárias.
- **Rolagem horizontal sem pista** de que há mais colunas. Corrija: cortar a última coluna pela metade, sombra na borda.
- **Ação só no hover** na linha. Corrija: menu "..." sempre visível no toque.
- **Rolagem infinita sem fim alcançável** (rodapé, totais). Corrija: paginação ou botão "carregar mais".
- **Todas as colunas importantes.** Corrija: ouvir o usuário e definir 2 a 3 campos primários.
- **Gráfico cortado ou ilegível** em 360 px. Corrija: redesenhar, não reduzir.

## Como aplicar

```css
/* Cartões no celular, tabela de md em diante */
.dados { display: grid; gap: .75rem; }
.dados thead { display: none; }
.dados tr { display: grid; gap: .25rem; padding: .75rem; border: 1px solid var(--borda); border-radius: .5rem; }
.dados td::before { content: attr(data-label) ": "; font-weight: 600; }

@media (width >= 48rem) {
  .dados { display: table; }
  .dados thead { display: table-header-group; }
  .dados tr { display: table-row; border: 0; padding: 0; }
  .dados td::before { content: none; }
  .dados th, .dados td { padding: .5rem .75rem; text-align: left; }
  .dados td.num { text-align: right; font-variant-numeric: tabular-nums; }
}

/* Rolagem horizontal com primeira coluna fixa */
.scroll { overflow-x: auto; }
.scroll th:first-child, .scroll td:first-child { position: sticky; left: 0; background: var(--bg); }
```

```html
<td data-label="Cliente">Maria Souza</td>
<td data-label="Total" class="num">R$ 1.250,00</td>
```

## Combina com / alternativas

- [02-mobile](02-mobile.md), [03-tablet](03-tablet.md), [04-desktop](04-desktop.md), [05-breakpoints-e-layout](05-breakpoints-e-layout.md), [07-toque-mouse-teclado](07-toque-mouse-teclado.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [11-tipografia-e-densidade](11-tipografia-e-densidade.md), [12-desempenho-e-rede](12-desempenho-e-rede.md)
- Skills vizinhas: **design-systems** (layouts prontos por tipo de sistema) e **design** (UI kits e ícones).

## Decisão rápida

- **Faça:** tabela no desktop, cartões ou 2 a 3 colunas no celular, menu "..." por linha, paginação em sistema de trabalho, total de resultados visível.
- **Evite:** tabela encolhida, ação só no hover, rolagem horizontal sem pista, rolagem infinita para trabalho, gráfico sem alternativa em texto.
