# Phosphor

> Família de ícones open source com seis pesos (thin, light, regular, bold, fill e duotone), com pacotes oficiais para web, React, Vue, Flutter e outros, além de plugin para Figma.

| | |
|---|---|
| **Site** | https://phosphoricons.com |
| **Categoria** | Linha 3 — Animações, componentes e ícones |
| **Tipo** | Pacote de ícones |
| **Stack** | SVG, React (`@phosphor-icons/react`), Vue (`@phosphor-icons/vue`), CSS/web fonts (`@phosphor-icons/web`), Web Components, Flutter, Elm, Figma |
| **Preço** | Grátis. O site oficial não oferece plano pago |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Phosphor é uma biblioteca de ícones desenhados numa mesma grade e com o mesmo estilo. Cada ícone existe em seis pesos: thin, light, regular, bold, fill e duotone. O README da homepage ainda fala em 1.248 ícones, mas o repositório `phosphor-icons/core` tinha 1.512 ícones no peso regular na data da verificação (contagem desatualizada no README).

Na prática, você instala o pacote do seu framework e importa cada ícone como componente. Em React: `import { Heart } from "@phosphor-icons/react"` e `<Heart weight="bold" size={24} />`. No HTML puro, você liga uma folha de estilo por peso e usa `<i class="ph ph-smiley"></i>`.

Há pacotes oficiais para web, React, Vue, Flutter, Elm, SwiftUI e Web Components. A comunidade mantém portes para Svelte, Astro, Rails, Laravel e outros. O site também permite buscar, filtrar por categoria, trocar peso, cor e tamanho e copiar o SVG.

## Por que usar

- **Consistência visual.** Todos os pesos compartilham a mesma geometria. Você muda o tom da interface trocando uma prop, sem trocar de biblioteca.
- **Hierarquia sem esforço.** Regular para o geral, fill para o estado ativo, duotone para destaque. Isso resolve o problema comum de ícone de aba ativa e inativa.
- **Custo zero e licença simples.** MIT permite uso comercial sem atribuição obrigatória e sem cobrança por assento.
- **Cobertura de stacks.** O mesmo set serve site, app e design no Figma, então design e dev falam dos mesmos nomes.

## Quando usar

- Quando o produto precisa de mais de um estilo de ícone (ativo/inativo, destaque, ênfase).
- Quando o time usa React, Vue ou Flutter e quer pacote oficial, não SVG colado à mão.
- Quando design e dev precisam do mesmo catálogo (plugin do Figma e nomes iguais no código).
- Quando a identidade pede ícones com personalidade mais suave que o padrão "fino e técnico".
- Quando você quer trocar de set sem custo: componentes aceitam `size`, `color` e `weight` de forma uniforme.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | ✅ Ótimo | Duotone e bold dão destaque a features e benefícios sem precisar de ilustração. |
| Site institucional | ✅ Ótimo | Catálogo amplo cobre serviços, contatos e redes; peso light passa sobriedade. |
| Portfólio | ✅ Ótimo | Dá para casar o peso do ícone com o peso da tipografia e manter identidade própria. |
| Blog/conteúdo | 🟡 Serve | Poucos ícones são necessários (compartilhar, busca). Um set menor resolve. |
| E-commerce | 🟡 Serve | Cobre carrinho, pagamento e entrega, mas faltam ícones de marcas e bandeiras de cartão. |
| SaaS / app web | ✅ Ótimo | Fill/regular para estados ativos e inativos é padrão útil em navegação. |
| Dashboard / painel admin | ✅ Ótimo | Muitos ícones de dados, ações e arquivos; tamanho e peso controlados por prop. |
| MVP / protótipo | ✅ Ótimo | Instala em um comando e é grátis; evita gastar tempo decidindo ícone. |
| Sistema interno corporativo | ✅ Ótimo | MIT e sem dependências de serviço externo; fácil de padronizar. |
| App mobile | 🟡 Serve | Há Flutter, SwiftUI e React Native (este via comunidade); confira a manutenção do porte. |

## Quando é bom

