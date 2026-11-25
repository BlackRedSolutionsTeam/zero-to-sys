# App mobile

> Telas de uso rápido com uma mão: abas na base, cabeçalho grande, cartões, listas com ações e uma folha inferior para tarefas curtas.

| | |
|---|---|
| **Tipo de sistema** | App mobile nativo ou multiplataforma (hábitos, treino, entregas, banco, saúde) |
| **Exemplo** | [`../examples/12-app-mobile.html`](../examples/12-app-mobile.html) (marca fictícia: Ritmo, app de hábitos; três telas num quadro de 390×844 px definido no próprio HTML, sem relação com a medida de um aparelho real) |
| **Layout base** | Coluna única: cabeçalho grande, conteúdo rolável, barra de abas inferior; botão de ação principal flutuante e folha inferior |
| **Referências reais** | Duolingo https://www.duolingo.com · Strava https://www.strava.com · Headspace https://www.headspace.com · Apple Fitness+ https://www.apple.com/br/apple-fitness-plus (exemplos de produtos do segmento; páginas abertas em 2026-11-24: Duolingo, app para aprender idiomas; Strava, app de corrida, ciclismo e caminhada; Headspace, app de meditação e sono; Apple Fitness+, serviço de atividades físicas da Apple) |
| **Componentes** | A skill design cobre só web. Para mobile use: SwiftUI (iOS), Jetpack Compose com Material 3 (Android), ou React Native / Flutter. Ícones: SF Symbols no iOS (developer.apple.com/design/human-interface-guidelines/sf-symbols), Material Symbols no Android, ou Lucide em apps multiplataforma. Em web mobile (PWA), shadcn/ui Drawer e Lucide servem para aproximar |
| **Verificado em** | 2026-11-24 |

## O que é

Um app usado em pé, no ônibus ou entre duas tarefas. Cada tela faz uma coisa, os controles ficam ao alcance do polegar e a ação mais frequente está sempre visível. O HTML do exemplo desenha o aparelho em CSS só para mostrar o resultado; num app de verdade a moldura não existe.

## Por que este layout

- **Abas na base** permitem trocar de seção preservando o estado de navegação de cada uma (Apple HIG, Tab bars, 2026-11-24); no Android, a barra de navegação serve a três a cinco destinos de mesma importância em janelas compactas (developer.android.com/develop/ui/compose/components/navigation-bar, 2026-11-24).
- **Cabeçalho grande:** o exemplo usa título de 32/37 px na tela inicial (tabela de tokens abaixo).
- **Cartões e linhas grandes** (o exemplo usa 44 px de toque, o tamanho padrão de controle no iOS segundo a Apple HIG, Accessibility, 2026-11-24).
- **Folha inferior:** no exemplo, o botão "Novo" abre uma folha sobre a tela, com fundo escurecido.
- **Botão principal:** o exemplo tem um botão flutuante de 56 px por tela.

## Quando usar

- Uso frequente e curto: marcar hábito, acompanhar entrega, ver saldo.
- Funções que dependem do aparelho: notificação, câmera, localização, sensores.
- Fluxos de poucos campos, com ações repetidas todos os dias.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Hábitos, treino, saúde | ✅ Ótimo | Uso diário, ações rápidas e progresso visual |
| Entregas, mobilidade, pedidos | ✅ Ótimo | Status em tempo real, mapa, notificações |
| Banco / carteira | ✅ Ótimo | Consulta rápida e confirmação por biometria; veja também `09-financeiro.md` |
| Rede social, mensagens | 🟡 Serve | Pede feed e conversas; veja `08-inbox-chat.md` |
| Painel administrativo | ❌ Evite | Tabelas densas e muitos filtros pedem tela grande: `03-admin-crud.md` |
| Documentação ou conteúdo longo | ❌ Evite | Leitura longa funciona melhor na web: `11-documentacao.md` |
| Landing page | ❌ Evite | É site, não app: `05-landing-saas.md` |

## Anatomia do layout

```
┌──────────────────────────┐
│ 9:41            ▂▄▆ ▭    │ área segura topo: 47 px (exemplo)
│ Terça, 24 nov        (🔔)│ barra de navegação: 48 px
│ Oi, Marina               │ título grande: 32/37
│ ┌──────────────────────┐ │
│ │ (3/5)  Quase lá      │ │ cartão destaque, raio 28
│ └──────────────────────┘ │
│ Hoje              Ver tudo│ título de seção 18
│ [ícone] Correr 20 min  (✓)│ linha 64 px, toque 44 px
│ [ícone] Beber água     (✓)│
│                 [+ Novo ]│ botão principal 56 px
├──────────────────────────┤
│  Hoje  Hábitos  Prog. Perfil│ abas: 56 px + 34 px área segura
└──────────────────────────┘
        390 × 844
```

