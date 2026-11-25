# HyperUI

> Biblioteca gratuita e open source de componentes Tailwind CSS para copiar e colar, de marketing e de aplicação, criada por Mark Mead.

| | |
|---|---|
| **Site** | https://hyperui.dev |
| **Categoria** | Linha 3 — Animações, componentes e ícones |
| **Tipo** | Biblioteca de componentes (snippets HTML + Tailwind) e templates de página |
| **Stack** | HTML + Tailwind CSS (repositório do site em Astro, TypeScript e Tailwind v4); alguns componentes usam Alpine.js |
| **Preço** | Grátis (o site se descreve como "free and open source"; nenhum plano pago encontrado) |
| **Licença** | MIT |
| **Verificado em** | 2026-11-24 |

## O que é

HyperUI é um catálogo de blocos de interface feitos só com classes utilitárias do Tailwind. Você navega no site, escolhe o componente, copia o HTML e cola no seu projeto. Não há pacote para instalar nem CLI obrigatória.

O site organiza o conteúdo em quatro grupos: Application, Marketing, Neobrutalism e Templates (páginas completas montadas com os componentes). Os exemplos têm variantes de modo escuro e de layout RTL, e o site afirma que todos passam no axe para WCAG 2.1 AA.

Há também ferramentas extras: um gerador de variantes dark a partir de markup Tailwind e material para agentes de IA (llms.txt, servidor MCP e uma skill instalável, segundo o README). Interações mais ricas ficam num site separado, o HyperUX (js.hyperui.dev).

O código do site está no GitHub (cerca de 12,3 mil estrelas na data da verificação), com a licença MIT.

## Por que usar

O ganho é velocidade sem dependência. Você pula a etapa de montar do zero seções comuns (hero, preços, FAQ, tabelas, formulários, cards) e fica com HTML puro que pode editar à vontade.

Como não é um pacote, não há versão para atualizar, nem API de componente para aprender, nem aumento de bundle por causa da biblioteca. O custo é zero e a licença MIT permite uso comercial.

A preocupação declarada com acessibilidade e dark mode economiza retrabalho em relação a snippets aleatórios da internet.

## Quando usar

- Montar uma landing page ou site institucional rápido em Tailwind.
- Montar telas de app (tabelas, formulários, menus laterais, paginação) sem desenhar tudo.
- Prototipar um MVP e validar a ideia antes de investir em design system.
- Em projetos que não usam React, como Laravel/Blade, Rails, Astro, Django ou HTML estático, onde bibliotecas de componentes React não servem.
- Como ponto de partida que o time vai adaptar à marca, sem querer manter uma lib.
- Para alimentar agentes de IA com referências de marcação limpa (llms.txt/MCP).

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | ✅ Ótimo | A categoria Marketing cobre as seções típicas e o resultado é HTML leve. |
| Site institucional | ✅ Ótimo | Seções padrão e fácil de personalizar com a identidade da marca. |
| Portfólio | 🟡 Serve | Dá a base (header, grid, contato), mas o diferencial visual precisa ser seu. |
| Blog/conteúdo | 🟡 Serve | Há cards e listagens, mas o foco do blog costuma ser tipografia e CMS. |
| E-commerce | 🟡 Serve | Há blocos de vitrine, carrinho e checkout, mas a lógica fica toda por sua conta. |
| SaaS / app web | 🟡 Serve | Bom para telas e layouts; estados, foco e modais interativos você implementa. |
| Dashboard / painel admin | 🟡 Serve | Há blocos de tabela, sidebar e stats, sem gráficos nem componentes de dados prontos. |
| MVP / protótipo | ✅ Ótimo | Copia, cola e valida sem custo nem compromisso. |
| Sistema interno corporativo | 🟡 Serve | Atende telas simples; para muitos formulários complexos, uma lib com comportamento compensa. |
| App mobile | ❌ Evite | É HTML/Tailwind para web; não gera UI nativa nem React Native. |

## Quando é bom

