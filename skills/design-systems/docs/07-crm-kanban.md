# CRM / gestão de tarefas em quadro

> Funil em colunas de etapas, com cartões que se movem da esquerda para a direita e um painel lateral para os detalhes, feito para ser operado rápido e com teclado.

| | |
|---|---|
| **Tipo de sistema** | CRM de vendas, gestão de tarefas e de projetos em quadro (kanban) |
| **Exemplo** | [07-crm-kanban.html](../examples/07-crm-kanban.html) (marca fictícia "Pipa CRM") |
| **Layout base** | Barra lateral estreita + cabeçalho com filtros + colunas de etapas + painel de detalhe à direita |
| **Referências reais** | Linear https://linear.app · Attio https://attio.com · Pipedrive https://www.pipedrive.com · Trello https://trello.com (exemplos de produtos do segmento; sites conferidos em 2026-11-24) |
| **Componentes** | shadcn/ui (Sheet para o painel, Tabs, Badge, Avatar, Command, Popover, Tooltip, Skeleton) e Lucide para os ícones. Fontes: ui.shadcn.com/docs/components e lucide.dev, conferidas em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

Uma tela em que cada coluna é uma etapa de um processo (prospecção, proposta, negociação, ganho) e cada cartão é um item de trabalho: um negócio, um cliente, uma tarefa. Mover o cartão de coluna é avançar o processo. Cada coluna mostra quantos cartões tem e o valor somado. Clicar no cartão abre um painel à direita com os dados completos, sem sair do quadro.

## Por que este layout

- No exemplo, cada coluna do quadro mostra no topo a contagem e a soma dos valores da etapa.
- O painel lateral mantém o contexto: o quadro continua visível atrás dele.
- A barra lateral estreita (só ícones) devolve largura às colunas.

## Quando usar

- Processo com etapas claras e ordem fixa (vendas, recrutamento, suporte de segundo nível).
- Equipe que atualiza o status várias vezes ao dia.
- Itens com poucos campos visíveis no cartão: responsável, valor, prazo, etiqueta.
- Quando a pergunta principal é "onde está travado?".

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| CRM de vendas B2B | ✅ Ótimo | O funil é o centro do trabalho |
| Recrutamento (vagas e candidatos) | ✅ Ótimo | Etapas fixas e muita movimentação |
| Gestão de tarefas / sprint | ✅ Ótimo | Etapas naturais: a fazer, fazendo, feito |
| Pós-venda / onboarding de clientes | ✅ Ótimo | Cada cliente passa por etapas |
| Suporte com muitas conversas | 🟡 Serve | Melhor uma caixa de entrada ([08](08-inbox-chat.md)); o quadro serve para escalonados |
| Cadastro grande de contatos (milhares) | 🟡 Serve | A visão de lista é a principal; o quadro filtra um recorte |
| Painel de indicadores | ❌ Evite | Use [02-dashboard-analytics.md](02-dashboard-analytics.md) |
| Dados sem etapas (cadastro, financeiro) | ❌ Evite | Sem fluxo, o quadro vira uma lista mal usada |

## Anatomia do layout

```
┌──┬──────────────────────────────────────────────────────────────┐
│  │ Funil de vendas  12 negócios · R$ 1.024.300  [Quadro|Lista]  [+ Novo] │  56 px
│■ ├──────────────────────────────────────────────────────────────┤
│○│ [Buscar /]  (Responsável) (Meus negócios) (Prazo) (Etiqueta) │  48 px
│▤ ├───────────┬───────────┬───────────┬───────────┬──────────────┤
│  │ ● Prospec.│ ● Qualif. │ ● Proposta│ ● Negoc.  │ ● Ganho      │
│  │ 3  R$173k │ 3  R$166k │ 2  R$241k │ 2  R$293k │ 2  R$152k    │
│  │ ┌───────┐ │ ┌───────┐ │ ┌───────┐ │ ┌───────┐ │              │
│  │ │cartão │ │ │cartão │ │ │cartão │ │ │cartão │ │ ──► painel   │
│  │ └───────┘ │ └───────┘ │ └───────┘ │ └───────┘ │    420 px    │
│  │ + Novo    │ + Novo    │           │           │              │
└──┴───────────┴───────────┴───────────┴───────────┴──────────────┘
```

