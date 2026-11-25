# Tabler Icons

> Biblioteca open source de mais de 6.500 ícones SVG de traço (outline) e preenchidos (filled), com pacotes prontos para React, Vue, Svelte, Angular e outros.

| | |
|---|---|
| **Site** | https://tabler.io/icons |
| **Categoria** | Linha 3 — Animações, componentes e ícones |
| **Tipo** | Pacote de ícones |
| **Stack** | SVG, React, React Native, Vue, Preact, Svelte, SolidJS, Angular, Astro, webfont, sprite, Figma, PNG/PDF/EPS |
| **Preço** | Grátis (open source). Pacotes pagos opcionais: Bundle (US$ 9, pagamento único, SVG/PNG/PDF) e All Package (US$ 69, pagamento único, inclui template admin, ilustrações e e-mails). Valores na data da verificação; o site pode mostrar promoção |
| **Licença** | MIT (uso pessoal e comercial, sem atribuição obrigatória) |
| **Verificado em** | 2026-11-24 |

## O que é

Tabler Icons é um conjunto de ícones feito pelo time do Tabler (o projeto de template admin). Na data da verificação, o site e o GitHub listavam 6.563 ícones: 5.509 outline e 1.054 filled.

Todos seguem a mesma grade de 24x24 px, com traço de 2 px por padrão. Tamanho, cor e espessura do traço são ajustáveis. Isso mantém o visual consistente em toda a interface.

Você usa de várias formas: pacote npm por framework (`@tabler/icons-react`, `@tabler/icons-vue`, etc.), SVG puro (`@tabler/icons`), sprite, webfont ou plugin do Figma. No site dá para buscar, copiar o SVG e baixar PNG.

## Por que usar

- **Cobertura grande:** com mais de 6.500 ícones, é raro faltar um conceito (finanças, dev, clima, e-commerce, interface).
- **Consistência:** grade e traço únicos evitam a mistura de estilos que deixa a interface amadora.
- **Custo zero:** licença MIT, sem cobrança por uso comercial nem atribuição.
- **Fluxo design-dev:** o mesmo conjunto existe no Figma e no código, o que reduz retrabalho de handoff.
- **Flexibilidade de formato:** serve de app React a página estática com webfont.

## Quando usar

- Projeto precisa de muitos ícones diferentes e não quer comprar um pacote.
- Time usa React, Vue, Svelte, Angular ou Astro e quer componentes prontos.
- Design e código precisam do mesmo set (Figma + npm).
- Interface densa, com muitas ações e status (painéis, tabelas, menus).
- Você já usa o template Tabler ou combina com shadcn/ui no lugar do Lucide.
- Precisa de ícones preenchidos para estados ativos (ex.: favorito marcado), mesmo que seja menor parte do set.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | 🟡 Serve | Atende bem para listas de benefícios, mas o visual de traço fino é genérico; para destaque, prefira ícones 3D ou ilustrações |
| Site institucional | ✅ Ótimo | Ícones simples de contato, redes e serviços, sem custo |
| Portfólio | 🟡 Serve | Funciona, mas pouco autoral; muitos portfólios usam o mesmo set |
| Blog/conteúdo | ✅ Ótimo | Poucos ícones de navegação e compartilhamento; basta SVG avulso e fica leve |
| E-commerce | ✅ Ótimo | Carrinho, entrega, pagamento, filtros e status existem em grande variedade |
| SaaS / app web | ✅ Ótimo | Cobertura ampla para funcionalidades diversas e consistência de UI |
| Dashboard / painel admin | ✅ Ótimo | É o caso de origem do projeto: ícones de dados, tabelas e configurações |
| MVP / protótipo | ✅ Ótimo | Instala em um comando e quase nunca falta ícone |
| Sistema interno corporativo | ✅ Ótimo | Gratuito, sem risco de licença, bom para telas densas |
| App mobile | 🟡 Serve | Há pacote React Native, mas apps nativos costumam seguir SF Symbols ou Material Symbols |

