# Landing page de produto (SaaS)

> Página única que explica um produto em seções empilhadas e leva a pessoa a um só gesto: criar a conta.

| | |
|---|---|
| **Tipo de sistema** | Landing page de produto SaaS (site de marketing de uma página) |
| **Exemplo** | [05-landing-saas.html](../examples/05-landing-saas.html), marca fictícia Pauta, ferramenta para times de produto |
| **Layout base** | Seções empilhadas em coluna central (conteúdo até 1160 px), cabeçalho fixo, hero centralizado |
| **Referências reais** | Linear https://linear.app · Vercel https://vercel.com · Stripe https://stripe.com · Framer https://framer.com · Raycast https://raycast.com (exemplos de produtos do segmento; sites conferidos em 2026-11-24, os cinco URLs responderam 200) |
| **Componentes** | Magic UI (efeitos e bento grid) e Aceternity UI (um ou dois destaques no hero) sobre shadcn/ui (botão, accordion para FAQ, toggle de preço, sheet para o menu móvel); HyperUI (marcação Tailwind CSS) se não houver React; Lucide para ícones. Fontes: ui.shadcn.com/docs/components (accordion, button, sheet, toggle), magicui.design/docs/components/bento-grid, ui.aceternity.com (seções hero), hyperui.dev, lucide.dev, conferidas em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Uma landing page de produto é a vitrine de um software. Ela mostra o que o produto faz, prova que outras pessoas usam e leva a um único chamado para ação, como "Começar grátis". Não é o app em si nem o site institucional da empresa.

O exemplo segue a ordem clássica: navegação, hero com prévia do produto, prova social, grade de recursos, como funciona, depoimentos, preços, perguntas frequentes, chamada final e rodapé.

## Por que este layout

- **Uma coluna:** o exemplo empilha as seções na ordem navegação, hero, prova social, recursos, passos, depoimentos, preços, perguntas e chamada final.
- **Prévia desenhada em HTML:** no exemplo, a prévia do produto é HTML/CSS, sem imagem externa, e muda de tema junto com a página.
- **Bento nos recursos:** o Magic UI define o bento grid como "um layout para mostrar os recursos de um produto de forma simples e elegante" (magicui.design/docs/components/bento-grid, 2026-11-24). No exemplo, o recurso principal ocupa 4 das 6 colunas.
- **Mesma ação repetida:** no exemplo, o botão principal aparece no cabeçalho, no hero, nos preços e no fim.

## Quando usar

- Lançar ou vender um produto digital (SaaS, app, ferramenta de time).
- Captar cadastros, lista de espera ou pedidos de demonstração.
- Ter uma página que o tráfego pago e as buscas possam abrir direto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Produto SaaS B2B ou B2C | ✅ Ótimo | É o caso central: explicar, provar e converter |
| Lançamento de app ou ferramenta | ✅ Ótimo | Hero com prévia e lista de espera funcionam bem |
| Produto técnico para devs | 🟡 Serve | Troque a prévia por trecho de código; documentação precisa de outro layout (ver 11) |
| Site institucional de empresa | 🟡 Serve | Sem produto único, as seções de recursos e preços perdem o sentido |
| Loja com catálogo | ❌ Evite | Precisa de vitrine, filtros e carrinho (ver 06) |
| Painel ou sistema interno | ❌ Evite | Quem já usa precisa de navegação e dados, não de convencimento (ver 02, 03) |

## Anatomia do layout

```
┌──────────────────────────────────────────────┐
│ Logo   Recursos Preços ...   Entrar [Começar]│ cabeçalho fixo 64 px
├──────────────────────────────────────────────┤
│              [Novo] aviso                    │
│        TÍTULO GRANDE em 2 linhas             │ hero
│          subtítulo · [CTA] [Vídeo]           │
│  ┌────────────────────────────────────────┐  │
│  │ prévia do produto (3 painéis)          │  │
│  └────────────────────────────────────────┘  │
├──────────────────────────────────────────────┤
│  Logos de clientes · 4 números               │ prova social
├──────────────────────────────────────────────┤
│  ┌──────────────┬────────┐                   │
│  │ recurso      │ rec. 2 │  bento            │
│  ├────────┬─────┴──┬─────┤  (6 colunas)      │
│  │ rec. 3 │ rec. 4 │ r.5 │                   │
│  └────────┴────────┴─────┘                   │
│  01 passo │ 02 passo │ 03 passo              │ como funciona
│  Depoimento grande                           │
│  depoimento │ depoimento │ depoimento        │
│  [Grátis] [Time ★] [Empresa]                 │ preços
│  Perguntas (accordion, 760 px)               │
│  Chamada final                               │
│  Rodapé em 4 colunas                         │
└──────────────────────────────────────────────┘
```

- **Largura do conteúdo:** máximo 1160 px, com 24 px de margem lateral (16 px no celular). A prévia do produto tem 1040 px.
- **Cabeçalho:** 64 px, fixo, com fundo translúcido e desfoque. Logo, 5 links, tema e dois botões.
- **Hero:** título de 44 a 84 px (fluido), até 14 caracteres por linha, subtítulo de 17 a 20 px. Espaço de 88 px acima.
- **Grades:** bento com 6 colunas e 16 px de espaço; passos e preços em 3 colunas; depoimentos em 3 colunas com um destaque de largura total.
- **Espaço entre seções:** 96 px (64 px em telas até 820 px).
- **Tablet (até 1024 px):** a prévia perde o painel direito e o bento vira 2 colunas.
- **Celular (até 820 px):** links viram menu em lista; passos, preços e depoimentos ficam em 1 coluna; rodapé em 2 colunas. Abaixo de 640 px o bento fica em 1 coluna, a prévia mostra só o quadro e os botões do hero ocupam a largura toda.

