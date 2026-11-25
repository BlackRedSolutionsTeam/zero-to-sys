# Financeiro / conta digital para empresas

> Tela de confiança para quem lida com dinheiro: saldo grande no topo, entradas e saídas claras e ações de pagar, transferir e cobrar sempre à mão.

| | |
|---|---|
| **Tipo de sistema** | Conta digital PJ, painel financeiro, controle de caixa |
| **Exemplo** | [09-financeiro.html](../examples/09-financeiro.html) (marca fictícia "Cedro Conta PJ") |
| **Layout base** | Navegação no topo + conteúdo centrado de 1120 px; no celular a navegação vai para uma barra fixa embaixo |
| **Referências reais** | Mercury https://mercury.com · Brex https://brex.com · Wise Business https://wise.com/business · Stripe Dashboard https://stripe.com/dashboard · Cora https://www.cora.com.br (os cinco URLs responderam HTTP 200 em 2026-11-24) |
| **Componentes** | Da skill design: shadcn/ui (Card, Tabs, Button, Input, Dialog, Skeleton, Badge), Lucide (ícones), Recharts ou SVG puro para o gráfico. Fontes: ui.shadcn.com/docs/components, lucide.dev e recharts.github.io ("biblioteca de gráficos composável feita com componentes React"), conferidas em 2026-11-24 |
| **Verificado em** | 2026-11-24 |

## O que é

É a tela inicial de uma conta bancária ou de um painel de finanças para empresas. Mostra quanto há disponível, o que entrou e saiu no período, os cartões e as últimas movimentações. Tudo o que o dono do negócio faz todo dia (pagar um boleto, fazer um Pix, emitir uma cobrança) fica a um clique.

## Por que este layout

- **Navegação no topo:** no exemplo, a largura toda do conteúdo fica para valores e listas, sem menu lateral.
- **Conteúdo centrado** com máximo de 1120 px.
- **Saldo em destaque:** fonte fluida de 36 a 56 px, no topo da tela.
- **Espaço em branco** generoso entre os blocos (grade de 24 px).
- **Fundo levemente esverdeado e verde-escuro de marca:** é a direção visual da marca fictícia Cedro.

## Quando usar

- Conta digital, carteira ou banco para pessoa jurídica.
- Painel de fluxo de caixa de um ERP ou de um app de gestão para pequenas empresas.
- Área financeira de um marketplace (repasses, recebíveis, extrato).
- Qualquer tela em que o valor e o sinal (entrada ou saída) não podem gerar dúvida.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Conta digital / fintech PJ | ✅ Ótimo | É o caso central |
| Gestão financeira de pequena empresa | ✅ Ótimo | Saldo, fluxo de caixa e extrato resolvem o dia a dia |
| Marketplace com repasses | ✅ Ótimo | Extrato e recebíveis seguem o mesmo padrão |
| Painel de métricas de produto (uso, retenção) | 🟡 Serve | Prefira o [dashboard analytics](02-dashboard-analytics.md), mais denso |
| Contabilidade com muitos lançamentos | 🟡 Serve | Funciona na visão geral, mas o extrato pede tabela densa |
| E-commerce (vitrine) | ❌ Evite | Foco é vender, não mostrar saldo |
| App de mensagens ou chat | ❌ Evite | Padrão de leitura completamente diferente |

## Anatomia do layout

```
┌──────────────────────────────────────────────────────────┐
│ Logo  Início Extrato Cartões Pagamentos Relatórios  ◐ 🔔 BG │ 64 px
├──────────────────────────────────────────────────────────┤
│        [ Visão geral | Carregando | Sem movimentações ]  │
│  Saldo disponível · Empresa          [Pagar][Transf.][Cobrar]
│  R$ 48.236,90                                            │
│ ┌─────────────────────────────┐ ┌──────────────────────┐ │
│ │ Fluxo de caixa (barras)     │ │ Cartão + fatura      │ │
│ │ Entradas | Saídas do mês    │ │ limite usado         │ │
│ └─────────────────────────────┘ └──────────────────────┘ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Últimas movimentações        [buscar]                 │ │
│ │ Hoje ........................ saldo do dia            │ │
│ │ (ícone) Nome · categoria · hora          + R$ 3.450   │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

- **Cabeçalho:** 64 px, fixo no topo, borda de 1 px. Links com 40 px de altura.
- **Conteúdo:** largura máxima de 1120 px, centrado, padding lateral de 24 px.
- **Grade:** 12 colunas com espaço de 24 px. Gráfico em 8 colunas, cartões em 4, lista em 12.
- **Saldo:** fonte fluida de 36 a 56 px (`clamp(36px, 7vw, 56px)`), negrito, tabular.
- **Linha de transação:** 40 px de ícone, cerca de 66 px de altura (calculado: 12 px de padding em cima e embaixo, nome de 15 px e linha de apoio de 13 px, com entrelinha de 1,5), padding vertical de 12 px.
- **Tablet (até 900 px):** a grade vira uma coluna, os nomes dos links do topo somem e ficam só os ícones.
- **Celular (até 640 px):** a navegação vira barra fixa embaixo (52 px); as ações ocupam a largura toda em três botões iguais; o padding lateral cai para 16 px.

## Tokens do exemplo

| Token | Claro | Escuro |
|---|---|---|
| Fundo | `#f3f6f4` | `#0c1511` |
| Superfície / borda | `#ffffff` / `#d9e2dc` | `#131e18` / `#26372d` |
| Texto / texto suave | `#14231c` / `#4f6258` | `#e8f0eb` / `#9db0a4` |
| Marca (verde-escuro) | `#0f4a36` | `#5fc995` |
| Entrada / saída | `#0b6b3a` / `#9b2c2c` | `#6fd69b` / `#ff9a94` |
| Aviso (agendado) | `#8a5a00` sobre `#fbefd2` | `#f0c46a` sobre `#3a2e12` |
| Foco | `#1a73e8` | `#7ab2ff` |