- **Seis pesos no mesmo set.** Evita misturar bibliotecas com traços diferentes, que é a principal causa de interface "desalinhada".
- **API uniforme.** `size`, `color`, `weight` e `mirrored` funcionam igual em todos os ícones, o que reduz código de estilo.
- **Duotone.** Dá um visual rico com uma única cor de tema, sem custo de ilustração.
- **Licença MIT.** Pode ir para produto comercial e cliente sem revisão jurídica extra.
- **Figma e web alinhados.** O time de design escolhe o ícone pelo mesmo nome que o dev importa.
- **Tree-shaking suportado.** Com imports nomeados, só entram os ícones usados (o README oficial recomenda esse formato).

## Quando é ruim

- **Bundle pode inchar com import errado.** O README avisa que, dependendo do bundler, importar tudo (`import * as Icons`) impede o tree-shaking. Em Next.js, vale configurar `optimizePackageImports`. Meça com um analisador de bundle.
- **Ícones dinâmicos por nome.** Montar o ícone a partir de uma string (vinda de CMS, por exemplo) obriga a importar o catálogo todo ou um mapa manual. Isso pesa no bundle.
- **Problemas de ecossistema.** Houve issues públicas de instalação em Next.js e de build com webpack no `@phosphor-icons/react`, e há uma de bundling com Vite 8+ (rolldown) no mesmo pacote; o pacote de Web Components não tem issue aberta desse tipo. Conferi no GitHub em 2026-11-24: as de Next.js (#109) e webpack (#99) estão fechadas; a de Vite 8+/rolldown (#155) segue aberta. Teste no seu build.
- **Pacote antigo.** `phosphor-react` foi substituído por `@phosphor-icons/react`. Tutoriais antigos citam o nome velho e quebram.
- **Server Components.** Em React com SSR/RSC é preciso usar o caminho `@phosphor-icons/react/ssr`. Quem não sabe esbarra em erros de contexto.
- **Sem ícones de marca completos.** Para logos de empresas e bandeiras, você precisa de outro pacote.
- **Estilo próprio.** Os traços arredondados e a identidade do set podem não casar com marcas de visual muito geométrico ou corporativo seco.
- **Portes de comunidade.** React Native, Svelte e outros dependem de mantenedores externos, com ritmo de atualização variável.
- **Supply chain.** Como qualquer pacote npm, fixe versão e use lockfile. Pacotes de ícones foram alvo de incidentes gerais no npm; confirme a procedência do nome.

## Como começar

React:

```bash
npm i @phosphor-icons/react
```

```jsx
import { Heart } from "@phosphor-icons/react";

<Heart size={24} weight="duotone" color="#e11d48" />
```

Vue:

```bash
npm i @phosphor-icons/vue
```

Os componentes usam o prefixo `Ph` (por exemplo `PhHeart`), para evitar colisão com elementos HTML.

HTML puro (CDN, uma folha por peso):

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css" />
<i class="ph ph-smiley"></i>
```

Dica: sempre use imports nomeados. Para Figma, procure o plugin Phosphor Icons na comunidade.

## Combina com / alternativas

Combina com:
- [shadcn/ui](01-shadcn-ui.md): troque o ícone padrão dos componentes por Phosphor para ter mais pesos.
- [Magic UI](02-magic-ui.md) e [Aceternity UI](03-aceternity-ui.md): seções de features com ícones duotone.
- [HyperUI](04-hyperui.md): blocos em que você substitui os SVGs embutidos por um set consistente.
- Geradores de UI por IA (v0, Lovable e similares): peça explicitamente Phosphor no prompt, pois o padrão costuma ser outro set.

Alternativas dentro da lista:
- [Lucide](05-lucide.md): traço único e leve, padrão do shadcn/ui. Melhor se você só precisa de um peso.
- [Tabler Icons](07-tabler-icons.md): catálogo muito grande em traço, bom para dashboards densos.

Fora da lista: Heroicons (Tailwind), Material Symbols (Google, com eixos variáveis de peso) e Iconoir.

## Decisão rápida

- **Use se:** precisa de variações de peso/estilo no mesmo set, trabalha com React, Vue ou Flutter, quer MIT e catálogo compartilhado com o Figma.
- **Evite se:** só usa meia dúzia de ícones de traço simples (Lucide basta), precisa de logos de marcas, escolhe ícones dinamicamente por nome em grande escala, ou seu build não tolera risco de tree-shaking mal configurado.
