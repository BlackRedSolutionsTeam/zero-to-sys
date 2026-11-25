# Agendamento (clínica, salão, consultório)

> Agenda semanal em grade, com eventos coloridos por profissional, e um fluxo curto de marcar horário, tanto para a equipe quanto para o cliente.

| | |
|---|---|
| **Tipo de sistema** | Agenda de atendimentos para clínica, salão, estúdio ou consultório |
| **Exemplo** | [10-agendamento.html](../examples/10-agendamento.html) (marca fictícia "Estúdio Lírio") |
| **Layout base** | Lateral esquerda (mini calendário, filtros, próximos) + grade semanal; novo agendamento em painel lateral; página pública centrada para o cliente |
| **Referências reais** | Cal.com https://cal.com · Calendly https://calendly.com · Fresha https://www.fresha.com · Square Appointments https://squareup.com/appointments · Acuity Scheduling https://www.acuityscheduling.com (páginas abertas em 2026-11-24; cada uma se descreve como software ou app de agendamento e reservas; no Fresha, reserva de salões e spas) |
| **Componentes** | Da skill design: shadcn/ui (Calendar, Sheet, Checkbox, Button, Input, Tabs, Skeleton; ui.shadcn.com/docs/components, 2026-11-24), Lucide (ícones; lucide.dev) |
| **Verificado em** | 2026-11-24 |

## O que é

É o sistema onde a equipe vê quem atende quem e a que horas, e onde o cliente marca sozinho o seu horário. A equipe trabalha na grade da semana. O cliente usa uma página pública simples, em quatro passos: serviço, profissional, horário e confirmação.

## Por que este layout

- **Grade de horas x dias:** o exemplo mostra a semana numa grade, com linha de 56 px por hora.
- **Cor por profissional**, com filtro por caixa de seleção.
- **Mini calendário na lateral** do exemplo.
- **Painel lateral** para criar o agendamento, com a agenda visível ao fundo.
- **Página do cliente** separada e centrada, sem os controles da equipe.
- **Tons pastel e cantos redondos** são a escolha visual do exemplo; troque pela marca do negócio.

## Quando usar

- Clínicas, consultórios, salões, barbearias, estúdios de estética e de bem-estar.
- Qualquer negócio com horário marcado e mais de um profissional ou recurso.
- Quando o cliente deve poder marcar sem ligar ou mandar mensagem.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Clínica ou consultório | ✅ Ótimo | Vários profissionais, retornos e serviços com duração diferente |
| Salão, barbearia, estúdio | ✅ Ótimo | A cor por profissional e a página pública resolvem o dia a dia |
| Aulas e coaching individual | 🟡 Serve | Funciona, mas um link simples de marcação pode bastar |
| Reserva de salas e recursos | 🟡 Serve | Troque profissional por sala; a grade é a mesma |
| Eventos com ingresso | ❌ Evite | Não há grade de horário por pessoa; use o padrão de e-commerce |
| Pipeline de vendas | ❌ Evite | Use o [CRM em kanban](07-crm-kanban.md) |

## Anatomia do layout

```
┌─────────────────────────────────────────────────────────┐
│ Logo  [Agenda|Visão do cliente]          ◐  [+ Novo ag.] │ 69 px
├───────────┬─────────────────────────────────────────────┤
│ Mini cal. │ 23 a 28 de nov. 2026        [Hoje] ‹ ›       │
│ ───────── │      Seg  Ter  Qua  Qui  Sex  Sáb            │
│ Profiss.  │ 08:00 ┌────┬────┬────┬────┬────┬────┐         │
│ ☑ Helena  │ 09:00 │ ev │ ev │    │ ev │    │ ev │         │
│ ☑ Camila  │ 10:00 │    │ ev │ ev │    │ ev │ ev │ ← agora │
│ ───────── │ ...   └────┴────┴────┴────┴────┴────┘         │
│ Próximos  │                                             │
└───────────┴─────────────────────────────────────────────┘
        Painel lateral (440 px): serviço > profissional > horário > confirmação
```

- **Cabeçalho:** cerca de 69 px (botões de 44 px, 12 px de respiro acima e abaixo, 1 px de borda); abas segmentadas (Agenda, Visão do cliente) e o botão primário "Novo agendamento".
- **Lateral:** 272 px, três blocos com cantos de 24 px e espaço de 24 px entre eles (mini calendário, profissionais e próximos).
- **Grade:** coluna de horas de 56 px e seis colunas de dia iguais; linha de horário de 56 px por hora (08:00 às 19:00); rolagem interna de até 640 px de altura.
- **Eventos:** posicionados por hora de início e duração, com margem de 3 px, raio de 12 px, barra de 4 px na cor forte e fundo pastel. Linha vermelha marca o horário atual.
- **Painel de novo agendamento:** 440 px, com barra de quatro passos, rodapé fixo com Voltar e Continuar; fecha com Esc e devolve o foco ao botão que o abriu.
- **Página do cliente:** coluna única de até 560 px, centrada, com dias em faixa rolável e horários em grade de três colunas.
- **Tablet (até 1100 px):** a lateral passa para cima da grade, em blocos lado a lado.
- **Celular (até 720 px):** a grade vira visão de um dia, com seletor de dias no topo; a lateral desce para baixo da agenda; o painel perde os cantos arredondados e ocupa a tela toda quando a janela tem até 440 px de largura (`width: min(440px, 100%)`).

## Tokens do exemplo