| Item | Valor |
|---|---|
| Fonte | Inter, com `system-ui` de reserva; `font-variant-numeric: tabular-nums` em todos os números |
| Escala | 12 / 13 / 15 (corpo) / 18 / 24 (KPI) / 36 a 56 (saldo, responsivo) |
| Raios | 6 px (botões), 12 px (blocos internos), 16 px (cards) |
| Sombra | claro: `0 1px 2px` + `0 4px 16px`, de 5 a 6% de opacidade; escuro: só `0 1px 2px` a 40% |
| Espaçamento | escala 4, 8, 12, 16, 24, 32, 48 px |

## Componentes e padrões essenciais

- **Saldo em destaque** com moeda menor e a data da última atualização.
- **Ações rápidas** (Pagar é a primária; Transferir e Cobrar são secundárias).
- **Cartões de KPI** de entradas e saídas no período, com ícone de seta e sinal no texto.
- **Gráfico de fluxo de caixa** com legenda e `aria-label` que descreve os valores. O WCAG 2.2, SC 1.1.1 (nível A) pede texto alternativo equivalente e, para gráficos, uma descrição longa; o ideal é oferecer os dados também em tabela (w3.org/WAI/WCAG22/Understanding/non-text-content.html, 2026-11-24).
- **Cartão da conta** com final do número, fatura, barra de limite e estado (desbloqueado, bloqueado).
- **Lista de transações agrupada por dia**, com o saldo do dia no cabeçalho do grupo, ícone, nome, categoria, hora e valor.
- **Entrada x saída sem depender só de cor** (WCAG 2.2, SC 1.4.1, nível A: w3.org/WAI/WCAG22/Understanding/use-of-color.html, 2026-11-24): sinal `+` e `−` no valor, seta ou ícone diferente e a palavra "Entrada" ou "Saída" embaixo do valor.
- **Status** em etiqueta. O exemplo mostra só "Agendado"; Pendente e Falhou são sugestões.
- **Estado carregando:** esqueleto no lugar do saldo, do gráfico e das linhas, sem mostrar R$ 0,00.
- **Estado vazio:** saldo zerado, explicação curta e dois botões (gerar cobrança, copiar chave Pix).
- **Estado de erro:** faixa vermelha com ícone, texto claro e botão "Tentar de novo"; avisar que os valores podem estar desatualizados.
- **Tema escuro** e foco visível em tudo que é clicável (WCAG 2.2, SC 2.4.7, nível AA).

## Quando é bom

- Valores alinhados à direita e com algarismos tabulares: o MDN descreve `tabular-nums` como figuras "todas do mesmo tamanho, para alinhar como em tabelas" (developer.mozilla.org/en-US/docs/Web/CSS/font-variant-numeric, 2026-11-24).
- Saldo, entradas, saídas, cartão e últimas movimentações aparecem na mesma tela.

## Quando é ruim

- Erros que as diretrizes oficiais apontam:
  - Mostrar entrada e saída só por verde e vermelho (WCAG 2.2, SC 1.4.1).
  - Gráfico sem texto alternativo (WCAG 2.2, SC 1.1.1).
  - Transação financeira sem uma destas três garantias: envio reversível, dados checados com chance de corrigir, ou etapa de revisão e confirmação antes de finalizar (WCAG 2.2, SC 3.3.4, nível AA: w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html, 2026-11-24). O exemplo não tem essa etapa.
  - Fonte sem algarismos tabulares: as colunas de valores desalinham (MDN, `font-variant-numeric`).

## Como começar

1. Abra [09-financeiro.html](../examples/09-financeiro.html) no navegador e alterne o tema e as abas (visão geral, carregando, sem movimentações).
2. Copie o bloco `:root` e o de tema escuro para o seu CSS.
3. Troque `--brand` pela cor da sua marca (mantenha tom escuro e contraste mínimo de 4,5:1 com o texto branco, WCAG 2.2, SC 1.4.3; no exemplo, `#0f4a36` com branco dá cerca de 10:1) e o nome "Cedro" pelo da sua empresa.
4. Monte com a skill design: Card, Tabs, Button, Input e Skeleton do shadcn/ui, ícones Lucide e o gráfico em Recharts ou SVG.
5. Mantenha as regras: números tabulares, sinal nos valores e esqueleto no carregamento. Acrescente você a etapa de confirmação antes de mover dinheiro (WCAG 2.2, SC 3.3.4).

## Combina com / alternativas

- [01-fundamentos.md](01-fundamentos.md): escalas de cor, tipografia e espaçamento usadas aqui.
- [02-dashboard-analytics.md](02-dashboard-analytics.md): quando o foco é análise e não saldo.
- [03-admin-crud.md](03-admin-crud.md): para o extrato completo com tabela, filtros e exportação.
- [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md): login seguro, verificação e limites da conta.
- [12-app-mobile.md](12-app-mobile.md): versão de app da mesma conta.

## Decisão rápida

- **Use se:** o usuário precisa ver saldo, entradas e saídas e agir rápido sobre o dinheiro.
- **Evite se:** o trabalho principal é conciliar muitos lançamentos ou analisar métricas de produto (ver 02 e 03).

_Referências: apenas a resposta dos sites (HTTP 200, 2026-11-24) foi conferida. A qualidade de design de cada produto vem do conhecimento geral e não foi reavaliada nas páginas._
