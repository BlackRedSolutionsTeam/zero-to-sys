# Modais, folhas e painéis

> Toda camada sobre a tela (modal, folha, painel, popover, toast) muda de forma conforme o dispositivo: no desktop flutua no centro ou na lateral, no celular sobe de baixo ou ocupa a tela toda.

| | |
|---|---|
| **Tema** | Camadas sobrepostas: modal, folha inferior, drawer, popover, menu de contexto, tooltip, toast, confirmação |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | MDN `<dialog>` https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog · Material Design 3 (bottom sheets, side sheets, dialogs, snackbar) https://m3.material.io/components · Apple HIG (sheets, alerts, popovers) https://developer.apple.com/design/human-interface-guidelines/sheets · WCAG 2.2 https://www.w3.org/TR/WCAG22/ · NN/g https://www.nngroup.com |
| **Verificado em** | 2026-11-24 |

## O que é

Camadas são elementos que aparecem acima da tela e pedem atenção ou oferecem uma ação rápida. Cada uma tem um peso: o modal bloqueia a tela, o painel lateral convive com ela, o popover é leve, o toast avisa sem interromper.

O mesmo conteúdo precisa de forma diferente em cada aparelho. Um modal de 480 px centralizado é natural no desktop e desperdiça espaço (ou é difícil de alcançar com o polegar) no celular.

## Por que importa

- No celular, o polegar alcança a parte de baixo da tela. Folha inferior fica perto da mão; botão de fechar no canto superior fica longe.
- Teclado virtual cobre metade da tela. Modal com formulário precisa rolar e não pode esconder o botão de enviar.
- Sem foco controlado, usuário de teclado e leitor de tela "cai" para a página de fundo.
- Tooltip depende de hover, que não existe no toque. Informação só em tooltip some no celular.

## Quando aplicar

- Ao projetar qualquer confirmação, formulário curto, filtro, menu de ações ou aviso.
- Ao portar um desktop para celular: liste cada modal e decida o equivalente.
- Ao revisar acessibilidade (foco, Esc, leitor de tela).

## Celular, tablet e desktop

| Componente | Celular | Tablet | Desktop |
|---|---|---|---|
| Modal de formulário curto | Folha inferior ou tela cheia (se tiver mais de 3 ou 4 campos) | Modal centralizado ou folha de página (formSheet) | Modal centralizado, com largura máxima (veja o exemplo de CSS) |
| Formulário longo ou fluxo | Tela cheia com título e botão fechar/voltar | Painel lateral ou modal grande | Painel lateral (drawer) ou página própria |
| Detalhe de item de lista | Navega para outra tela (push) | Painel lateral ao lado da lista (mestre-detalhe) | Painel lateral ou coluna de detalhe |
| Menu de ações de um item | Folha de ações inferior | Popover ancorado ao botão | Menu de contexto (clique direito) e menu "⋯" |
| Filtros | Folha inferior ou tela cheia com "Aplicar" | Painel lateral | Barra ou painel lateral fixo |
| Seleção (select, data) | Seletor nativo ou folha | Popover | Popover/dropdown |
| Confirmação destrutiva | Alerta central curto ou folha com botão destrutivo | Alerta central | Modal pequeno centralizado |
| Tooltip | Não existe: texto visível, rótulo ou toque longo com alternativa | Idem (toque) e hover se houver mouse | Hover e foco por teclado |
| Toast/snackbar | Parte de baixo, acima da barra de navegação | Baixo, centralizado ou à esquerda | Parte de baixo, um por vez, sem cobrir navegação (Material 3, snackbar) |
| Fechar | Botão, arrastar para baixo, voltar do sistema | Botão, toque fora, Esc se houver teclado | Botão, Esc, clique fora |

## Para que tipo de projeto

| Tipo | Prioridade | Por quê |
|---|---|---|
| Landing page | Baixa | Poucas camadas: menu mobile, cookies e formulário de contato. |
| E-commerce | Alta | Carrinho lateral, filtros em folha, seletor de tamanho e checkout rápido pesam na conversão no celular. |
| SaaS | Alta | Muitos formulários e ações por item; precisa de drawer no desktop e folha no celular. |
| Dashboard | Média | Filtros e detalhes em painel lateral; poucos modais. |
| Sistema interno | Alta | Confirmações destrutivas e formulários em drawer são o dia a dia. |
| App de campo | Alta | Uso com uma mão e luvas: folhas inferiores, alvos grandes, poucas camadas empilhadas. |
| Blog/conteúdo | Baixa | Quase só toast de cookies e menu. |

## Regras práticas

