# Toque, mouse e teclado

> Cada entrada tem um jeito de errar: o dedo é impreciso, o mouse tem hover, o teclado depende de foco. Projete a tela para os três.

| | |
|---|---|
| **Tema** | Alvos de toque, hover, gestos, arrastar, atalhos, foco, cursor, feedback e tempo de resposta |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | WCAG 2.2, alvo mínimo 2.5.8: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html · Apple HIG, layout e acessibilidade: https://developer.apple.com/design/human-interface-guidelines/accessibility · Material 3, acessibilidade: https://m3.material.io/foundations/designing/structure · MDN, media feature `hover`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover · NN/g, tempos de resposta: https://www.nngroup.com/articles/response-times-3-important-limits/ |
| **Verificado em** | 2026-11-24 |

## O que é

É como o usuário aciona a tela: dedo (toque), mouse ou trackpad (ponteiro) e teclado. Um mesmo aparelho pode ter vários (tablet com teclado, notebook com tela de toque). Por isso o CSS tem `pointer` (precisão: `none`, `coarse`, `fine`) e `hover` (se o ponteiro principal consegue pairar sobre elementos), além de `any-pointer` e `any-hover`.

## Por que importa

- Dedo grande em alvo pequeno gera erro e frustração; é também falha de acessibilidade.
- Hover nem sempre existe no toque: a MDN diz que `hover: none` inclui aparelhos que emulam hover com toque longo, inconveniente (developer.mozilla.org, @media/hover, 2026-11-24).
- Quem não usa mouse (teclado, leitor de tela, chave) precisa de foco visível e ordem lógica.
- Resposta lenta parece defeito: NN/g cita 0,1 s como instantâneo, 1 s como limite para manter o raciocínio e 10 s como limite da atenção.

## Quando aplicar

- Em todo botão, link, ícone e linha clicável.
- Em toda função que hoje só existe via hover, clique direito ou gesto.
- Em sistemas de uso intenso no desktop: atalhos e navegação por teclado.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Entrada principal | Toque (`pointer: coarse`) | Toque, às vezes teclado e mouse | Mouse e teclado (`pointer: fine`) |
| Tamanho do alvo | 44 pt (Apple) / 48 dp (Material) | Idem; mais espaço entre alvos | Mínimo 24 px (WCAG AA); 32 a 40 px é comum em interface densa |
| Espaçamento entre alvos | Apple: cerca de 12 pt de respiro em volta de controles com borda e 24 pt nos sem borda (HIG, conferido); Material: 8 dp ou mais entre alvos (Material 3, conferido) | Idem | O mínimo do WCAG é cumprido se o círculo de 24 px de cada alvo não toca o do vizinho |
| Hover | Não existe: nada essencial só no hover | Pode não existir (`hover: none`) | Tooltip, realce de linha, menu ao pairar (só como extra) |
| Gestos | Deslizar, puxar para atualizar, segurar, sempre com botão equivalente | Idem; arrastar entre painéis | Menos usados; clique, arrastar e soltar com alternativa |
| Menu de contexto | Pressionar e segurar, com ação visível "..." | Idem | Clique direito, e botão "..." também |
| Teclado | Teclado virtual (ver [08](08-formularios.md)) | Teclado físico opcional | Tab, Enter, Esc, setas, atalhos |
| Foco visível | Importante com teclado externo | Idem | Obrigatório |
| Cursor | Não há | Não há | `pointer` em clicáveis, `not-allowed`, `grab` em arrastáveis |
| Feedback | Estado de pressionado imediato; vibração leve opcional | Idem | Hover, foco, ativo, carregando |

## Para que tipo de projeto

| Tipo de projeto | Prioridade | Por quê |
|---|---|---|
| Landing page | Média | Poucos controles, mas CTA grande no toque |
| E-commerce | Alta | Compra no celular; erro de toque custa venda |
| SaaS | Alta | Uso misto; teclado no desktop, toque no celular |
| Dashboard | Alta | Linhas, filtros e ícones pequenos; precisa de densidade e alvo |
| Sistema interno | Alta | Digitação intensa no desktop: Tab, Enter e atalhos poupam horas |
| App de campo | Alta | Luva, sol, uma mão: alvos grandes |
| Blog/conteúdo | Baixa | Links no texto; garanta espaçamento |

## Regras práticas