- **Barra lateral:** 56 px de largura, ícones de 18 px em botões de 36 px. Marca no topo, tema e configurações embaixo.
- **Cabeçalho:** 56 px de altura. Título, resumo (negócios e valor total), alternância Quadro / Lista / Estados e botão primário com `<kbd>`.
- **Barra de filtros:** busca de 220 px mínimo (atalho `/`) e chips de filtro de 28 px de altura.
- **Colunas:** 280 px de largura, 12 px de espaço entre elas, raio de 12 px. O quadro rola na horizontal dentro do próprio contêiner; cada coluna rola na vertical.
- **Cartão:** largura total da coluna menos 16 px, padding de 12 px, 8 px entre as linhas. Empresa, descrição, etiqueta, e na base valor, prazo e avatar de 24 px.
- **Painel de detalhe:** 420 px à direita, sobre o quadro com um véu escuro. Fecha com `Esc`.
- **Tablet (até 1100 px):** o resumo some do cabeçalho; as colunas continuam em 280 px com rolagem horizontal.
- **Celular (até 720 px):** a barra lateral vira barra inferior de 56 px, cada coluna ocupa 84% da largura com encaixe na rolagem, e o painel abre em tela cheia. Rótulos e atalhos de teclado dos botões somem.

## Tokens do exemplo

| Token | Escuro (padrão) | Claro |
|---|---|---|
| Fundo / superfície / cartão | `#0b0d12` / `#11141b` / `#171b24` | `#f5f6f9` / `#ffffff` / `#f0f2f6` |
| Borda / borda forte | `#232936` / `#2f3747` | `#e1e5ec` / `#cdd3de` |
| Texto / suave / apagado | `#e7eaf0` / `#9aa3b5` / `#6f7a8f` | `#161a23` / `#555f73` / `#7b8599` |
| Marca (violeta discreto) | `#8b7cf6` | `#5b49d6` |
| Erro / atraso | `#f08a8a` | `#b3261e` |
| Etiquetas (fundo translúcido) | azul `#8ebdf7`, verde `#78d1a0`, âmbar `#e5b867`, violeta `#b7aafb`, verde-água `#6fd0cf` | mesmas famílias, texto escuro sobre fundo claro |
| Fonte | Inter, com pilha do sistema como alternativa (não é carregada de CDN) | igual |
| Escala de texto | 11 (etiqueta) · 12 (apoio) · 13 (base) · 15 (título) · 18 (painel) · 24 (valor) | igual |
| Raio | 4 px (etiqueta, kbd) · 8 px (cartão, botão) · 12 px (coluna) | igual |
| Sombra | só no painel: `0 12px 32px rgba(0,0,0,.5)` | `0 12px 32px rgba(20,28,50,.16)` |
| Espaçamento | escala de 4 / 8 px (4, 8, 12, 16, 24) | igual |

Números usam `font-variant-numeric: tabular-nums`, que o MDN descreve como figuras "todas do mesmo tamanho, para alinhar como em tabelas" (developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric, 2026-11-24).

## Componentes e padrões essenciais

