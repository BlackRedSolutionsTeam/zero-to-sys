# Fundamentos de layout

> As regras que valem para qualquer tela de sistema: grade, tipografia, cor, estados, responsividade e acessibilidade. Leia antes de abrir o doc de um tipo específico.

| | |
|---|---|
| **Tipo de sistema** | Todos (base comum aos outros 11 docs) |
| **Exemplo** | Não tem HTML próprio; todos os exemplos em `../examples/` seguem estas regras |
| **Layout base** | Não se aplica |
| **Referências reais** | Material Design 3 (https://m3.material.io), Apple Human Interface Guidelines (https://developer.apple.com/design/human-interface-guidelines), WCAG 2.2 (https://www.w3.org/TR/WCAG22/), Refactoring UI (https://www.refactoringui.com) |
| **Componentes** | shadcn/ui para componentes, Lucide para ícones (ver skill `design`) |
| **Verificado em** | 2026-11-24 |

## O que é

Um conjunto curto de decisões que se repete em toda interface boa: uma escala de espaço, uma escala de texto, poucos neutros, uma cor de marca, cores de estado e estados bem tratados. Os docs de cada tipo de sistema só dizem como combinar essas peças. Aqui estão as peças.

## Por que estas regras

- **Consistência custa menos que talento.** Com escala fixa, ninguém precisa decidir "12 ou 14 px" a cada tela.
- **Tokens permitem trocar a marca e o tema** sem reescrever o CSS.
- **Estados e acessibilidade** separam produto de protótipo: é neles que o usuário real passa o tempo.

## Quando usar

Sempre. Consulte antes de montar qualquer tela e confira o resultado contra a lista de erros comuns no fim deste doc.

## Para que tipo de projeto

| Projeto | Encaixe | Por quê |
|---|---|---|
| Sistema web (painel, CRUD, CRM, financeiro) | ✅ Ótimo | Telas densas e repetitivas ganham muito com escala e tokens |
| Landing page e site de marketing | 🟡 Serve | Vale a escala e a cor, mas o ritmo vertical é mais generoso e a tipografia, maior |
| App mobile | 🟡 Serve | Mesma lógica, com alvo de toque maior e regras da plataforma (ver 12-app-mobile.md) |
| Protótipo descartável | ✅ Ótimo | Tokens deixam o protótipo bonito com pouco esforço |
| Arte editorial ou site experimental | ❌ Evite | Quebrar a regra é o ponto; use estas regras só como contraste |

## Regras por tema

### Grade e espaçamento

- Escala de 4 px dos exemplos (tokens `--s1` a `--s7` abaixo): 4, 8, 12, 16, 24, 32, 48. Os exemplos 03 e 04 usam também 20 px. Fonte: os HTML em `../examples/`.
- Grades dos exemplos: KPIs em 4 colunas (2 no tablet, 1 no celular), gráficos em 2fr/1fr, vão de 12 a 16 px.
- Limite a linha de texto a 80 caracteres (WCAG 1.4.8, nível AAA, w3.org/WAI/WCAG22/Understanding/visual-presentation, 2026-11-24). O Material 3 sugere 40 a 60 caracteres por linha (m3.material.io/foundations/layout/breakpoints/overview, 2026-11-24). Os exemplos limitam o conteúdo a 1440 px (02) e 1280 px (03).
- Nos exemplos, o texto alinha à esquerda e os números das tabelas, à direita.

### Escala tipográfica

Tamanhos em px usados nos exemplos (fonte: `../examples/02`, `03` e `04`):

| Uso | 02 dashboard | 03 admin | 04 entrada e conta |
|---|---|---|---|
| Rótulo pequeno, legenda | 11 a 12 | 11 a 12 | 14 |
| Texto de interface | 14 | 14 | 17 (16 até 767 px) |
| Título de cartão ou drawer | 14 | 16 | 18 a 24 |
| Título de página | 22 | 20 | 30 a 36 |
| Número grande (KPI) | 26 | 20 | não tem |

Os exemplos usam uma família (Inter, com a pilha do sistema como reserva) e pesos de 500 a 700. O Material 3 usa 14 como tamanho-base da escala (m3.material.io/styles/typography/type-scale-tokens, 2026-11-24). Números em tabelas e KPIs usam `font-variant-numeric: tabular-nums`, que ativa dígitos de largura igual, próprios para alinhar em tabelas (MDN font-variant-numeric). No iOS, o tamanho padrão é 17 pt e o mínimo, 11 pt (Apple HIG, Accessibility, 2026-11-24). Para campos, use `font-size: 1rem` (16 px é o tamanho padrão dos navegadores, MDN font-size).

### Hierarquia visual

- Os exemplos usam três níveis de texto (principal, secundário e terciário: `--text`, `--text-2`, `--text-3`) e um botão primário por região; os demais são secundários (com borda) ou fantasma (sem borda).

### Cor

- **Neutros** (nos exemplos, levemente tingidos de azul ou de quente): fundo, superfícies, bordas e 3 níveis de texto.
- **Uma cor de marca**: ação principal, link, item ativo, foco. Ela aparece pouco; por isso destaca.
- **Estado**: sucesso (verde), alerta (âmbar), erro (vermelho), informação (azul). Leve texto ou ícone junto: não transmita informação só pela cor (Apple HIG, Accessibility, 2026-11-24).
- **Contraste WCAG AA**: 4,5:1 para texto normal; 3:1 para texto grande, de 18 pt (cerca de 24 px) ou 14 pt em negrito (cerca de 18,5 px) (WCAG 1.4.3, w3.org/WAI/WCAG22/Understanding/contrast-minimum, 2026-11-24). Componentes de interface e objetos gráficos, como bordas de campos e ícones que carregam sentido, também pedem 3:1 (WCAG 1.4.11, nível AA).
- Os gráficos do exemplo 02 usam 3 cores de série.

### Raio e sombra

- Raios dos exemplos: 6 px (campos, botões), 8 px (menus), 10 a 12 px (cartões), pílula (999 px). Os exemplos repetem a mesma família de raios.
- Sombras dos exemplos: cartões com borda de 1 px e sombra mínima (`0 1px 2px`); sombra forte só no que flutua (drawer, gaveta). No tema escuro, o exemplo 02 troca a sombra dos cartões por borda.

### Densidade

Medidas dos exemplos (fonte: `../examples/02`, `03` e `04`):

| | 02 dashboard | 03 admin | 04 entrada e conta |
|---|---|---|---|
| Linha de tabela | 48 px | 44 px | não tem |
| Campo | 36 px (busca) | 32 px | 52 px |
| Botão | 36 px | 32 px | 48 px |
| Padding de cartão | 16 px | 12 px por 16 px | 40 px (onboarding) |
| Texto base | 14 px | 14 px | 17 px |

No iOS, o tamanho padrão de um controle é 44x44 pt e o mínimo, 28x28 pt (Apple HIG, Accessibility, 2026-11-24). No WCAG 2.2, o piso é 24x24 px (2.5.8, AA) e o nível reforçado pede 44x44 px (2.5.5, AAA).

### Estados

- **Vazio**: nos exemplos, ícone, título que diz o que falta, uma frase e o botão da ação.
- **Carregando**: nos exemplos, esqueleto com a forma do conteúdo; o exemplo 02 marca a área com `aria-busy="true"`, que avisa as tecnologias assistivas de que o conteúdo está sendo atualizado (MDN aria-busy).
- **Erro**: nos exemplos, mensagem com a causa e botão "Tentar de novo", com o que já carregou mantido. O exemplo 02 usa `role="alert"`, que faz as tecnologias assistivas anunciarem a mensagem na hora (MDN alert role).
- **Hover**: nos exemplos, mudança sutil de fundo em linhas, botões e itens de menu.
- **Foco**: nos exemplos 02 e 03, anel de 2 px na cor de marca com 2 px de afastamento (o 04 usa 3 px), aplicado com `:focus-visible`, que só aparece quando o navegador julga que o foco deve ficar evidente (MDN :focus-visible). O WCAG 2.4.13 (AAA) pede um indicador com área de pelo menos um perímetro de 2 px e contraste de 3:1 entre foco e sem foco (w3.org/WAI/WCAG22/Understanding/focus-appearance, 2026-11-24).
- Os exemplos tratam também: desativado, selecionado e sucesso (confirmação curta).

### Movimento

- Toda troca de tela e de estado (abrir, fechar, carregar, selecionar, entrar e sair de lista) tem transição curta. Vale para todos os tipos de layout deste catálogo, do dashboard ao app mobile.
- Duração e curva são tokens (`--dur-fast`, `--dur`, `--dur-slow`, `--ease`, `--ease-exit`), usados por todas as telas.
- O que animar, durações, curvas, código e movimento reduzido: [user-experience, documento 16](../../user-experience/docs/16-movimento-e-transicoes.md).

### Responsividade

Breakpoints do Material 3 (m3.material.io/foundations/layout/breakpoints/overview, 2026-11-24):

| Breakpoint | Largura | Painéis (M3) |
|---|---|---|
| Compact | abaixo de 600 dp | 1; barra de navegação ou trilho modal |
| Medium | 600 a 839 dp | 1 (recomendado) ou 2; duas colunas só com conteúdo de baixa densidade |
| Expanded | 840 a 1199 dp | 1 ou 2 (recomendado) |
| Large | 1200 a 1599 dp | 1 ou 2 (recomendado) |
| Extra-large | 1600 dp ou mais | de 1 a 3 (recomendado) |

Os exemplos usam seus próprios pontos de quebra: 02 em 1100, 860 e 520 px; 03 em 1023, 860 e 520 px; 04 em 1023 e 767 px. Neles, só as tabelas largas rolam na horizontal, dentro do próprio contêiner.

### Tema claro e escuro

- Nos exemplos, tudo vem de tokens; o tema escuro redefine os mesmos nomes em `@media (prefers-color-scheme: dark)` e em `[data-theme="dark"]`, com botão para alternar.
- Nos exemplos, o escuro usa fundo cinza muito escuro (não `#000`), superfícies progressivamente mais claras e marca e estado clareados. Confira o contraste nos dois temas (Apple HIG, Accessibility, 2026-11-24).

### Acessibilidade

- Foco visível em tudo (`:focus-visible`, MDN).
- Alvo de toque: 44x44 pt é o padrão no iOS (Apple HIG, Accessibility, 2026-11-24); o piso do WCAG 2.2 é 24x24 px (2.5.8, AA).
- `prefers-reduced-motion: reduce` vale quando a pessoa pediu menos movimento não essencial no dispositivo; os exemplos o usam para desligar o esqueleto pulsante e as transições (MDN prefers-reduced-motion).
- Tabelas com `th scope`, que indica a quais células o cabeçalho se aplica (MDN th).
- Não transmita informação só pela cor (Apple HIG, Accessibility): nos exemplos, status leva texto e a tendência leva seta.

## Tokens de referência

```css
:root{
  /* Neutros (cinza-azulado) */
  --bg:#f6f7f9; --surface:#fff; --surface-2:#f1f3f6;
  --border:#e3e7ed; --border-strong:#cfd5de;
  --text:#151b26; --text-2:#4a5565; --text-3:#636e7f;   /* --text-3 sobre --surface 5,2:1, sobre --bg 4,8:1 e sobre --surface-2 4,6:1 (calculado pela fórmula de luminância relativa do WCAG 1.4.3) */
  /* Marca (uma só) */
  --brand:#4338ca; --brand-hover:#3730a3; --brand-soft:#eceefe; --on-brand:#fff;
  /* Estado */
  --ok:#0f7b4f; --warn:#a15c07; --err:#c0322b; --info:#1d62c4;
  --ok-soft:#e1f5ec; --warn-soft:#fdf0d9; --err-soft:#fde8e6;
  /* Tipografia */
  --font:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --fs-xs:12px; --fs-sm:14px; --fs-md:16px; --fs-lg:22px; --fs-xl:26px;
  /* Espaço (4/8) */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px;
  /* Raio e sombra */
  --r-sm:6px; --r-md:8px; --r-lg:12px; --r-full:999px;
  --shadow:0 1px 2px rgba(21,27,38,.06);
  --shadow-pop:0 8px 24px rgba(21,27,38,.14);
  /* Movimento */
  --dur-fast:120ms; --dur:200ms; --dur-slow:280ms;
  --ease:cubic-bezier(.2,0,0,1); --ease-exit:cubic-bezier(.4,0,1,1);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){ /* mesmos nomes, valores escuros */ }}
[data-theme="dark"]{ /* repita os valores escuros aqui */ }
```

## Erros comuns que deixam a interface amadora

- Espaçamentos soltos, fora da escala, e margens diferentes entre telas.
- Cinza claro demais sobre branco (abaixo de 4,5:1, WCAG 1.4.3) e placeholder usado como rótulo.
- Cor de marca em tudo: botões, títulos, ícones e fundos ao mesmo tempo.
- Tela vazia sem orientação; erro genérico; carregamento sem indicação.
- Sem foco visível (`outline:none` sem substituto) e sem hover.
- Tela, modal e menu que aparecem e somem de uma vez, sem transição.
- Números sem alinhamento à direita nem `tabular-nums`.
- Status só com cor (Apple HIG, Accessibility).
- Tabela que estoura a tela no celular.

## Como começar

1. Copie o bloco `:root` acima e troque `--brand` pela cor da marca (confira o contraste do texto sobre ela).
2. Escolha a densidade (confortável ou compacta) e a fonte.
3. Monte as telas com shadcn/ui e Lucide (skill `design`), usando só os tokens.
4. Abra o doc do tipo de sistema, copie o exemplo HTML mais próximo e adapte.
5. Passe pela lista de erros comuns e teste abaixo de 600 px, entre 600 e 839 px e acima de 1200 px (breakpoints do Material 3), nos dois temas.

## Combina com / alternativas

Aplica-se a [02-dashboard-analytics.md](02-dashboard-analytics.md), [03-admin-crud.md](03-admin-crud.md), [04-auth-onboarding-configuracoes.md](04-auth-onboarding-configuracoes.md), [05-landing-saas.md](05-landing-saas.md), [06-ecommerce.md](06-ecommerce.md), [07-crm-kanban.md](07-crm-kanban.md), [08-inbox-chat.md](08-inbox-chat.md), [09-financeiro.md](09-financeiro.md), [10-agendamento.md](10-agendamento.md), [11-documentacao.md](11-documentacao.md) e [12-app-mobile.md](12-app-mobile.md). Alternativa: adotar um sistema pronto (Material, Radix Themes) e aceitar o visual dele.

## Decisão rápida

- **Use se:** vai montar qualquer tela de produto e quer resultado consistente sem designer.
- **Evite se:** o projeto é experimental ou artístico e quebrar a regra é intencional.