## Quando é bom

- **Licença MIT:** sem custo, sem atribuição e sem risco jurídico em projeto comercial.
- **Volume:** milhares de ícones reduzem a necessidade de misturar sets, que é o que quebra a consistência.
- **Traço ajustável:** dá para afinar a espessura (por exemplo 1.5) para combinar com a marca sem editar arquivos.
- **Pacotes por framework:** um componente por ícone, com props de tamanho e cor, evita colar SVG à mão.
- **Várias saídas:** webfont e sprite ajudam em sites sem build; PNG/PDF/EPS ajudam em materiais fora do código.
- **Projeto ativo:** releases frequentes trazem ícones novos com regularidade.

## Quando é ruim

- **Bundle e build lentos no React:** o pacote expõe um arquivo único com todos os ícones. Há issue aberta (#1161) relatando bundle enorme em um cenário de biblioteca com Remix/Vite, e pedidos de imports modulares por causa de lentidão do dev server. O `package.json` do `@tabler/icons-react` declara `sideEffects: false`, o que permite tree-shaking com imports nomeados. Use o analisador de bundle e, se preciso, imports diretos por ícone.
- **Poucos ícones preenchidos:** só 1.054 de 6.563 têm versão filled. Se o design depende de pares outline/filled para tudo, vai faltar variante.
- **Visual genérico:** traço de 2 px é muito comum. Em marca com identidade forte ele não diferencia o produto.
- **Muita escolha:** milhares de ícones sem curadoria levam a usos inconsistentes (conceitos parecidos com desenhos diferentes) se o time não definir um subconjunto.
- **Pacotes pagos confundem:** o que se paga (Bundle, All Package) são arquivos SVG/PNG/PDF e extras do template, não o uso nos pacotes npm, que já são gratuitos. Verifique antes de comprar.
- **Fragmentação de pacotes:** há um pacote por framework, e o Svelte tem dois (`icons-svelte` para Svelte 4 e `icons-svelte-runes` para Svelte 5). Escolher o errado causa erro de instalação.
- **Acessibilidade é com você:** ícones são decorativos por padrão; botões só com ícone precisam de `aria-label`.

## Como começar

React:

```bash
npm install @tabler/icons-react
```

```jsx
import { IconHome } from '@tabler/icons-react';

<IconHome size={24} stroke={1.5} />
```

Outros formatos (instalações confirmadas pelo repositório):

```bash
npm install @tabler/icons          # SVG puro
npm install @tabler/icons-vue      # Vue
npm install @tabler/icons-webfont  # webfont
```

Para ícones preenchidos, os nomes mudam (no webfont, `tabler-icons-filled.css`; no SVG, a pasta `icons/filled/`). Confira o nome do componente filled no site antes de usar.

## Combina com / alternativas

Combina com:
- [shadcn/ui](./01-shadcn-ui.md): troca simples quando o Lucide não tem o ícone.
- [HyperUI](./04-hyperui.md): blocos em Tailwind que aceitam ícones SVG avulsos.

Alternativas dentro desta lista:
- [Lucide](./05-lucide.md): menor, mais curado e padrão do shadcn/ui; melhor se você quer leveza e consistência.
- [Phosphor](./06-phosphor.md): seis pesos por ícone (thin a duotone); melhor para variar o estilo.

Alternativas de fora:
- Heroicons (Tailwind Labs).
- Material Symbols (Google).
- Iconify (agregador de vários sets).

## Decisão rápida

- **Use se:** precisa de muitos ícones gratuitos, com licença MIT, consistentes e disponíveis em React, Vue ou Figma; o projeto é app, painel, e-commerce ou sistema interno.
- **Evite se:** quer um conjunto pequeno e curado (prefira Lucide), precisa de várias espessuras ou duotone (prefira Phosphor), a marca exige ícones autorais ou o bundle é muito sensível e você não vai controlar os imports.
