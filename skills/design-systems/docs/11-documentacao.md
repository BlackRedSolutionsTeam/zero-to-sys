# Documentação / central de ajuda

> Site de leitura com três colunas (navegação, texto, índice da página) e busca sempre à mão: o leitor chega com uma pergunta e precisa achar a resposta em segundos.

| | |
|---|---|
| **Tipo de sistema** | Site de documentação (guias, referência de API, central de ajuda) |
| **Exemplo** | [`../examples/11-documentacao.html`](../examples/11-documentacao.html) (marca fictícia: Sinal, API de envio de mensagens) |
| **Layout base** | Três colunas: navegação em árvore, conteúdo com largura de leitura, índice "nesta página" |
| **Referências reais** | Stripe Docs https://stripe.com/docs · Vercel Docs https://vercel.com/docs · GitHub Docs https://docs.github.com · MDN Web Docs https://developer.mozilla.org · Cloudflare Developers https://developers.cloudflare.com (exemplos de produtos do segmento; páginas abertas em 2026-11-24: cada uma é o portal de documentação da empresa ou, no caso do MDN, de tecnologias web) |
| **Componentes** | Da skill design: shadcn/ui (Command para a busca, Sheet para a gaveta de navegação, Tabs, Table, Collapsible, Alert para callouts, Breadcrumb; ui.shadcn.com/docs/components, 2026-11-24) e Lucide (ícones; lucide.dev). Código com Shiki (shiki.style) ou highlight.js (highlightjs.org) |
| **Verificado em** | 2026-11-24 |

## O que é

É o site onde o produto se explica: começo rápido, guias por tarefa, referência de API, perguntas frequentes. Quem lê quase sempre está no meio de outra tarefa (integrando, resolvendo um erro). Por isso a tela é uma ferramenta de consulta, não uma página de marketing.

## Por que este layout

- **Navegação à esquerda:** o exemplo tem três colunas (navegação, conteúdo e índice).
- **Coluna de texto estreita** (até 80 caracteres por linha; WCAG 1.4.8, w3.org/WAI/WCAG22/Understanding/visual-presentation) deixa espaço para código e tabelas.
- **Índice à direita**, que lista os títulos H2 e H3 da página.
- **Busca no cabeçalho** com atalho Ctrl K ou Cmd K.
- **Anterior / próximo** no fim da página.

## Quando usar

- Documentação de API, SDK, biblioteca ou design system.
- Central de ajuda com dezenas de artigos organizados por tema.
- Manual de produto, base de conhecimento interna, guia de onboarding técnico.
- Qualquer conteúdo longo que o leitor consulta em vez de ler de uma vez.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / SDK / produto para devs | ✅ Ótimo | Código, tabelas de parâmetros e referência exigem exatamente esta estrutura |
| Design system | ✅ Ótimo | Muitas páginas de componente com navegação por categoria |
| Central de ajuda para clientes | ✅ Ótimo | Busca forte e artigos curtos; a árvore pode ser mais rasa |
| Base de conhecimento interna | ✅ Ótimo | Muito conteúdo, vários autores, necessidade de busca |
| Blog técnico | 🟡 Serve | Use só a coluna de texto e o índice; a árvore lateral sobra |
| Landing page de produto | ❌ Evite | O objetivo é converter, não consultar; veja `05-landing-saas.md` |
| Painel de dados | ❌ Evite | Pede densidade e gráficos; veja `02-dashboard-analytics.md` |
| App mobile | ❌ Evite | Ajuda dentro do app é outra coisa: um bottom sheet ou tela simples (`12-app-mobile.md`) |

## Anatomia do layout

```
┌────────────────────────────────────────────────────────────────────┐
│ Logo  Guias  Referência  SDKs        [ Buscar…  Ctrl K ]  ☾        │ 56
├───────────┬──────────────────────────────────────────┬─────────────┤
│ PRIMEIROS │ Guias › Primeiros passos                 │ NESTA PÁGINA│
│  Intro    │ # Título                                 │ ▌Antes      │
│ ▌Atual    │ Texto de abertura                        │  Passos     │
│  Chaves   │ ## Seção                                 │  Parâmetros │
│ ENVIANDO  │ [código ........................ Copiar] │  Status     │
│  ▸ Canais │ ┌ Aviso ──────────────────────────┐      │             │
│           │ Tabela · Passos 1 2 3                    │             │
│  268 px   │ [← Anterior]            [Próximo →]      │   216 px    │
└───────────┴──────────────────────────────────────────┴─────────────┘
```

- **Cabeçalho:** 56 px, fixo no topo. Logo, abas de seção, busca (40 px de altura mínima, 300 px de largura) e botão de tema.
- **Navegação lateral:** 268 px, fixa, com rolagem própria. Grupos com título em caixa alta de 12 px; itens de 32 px de altura; subníveis recuados 17 px com linha guia. Item atual com fundo azul suave.
- **Conteúdo:** largura máxima de 720 px (`--read`), centralizada, com 56 px de respiro nas laterais. Corpo 16 px / 1,7. Títulos H2 com 48 px acima e 12 px abaixo.
- **Índice:** 216 px, fixo, com marca azul no item da seção visível. Mostra só H2 e H3.
- **Código:** 13,5 px mono, cabeçalho de 40 px com nome do arquivo ou abas de linguagem e botão Copiar. Rola na horizontal dentro do bloco.
- **Tablet (até 1180 px):** o índice some; navegação e conteúdo continuam.
- **Celular (até 860 px):** a navegação vira gaveta aberta pelo botão de menu (largura de 300 px, com fundo escurecido); a busca vira ícone; margens de 16 px; tabelas e código rolam por dentro.

