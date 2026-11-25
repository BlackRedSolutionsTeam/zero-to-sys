# E-commerce (vitrine, produto e carrinho)

> Loja online clara e com cara de marca: vitrine com filtros, página de produto que convence e carrinho em painel lateral.

| | |
|---|---|
| **Tipo de sistema** | E-commerce de marca própria (loja virtual com catálogo pequeno ou médio) |
| **Exemplo** | [06-ecommerce.html](../examples/06-ecommerce.html), marca fictícia Barro & Brasa (ateliê de cerâmica), com abas Vitrine / Página de produto e carrinho em drawer |
| **Layout base** | Cabeçalho fixo; vitrine em duas colunas (filtros 240 px + grade); página de produto em duas colunas (galeria + compra); carrinho em painel lateral de 440 px |
| **Referências reais** | Aesop https://www.aesop.com (a Wikipedia lista aesop.com como site oficial da marca) · Allbirds https://www.allbirds.com (200) · Glossier https://glossier.com (200) · Fellow https://fellowproducts.com (200) · Blue Bottle Coffee https://bluebottlecoffee.com (a Wikipedia lista bluebottlecoffee.com como site oficial). Exemplos de produtos do segmento (sites conferidos em 2026-11-24; Aesop e Blue Bottle bloqueiam acesso automático, então a conferência foi pelas fontes citadas: en.wikipedia.org/wiki/Aesop_(brand) e en.wikipedia.org/wiki/Blue_Bottle_Coffee). |
| **Componentes** | shadcn/ui (sheet para o carrinho e os filtros no celular, select, checkbox, slider, tabs, toggle group para variações, dialog); HyperUI (marcação Tailwind CSS) para lojas sem React; Lucide para ícones; Magic UI com moderação. Fontes: ui.shadcn.com/docs/components (sheet, select, checkbox, slider, tabs, toggle group, dialog), hyperui.dev, lucide.dev, magicui.design, conferidas em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Uma loja online de marca vende poucos produtos bem apresentados, em vez de milhares de itens. O fluxo tem três telas que se repetem: a vitrine (lista com filtros), a página de produto (galeria, variações, preço, compra) e o carrinho.

O exemplo mostra a vitrine e a página de produto em abas e abre o carrinho como drawer, para a pessoa não perder o lugar onde estava. Como não há fotos, os produtos são ilustrados em SVG, com formas e cores sólidas.

## Por que este layout

- **Vitrine com filtros laterais:** no exemplo, os filtros ficam numa coluna de 240 px. No celular, viram uma folha inferior.
- **Cartão simples:** imagem, nome, detalhe, preço e botão de adicionar. O resto fica na página de produto.
- **Galeria + compra lado a lado:** a imagem fica à esquerda e as opções de compra à direita.
- **Carrinho em painel:** adicionar abre o painel; a pessoa continua comprando ou finaliza.
- **Visual quente e serifado:** é a identidade da marca fictícia (Fraunces nos títulos). Sem foto, os produtos são ilustrações em SVG.

## Quando usar

- Marca própria com catálogo de dezenas a poucas centenas de itens.
- Produtos em que aparência e história pesam (cerâmica, café, moda, cosmético).
- Loja nova que precisa parecer confiável rápido.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Loja de marca própria (artesanato, café, moda, beleza) | ✅ Ótimo | Casa com o visual e o fluxo do exemplo |
| Loja com variações (cor, tamanho) | ✅ Ótimo | A página de produto já trata variações e falta de estoque |
| Marketplace com milhares de itens | 🟡 Serve | Falta busca avançada, comparação e paginação pesada |
| Venda de assinatura ou software | ❌ Evite | Use landing de produto (ver 05) |
| Catálogo B2B com pedido por planilha | ❌ Evite | Precisa de tabela e pedido em lote (ver 03) |
| Painel de vendedor | ❌ Evite | É sistema interno (ver 02, 03) |

## Anatomia do layout