- **Tela:** 390×844 px é o tamanho do quadro desenhado no HTML do exemplo (`.phone` em `examples/12-app-mobile.html`), não a medida de um aparelho. A página de dimensões da Apple (developer.apple.com/design/human-interface-guidelines/layout, aberta em 2026-11-24) carrega, mas o texto extraído não trouxe a tabela de dimensões por aparelho; por isso não afirmo que 390×844 é a tela de algum iPhone. Margens laterais de 20 px (também do exemplo).
- **Área segura:** os 47 px do topo e os 34 px da base vêm das variáveis `--safe-top` e `--safe-bottom` do `:root` do exemplo (`examples/12-app-mobile.html`); não foram lidos de aparelho nem conferidos na Apple. A Apple define a área segura como a região não coberta por hardware (como a Dynamic Island) nem por barras, e pede que o conteúdo a respeite (HIG, Layout, 2026-11-24). Em CSS real: `env(safe-area-inset-top)` e `env(safe-area-inset-bottom)` (MDN, env()).
- **Barra de abas:** 56 px de conteúdo mais a área segura; o exemplo tem 4 destinos; ícone de 24 px com rótulo de 11 px; item ativo na cor da marca.
- **Linhas de lista:** altura mínima de 64 px, ícone de 48 px, ação de 44×44 px, intervalo de 8 px entre cartões.
- **Botão principal:** 56 px de altura, raio total, 16 px acima da barra de abas.
- **Folha inferior:** raio de 32 px no topo, alça de 40×5 px, fundo escurecido a 45%. A Apple recomenda alça em folha redimensionável (HIG, Sheets, 2026-11-24).
- **Tablet (Android):** a barra de navegação inferior é indicada para janelas compactas, abaixo de 600 dp (developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes e .../components/navigation-bar, 2026-11-24). O exemplo não cobre tablet.
- **Telas estreitas:** o conteúdo deve se reorganizar sem rolagem em duas dimensões a 320 px (WCAG 1.4.10).

## Tokens do exemplo

| Token | Valor (claro / escuro) |
|---|---|
| Fundo / superfície / superfície 2 | `#f6f7fb` / `#ffffff` / `#eef0f7` · `#0f1117` / `#191c26` / `#222633` |
| Texto / texto 2 / texto 3 | `#11131a` / `#4b5163` / `#6a7186` · `#f2f4fa` / `#b9bfd0` / `#8f97ac` |
| Marca (azul-elétrico) | `#2b4bff`, pressionado `#1f39d1`, suave `#e6eaff` · `#7b92ff`, suave `#1d2550` |
| Sucesso / alerta | `#0f8a5f` / `#c2410c` · `#4fd6a0` / `#ff9b6b` |
| Fonte | Plus Jakarta Sans, com `ui-rounded` e a fonte do sistema como reserva |
| Escala tipográfica | título 32/37 · seção 18 · item 16 · apoio 13–14 · aba 11 |
| Raio | 12 (campos), 20 (cartões), 28 (cartão de destaque), 32 (folha), 999 (botões e chips) |
| Sombra | cartão `0 1px 2px rgba(17,19,26,.05)` + `0 6px 16px rgba(17,19,26,.06)`; folha `0 -8px 32px rgba(17,19,26,.18)` |
| Espaçamento | escala de 4/8: 8, 12, 16, 20, 24; alvo de toque do exemplo: 44 |

## Componentes e padrões essenciais

- **Barra de abas** com 3 a 5 destinos e estado ativo claro.
- **Cabeçalho grande** que encolhe ao rolar.
- **Cartão de resumo** com um número ou anel de progresso.
- **Lista com ação:** botão de concluir na linha; gestos de deslizar revelam editar e excluir, e deve existir caminho sem gesto de trajeto (WCAG 2.5.1, w3.org/WAI/WCAG22/Understanding/pointer-gestures).
- **Botão de ação principal** único por tela.
- **Folha inferior** para criar e editar, com alça, botão fechar e foco no primeiro campo.
- **Estados:** o exemplo mostra o carregamento com esqueleto das linhas. Vazio, erro e sem conexão não estão no exemplo.
- **Feedback tátil:** a Apple prevê háptico de sucesso para indicar que uma ação terminou (HIG, Playing haptics, 2026-11-24). O exemplo não vibra.
- **Acessibilidade:** texto que cresce com o tamanho de fonte do sistema (Dynamic Type no iOS, Apple HIG, Accessibility), rótulos para leitor de tela, contraste mínimo de 4,5:1 (WCAG 1.4.3).

