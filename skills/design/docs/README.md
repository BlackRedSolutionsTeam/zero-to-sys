# UI kits e ícones

Um documento por ferramenta, explicando quando usar, para que tipo de site, quando é bom, quando é ruim e por quê. A lista ficou só com o que passa em três critérios: qualidade real, visual profissional e boa variedade grátis. Preços, licenças e números foram verificados nos sites oficiais em 2026-11-24.

## Componentes

| Ferramenta | O que é | Grátis | Doc |
|---|---|---|---|
| shadcn/ui | Componentes React acessíveis (Radix + Tailwind) que você copia para o projeto | Tudo, MIT | [01-shadcn-ui.md](01-shadcn-ui.md) |
| Magic UI | Componentes animados no estilo shadcn, para páginas de marketing | Todos os componentes, MIT (só templates são pagos) | [02-magic-ui.md](02-magic-ui.md) |
| Aceternity UI | Componentes React com efeitos de destaque para landing pages | 100+ componentes (templates e blocos Pro são pagos) | [03-aceternity-ui.md](03-aceternity-ui.md) |
| HyperUI | Blocos Tailwind para copiar e colar, sem depender de React | Tudo, MIT | [04-hyperui.md](04-hyperui.md) |

## Ícones

| Ferramenta | O que é | Grátis | Doc |
|---|---|---|---|
| Lucide | Ícones de traço limpo, padrão do shadcn/ui | Tudo, ISC | [05-lucide.md](05-lucide.md) |
| Phosphor | Ícones em 6 pesos (thin a fill e duotone) | Tudo, MIT | [06-phosphor.md](06-phosphor.md) |
| Tabler Icons | Mais de 6.500 ícones SVG outline e filled | Tudo, MIT | [07-tabler-icons.md](07-tabler-icons.md) |

## Qual escolher

- **Base de qualquer app ou site em React:** [shadcn/ui](01-shadcn-ui.md) com [Lucide](05-lucide.md).
- **Landing page com animação e efeitos:** [Magic UI](02-magic-ui.md) primeiro, por ser mais sóbrio; [Aceternity UI](03-aceternity-ui.md) para um ou dois efeitos de destaque no hero.
- **Site sem React (HTML ou Tailwind puro):** [HyperUI](04-hyperui.md).
- **Ícones:** [Lucide](05-lucide.md) como padrão, [Phosphor](06-phosphor.md) quando precisar de pesos diferentes, [Tabler Icons](07-tabler-icons.md) quando faltar ícone. Use um set só por projeto.

## O que saiu da lista e por quê

| Ferramenta | Motivo |
|---|---|
| 21st.dev | Plano grátis limitado a 2 cópias de componente por dia; componentes publicados por autores da comunidade, cada um com página própria de autor (21st.dev/community/components, 2026-11-24) |
| Uiverse | Qualidade muito irregular, visual amador em boa parte; repositório parado desde 2024 |
| Motion Primitives | Bom, mas catálogo pequeno, em beta e com manutenção lenta; o Magic UI cobre o mesmo uso |
| Cruip | Quase tudo pago |
| Kage | Galeria de referências de interfaces; o site também lista uma seção de componentes (cerca de 3.379 em 2026-11-24). Preço e licença não constam no site |
| Kitbitz | Ilustração à mão tem estilo informal; site no ar em kitbitz.art (título: "2,000+ free hand-drawn illustrations"; conferido em 2026-11-24). Licença: a página inicial do próprio site não declara licença nem termos de uso (só a palavra "free" no título) e não tem link para página de licença, FAQ ou termos (kitbitz.art, 2026-11-24). Sem licença publicada pelo autor não dá para garantir uso comercial, e esse é um motivo a mais para ficar fora |
| 3dicons | Estilo 3D datado e catálogo pequeno; recursos de edição no plano pago |
| LottieFiles | Animações, não componentes; o plano grátis tem limites (lottiefiles.com/pricing, 2026-11-24) |