## Tokens do exemplo

| Token | Valor (claro / escuro) |
|---|---|
| Fundo / fundo secundário | `#ffffff` / `#f7f8fa` · `#0e1116` / `#151a22` |
| Texto / texto 2 / texto 3 | `#14161a` / `#444b57` / `#646c79` · `#eceff4` / `#b4bcc9` / `#8e98a8` |
| Marca (links, destaques) | `#1f4fd8`, hover `#173fae`, fundo suave `#eaf0fe` · `#7fa2ff`, suave `#17233f` |
| Borda | `#e6e8ec` · `#242b36` |
| Aviso | barra `#b97700`, fundo `#fff7e6` · `#e0a63a`, `#2a2210` |
| Código | fundo `#f5f6f8`; chave `#1f4fd8`, texto `#0b7a56`, comentário `#6b7480` |
| Fonte | Inter (texto); JetBrains Mono (código); ambas com pilha do sistema como reserva |
| Escala tipográfica | H1 40/46 · H2 26/34 · H3 19 · lead 19/30 · corpo 16/27 · código 13,5/23 · rótulo 12–14 |
| Raio | 4 px (kbd, código em linha), 8 px (blocos, tabelas, botões, campo de busca), 12 px (modal de busca) |
| Sombra | só no modal de busca e na gaveta: `0 12px 32px rgba(20,22,26,.16)` |
| Espaçamento | escala de 4/8: 8, 12, 16, 24, 32, 48, 56 |

## Componentes e padrões essenciais

- **Busca** com atalho `Ctrl K` / `⌘ K`, abre um modal com resultados agrupados por seção, navegação por setas e fechamento com `Esc`.
- **Navegação em árvore** com grupos recolhíveis, item atual marcado e `aria-current="page"` (MDN, aria-current).
- **Migalhas** acima do título e **metadados** (tempo de leitura, data de atualização, versão da API).
- **Títulos com âncora** (`#`) ao passar o mouse, para link direto.
- **Bloco de código** com botão copiar, abas por linguagem e realce de sintaxe com contraste AA (mínimo 4,5:1; WCAG 1.4.3).
- **Callouts** de dois tipos (info e aviso), com ícone, para não depender só da cor.
- **Tabela** de parâmetros com rolagem horizontal própria no celular.
- **Passos numerados** com linha de ligação.
- **Estados:** o exemplo mostra a busca sem resultado ("Nada encontrado para X"). Carregando, erro 404 e seção vazia não estão no exemplo.
- **Rodapé da página:** "Esta página ajudou?", link para editar e anterior/próximo.

## Quando é bom

- O exemplo tem busca com atalho e navegação anterior/próximo (`examples/11-documentacao.html`).

## Quando é ruim

- **Linha de texto larga demais:** passar de 80 caracteres foge do limite da WCAG 1.4.8.
- **Código sem copiar** ou com tema abaixo de 4,5:1 de contraste (WCAG 1.4.3).
- **Índice que não acompanha a rolagem**: o exemplo marca o item da seção visível e lista só H2 e H3.
- **Ignorar a preferência de tema do sistema:** o exemplo respeita `prefers-color-scheme` (MDN).

## Como começar

1. Abra [`../examples/11-documentacao.html`](../examples/11-documentacao.html) no navegador, redimensione a janela e alterne o tema.
2. Copie o bloco `:root` de variáveis para o seu projeto e troque `--brand` pela cor da sua marca (o azul `#1f4fd8` sobre branco tem contraste de 6,6:1; o mínimo para texto normal é 4,5:1, WCAG 1.4.3, w3.org/WAI/WCAG22/Understanding/contrast-minimum).
3. Troque a marca fictícia (Sinal) pelo nome, logotipo e seções reais.
4. Monte com a skill design: Command para a busca, Sheet para a gaveta, Alert para os callouts, Tabs para os blocos de código, Lucide para os ícones.
5. Gere as páginas a partir de Markdown (por exemplo com Docusaurus docusaurus.io, Nextra nextra.site, Astro Starlight starlight.astro.build ou Mintlify mintlify.com; sites no ar em 2026-11-24) em vez de escrever HTML à mão.
6. Teste em 320 px de largura: nenhuma rolagem horizontal da página (WCAG 1.4.10, w3.org/WAI/WCAG22/Understanding/reflow).

## Combina com / alternativas

- [`01-fundamentos.md`](01-fundamentos.md) para tipografia, grade e contraste.
- [`05-landing-saas.md`](05-landing-saas.md): a landing leva ao "Começar" da documentação.
- [`04-auth-onboarding-configuracoes.md`](04-auth-onboarding-configuracoes.md) para a tela de chaves de API citada nos guias.
- [`08-inbox-chat.md`](08-inbox-chat.md) se o suporte também for por chat.
- Alternativa para pouco conteúdo: uma única página longa com índice, sem árvore.

## Decisão rápida

- **Use se:** o conteúdo é de consulta, tem vários artigos e inclui código ou passos.
- **Evite se:** o objetivo é vender ou mostrar dados; ou se o conteúdo cabe em uma página só.