- **Coluna** com nome, contagem, valor somado, botão de adicionar e "Novo negócio" no rodapé.
- **Cartão** clicável (é um `<button>`): empresa, descrição curta, etiqueta, valor, prazo, responsável. No exemplo, o prazo vencido só muda para vermelho; o WCAG 2.2, SC 1.4.1 (nível A) diz que a cor não pode ser o único meio visual de passar a informação (w3.org/WAI/WCAG22/Understanding/use-of-color.html, 2026-11-24). Em produção, acrescente texto ou ícone próprio ("Atrasado").
- **Arrastar e soltar** entre colunas, com alternativa sem arrastar: o WCAG 2.2, SC 2.5.7 (nível AA) exige que toda função de arraste possa ser feita com um único ponteiro sem arrastar (w3.org/WAI/WCAG22/Understanding/dragging-movements.html, 2026-11-24). O exemplo não implementa arraste nem movimento por teclado; só mostra a dica "← → mover etapa". Isso fica por sua conta.
- **Alternância Quadro / Lista**, com a mesma filtragem nas duas visões.
- **Filtros em chips** (responsável, etiqueta, prazo) e busca com atalho `/`.
- **Painel de detalhe**: propriedades, barra de etapas, atividade em ordem cronológica, nota, ações de avançar e perder.
- **Atalhos em `<kbd>`**: `N` novo, `/` buscar, `Esc` fechar. O exemplo mostra os três no botão e numa linha de dicas, mas só `/` e `Esc` funcionam.
- **Estado vazio** (coluna sem cartões): explica e oferece a ação de criar.
- **Estado carregando**: cartões em esqueleto no lugar dos reais, sem deslocar o layout.
- **Estado de erro**: mensagem clara, dizendo que os dados estão salvos, com botão "Tentar de novo".
- **Tema claro e escuro**, com foco visível (WCAG 2.2, SC 2.4.7) e contraste mínimo de 4,5:1 para texto normal (SC 1.4.3, nível AA).

## Quando é bom

- Mostra todas as etapas lado a lado, com contagem e valor somado em cada uma.
- O painel de detalhe abre sem tirar o quadro da tela.

## Quando é ruim

- **Só arrastar:** sem alternativa de um toque ou clique, não atende ao WCAG 2.2, SC 2.5.7 (AA).
- **Cor como único sinal:** etiquetas e prazos precisam de texto ou ícone também (WCAG 2.2, SC 1.4.1, nível A).
- **Valor sem formato:** o exemplo usa `R$ 84.000`, com separador de milhar e números tabulares (MDN, `font-variant-numeric`).
- **Rolagem horizontal da página:** no exemplo só o quadro rola, não a página. O WCAG 2.2, SC 1.4.10 (AA) pede conteúdo sem rolagem em duas direções a 320 px de largura, com exceção para o que exige layout bidimensional (w3.org/WAI/WCAG22/Understanding/reflow.html, 2026-11-24).

## Como começar

1. Abra [07-crm-kanban.html](../examples/07-crm-kanban.html) no navegador e teste o tema, a aba Lista, a aba Estados e o painel.
2. Copie o bloco `:root` de variáveis e o bloco do tema alternativo para o seu projeto.
3. Troque a marca: `--brand` e o nome, e ajuste as cinco cores de etiqueta ao seu vocabulário.
4. Monte com a skill `design`: Sheet (painel), Tabs (visões), Badge (etiquetas), Avatar, Command (busca e atalhos), Skeleton (carregando) e ícones Lucide.
5. Troque os dados fictícios pelos reais e ligue o arrastar (por exemplo, dnd kit, que lista teclado entre os métodos de entrada que suporta: dndkit.com, 2026-11-24) e acrescente um jeito de mover sem arrastar.

## Combina com / alternativas

- [01-fundamentos.md](01-fundamentos.md): tokens, escala de espaço e contraste.
- [03-admin-crud.md](03-admin-crud.md): para a visão de lista com filtros e edição em massa.
- [08-inbox-chat.md](08-inbox-chat.md): quando o trabalho é conversar com o cliente.
- [02-dashboard-analytics.md](02-dashboard-analytics.md): para relatórios de funil e previsão.
- [10-agendamento.md](10-agendamento.md): quando o prazo é um horário marcado.

## Decisão rápida

**Use se:** o trabalho passa por etapas em ordem, a equipe atualiza o status com frequência e você quer ver o funil e os valores por etapa de uma vez.

**Evite se:** não há etapas, os itens têm dezenas de campos para comparar (prefira tabela) ou o público é leigo e ocasional (prefira um fluxo guiado).
