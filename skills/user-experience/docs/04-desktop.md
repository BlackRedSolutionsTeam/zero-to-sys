# Projetar para desktop

> Mouse, teclado e tela larga: mais informação ao mesmo tempo, atalhos, hover e várias tarefas, sem trazer os vícios do celular.

| | |
|---|---|
| **Tema** | Design de interface para desktop e notebook (ponteiro fino, teclado, janelas) |
| **Vale para** | Web responsiva, PWA, app nativo (Electron, Tauri) |
| **Referências oficiais** | WCAG 2.2, 2.1.1 Teclado, 2.4.7 Foco visível, 1.4.10 Reflow (https://www.w3.org/WAI/WCAG22/Understanding/reflow.html); MDN, `hover` e `pointer` (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover); Android, classes de tamanho (https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes); NN/g (https://www.nngroup.com) |
| **Verificado em** | 2026-11-24 |

## O que é

No desktop a pessoa trabalha: mouse de precisão, teclado físico, tela larga e várias janelas ou abas abertas. Sessões longas pedem informação densa, velocidade e controle. Funções que o celular esconde aqui devem estar visíveis.

A janela também varia: a pessoa pode deixá-la estreita ao lado de outra. No Android, extragrande é 1600 dp ou mais, e grande é 1200 a 1599 dp (developer.android.com, window size classes, 2026-11-24).

## Por que importa

- Quem usa o sistema o dia todo sente cada clique a mais; atalhos reduzem passos.
- Layout de celular no desktop desperdiça tela, esconde navegação e força a pessoa a rolar demais.
- Linhas muito longas dificultam a leitura: o WCAG 1.4.8 (AAA) pede no máximo 80 caracteres por linha (w3.org/WAI/WCAG22/Understanding/visual-presentation) e o Material 3 recomenda 40 a 60 (m3.material.io/foundations/layout/breakpoints/overview, 2026-11-24).
- Teclado é requisito de acessibilidade: sem ele, parte das pessoas não usa o sistema.

## Quando aplicar

- Em sistemas de trabalho: SaaS, ERP, painéis, editores, backoffice.
- Ao projetar tabelas, filtros, formulários longos e telas com várias ações.
- Em qualquer site, para a janela larga não ficar vazia nem esticada.

## Celular, tablet e desktop

Comparação do desktop com os outros dois:

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Entrada | Toque | Toque (+ teclado e caneta) | Mouse e teclado |
| Alvo | 44 a 48 px | 44 a 48 px | Mínimo WCAG 24 px (2.5.8); Material 3: 44 dp para ponteiro |
| Hover | Não | Quase nunca | Sim: dicas, ações na linha, pré-visualização |
| Atalhos | Raros | Com teclado | Esperados em telas de trabalho |
| Painéis (Material 3) | Um | Um (recomendado) ou dois | Um a três, conforme a faixa (large: um ou dois; extra-large: um a três) |
| Navegação | Barra inferior | Trilho lateral | Barra lateral visível ou topo com menus |
| Densidade | Baixa | Média | Alta, com opção compacta |
| Tabelas | Cartões | Tabela com poucas colunas | Tabela completa, ordenação, colunas fixas |
| Clique direito / arrastar | Não | Toque longo, arrastar com dedo | Menu de contexto, arrastar e soltar |
| Janela | Fixa | Dividida | Redimensionável, várias abas |
| Largura do conteúdo | Total | Total, com limite no texto | Limite máximo no texto e nos formulários |

## Para que tipo de projeto

| Tipo de sistema | Prioridade | Por quê |
|---|---|---|
| SaaS | Alta | Uso diário e longo; produtividade manda |
| Dashboard / painel | Alta | Muitos indicadores e tabelas; tela larga ajuda |
| Sistema interno / ERP | Alta | Digitação intensa, lote, atalhos |
| E-commerce (admin e catálogo) | Alta | Cadastro e pedidos pesados |
| Landing page | Média | Largura máxima e hierarquia; sem excesso de recursos |
| Blog / conteúdo | Média | Limite de caracteres por linha (Material 3: 40 a 60) e margens boas |
| App de campo | Baixa | Desktop só para o escritório e relatórios |
| Ponto de venda | Baixa a média | Administração; o balcão costuma ser tablet |

## Regras práticas

- **Alvo com mouse:** o WCAG 2.2 (2.5.8, AA) exige mínimo de 24 x 24 px CSS, com exceções. Para ponteiro, o Material 3 recomenda 44 x 44 dp e a Apple, no macOS, 28 x 28 pt padrão e 20 x 20 pt mínimo (ambos conferidos). Em interface densa, o piso é o 24 px do WCAG 2.5.8.
- **Teclado:** tudo que o mouse faz deve funcionar sem ele (WCAG 2.1.1, A) e o foco deve ser visível (2.4.7, AA). Ordem do Tab segue a ordem visual.
- **Hover só como reforço:** o conteúdo ou a função não pode existir apenas no hover (WCAG 1.4.13, Content on Hover or Focus, nível AA: o conteúdo extra deve poder ser dispensado, ficar sob o ponteiro e permanecer visível). Use `@media (hover: hover) and (pointer: fine)` para estilos de hover.
- **Largura do texto:** limite as linhas: Material 3 recomenda 40 a 60 caracteres e o WCAG 1.4.8 (AAA) aceita até 80. Use `max-width` em `ch` (os exemplos desta coleção usam 70ch).
- **Largura máxima:** conteúdo de leitura com limite; painéis podem ocupar a tela. Pontos úteis: 1200 e 1600 px como no Android (1200 a 1599 dp grande, 1600 dp extragrande). Em CSS são referência, não regra oficial.
- **Reflow:** em janela de 320 px o conteúdo deve continuar utilizável sem rolar para os lados (WCAG 1.4.10), pois 320 px equivalem a uma janela de 1280 px com zoom de 400 % (w3.org/TR/WCAG22, 1.4.10, 2026-11-24).
- **Atalhos:** não sobrescreva atalhos definidos pelo sistema (Apple HIG, Accessibility, "Avoid overriding system-defined keyboard shortcuts"; developer.apple.com/design/human-interface-guidelines/accessibility, 2026-11-24). Atalhos de uma tecla só: WCAG 2.1.4.

## Erros comuns

- **Menu hambúrguer escondendo a navegação** em tela larga. Corrija: barra lateral ou topo sempre visíveis.
- **Botões gigantes e largura total** do celular. Corrija: tamanho normal, alinhado, com `max-width`.
- **Linhas de texto com 150 caracteres.** Corrija: `max-width: 70ch`.
- **Formulário em coluna única de 1600 px.** Corrija: limite a largura e use duas colunas quando fizer sentido.
- **Ações só no hover**, inacessíveis por teclado. Corrija: também por foco e por menu.
- **Sem foco visível** (`outline: none`). Corrija: estilo de foco claro.
- **Rolagem lateral** em tabela sem alternativa. Corrija: colunas fixas, rolagem local e visibilidade de colunas.

## Como aplicar

Estilos de ponteiro fino e hover:

```css
@media (hover: hover) and (pointer: fine) {
  .row:hover { background: var(--hover); }
  .row .actions { opacity: 0; }
  .row:hover .actions, .row:focus-within .actions { opacity: 1; }
}
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
```

Largura máxima e texto confortável:

```css
.page { max-width: 1440px; margin-inline: auto; padding-inline: 24px; }
.prose { max-width: 70ch; }
.layout { display: grid; grid-template-columns: 240px minmax(0, 1fr) 320px; }
```

Atalho de teclado em React (sem biblioteca):

```tsx
useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
    if (e.target instanceof HTMLElement && e.target.matches("input, textarea, select")) return;
    if (e.key === "/") { e.preventDefault(); searchRef.current?.focus(); }
  };
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, []);
```

Tailwind:

```html
<aside class="hidden lg:block w-60">...</aside>
<main class="mx-auto max-w-screen-2xl px-6">...</main>
```

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md), [02-mobile.md](02-mobile.md), [03-tablet.md](03-tablet.md).
- [05-breakpoints-e-layout.md](05-breakpoints-e-layout.md): largura máxima e grade.
- [06-navegacao.md](06-navegacao.md): barra lateral e topo.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): hover, atalhos, foco.
- [09-tabelas-e-dados.md](09-tabelas-e-dados.md): tabelas densas e lote.
- [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md): painéis laterais.
- [11-tipografia-e-densidade.md](11-tipografia-e-densidade.md): densidade.
- Skills vizinhas: `design-systems` (layouts por tipo de sistema) e `design` (UI kits e ícones).

## Decisão rápida

- **Faça:** navegação visível; densidade maior com opção compacta; hover e atalhos como reforço; foco visível; largura máxima no texto; atalhos que não sobrescrevem os do sistema.
- **Evite:** hambúrguer escondendo o essencial, botões gigantes, linhas longas, ação só no hover, tabela sem alternativa, esticar o layout do celular.