- Use `<dialog>` com `showModal()`: o navegador isola o fundo (inert), trata Esc e põe `aria-modal` implícito. Fonte: MDN, `<dialog>` (2026-11-24). A tag é Baseline amplamente disponível desde março 2022 (MDN).
- Tamanho de alvo: mínimo de 24 x 24 CSS px (WCAG 2.2, 2.5.8, nível AA); 44 x 44 pt padrão e 28 x 28 pt mínimo no iOS (Apple HIG, Accessibility); 48 x 48 dp no Android (support.google.com/accessibility/android/answer/7101858). As fontes divergem; use o maior no toque.
- Botão de fechar sempre visível. MDN lembra que nem todos os usuários conseguem apertar Esc.
- Devolva o foco ao elemento que abriu a camada ao fechar. O `<dialog>` modal faz isso por padrão (HTML Standard, html.spec.whatwg.org, passos de fechamento do dialog, 2026-11-24); confira em camada própria.
- Trave a rolagem do fundo enquanto o modal está aberto (`overscroll-behavior: contain` na camada e `overflow: hidden` no `body` ou `:has(dialog[open])`).
- Folha inferior: altura inicial entre meia tela e 90%, com alça de arraste visível. Apple e Material descrevem paradas (detents); os percentuais exatos variam e não foram confirmados como norma.
- Confirmação destrutiva: o botão diz o verbo ("Excluir pedido"), não "OK"; use `autofocus` no botão seguro (Cancelar); o MDN recomenda `autofocus` no botão de fechar do `<dialog>`. Ofereça "Desfazer" quando possível (Material 3, snackbar: "Undo" para o usuário corrigir a escolha).
- Toast: avisos de status devem ser anunciados por leitor de tela sem mover o foco (`role="status"`, WCAG 4.1.3). Tempo de exibição: o Material 3 (m3.material.io/components/snackbar/guidelines, conferido em 2026-11-24) diz que snackbar sem ação pode sumir sozinho após 4 a 10 segundos, conforme a plataforma, e que snackbar com ação fica até o usuário agir ou fechar. Na web, o Material pede também aviso inline junto da ação, ou uma ação no snackbar, para quem precisa de mais tempo. Só um snackbar por vez. O WCAG 4.1.3 e o `role="status"` não definem tempo. A HIG da Apple (Accessibility) pede minimizar elementos que somem por tempo e preferir dispensar por ação explícita. Não esconda erros que exigem ação.
- Tooltip no toque: coloque o texto no rótulo, num ícone de ajuda que abre popover ao toque, ou use `aria-label` além do visual. Conteúdo em hover deve ser dispensável, persistente e alcançável por foco (WCAG 1.4.13).
- Toda camada entra e sai com transição, na direção de onde veio; com `prefers-reduced-motion`, só opacidade ([doc 16](16-movimento-e-transicoes.md)).

## Erros comuns

- **Modal de desktop encolhido no celular:** cantos pequenos, botão X minúsculo. Corrija com folha inferior ou tela cheia abaixo de 600 px.
- **Teclado cobre o botão:** use `100dvh` e `max-height` com rolagem interna e deixe o botão de enviar fixo no rodapé da camada.
- **Fundo continua rolando:** trave o `body` e use `overscroll-behavior`.
- **Foco escapa:** modal feito com `div` sem inert. Troque por `<dialog>`.
- **Informação só no tooltip:** mova para texto visível.
- **Toast que some com erro importante:** use mensagem fixa no campo ou na página.
- **Clique fora fecha formulário preenchido:** use `closedby="closerequest"` e peça confirmação se houver dados não salvos.

## Como aplicar

Modal nativo que vira folha no celular:

```html
<dialog id="filtros" aria-labelledby="t">
  <form method="dialog">
    <h2 id="t">Filtros</h2>
    <!-- campos -->
    <button value="cancel" formnovalidate>Cancelar</button>
    <button value="ok">Aplicar</button>
  </form>
</dialog>
<button onclick="document.getElementById('filtros').showModal()">Filtros</button>
```

```css
dialog { border: 0; border-radius: 16px; width: min(560px, 92vw); max-height: 85dvh; overflow: auto; overscroll-behavior: contain; }
dialog::backdrop { background: rgb(0 0 0 / .5); }
body:has(dialog[open]) { overflow: hidden; }
@media (max-width: 599px) {
  dialog { margin: auto 0 0; width: 100%; max-width: none; border-radius: 16px 16px 0 0; padding-bottom: env(safe-area-inset-bottom); }
}
```

Fechar ao tocar fora (atributo `closedby="any"`, suporte pelo MDN/BCD em 2026-11-24: Chrome 134, Firefox 141, Safari 27.3 e iOS equivalente; em versões anteriores use fallback em JS). Sem o atributo, o `showModal()` age como `closerequest` (Esc, sem clique fora; MDN):

```html
<dialog closedby="any">...</dialog>
```

Toast acessível:

```html
<div role="status" aria-live="polite" class="toast">Pedido salvo. <button>Desfazer</button></div>
```

## Combina com / alternativas

- [02-mobile.md](02-mobile.md), [03-tablet.md](03-tablet.md), [04-desktop.md](04-desktop.md): contexto de cada aparelho.
- [06-navegacao.md](06-navegacao.md): botão voltar e folhas.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): alvos, hover, foco.
- [08-formularios.md](08-formularios.md): formulário dentro de camada.
- [13-ios-android-web.md](13-ios-android-web.md): folhas nativas de cada plataforma.
- Skills vizinhas: design-systems (layouts prontos por tipo de sistema), design (UI kits e ícones), stacks.
- Alternativa a modal: página própria (melhor para fluxos longos e links compartilháveis).

## Decisão rápida

**Faça**
- `<dialog>` + `showModal()`; folha ou tela cheia no celular; drawer no desktop para edição.
- Verbo no botão destrutivo, Cancelar com foco inicial, "Desfazer" quando der.
- Fechar por botão, Esc, gesto e (se seguro) clique fora.

**Evite**
- Informação essencial só em tooltip.
- Fundo rolando atrás, foco perdido, toast para erro crítico.
