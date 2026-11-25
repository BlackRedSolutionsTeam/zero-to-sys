# Navegação por dispositivo

> A estrutura de navegação é a mesma nos três aparelhos; muda a forma: barra inferior no celular, trilho no tablet, barra lateral ou topo no desktop.

| | |
|---|---|
| **Tema** | Navegação principal, secundária, voltar, busca e navegação profunda |
| **Vale para** | Web responsiva, PWA, app nativo (iOS e Android) |
| **Referências oficiais** | Apple HIG, tab bars: https://developer.apple.com/design/human-interface-guidelines/tab-bars · Material 3, navigation bar: https://m3.material.io/components/navigation-bar/guidelines · Material 3, navigation rail: https://m3.material.io/components/navigation-rail/overview · Nielsen Norman Group, menus escondidos: https://www.nngroup.com/articles/hamburger-menus/ · Android, classes de tamanho: https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes |
| **Verificado em** | 2026-11-24 |

## O que é

Navegação é o conjunto de caminhos entre as telas. Tem três camadas: a **principal** (as áreas do sistema), a **secundária** (abas, filtros, subseções dentro de uma área) e a **profunda** (lista, detalhe, edição). A Apple chama a principal de tab bar no iPhone; o Material chama de navigation bar (celular), navigation rail (tablet) e drawer ou sidebar (telas grandes).

Observação sobre as fontes: a página de tab bars da Apple foi lida em 2026-11-24 no navegador. As páginas de navigation bar e breakpoints do Material 3 também foram lidas no navegador na mesma data.

## Por que importa

- É o que decide se o usuário acha as funções. NN/g (estudo de 2016, 179 participantes) mediu uso de menus escondidos em 27 % dos casos no desktop, contra 48 % da navegação visível, e desaconselha navegação escondida no desktop (nngroup.com/articles/hamburger-menus, 2026-11-24).
- O Material 3 posiciona a barra de navegação na base da janela "for convenient access" e manda usar trilho, não barra, em desktop (m3.material.io/components/navigation-bar/guidelines, 2026-11-24).
- Trocar de aparelho sem a estrutura mudar de forma faz o usuário reaprender o sistema.

## Quando aplicar

- Ao definir o mapa do sistema (antes das telas).
- Ao adaptar para tablet: é o ponto em que mais sistemas ficam "meio celular, meio desktop".
- Ao ver uma área com mais de 5 destinos no celular: decida o que vai para "Mais".

## Celular, tablet e desktop

| Aspecto | Celular (< 600 dp) | Tablet (600 a < 1200 dp) | Desktop (≥ 1200 dp, mouse) |
|---|---|---|---|
| Navegação principal | Barra de abas inferior, 3 a 5 itens | Trilho de navegação (rail) à esquerda; barra lateral expandida em paisagem larga | Barra lateral fixa (trilho expandido no Material 3) ou barra no topo |
| Rótulos | Ícone + texto sempre | Ícone + texto no trilho; texto opcional | Texto sempre; ícone opcional |
| Mais de 5 destinos | Item "Mais" ou lista na última aba | Trilho comporta mais; agrupe | Agrupe em seções recolhíveis |
| Navegação secundária | Abas no topo da tela ou seletor segmentado | Abas ou painel à esquerda da lista | Abas, subitens na lateral, migalhas |
| Voltar | Gesto de borda ou botão do sistema + seta na barra superior | Seta + painel de detalhe lado a lado | Botão voltar do navegador, migalhas, link "Voltar à lista" |
| Busca | Ícone que abre campo em tela cheia, ou aba de busca | Campo no topo da coluna | Campo sempre visível |
| Navegação profunda | Uma tela por nível, pilha | Lista + detalhe (dois painéis) | Lista + detalhe + migalhas; abas do navegador |
| Menu escondido | NN/g: no celular, links visíveis se houver até 4 itens de topo; esconda só o excedente | Idem | NN/g desaconselha navegação escondida no desktop |

## Para que tipo de projeto

| Tipo de projeto | Padrão recomendado | Por quê |
|---|---|---|
| Landing page | 🟡 Topo simples + âncoras; hambúrguer aceitável | Poucos links; o CTA importa mais |
| E-commerce | ✅ Barra inferior no app; categorias em menu largo no desktop | Busca e carrinho precisam estar sempre à mão |
| SaaS | ✅ Barra lateral no desktop, barra inferior no celular | Muitas áreas; mesma estrutura em formas diferentes |
| Dashboard | ✅ Barra lateral recolhível | Ganha largura para os dados |
| Sistema interno | ✅ Barra lateral agrupada | Dezenas de telas; usuário aprende os caminhos |
| App de campo | ✅ Barra inferior com 3 a 4 itens grandes | Uma mão, pressa |
| Blog/conteúdo | 🟡 Topo + busca | Navegação é por busca e links |
| Hambúrguer para tudo | ❌ Evite | Esconde as áreas principais |