| Token | Claro | Escuro |
|---|---|---|
| Fundo (neutro quente) | `#faf7f4` | `#17141b` |
| Superfície / borda | `#ffffff` / `#e6ded6` | `#201c26` / `#383140` |
| Texto / texto suave | `#2b2630` / `#675f6c` | `#f1edf4` / `#b0a8b7` |
| Marca (azul-lavanda) | `#5b52b8` | `#a9a2f2` |
| Pastéis de evento | `#dcd9f7` `#f9d9e3` `#d4ebe0` `#fbe6c4` | `#3a3665` `#5a2f43` `#27483a` `#5a4420` |
| Barra do evento | `#5b52b8` `#c2457a` `#2f8a62` `#b9791a` | `#a9a2f2` `#f08ab4` `#6fd0a0` `#f0bd6a` |
| Agora / foco | `#d6455d` / `#1a73e8` | `#ff7f93` / `#7ab2ff` |

| Item | Valor |
|---|---|
| Fonte | Nunito Sans, com `system-ui` de reserva (o exemplo não carrega a fonte: ela só aparece se estiver instalada); algarismos tabulares nas horas (`font-variant-numeric: tabular-nums`, MDN) |
| Escala | 11 / 12 (evento) / 13 / 15 (corpo) / 18 / 20 (título da semana) / 28 (título público) |
| Raios | 10 px (campos), 16 px (opções), 24 px (cards), 99 px (botões e horários) |
| Sombra | `0 2px 6px` + `0 10px 30px`, de 5 a 7% de opacidade |
| Espaçamento | escala 4, 8, 12, 16, 24, 32, 48 px; linha de horário de 56 px |

## Componentes e padrões essenciais

- **Grade semanal** com cabeçalho de dias (dia de hoje em destaque) e linha do horário atual.
- **Evento:** nome do cliente, serviço e hora; a cor identifica o profissional e nunca é a única informação (WCAG 1.4.1, w3.org/WAI/WCAG22/Understanding/use-of-color).
- **Mini calendário** com dia selecionado e dias de outros meses esmaecidos.
- **Filtros por profissional** com caixa de seleção e bolinha da cor.
- **Próximos atendimentos** em lista curta, com hora, cliente e serviço.
- **Fluxo de novo agendamento** em quatro passos com barra de progresso e resumo final.
- **Horários indisponíveis** riscados e desabilitados (`text-decoration: line-through` e `disabled` no exemplo).
- **Página pública do cliente:** serviço, dia, horário, nome e WhatsApp, com a regra de cancelamento visível.
- **Estado vazio:** dia sem atendimentos com explicação e botão de novo agendamento.
- **Carregando:** esqueletos no lugar dos eventos. O estado de erro não está no exemplo.
- **Foco visível** e teclado no painel: Esc fecha e o foco volta ao elemento que abriu (padrão de diálogo modal, w3.org/WAI/ARIA/apg/patterns/dialog-modal, 2026-11-24).

## Quando é bom

- O exemplo tem duas vistas: o painel da equipe e a página pública do cliente (`examples/10-agendamento.html`).

## Quando é ruim

- Equipes grandes: a grade única, com uma cor por profissional, fica apertada. O exemplo não cobre esse caso.
- Eventos muito curtos: a linha de 56 px por hora do exemplo não os comporta.
- Erros comuns desse tipo de tela:
  - Eventos com texto sem contraste suficiente sobre a cor do profissional: o mínimo é 4,5:1 para texto normal (WCAG 1.4.3, w3.org/WAI/WCAG22/Understanding/contrast-minimum).
  - Grade de semana no celular com sete colunas minúsculas: o conteúdo deve se reorganizar sem rolagem em duas dimensões a 320 px (WCAG 1.4.10, w3.org/WAI/WCAG22/Understanding/reflow).
  - Painel que não fecha com Esc ou que perde o foco ao fechar (padrão de diálogo modal, APG).

## Como começar

1. Abra [10-agendamento.html](../examples/10-agendamento.html), alterne as três abas (Agenda, Visão do cliente, Dia sem horários) e abra "Novo agendamento".
2. Copie os tokens do `:root` e do tema escuro; mantenha a regra "pastel + texto escuro" ao trocar as cores.
3. Troque `--brand` e o nome "Estúdio Lírio" pela marca, e as cores `--p1..p4` pelos profissionais.
4. Monte com a skill design: Calendar, Sheet, Checkbox, Button e Skeleton do shadcn/ui e ícones Lucide.
5. No celular, mostre um dia por vez; nunca deixe a semana inteira em colunas espremidas.

## Combina com / alternativas

- [01-fundamentos.md](01-fundamentos.md): escalas de cor, raio e espaçamento.
- [03-admin-crud.md](03-admin-crud.md): cadastro de clientes, serviços e profissionais.
- [07-crm-kanban.md](07-crm-kanban.md): para acompanhar leads antes de virarem clientes.
- [08-inbox-chat.md](08-inbox-chat.md): confirmações e conversas por WhatsApp.
- [09-financeiro.md](09-financeiro.md): cobrança e recebimento dos atendimentos.
- [12-app-mobile.md](12-app-mobile.md): versão de app para o cliente.

## Decisão rápida

- **Use se:** há horário marcado, vários profissionais e o cliente deve poder marcar sozinho.
- **Evite se:** o negócio é de fluxo livre, sem hora marcada, ou de venda de ingressos.

_Referências: apenas a resposta dos sites (HTTP 200) foi conferida. A qualidade de design de cada produto vem do conhecimento geral e não foi reavaliada nas páginas._