## Quando é bom

- O exemplo tem alvos de toque de 44 px, o tamanho padrão de controle no iOS (Apple HIG, Accessibility, 2026-11-24).
- O exemplo tem tema claro e escuro, com botão para alternar.

## Quando é ruim

- **Alvos pequenos:** abaixo de 44x44 pt no iOS (padrão da Apple HIG, Accessibility; mínimo 28x28 pt) ou de 48x48 dp no Android (support.google.com/accessibility/android/answer/7101858), e ícones sem rótulo.
- **Conteúdo atrás da barra de abas ou do indicador de início** por ignorar a área segura.
- **Abas demais:** no iOS, quando falta espaço a última aba vira "Mais" e esconde o conteúdo (Apple HIG, Tab bars).
- **Ação só por gesto de trajeto**, sem alternativa (WCAG 2.5.1).
- **Cor como único sinal** de estado (concluído, erro): WCAG 1.4.1; Apple HIG, Accessibility.
- **Tema escuro sem checar contraste** ou texto que não respeita o tamanho de fonte do usuário (Apple HIG, Accessibility, 2026-11-24).

## O que muda entre iOS e Android

| Ponto | iOS | Android |
|---|---|---|
| Navegação principal | Barra de abas na base (Apple HIG, Tab bars) | Barra de navegação inferior, de 3 a 5 destinos, em janelas compactas (developer.android.com, Navigation bar) |
| Voltar | Botão Voltar padrão da barra de navegação (Apple HIG, Toolbars) | Gesto de voltar do sistema, com voltar preditivo (developer.android.com/guide/navigation/custom-back/predictive-back-gesture) |
| Barra superior | Título grande que vira título padrão ao rolar (Apple HIG, Toolbars) | Top app bar: pequena, centralizada, média ou grande (developer.android.com, App bars) |
| Ação principal | Botão na barra superior ou botão preenchido na tela (escolha do exemplo) | FAB, FAB pequeno, grande ou estendido (developer.android.com, Floating action button) |
| Fonte do sistema | San Francisco (SF Pro) com Dynamic Type (Apple HIG, Typography) | Fonte do sistema com a escala de fonte escolhida pelo usuário |
| Folhas e menus | Sheet com alça (grabber) e alturas fixas, os detents (Apple HIG, Sheets) | `ModalBottomSheet` (developer.android.com, Bottom sheets) |
| Ícones | SF Symbols | Material Symbols |

O exemplo usa a convenção iOS (abas, ilha, indicador de início) com cor e forma próprias. Para Android, troque a barra de abas pela navigation bar do Material 3 e o botão flutuante pelo FAB padrão.

**Diretrizes oficiais:** Apple Human Interface Guidelines https://developer.apple.com/design/human-interface-guidelines (200 em 2026-11-24) e Material Design 3 https://m3.material.io (200 em 2026-11-24). Siga os valores de alvo de toque e área segura que elas publicam; os números de área segura e raios deste documento são os do exemplo.

## Como começar

1. Abra [`../examples/12-app-mobile.html`](../examples/12-app-mobile.html), alterne o tema e toque em "Novo" para ver a folha.
2. Copie os tokens do `:root` (cores, raios, sombras) para o tema do seu app; no SwiftUI ou no Compose, transforme-os em cores e formas do tema.
3. Troque a marca fictícia (Ritmo) pela sua e escolha uma cor de marca com contraste AA sobre o texto que vai em cima.
4. Monte as telas com componentes nativos (TabView, NavigationStack e sheet no SwiftUI; NavigationBar, TopAppBar e ModalBottomSheet no Compose). Como a skill design é só web, só use shadcn/ui se o app for web (PWA).
5. Teste com fonte grande, tema escuro e em um aparelho real, incluindo os cantos com área segura.

## Combina com / alternativas

- [`01-fundamentos.md`](01-fundamentos.md) para cor, tipografia e contraste.
- [`04-auth-onboarding-configuracoes.md`](04-auth-onboarding-configuracoes.md) para login e primeiros passos.
- [`09-financeiro.md`](09-financeiro.md) e [`06-ecommerce.md`](06-ecommerce.md) quando o app é de dinheiro ou compra.
- [`10-agendamento.md`](10-agendamento.md) para horários e calendário.
- Alternativa: PWA responsiva, quando não vale publicar nas lojas.

## Decisão rápida

- **Use se:** o uso é diário e curto, com ações simples e funções do aparelho.
- **Evite se:** o trabalho é denso (tabelas, filtros, relatórios) ou o conteúdo é longo; faça na web.
