# Pontos de quebra e layout responsivo

> O layout muda quando o conteúdo pede, não quando o aparelho muda: comece pelo celular e acrescente espaço conforme a janela cresce.

| | |
|---|---|
| **Tema** | Pontos de quebra (breakpoints), grade fluida, unidades de viewport e padrões de adaptação |
| **Vale para** | Web responsiva, PWA (igual à web), app nativo (classes de tamanho de janela do Android/Material) |
| **Referências oficiais** | Tailwind: https://tailwindcss.com/docs/responsive-design · Android (classes de tamanho de janela, alinhadas ao Material 3): https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes · MDN (unidades de comprimento): https://developer.mozilla.org/en-US/docs/Web/CSS/length · Material 3: https://m3.material.io/foundations/layout/applying-layout/window-size-classes |
| **Verificado em** | 2026-11-24 |

## O que é

Layout responsivo é a tela se reorganizar conforme o espaço disponível. Um ponto de quebra é a largura em que o layout muda. Em CSS, vira uma `@media (width >= 48rem)` ou uma container query.

A abordagem mobile-first escreve o CSS base para a tela pequena e usa `min-width` para acrescentar o que cabe em telas maiores. O Tailwind funciona assim: um prefixo como `md:` vale naquela largura e acima.

## Por que importa

- Dispositivos caem em faixas diferentes conforme a orientação (Material 3, Breakpoints); o desktop sozinho não representa o público.
- Aparelhos mudam de largura em tempo real: rotação, tela dividida, janela redimensionada, dobrável abrindo. A documentação do Android diz que a classe de tamanho de janela muda durante a vida do app e que a decisão não deve usar o tamanho físico da tela.
- O Material 3 manda projetar por breakpoint e não por aparelho, porque o espaço da janela é dinâmico (m3.material.io/foundations/layout/breakpoints/overview, 2026-11-24).

## Quando aplicar

- Em toda tela nova, antes de desenhar o desktop.
- Quando um componente vive em lugares de larguras diferentes (cartão em grade, em coluna lateral, em modal): use container query.
- Quando a tela tem altura crítica (login, hero, folha inferior): use as unidades de viewport certas.

## Celular, tablet e desktop