## Tokens do exemplo

| Token | Escuro (padrão) | Claro |
|---|---|---|
| Fundo / superfície / superfície 2 | `#0B0C0A` / `#13150F` / `#1A1D15` | `#FAFAF5` / `#FFFFFF` / `#F1F2E8` |
| Texto / texto suave | `#F2F4EC` / `#A3A998` | `#14160F` / `#585E4C` |
| Borda | `#2A2E22` | `#DADDCC` |
| Destaque (fundo de botão) | `#C6F432` com texto `#10130A` | igual |
| Destaque como texto | `#C6F432` | `#3F6212` (verde escuro; cerca de 6,8:1 sobre o fundo claro, acima do 4,5:1 do WCAG 1.4.3) |
| Fonte de título | Bricolage Grotesque 500/700 (Google Fonts), fallback Georgia | |
| Fonte de texto | Inter 400/500/600, fallback fonte do sistema | |
| Escala | 13 (rótulo) · 15 · 16 · 20 · 32–52 (h2) · 44–84 (h1); só os títulos e o subtítulo (17–20) são fluidos, com `clamp()` | |
| Raio | 8 · 12 · 20 px; botões e etiquetas em pílula (999 px) | |
| Sombra | `0 24px 60px -24px` só na prévia do produto; o resto usa borda de 1 px | |
| Espaçamento | escala de 4/8 px: 8, 16, 24, 32, 48, 64, 96 | |

## Componentes e padrões essenciais

- **Cabeçalho fixo** com CTA e alternância de tema; menu em lista no celular.
- **Hero:** título com uma palavra em destaque, subtítulo, dois botões (principal e secundário) e uma linha de confiança ("Sem cartão de crédito").
- **Prévia do produto** em HTML/CSS, marcada como imagem (`role="img"` com `aria-label`) e escondida do leitor de tela por dentro.
- **Prova social:** logos (texto, sem arquivos), 4 números concretos.
- **Bento de recursos:** 1 célula grande, o resto médias; cada uma com ícone, título curto e uma frase.
- **Depoimento com nome, cargo e empresa;** um em destaque.
- **Preços:** três planos, o do meio marcado, alternância mensal/anual (aqui o JS troca o valor), lista curta de benefícios e um botão por plano.
- **FAQ em `<details>`:** o MDN descreve o elemento como acordeão "sem script" e diz que, com o foco no `<summary>`, a barra de espaço abre e fecha (developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details, 2026-11-24).
- **Estados:** o formulário de cadastro (quando houver) precisa de carregando no botão, erro por campo, descrito em texto (WCAG 2.2, SC 3.3.1) e confirmação de envio. A página em si não tem estado vazio.
- **Foco visível** (WCAG 2.2, SC 2.4.7, nível AA: w3.org/WAI/WCAG22/Understanding/focus-visible.html), hover em tudo que clica e `prefers-reduced-motion` respeitado (MDN, `prefers-reduced-motion`: detecta quem pediu menos movimento no sistema).

## Quando é bom

- Leve: sem imagens externas, só um arquivo e duas fontes.

## Quando é ruim

- **Efeitos de movimento** (parallax, partículas): respeite `prefers-reduced-motion` (MDN).
- **Contraste fraco:** o WCAG 2.2, SC 1.4.3 (AA) pede 4,5:1 para texto normal e 3:1 para texto grande (w3.org/WAI/WCAG22/Understanding/contrast-minimum.html, 2026-11-24). No exemplo, o verde-lima `#C6F432` sobre `#FAFAF5` dá cerca de 1,2:1, por isso o texto no tema claro usa `#3F6212` (cerca de 6,8:1).

## Como começar

1. Abra [05-landing-saas.html](../examples/05-landing-saas.html) no navegador e veja os dois temas pelo botão do cabeçalho.
2. Copie o bloco `:root` e o do tema claro. Troque o nome, o destaque e as duas fontes pela sua marca; confira o contraste do destaque como texto (mínimo 4,5:1, WCAG 1.4.3).
3. Reescreva os textos com os resultados reais do produto, na ordem das seções. Apague as seções sem conteúdo.
4. Monte com a skill design: shadcn/ui na base (botão, accordion, sheet), Magic UI para o bento e efeitos discretos, Lucide para ícones. Sem React, use HyperUI.
5. Teste de 360 a 1440 px e com teclado antes de publicar.

## Combina com / alternativas

- [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md): para onde o botão "Começar" leva.
- [11-documentacao.md](11-documentacao.md): quando o produto precisa de docs longas.
- [06-ecommerce.md](06-ecommerce.md): se o que se vende é um produto físico.
- [01-fundamentos.md](01-fundamentos.md): tokens, grade e acessibilidade comuns.

## Decisão rápida

- **Use se:** você tem um produto digital a explicar e quer cadastros ou demonstrações.
- **Evite se:** a pessoa já é cliente e precisa trabalhar (use dashboard ou app) ou se há catálogo grande para navegar (use loja).