```
┌──────────────────────────────────────────────┐
│ Aviso de frete grátis                        │
│ Logo  Canecas Vasos...  [busca]  ☾ conta  🛍2│ cabeçalho 72 px
├────────────┬─────────────────────────────────┤
│ Filtros    │ 6 de 42 peças      [Ordenar ▾]  │
│ Categoria  │ ┌─────┐ ┌─────┐ ┌─────┐         │
│ Cor        │ │ img │ │ img │ │ img │         │ grade 3 colunas
│ Preço      │ │nome │ │nome │ │nome │         │
│ Estoque    │ │R$ + │ │R$ + │ │R$ + │         │
│            │ └─────┘ └─────┘ └─────┘         │
├────────────┴─────────────────────────────────┤
│ Página de produto:                           │
│ [mini] ┌─────────────┐  Nome, nota, R$       │
│ [mini] │ imagem 1:1  │  Cor ● ● ● ●          │
│ [mini] │             │  Tamanho [P][M][G]    │
│        └─────────────┘  [- 1 +] [Adicionar]  │
│                          frete · troca       │
└──────────────────────────────────────────────┘
                          ┌─ Carrinho ──────┐
                          │ itens, barra de │ drawer 440 px
                          │ frete, total    │
                          │ [Finalizar]     │
                          └─────────────────┘
```

- **Largura do conteúdo:** máximo 1240 px, margem de 24 px (16 px no celular).
- **Cabeçalho:** 72 px, fixo, com aviso acima (cerca de 38 px: texto de 14 px com linha de 1,55 e 8 px de padding em cima e embaixo). Busca de até 380 px.
- **Vitrine:** filtros de 240 px (fixos ao rolar) e grade de 3 colunas com 24 px de espaço horizontal e 32 px vertical. Imagem quadrada com raio de 20 px.
- **Página de produto:** colunas 1,1 : 1 com 56 px de espaço; miniaturas de 72 px (64 px no celular); imagem em proporção 1:1.
- **Carrinho:** 440 px de largura (tela cheia no celular), cabeçalho, lista com rolagem e rodapé fixo com total e botão.
- **Espaço entre blocos:** 32 a 48 px; fim da página com 80 px.
- **Tablet (até 1024 px):** grade em 2 colunas, categorias do cabeçalho viram menu.
- **Celular (até 820 px):** filtros viram folha inferior aberta por botão; busca sai do cabeçalho; produto em 1 coluna. Abaixo de 560 px, a grade mantém 2 colunas, as miniaturas ficam em fila abaixo da imagem e o botão de conta é ocultado.

## Tokens do exemplo

| Token | Claro (padrão) | Escuro |
|---|---|---|
| Fundo / superfície / superfície 2 | `#FAF3E7` / `#FFFBF4` / `#F2E7D5` | `#1D1410` / `#271B15` / `#33241C` |
| Texto / texto suave | `#3B2418` / `#74574A` | `#F6EBDD` / `#C2A896` |
| Borda | `#E3D3BA` | `#4A362B` |
| Marca terracota | `#B4532A` (hover `#9A431F`) com texto branco | `#D8744A` com texto `#1D1410` |
| Estoque ok / erro | `#4F6B3A` / `#A32A1B` | `#A5C48A` / `#F08A78` |
| Fonte de título | Fraunces 500/600 (Google Fonts), fallback Georgia | |
| Fonte de texto | Inter 400/500/600, fallback fonte do sistema | |
| Escala | 13 · 14 · 15 · 16 · 19 (nome do produto) · 24 · 30 (preço) · 34–56 (título) | |
| Raio | 8 · 12 · 20 px; botões em pílula | |
| Sombra | `0 12px 32px -12px` só no drawer e na folha de filtros | |
| Espaçamento | escala de 4/8 px: 8, 12, 16, 24, 32, 48, 56, 80 | |

## Componentes e padrões essenciais