Faixas de referência. As do Tailwind são as padrão da v4 (confirmadas na documentação). As de Material/Android são as classes de tamanho de janela (confirmadas na página do Android, que diz mapear compact, medium e expanded do Material; large e extra-large foram acrescentadas para desktop). A página do Material 3 foi lida em 2026-11-24: o nome atual é "breakpoints" (antes "window size class"), com as mesmas cinco faixas — compact abaixo de 600 dp, medium 600 a 839, expanded 840 a 1199, large 1200 a 1599, extra-large 1600 ou mais — e recomenda 1 painel em compact e medium, 2 em expanded e large, até 3 em extra-large (https://m3.material.io/foundations/layout/breakpoints/overview).

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Classe Material/Android (dispositivos comuns, segundo a página Breakpoints) | Compacta: < 600 dp (celular em retrato) | Média: 600 a 839 dp (tablet e dobrável em retrato). Expandida: 840 a 1199 dp (celular em paisagem, tablet e dobrável em paisagem; a página lista também desktop) | Expandida: 840 a 1199 dp (desktop). Grande: 1200 a 1599 dp. Extragrande: ≥ 1600 dp (também monitor ultralargo) |
| Prefixo Tailwind | base, até `sm` (640 px) | `md` (768 px), `lg` (1024 px) | `lg` (1024 px), `xl` (1280 px), `2xl` (1536 px) |
| Colunas de conteúdo | 1 | 2 (ou lista + detalhe a partir de ~840 dp) | 2 a 3, com largura máxima |
| Navegação | Barra inferior | Trilho lateral | Barra lateral ou topo (ver [06](06-navegacao.md)) |
| Padrão de adaptação | Reempilhar e esconder o secundário | Revelar o painel de apoio | Redimensionar com teto e trocar componentes (tabela, menu) |
| Margens laterais | Pequenas e iguais nas duas laterais | Maiores que no celular | Centralizar com `max-width` |
| Altura | `dvh` ou `svh` por causa da barra do navegador | Orientação muda o layout | Altura raramente limita |

## Para que tipo de projeto

| Tipo de projeto | Prioridade | Por quê |
|---|---|---|
| Landing page | Alta | Hero, seções e CTA precisam de `svh`/`dvh` e reempilhamento |
| E-commerce | Alta | Grade de produtos muda de 2 para 4+ colunas; filtros viram folha no celular |
| SaaS | Alta | Mesmo produto em três larguras; navegação e tabelas mudam de forma |
| Dashboard | Alta | Cartões e gráficos em grade fluida; container queries nos widgets |
| Sistema interno | Média | Costuma ser desktop, mas tablets e celulares aparecem; cubra ao menos a largura média |
| App de campo | Alta | Celular em pé, uma mão, sol; desktop quase não importa |
| Blog/conteúdo | Média | Uma coluna com largura de leitura resolve quase tudo |

## Regras práticas

- Escreva o CSS base sem media query e use só `min-width` (Tailwind: `md:`, `lg:`). Fonte: documentação do Tailwind (mobile-first).
- Escolha o ponto de quebra onde o layout começa a ficar ruim (linha longa, coluna apertada), não em 375 ou 768 por serem tamanhos de aparelho. Fonte: princípio da documentação do Android de não decidir por hardware.
- Valores de partida: 640, 768, 1024, 1280, 1536 px (Tailwind) ou 600, 840, 1200, 1600 dp (Android/Material). São padrões prontos, não leis; ajuste.
- O Material 3 recomenda ajustar margens e tipografia para manter 40 a 60 caracteres por linha em todos os breakpoints (conferido). Limite o texto corrido com `max-width` em `ch`.
- Use `dvh` quando a altura precisa acompanhar a barra do navegador, `svh` quando o conteúdo nunca pode ser coberto e `lvh` para preencher com a barra recolhida. A MDN avisa que `dvh` não é estável e pode prejudicar desempenho se redimensionar durante a rolagem.
- Para componentes, prefira container query à media query: o componente sabe o espaço que ele tem, não o da janela.
- Considere também a altura em celular deitado: a classe de altura compacta é < 480 dp, onde dois painéis não funcionam bem.
- Inclua `<meta name="viewport" content="width=device-width, initial-scale=1">` e não bloqueie o zoom: a MDN diz que `user-scalable=no` impede pessoas com baixa visão de ler o conteúdo (developer.mozilla.org, meta viewport, 2026-11-24).

## Erros comuns

- **Quebrar em 375, 768 e 1440 px "porque são os aparelhos".** Corrija: escolha pelo conteúdo e teste arrastando a janela, não só os tamanhos prontos.
- **Desktop encolhido no celular:** mesma tela, só menor. Corrija trocando o componente (tabela vira cartões, menu lateral vira barra inferior).
- **`height: 100vh` no celular:** o conteúdo some atrás da barra do navegador. Corrija com `100dvh` (e `100vh` como reserva).
- **Texto esticado em monitor largo.** Corrija com `max-width` e centralização.
- **Tela só testada em pé.** Teste deitado e em janela dividida.
- **Rolagem horizontal da página** por imagem ou tabela sem `max-width: 100%` / `overflow-x: auto`.

## Como aplicar

```css
/* Mobile-first: base sem media query, depois min-width */
.page { display: grid; gap: 1rem; padding: 1rem; }
@media (width >= 48rem) { .page { grid-template-columns: 1fr 2fr; padding: 1.5rem; } }
@media (width >= 80rem) { .page { max-width: 80rem; margin-inline: auto; } }

/* Grade fluida sem breakpoint */
.cards { display: grid; gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(min(16rem, 100%), 1fr)); }

/* Tipografia fluida com limites */
h1 { font-size: clamp(1.5rem, 1rem + 2vw, 2.5rem); }

/* Altura com barra do navegador */
.hero { min-height: 100vh; min-height: 100dvh; }

/* Container query: o cartão decide pelo espaço dele */
.card-wrap { container-type: inline-size; }
@container (min-width: 28rem) { .card { display: flex; gap: 1rem; } }
```

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Tailwind: reempilhar no celular, lado a lado de md em diante -->
<div class="flex flex-col md:flex-row gap-4">
  <aside class="md:w-64">...</aside>
  <main class="flex-1 max-w-3xl">...</main>
</div>
<!-- Tailwind container query -->
<div class="@container"><div class="flex flex-col @md:flex-row">...</div></div>
```

Quatro padrões de adaptação: **reempilhar** (colunas viram pilha), **revelar** (mostrar painel ou coluna extra com espaço), **redimensionar** (largura e espaçamento fluidos com teto) e **trocar componente** (tabela por cartões, barra inferior por barra lateral).

## Combina com / alternativas

- [01-contexto-de-uso](01-contexto-de-uso.md), [02-mobile](02-mobile.md), [03-tablet](03-tablet.md), [04-desktop](04-desktop.md)
- [06-navegacao](06-navegacao.md), [09-tabelas-e-dados](09-tabelas-e-dados.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [11-tipografia-e-densidade](11-tipografia-e-densidade.md), [12-desempenho-e-rede](12-desempenho-e-rede.md), [13-ios-android-web](13-ios-android-web.md)
- Skills vizinhas: **design-systems** (layouts prontos por tipo de sistema) e **design** (UI kits e ícones).

## Decisão rápida

- **Faça:** CSS base para celular; `min-width`; quebra pelo conteúdo; container query em componentes; `dvh` em telas cheias; `max-width` no texto.
- **Evite:** quebra por modelo de aparelho; `100vh` em tela cheia no celular; desktop apenas encolhido; bloquear zoom.