- Alvo de toque: **44 × 44 pt** padrão e **28 × 28 pt** mínimo na Apple para iOS e iPadOS; no macOS, 28 × 28 pt padrão e 20 × 20 pt mínimo (HIG, Accessibility, conferido); **48 × 48 dp** para toque e **44 × 44 dp** para ponteiro (mouse, caneta) no Material 3 (conferido); **24 × 24 CSS px** no WCAG 2.2 AA (2.5.8, confirmado) e **44 × 44 CSS px** no nível AAA (2.5.5, confirmado). As fontes divergem: o AA é o piso do WCAG; para toque, use 44 a 48.
- Exceção do WCAG 2.5.8: alvos menores que 24 px passam se houver espaço (círculo de 24 px sem tocar outro alvo), se forem links no meio de texto, controles do navegador ou se o tamanho for essencial.
- O alvo pode ser maior que o ícone: use `padding`, mantendo o desenho de 24 px dentro de uma área de 44 a 48.
- Envolva efeitos de hover em `@media (hover: hover)`, e garanta que o toque também alcance a função.
- Todo gesto precisa de alternativa visível (botão, menu): WCAG 2.5.1 (A) pede alternativa de ponteiro único para gestos multiponto ou de caminho. Isso vale para deslizar para apagar e puxar para atualizar.
- Arrastar e soltar precisa de alternativa por clique ou teclado (WCAG 2.5.7, novo no 2.2).
- Foco visível em todo controle (WCAG 2.4.7); no 2.2, o foco não pode ficar escondido atrás de barras fixas (2.4.11).
- Ordem de foco igual à ordem visual e lógica; a MDN desaconselha `tabindex` positivo (developer.mozilla.org, tabindex, 2026-11-24).
- Resposta: ação com retorno em até ~100 ms (instantâneo, NN/g); acima de 1 s mostre indicador; acima de 10 s mostre progresso (NN/g).
- Atalhos de uma tecla (WCAG 2.1.4, A): permita desligar, remapear com tecla não imprimível ou ative só com o componente em foco.

## Erros comuns

- **Ícone de 24 px sem área de toque.** Corrija com padding até 44 a 48.
- **Informação só no hover** (tooltip com texto essencial, botão que aparece ao pairar). Corrija: mostre sempre no toque, ou use botão "...".
- **Swipe sem botão.** Corrija: ação também no menu da linha.
- **`outline: none` sem substituto.** Corrija com `:focus-visible` forte.
- **Botões colados** na barra inferior. Corrija: espaço entre alvos e `safe-area-inset-bottom`.
- **Clique direito personalizado** que remove o menu do navegador sem necessidade. Corrija: só onde há ganho real.
- **Hover emulado em toque.** Corrija com `@media (hover: hover)` (MDN, hover).

## Como aplicar

```css
/* Alvo mínimo em toque; compacto em ponteiro preciso */
button, [role="button"], a.nav { min-height: 44px; min-width: 44px; }
@media (pointer: fine) { .dense button { min-height: 32px; } }

/* Hover só onde existe */
@media (hover: hover) and (pointer: fine) {
  .row:hover { background: var(--row-hover); }
  .row .actions { opacity: 0; } .row:hover .actions, .row:focus-within .actions { opacity: 1; }
}
/* Em toque, as ações ficam sempre visíveis */
@media (hover: none) { .row .actions { opacity: 1; } }

:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.clickable { cursor: pointer; } [aria-disabled="true"] { cursor: not-allowed; }
```

```js
// Atalho com cuidado: não dispara dentro de campos
addEventListener('keydown', e => {
  if (e.target.closest('input, textarea, [contenteditable]')) return;
  if (e.key === '/') { e.preventDefault(); search.focus(); }
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); openPalette(); }
});
navigator.vibrate?.(10); // opcional; sem suporte no Safari/iOS (MDN browser-compat-data, api.Navigator.vibrate: Safari "false"; MDN: "Limited availability", 2026-11-24); exige interação prévia do usuário
```

## Combina com / alternativas

- [01-contexto-de-uso](01-contexto-de-uso.md), [02-mobile](02-mobile.md), [03-tablet](03-tablet.md), [04-desktop](04-desktop.md), [06-navegacao](06-navegacao.md), [08-formularios](08-formularios.md), [09-tabelas-e-dados](09-tabelas-e-dados.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [12-desempenho-e-rede](12-desempenho-e-rede.md)
- Skills vizinhas: **design-systems** (layouts prontos por tipo de sistema) e **design** (UI kits e ícones).

## Decisão rápida

- **Faça:** alvo de 44 a 48 no toque; hover só como extra; botão para todo gesto; foco visível; Tab em ordem lógica; feedback em 100 ms.
- **Evite:** função só no hover, no swipe ou no clique direito; `outline: none`; alvos de 24 px colados; atalhos que disparam dentro de campos.
