# shadcn/ui

> Coleção de componentes React acessíveis (Tailwind + primitivos como Radix) que você copia para dentro do projeto e edita, em vez de instalar como biblioteca.

| | |
|---|---|
| **Site** | https://ui.shadcn.com |
| **Categoria** | Linha 2 — Componentes, templates e assets |
| **Tipo** | Biblioteca de componentes "open code" + CLI de distribuição |
| **Stack** | React, Tailwind CSS, Radix UI, Base UI ou React Aria (variantes nas páginas de componente, 2026-11-24), TypeScript; Next.js, Vite, React Router, Astro, TanStack Start, Laravel |
| **Preço** | Grátis (nenhum plano pago encontrado nas páginas oficiais lidas) |
| **Licença** | MIT (arquivo LICENSE do repositório shadcn-ui/ui no GitHub; a página de docs não a nomeia) |
| **Verificado em** | 2026-11-24 |

## O que é

shadcn/ui não é um pacote que você instala e importa. A própria documentação diz: "não é uma biblioteca de componentes; é como você constrói a sua". Você roda um comando e o código do componente (botão, dialog, tabela) é gravado na sua pasta, pronto para editar.

Os componentes seguem uma interface composável e previsível. Um esquema de arquivos planos descreve cada componente e suas dependências, e uma CLI distribui isso entre projetos. Esse mesmo esquema permite criar registries próprios, por exemplo de um design system interno.

O estilo vem de Tailwind e o comportamento acessível (foco, teclado, ARIA) vem de primitivos headless. As páginas de componente oferecem variantes Base UI, React Aria e Radix UI, com Radix exibido por padrão (conferido em 2026-11-24).

## Por que usar

- **Dono do código:** você altera qualquer detalhe sem brigar com `className` ou override de CSS.
- **Acessibilidade pronta:** teclado e leitores de tela vêm dos primitivos, sem reinventar.
- **Consistência:** todos os componentes compartilham a mesma API e tokens (tema por variáveis CSS).
- **Custo zero de licença** e sem peso de uma biblioteca fechada.
- **Bom para IA:** o código é aberto e legível, então LLMs (Cursor, v0) leem e modificam com facilidade.

## Quando usar

- Produto com identidade visual própria que não pode parecer "Material" ou "Bootstrap".
- Time que já usa React e Tailwind.
- Início de um design system interno, usando o registry para distribuir.
- Projeto gerado ou editado por IA.
- Apps com muitos componentes de interação: formulários, dialogs, menus, tabelas, comboboxes.

## Para que tipo de site

| Tipo de site/projeto | Encaixe | Por quê |
|---|---|---|
| Landing page / site de marketing | 🟡 Serve | Cobre botões e formulários, mas não traz seções visuais nem animações; combine com Magic UI ou Aceternity |
| Site institucional | 🟡 Serve | Funciona se já houver React; para conteúdo estático é mais peso que o necessário |
| Portfólio | 🟡 Serve | Bom se o dev quer controle total; pouco ganho em páginas simples |
| Blog/conteúdo | ❌ Evite | Pouca interação; React e Tailwind pesam mais que HTML simples ou um CMS |
| E-commerce | 🟡 Serve | Ótimo para carrinho, filtros e checkout; vitrine pede design próprio |
| SaaS / app web | ✅ Ótimo | Muita interação, acessibilidade e identidade própria: o caso central |
| Dashboard / painel admin | ✅ Ótimo | Tabelas, formulários, gráficos, sidebar e blocos prontos |
| MVP / protótipo | ✅ Ótimo | Sobe rápido com visual decente e dá para evoluir sem trocar de base |
| Sistema interno corporativo | ✅ Ótimo | Formulários densos e acessíveis; time controla a manutenção |
| App mobile | ❌ Evite | É React para web; não gera UI nativa (React Native exige outra solução) |

## Quando é bom

- **Customização total:** o código é seu, então não existe teto de personalização.
- **Sem lock-in de versão:** nenhuma atualização quebra seu app sem você aceitar.
- **Só entra o que você usa:** cada componente adicionado é um arquivo, sem carregar a biblioteca inteira.
- **Padrão de mercado:** muita gente conhece, há muitos blocos, templates e registries de terceiros.
- **Funciona em vários frameworks:** Next.js, Vite, React Router, Astro, TanStack Start e Laravel têm guias oficiais.
- **Tema simples:** cores e raios mudam por variáveis CSS, e o criador visual (shadcn/create) gera o setup.

## Quando é ruim

- **Manutenção é sua:** correção de bug upstream exige copiar de novo (perdendo edições) ou comparar na mão.
- **Escala corporativa:** com vários times, cada projeto pode divergir e virar um UI kit próprio para manter. Mitigação: registry interno.
- **Dependência da base headless:** críticas citam ritmo lento de manutenção do Radix e bugs (ex.: erro de "update depth"). A migração para outras bases reduz o risco, mas o cenário não é consistente entre fontes.
- **Exige React e Tailwind:** quem não usa essa stack não aproveita; Vue, Svelte ou Angular dependem de portes não oficiais.
- **Componentes básicos:** alguns devs acham a profundidade limitada (data grid avançado, calendário complexo, editor rich text) e precisam de libs extras.
- **Curva para não devs:** designers não editam; mudar algo é mexer em código.
- **Visual "shadcn" genérico:** sem personalização, muitos produtos ficam parecidos.
- **Sem suporte comercial:** só comunidade e GitHub; não há SLA.

## Como começar

Projeto novo (comando da documentação oficial):

```bash
pnpm dlx shadcn@latest init -t next
```

Templates aceitos: `next`, `vite`, `start`, `react-router`, `astro`. Em Laravel, rode `laravel new` e depois `npx shadcn@latest init`.

Para adicionar um componente (sintaxe da CLI conferida em ui.shadcn.com em 2026-11-24):

```bash
npx shadcn@latest add button
```

Alternativa visual: montar um preset em shadcn/create e copiar o comando gerado. Ícones: o shadcn costuma usar [Lucide](05-lucide.md).

## Combina com / alternativas

- [Magic UI](02-magic-ui.md) e [Aceternity UI](03-aceternity-ui.md): efeitos e seções animadas para complementar.
- [Lucide](05-lucide.md): ícones.
- Alternativas de fora: Material UI (ou Mantine), Chakra UI / HeroUI, Radix Themes.

## Decisão rápida

- **Use se:** o projeto é React + Tailwind, precisa de identidade própria, acessibilidade e controle do código, e o time aceita manter os componentes.
- **Evite se:** o site é conteúdo estático, a stack não é React, o time quer atualizar tudo subindo uma versão de pacote, ou o destino é app nativo.
