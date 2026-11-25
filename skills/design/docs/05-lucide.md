# Lucide

> Biblioteca open source de ícones SVG de traço limpo e consistente, nascida como fork do Feather e usada como pacote padrão do shadcn/ui.

| | |
|---|---|
| **Site** | https://lucide.dev |
| **Categoria** | Linha 3 — Animações, componentes e ícones |
| **Tipo** | Pacote de ícones |
| **Stack** | SVG, pacotes para JavaScript, React, Vue, Svelte, Solid, Preact, Angular, Astro e React Native |
| **Preço** | Grátis (open source). Sem planos pagos encontrados |
| **Licença** | ISC (geral); ícones derivados do Feather em MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Lucide é um conjunto de ícones em SVG mantido pela comunidade. Na data da verificação, a busca do site listava 2119 ícones. Todos seguem o mesmo estilo: traço uniforme, cantos arredondados e grade fixa.

Na prática, você instala o pacote do seu framework e importa cada ícone como um componente. O componente renderiza um SVG inline. Tamanho, cor e espessura do traço mudam por props (`size`, `color`, `strokeWidth`). Também há pacotes para uso sem framework e acesso aos SVGs avulsos. Na versão 1.x os pacotes de framework seguem o padrão `@lucide/<framework>` (confirmados no npm: `@lucide/vue`, `@lucide/svelte`, `@lucide/angular`, `@lucide/astro`, além de `lucide-react`, `lucide-react-native` e `lucide-solid`).

O projeto é tree-shakable: só os ícones importados entram no bundle. Como o SVG usa `currentColor`, o ícone herda a cor do texto e funciona bem com Tailwind.

## Por que usar

- **Consistência:** um único estilo visual em toda a interface, sem misturar ícones de fontes diferentes.
- **Custo zero:** licença permissiva (ISC), uso comercial liberado, sem assinatura.
- **Integração:** já vem no shadcn/ui, então quem usa esse sistema não precisa decidir nada.
- **Peso:** SVG inline e importação por ícone mantêm o bundle pequeno.
- **Cobertura:** mais de 2 mil ícones cobrem a maioria das necessidades de UI.

## Quando usar

- Projeto com shadcn/ui, v0, Lovable ou similares, que já geram código com Lucide.
- Interface de produto (menus, botões, tabelas, formulários, estados vazios).
- Quando o time quer um estilo de traço único e sem custo.
- Projeto em React, Vue, Svelte, Angular, Astro ou React Native.
- Quando você precisa mudar espessura de traço ou cor por props, sem editar SVG.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | 🟡 Serve | Bom para listas de recursos, mas o estilo é neutro e pode parecer genérico |
| Site institucional | 🟡 Serve | Cobre o básico; falta personalidade de marca |
| Portfólio | 🟡 Serve | Funciona como apoio, mas não cria identidade própria |
| Blog/conteúdo | ✅ Ótimo | Poucos ícones, leves e discretos (busca, compartilhar, menu) |
| E-commerce | ✅ Ótimo | Carrinho, busca, filtros, usuário e frete têm ícones prontos |
| SaaS / app web | ✅ Ótimo | É o caso central: UI densa com muitos ícones funcionais |
| Dashboard / painel admin | ✅ Ótimo | Traço fino e legível em tamanhos pequenos (16–20 px) |
| MVP / protótipo | ✅ Ótimo | Zero configuração e vem por padrão nas ferramentas de geração de UI |
| Sistema interno corporativo | ✅ Ótimo | Gratuito, estável e sem risco de licença |
| App mobile | ✅ Ótimo | Existe pacote para React Native |

## Quando é bom

- **Estilo coeso:** todos os ícones compartilham grade e traço, então a interface fica uniforme sem esforço.
- **Personalização por props:** cor, tamanho e espessura mudam no código, sem abrir editor de vetor.
- **Tree-shaking:** só o que você importa vai para o build, o que ajuda na performance.
- **Licença simples:** ISC permite uso comercial; basta manter o aviso de copyright.
- **Ecossistema:** muitos frameworks suportados; cerca de 26 mil estrelas no GitHub (lucide-icons/lucide, 2026-11-24).
- **Padrão do shadcn/ui:** código gerado por IA costuma já usar Lucide, o que reduz retrabalho.

## Quando é ruim

- **Sem ícones de marca:** a versão 1 removeu logos (GitHub, Figma, Facebook etc.) por pressão legal e questões de marca registrada. O guia oficial recomenda Simple Icons. Quem atualiza de versões antigas pode ter imports quebrados.
- **Só traço (outline):** não há variações de peso como no Phosphor (thin, bold, fill, duotone). Se o design pede ícones preenchidos ou duotone, falta opção.
- **Visual genérico:** por ser o padrão de muita ferramenta, vários sites ficam parecidos. Para identidade forte, será preciso ícones próprios.
- **Importação dinâmica exige cuidado:** usar um componente por nome em runtime pode puxar mais ícones do que o necessário. Na pesquisa, as fontes divergiram sobre o efeito no bundle; meça no seu build.
- **Importar o pacote inteiro:** `import * as icons` desfaz o tree-shaking e infla o bundle. Use imports nomeados.
- **Acessibilidade é responsabilidade sua:** o ícone sozinho não tem texto. Ícone sem rótulo precisa de `aria-label`; ícone decorativo deve ser escondido de leitores de tela.
- **Mudanças entre versões:** nomes de ícones já foram renomeados e removidos ao longo do tempo. Fixe a versão e leia o changelog antes de atualizar.
- **Ícone faltando:** nichos específicos (setor financeiro, saúde, marcas) podem não ter o símbolo exato. Será necessário desenhar ou combinar com outra biblioteca.

## Como começar

React:

```bash
npm i lucide-react
```

```jsx
import { Camera } from "lucide-react";

<Camera size={20} strokeWidth={1.5} />
```

Em projeto shadcn/ui, o Lucide já é instalado como biblioteca de ícones padrão. Para outros frameworks, veja a lista de pacotes em https://lucide.dev (guia "Get Started"). Para Vue, Svelte, Angular e Astro use `npm i @lucide/vue` (ou `@lucide/svelte`, `@lucide/angular`, `@lucide/astro`); os pacotes antigos `lucide-vue-next` e `lucide-svelte` são legados.

## Combina com / alternativas

Combina com:
- [shadcn/ui](01-shadcn-ui.md): usa Lucide como padrão.
- [Magic UI](02-magic-ui.md) e [Aceternity UI](03-aceternity-ui.md): componentes que normalmente aceitam ícones Lucide.

Alternativas dentro da lista:
- [Phosphor](06-phosphor.md): mais pesos e estilos (fill, duotone).
- [Tabler Icons](07-tabler-icons.md): catálogo ainda maior, também em traço.

Alternativas de fora:
- Heroicons
- Radix Icons
- Simple Icons (apenas para logos de marcas)

## Decisão rápida

- **Use se:** o projeto é uma interface de produto, usa shadcn/ui ou ferramentas de geração de UI, e você quer ícones leves, gratuitos e consistentes.
- **Evite se:** precisa de logos de marca, ícones preenchidos ou duotone, ou de uma identidade visual própria que não pareça template.