- **Gratuito e MIT:** sem cobrança por projeto nem risco de licença para uso comercial.
- **Sem lock-in:** o código é seu depois de colado; se o HyperUI sumir, nada quebra.
- **Zero dependência de runtime:** não entra no bundle, então não pesa na performance.
- **Agnóstico de framework:** é HTML, serve em qualquer stack que aceite Tailwind.
- **Acessibilidade e dark mode considerados:** a base é melhor que a de snippets soltos, segundo as afirmações do próprio site.
- **Fácil de ler e editar:** são só classes utilitárias, sem abstração para aprender.
- **Preparado para IA:** llms.txt, MCP e skill facilitam gerar telas coerentes com um agente.

## Quando é ruim

- **Sem componentes reutilizáveis:** é copiar e colar. Se o mesmo botão aparece em 30 lugares, você mesmo precisa extrair para componente, senão a manutenção vira repetição de classes.
- **Sem atualização automática:** correções feitas no HyperUI não chegam ao seu código; você teria de recopiar à mão.
- **Interatividade limitada:** nenhum dos 658 exemplos HTML do repositório usa Alpine.js (`x-data`); 92 trazem `<script>` próprio e 32 carregam Chart.js (markmead/hyperui, commit `aea6d12`, 2026-11-24). O site não traz o comportamento complexo (modais com foco preso, combobox, datepicker). Para isso, use Radix/shadcn/Headless UI.
- **Customização por classes:** não há tokens nem temas em runtime; trocar a identidade visual exige editar classes (ou ter bom `@theme` no Tailwind).
- **Catálogo menor que o de produtos pagos:** comparação do daisyUI (concorrente, vale desconfiar) cita um número bem menor que o do Tailwind UI. Conferi no site em 2026-11-24: as categorias listadas somam cerca de 242 componentes, mais 7 templates; o site não informa um total único.
- **Exige Tailwind e possivelmente plugins:** a mesma comparação cita a necessidade do `@tailwindcss/forms`. O site não informa a versão do Tailwind nem cita o plugin; o repositório oficial (MIT) usa Tailwind v4 e tem `@tailwindcss/forms` como dependência. Confira a compatibilidade antes de colar em projetos v3.
- **Risco de visual genérico:** muita gente usa a mesma biblioteca, e o site pode ficar com cara de template se não for personalizado.
- **Pouca documentação de problemas conhecidos:** a página oficial não traz lista de limitações, e a FAQ indica que pendências ficam no GitHub. O repositório markmead/hyperui (licença MIT) tinha 0 issues abertas em 2026-11-24 (`gh api repos/markmead/hyperui`, campo `open_issues_count`).

## Como começar

1. Tenha um projeto com Tailwind CSS configurado (confirme a versão usada pelo componente).
2. Acesse https://hyperui.dev e escolha a categoria (Marketing, Application, Neobrutalism ou Templates).
3. Copie o HTML do componente e cole no seu projeto; adapte textos, cores e espaçamentos.
4. Se o componente exigir `@tailwindcss/forms` ou Alpine.js, instale-os (veja a nota do componente).
5. Opcional, para agentes de IA: o README do repositório descreve llms.txt, servidor MCP e uma skill via `npx skills add` (https://github.com/markmead/hyperui). Não testei esses comandos.

## Combina com / alternativas

- [shadcn/ui](01-shadcn-ui.md): use no lugar do HyperUI quando precisar de comportamento (dialog, select, form) em React; use o HyperUI só para seções de marketing.
- [Magic UI](02-magic-ui.md) e [Aceternity UI](03-aceternity-ui.md): somam animação em cima de uma base simples.
- [Lucide](05-lucide.md) ou [Phosphor](06-phosphor.md): ícones para os blocos.
- Fora da lista: Tailwind UI/Tailwind Plus (pago, catálogo maior), Flowbite e daisyUI (componentes com mais comportamento ou classes semânticas), Meraki UI.

## Decisão rápida

- **Use se:** precisa de seções e telas em Tailwind rápido, de graça, sem dependência, em qualquer framework, ou está montando um MVP, landing ou site institucional.
- **Evite se:** precisa de componentes interativos complexos prontos, atualização por pacote, design system com tokens e temas, ou UI mobile nativa.