- **Cabeçalho** com busca, conta, carrinho com contador e tema.
- **Filtros:** categoria, cor (amostras), faixa de preço, disponibilidade, com contagem por opção.
- **Barra de ferramentas:** quantidade mostrada e ordenação.
- **Cartão de produto:** imagem, selo (Novo, Mais vendido, Últimas unidades), nome, detalhe, preço, botão de adicionar rápido.
- **Página de produto:** galeria com miniaturas, nome, nota, preço e parcelas, estoque, cor, tamanho (com opção esgotada riscada), quantidade, botão de compra, cálculo de frete por CEP, troca e pagamento.
- **Carrinho em drawer:** itens com quantidade e remover, barra de progresso do frete grátis, subtotal, total, finalizar e continuar comprando. Fecha com Esc, clique fora e botão (o APG lista Esc como tecla que fecha o diálogo).
- **Estado vazio do carrinho** com ilustração e botão para voltar à loja (o exemplo mostra ao remover tudo).
- **Estados que a loja de verdade precisa:** vitrine carregando (esqueletos dos cartões), busca sem resultado com sugestão de limpar filtros, erro de CEP inválido, erro de estoque ("só restam 2") e botão de compra em carregamento. O exemplo mostra o vazio do carrinho e o tamanho esgotado; os demais ficam por sua conta.

## Quando é bom

- Preço, parcelas, estoque, variações e frete aparecem na própria página de produto.
- O drawer mantém a vitrine ou a página de produto visível atrás do painel.

## Quando é ruim

- **Custo extra só no checkout:** na pesquisa do Baymard, "custos extras altos (frete, imposto, taxas)" é o principal motivo de abandono do checkout, com 40% (baymard.com/lists/cart-abandonment-rate, 2026-11-24, sem contar quem só estava navegando). Mostre frete e prazo antes, como o exemplo faz.
- **Alvo de toque pequeno:** o WCAG 2.2 pede no mínimo 24 x 24 px CSS no nível AA (SC 2.5.8) e 44 x 44 px no nível AAA (SC 2.5.5) (w3.org/WAI/WCAG22/Understanding/target-size-minimum.html e target-size-enhanced.html, 2026-11-24). Os botões do exemplo têm 44 px ou mais.
- **Contraste baixo da cor da marca** em botões e preços: mínimo de 4,5:1 para texto normal (WCAG 2.2, SC 1.4.3). No exemplo, branco sobre `#B4532A` dá cerca de 5,0:1 e `#1D1410` sobre `#D8744A`, cerca de 5,6:1.

## Como começar

1. Abra [06-ecommerce.html](../examples/06-ecommerce.html) no navegador, troque entre as abas, adicione itens e abra o carrinho.
2. Copie os tokens do `:root` e do tema escuro; troque nome, terracota e fontes pela sua marca.
3. Substitua as ilustrações (`<symbol>` de SVG) por fotos reais ou mantenha o estilo ilustrado, com cores sólidas.
4. Monte com a skill design: shadcn/ui (sheet, select, checkbox, slider, tabs) e Lucide. Sem React, use HyperUI.
5. Conecte a plataforma de pagamento e de estoque; o JS do exemplo só simula o carrinho.
6. Teste de 360 a 1440 px e com teclado, incluindo o foco: o padrão de diálogo modal do WAI-ARIA APG manda o foco ir para dentro do painel ao abrir e voltar ao elemento que o abriu ao fechar (w3.org/WAI/ARIA/apg/patterns/dialog-modal/, 2026-11-24).

## Combina com / alternativas

- [05-landing-saas.md](05-landing-saas.md): para vender software em vez de produto físico.
- [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md): conta, login e endereços.
- [09-financeiro.md](09-financeiro.md): pedidos, pagamentos e conciliação no lado da loja.
- [01-fundamentos.md](01-fundamentos.md): tokens, grade e acessibilidade.

## Decisão rápida

- **Use se:** você vende produtos físicos de uma marca com identidade e catálogo moderado.
- **Evite se:** vende software por assinatura, ou o catálogo é enorme e comparativo (marketplace).