## Regras práticas

- Barra inferior: 3 a 5 destinos, sempre com rótulo de 1 a 2 palavras; com menos de 3, use abas; com mais de 5, use trilho de navegação modal ou abas. Não é para desktop: de expanded para cima, troque por trilho (Material 3, Navigation bar, conferido). A Apple não fixa um número: pede poucas abas, rótulo de uma palavra, e avisa que, sem espaço, a última aba vira "Mais" e esconde as outras, o que deve ser evitado. No iPadOS, quando o usuário escolhe as abas, a recomendação é cinco ou menos (HIG, Tab bars, conferido).
- No iPhone a barra de abas fica embaixo; no iPad ela fica no topo e pode virar barra lateral (HIG, Tab bars). Não esconda nem desative abas sem conteúdo: explique por que a seção está vazia.
- Alvo de cada aba com pelo menos 44 pt (Apple) ou 48 dp (Material); ver [07](07-toque-mouse-teclado.md).
- Mostre sempre o rótulo em texto; ícone sozinho é ambíguo (NN/g, Icon Usability: os rótulos dos ícones devem estar sempre visíveis, sem interação; nngroup.com/articles/icon-usability, 2026-11-24; Material 3: todo item exige rótulo de 1 a 2 palavras).
- O item ativo precisa de mais que cor: forma, peso ou indicador (Apple HIG, Accessibility: "Convey information with more than color alone"; Material 3 usa indicador ativo e ícone preenchido).
- Mantenha a mesma ordem e os mesmos nomes dos itens; o WCAG 3.2.3 (AA, Navegação consistente) pede a mesma ordem relativa dos mecanismos repetidos nas páginas do conjunto (w3.org/TR/WCAG22).
- No navegador, o botão Voltar deve voltar uma tela do app: use `history.pushState` (MDN, History.pushState) para uma entrada por tela real, sem prender o usuário.
- Em tela larga, o trilho passa a barra lateral a partir da classe expandida (840 dp, Material); o ponto exato é decisão do produto.

## Erros comuns

- **Hambúrguer com as áreas principais.** Corrija: barra inferior no celular, lateral no desktop.
- **Barra inferior com 7 itens ou só ícones.** Corrija: máximo de 5 com texto; o resto em "Mais".
- **Desktop com barra inferior** estendida na largura toda. Corrija: barra lateral.
- **Tablet com a navegação do celular esticada.** Corrija: trilho ou lateral, e lista + detalhe.
- **Voltar do navegador que sai do sistema** em SPA sem rotas. Corrija: uma URL por tela.
- **Busca escondida** em sistema com muito conteúdo. Corrija: campo visível no desktop, ícone claro no celular.
- **Navegação que muda de lugar** entre telas. Corrija: posição fixa.

## Como aplicar

```html
<!-- Uma só estrutura, três formas -->
<nav aria-label="Principal" class="app-nav">
  <a href="/inicio" aria-current="page">Início</a>
  <a href="/pedidos">Pedidos</a>
  <a href="/clientes">Clientes</a>
  <a href="/mais">Mais</a>
</nav>
```

```css
.app-nav { position: fixed; inset: auto 0 0 0; display: flex; justify-content: space-around;
  padding-bottom: env(safe-area-inset-bottom); }           /* celular: barra inferior */
.app-nav a { min-height: 48px; min-width: 48px; display: grid; place-items: center; }

@media (width >= 37.5rem) {                                 /* 600 px: trilho */
  .app-nav { inset: 0 auto 0 0; flex-direction: column; justify-content: flex-start; width: 5rem; }
}
@media (width >= 75rem) {                                   /* 1200 px: lateral completa */
  .app-nav { width: 16rem; align-items: stretch; }
}
```

```tsx
// Tailwind: mesma ideia
<nav className="fixed inset-x-0 bottom-0 flex justify-around md:inset-y-0 md:left-0 md:right-auto md:w-20 md:flex-col xl:w-64">
```

## Combina com / alternativas

- [02-mobile](02-mobile.md), [03-tablet](03-tablet.md), [04-desktop](04-desktop.md), [05-breakpoints-e-layout](05-breakpoints-e-layout.md), [07-toque-mouse-teclado](07-toque-mouse-teclado.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [13-ios-android-web](13-ios-android-web.md)
- Skills vizinhas: **design-systems** (layouts prontos por tipo de sistema) e **design** (UI kits e ícones).

## Decisão rápida

- **Faça:** barra inferior (3 a 5 itens com texto) no celular; trilho no tablet; lateral no desktop; mesma ordem nos três; voltar sempre funcional; busca fácil.
- **Evite:** hambúrguer para áreas principais; mais de 5 abas (a última vira "Mais" e esconde as outras); ícone sem rótulo; trocar a posição da navegação entre telas.
