# Contexto de uso

> O que muda de verdade entre celular, tablet e desktop: não é só a largura da tela, é como a pessoa segura, olha, toca e quanto tempo fica.

| | |
|---|---|
| **Tema** | Contexto de uso por dispositivo (postura, entrada, atenção, ambiente, rede, tela) |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | Android: janelas e classes de tamanho (https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes); Apple HIG, Layout (https://developer.apple.com/design/human-interface-guidelines/layout); WCAG 2.2, 2.5.8 e 1.4.10 (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html); MDN, `hover` e `pointer` (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover) |
| **Verificado em** | 2026-11-24 |

## O que é

Contexto de uso é o conjunto de condições em que a pessoa usa o sistema: como segura o aparelho, a que distância fica da tela, o que usa para apontar (dedo, mouse, teclado, caneta), onde está, quanto tempo tem e quanta atenção dá.

Celular, tablet e desktop mudam todas essas condições ao mesmo tempo. Por isso "projetar para três tamanhos" é só uma parte do trabalho. O resto é decidir **o que cada tela faz** em cada situação.

Também é importante lembrar que **dispositivo é mais que largura de tela**. Existem notebooks com tela de toque, tablets com teclado e trackpad, celulares dobráveis que viram tablet, janelas de desktop redimensionadas até ficarem do tamanho de um celular. A documentação do Android diz isso de forma direta: as classes de tamanho "não são para lógica do tipo `isTablet`"; valem para a janela disponível, não para o aparelho.

## Por que importa

- Uma tela copiada do desktop para o celular obriga a pessoa a dar zoom e acertar alvos pequenos com o dedo.
- Uma tela de celular esticada no desktop deixa linhas de texto longas demais e botões gigantes, com metade da tela vazia.
- Quem usa o sistema na rua, de pé, com uma mão, precisa de outra tela que quem usa à mesa por 8 horas.
- Erro de contexto vira abandono (carrinho, cadastro) ou retrabalho (digitação lenta, erro de toque).

## Quando aplicar

- No começo do projeto, antes de desenhar telas: descreva quem usa, onde e em que aparelho.
- Ao decidir quais telas existem em cada dispositivo (nem toda tela precisa existir nos três).
- Ao revisar um sistema que "funciona, mas cansa" em algum aparelho.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop | O que isso implica no design |
|---|---|---|---|---|
| Como segura | Uma mão (polegar) ou duas; em pé ou andando | Duas mãos, no colo, apoiado, ou em suporte | Parado, mãos no teclado e mouse | Celular: ações no alcance do polegar. Desktop: ações perto do cursor e atalhos |
| Distância da tela | Perto | Média | Maior | No iPhone, a distância de uso "tende a ser no máximo de um pé ou dois", ou seja, cerca de 30 a 60 cm (Apple HIG, Designing for iOS, conferido em 2026-11-24; a conversão para cm é nossa). Texto e alvos precisam ser legíveis nessa distância |
| Entrada | Toque (dedo é impreciso, cobre o alvo) | Toque; às vezes teclado, trackpad, caneta | Mouse e teclado; às vezes toque | Alvos maiores no toque; hover e atalhos só onde há ponteiro fino |
| Sessão | Curta, interrompida, uma tarefa | Média a longa, leitura e consulta | Longa, várias tarefas, várias abas | Celular: fluxo curto e que salva rascunho. Desktop: densidade e multitarefa |
| Foco | Atenção dividida | Atenção boa, postura relaxada | Atenção alta, trabalho | Celular: menos por tela. Desktop: mais informação visível ao mesmo tempo |
| Ambiente | Rua, transporte, fila, sol | Sofá, loja, campo, consultório | Escritório, casa | Rua: contraste alto e tolerância a erro. Escritório: pode ser denso |
| Rede e bateria | Oscilante; bateria limitada | Wi-Fi na maior parte; bateria média | Estável; sem limite de bateria (em geral) | Celular: poupar dados, mostrar estado offline. Veja [12-desempenho-e-rede.md](12-desempenho-e-rede.md) |
| Tela | Estreita, alta; retrato como padrão | Média; retrato e paisagem; janela pode encolher | Larga, paisagem; janela redimensionável | Android: compacta < 600 dp, média 600 a 839 dp, expandida 840 a 1199 dp, grande 1200 a 1599 dp, extragrande 1600 dp ou mais |
| Teclado | Virtual, ocupa parte da tela | Virtual ou físico | Físico | Formulários no celular precisam rolar e não ficar atrás do teclado |
| Mistura | Dobrável vira tablet | Tablet com teclado vira notebook | Notebook com toque | Decida por recursos (toque, hover, largura da janela), não pelo nome do aparelho |

## Para que tipo de projeto

| Tipo de sistema | Prioridade de pensar o contexto | Por quê |
|---|---|---|
| Landing page / site de marketing | Alta | No mundo, celular tem 59,9% do tráfego, desktop 38,51% e tablet 1,59%; no Brasil, desktop 64,72%, celular 34,67% e tablet 0,61% (StatCounter Global Stats, outubro de 2026, gs.statcounter.com/platform-market-share/desktop-mobile-tablet, conferido em 2026-11-24). Confira o tráfego do seu site; a primeira dobra decide |
| E-commerce | Alta | Navega no celular e compra em qualquer um; checkout curto em tela pequena |
| SaaS / app web | Alta | Uso diário no desktop, consulta e aprovação no celular |
| Dashboard / painel | Média | Desktop é o principal; celular pede resumo, não o painel inteiro |
| Sistema interno / ERP | Média | Desktop para trabalho pesado; celular para aprovar e consultar |
| App de campo (vistoria, entrega) | Alta | Rua, sol, uma mão, rede ruim, luvas: o contexto manda em tudo |
| Ponto de venda / saúde / leitura | Alta | Tablet em suporte ou na mão; toque com tela grande |
| Blog / conteúdo | Média | Leitura em qualquer tela; foco em tipografia e largura da linha |

## Regras práticas

- Decida layout pela **largura da janela**, não pelo nome do aparelho. Fonte: documentação de classes de tamanho do Android.
- Planeje pelo menos três faixas: compacta (< 600), média (600 a 839) e expandida (840 ou mais) em dp. Fonte: Android / Material 3.
- Faça o conteúdo caber em 320 px de largura sem rolar para os lados. Fonte: WCAG 2.2, 1.4.10 Reflow, nível AA.
- Alvo de toque: 44 x 44 pt padrão e 28 x 28 pt mínimo no iOS (Apple HIG, Accessibility, conferido em 2026-11-24), 48 x 48 dp (Material 3, Accessibility designing, conferido em 2026-11-24) e mínimo de 24 x 24 px CSS (WCAG 2.2, 2.5.8, AA). As fontes divergem: use 44 a 48 como alvo e 24 px como piso absoluto.
- Detecte capacidades, não aparelhos: `hover`, `pointer`, `any-pointer` (MDN). `hover: none` inclui aparelhos que simulam hover com um toque longo incômodo (MDN, `hover`, 2026-11-24).
- Considere a altura também: celular em paisagem tem altura compacta (< 480 dp), onde duas colunas não cabem. Fonte: Android.
- Teste na janela redimensionada, em tela dividida e com zoom de 400 % (equivale a 320 px em 1280 px). Fonte: WCAG 1.4.10.

## Erros comuns

- **Pensar em "mobile / desktop" só.** O tablet some e a tela fica esticada ou espremida. Corrija: liste os três e a faixa média.
- **`isMobile` por user agent.** Quebra com iPad, notebook com toque e janela estreita. Corrija: media queries por largura e por capacidade.
- **Esconder funções no celular "por falta de espaço".** Corrija: reorganize em etapas, em vez de remover a função que a pessoa precisa em campo.
- **Hover como único jeito de ver algo** (tooltip, menu). No toque não existe. Corrija: mostre também por toque ou texto visível.
- **Testar só no redimensionar do navegador.** Corrija: teste em aparelho real, com teclado virtual e sol.
- **Supor rede boa.** Corrija: estados de carregamento, erro e offline.

## Como aplicar

Escreva uma ficha por tela antes de desenhar:

```md
Tela: Aprovar pedido
- Quem / onde: gerente, no celular, em pé, 30 segundos
- Celular: lista de pendentes + botão Aprovar (1 toque) + motivo opcional
- Tablet: lista à esquerda, detalhe à direita
- Desktop: tabela com seleção em lote e atalho A para aprovar
```

Detecte capacidades em CSS, não aparelhos:

```css
/* Toque: alvos maiores */
@media (pointer: coarse) { .btn { min-height: 48px; } }
/* Mouse: pode ser mais denso e ter hover */
@media (hover: hover) and (pointer: fine) { .btn { min-height: 32px; } .btn:hover { background: var(--hover); } }
```

## Combina com / alternativas

- [02-mobile.md](02-mobile.md), [03-tablet.md](03-tablet.md), [04-desktop.md](04-desktop.md): cada dispositivo em detalhe.
- [05-breakpoints-e-layout.md](05-breakpoints-e-layout.md): como traduzir isto em pontos de quebra.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): entrada em detalhe.
- [12-desempenho-e-rede.md](12-desempenho-e-rede.md): rede e bateria.
- [13-ios-android-web.md](13-ios-android-web.md): diferenças entre plataformas.
- Skills vizinhas: `design-systems` (layouts prontos por tipo de sistema) e `design` (UI kits e ícones).

## Decisão rápida

- **Faça:** descreva quem usa, onde e com que entrada; decida por largura da janela e capacidades; trate o tablet como dispositivo de verdade; teste em aparelho real.
- **Evite:** `isMobile` por user agent, tela única esticada, hover como única via, supor rede boa.
