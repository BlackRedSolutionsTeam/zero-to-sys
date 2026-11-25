# Projetar para tablet

> O dispositivo mais esquecido: nem celular esticado, nem desktop espremido. Duas colunas, toque com tela grande e janela que pode encolher.

| | |
|---|---|
| **Tema** | Design de interface para tablet (retrato e paisagem, toque, teclado e caneta opcionais) |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | Android, classes de tamanho e telas grandes (https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes); Material 3, layouts canônicos (https://m3.material.io/foundations/layout/canonical-layouts/list-detail); Apple HIG, Layout (https://developer.apple.com/design/human-interface-guidelines/layout); WCAG 2.2 (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) |
| **Verificado em** | 2026-11-24 |

## O que é

Tablet é uma tela média usada com toque, em geral com as duas mãos, no colo, em suporte ou apoiada numa mesa. Pode ganhar teclado, trackpad e caneta, e vira meio notebook. Em Android e iPadOS a janela do app muda de tamanho (tela dividida, janelas flutuantes), então "tablet" muitas vezes quer dizer "janela média", não "aparelho grande".

Pelas classes do Android: largura média é 600 a 839 dp (93,73 % dos tablets em retrato) e expandida é 840 a 1199 dp (97,22 % dos tablets em paisagem), segundo a página de classes de tamanho do Android (2026-11-24). A orientação do tablet, portanto, pode trocar a classe.

## Por que importa

- O layout do celular esticado deixa botões enormes e linhas longas; o do desktop espremido deixa alvos pequenos para o dedo.
- Em muitos negócios o tablet é o aparelho principal (balcão, consultório, loja, campo).
- A janela pode ficar estreita no meio do uso (tela dividida); o layout precisa aguentar.
- Uma documentação do Android observa que, para apps que miram o Android 16 (API 36), o sistema ignora restrições de orientação, proporção e redimensionamento em telas com menor lado a partir de 600 dp (developer.android.com, support-different-display-sizes, 2026-11-24). A Apple também pede layout que se adapte a rotação e a janelas redimensionadas (HIG, Layout). Não trave a orientação.

## Quando aplicar

- Quando o sistema tem lista e detalhe (e-mail, pedidos, clientes, prontuário).
- Quando a pessoa pode usar o tablet como aparelho principal.
- Quando a tela faz sentido com duas áreas lado a lado.

## Celular, tablet e desktop

Comparação do tablet com os outros dois:

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Colunas | Uma | Duas (lista + detalhe) em paisagem; uma ou duas em retrato | Várias |
| Navegação | Barra inferior | Barra inferior ou trilho lateral (média); trilho lateral (expandida) | Barra lateral completa |
| Entrada | Toque | Toque, mais teclado, trackpad e caneta quando houver | Mouse e teclado |
| Alvo | 44 a 48 px | 44 a 48 px (a tela grande não diminui o dedo) | Pode ser menor com mouse; WCAG: mínimo 24 px, Material: 44 dp para ponteiro |
| Orientação | Quase sempre retrato | Troca o tempo todo; ambas precisam funcionar | Fixa (paisagem) |
| Janela | Fixa | Pode ser estreita (tela dividida) | Redimensionável |
| Hover | Não | Só com trackpad ou mouse | Sim |
| Densidade | Baixa | Média | Alta |
| Largura do texto | Uma coluna | Limite a largura do texto | Limite a largura do texto |

## Para que tipo de projeto

| Tipo de sistema | Prioridade | Por quê |
|---|---|---|
| Ponto de venda | Alta | Tablet no balcão: toque, tela grande, uma pessoa por vez |
| Saúde (prontuário, checklist) | Alta | Lista de pacientes + detalhe; consulta em pé ou sentado |
| App de campo | Alta | Vistoria, inventário, agro: tela grande, sol, mãos ocupadas |
| Leitura e conteúdo | Alta | Revistas, cursos, documentos; retrato e paisagem |
| E-commerce | Média | Navegação de sofá; vitrine em grade |
| SaaS | Média | Reunião e consulta; aproveite duas colunas |
| Dashboard | Média | Boa leitura; filtros ficam em painel lateral |
| Landing page | Baixa | Basta a grade responsiva; não precisa de layout próprio |
| Sistema interno | Média | Aprovações e consulta em reunião |

## Regras práticas

- **Decida pela largura da janela:** compacta < 600 dp, média 600 a 839, expandida 840 a 1199, grande 1200 a 1599, extragrande 1600 ou mais (Android). Em web, use os mesmos valores em px como ponto de partida (não são oficiais para CSS). Fonte da navegação: Material 3, Navigation bar (barra só em janelas compacta e média; trilho em média e expandida).
- **Lista + detalhe** em larguras a partir de 840 dp; em média, pode ser uma coluna que abre o detalhe. Fonte: Material 3, List-detail (compacta: 1 painel; média: 1 recomendado ou 2; expandida: 2).
- **Altura compacta (< 480 dp):** não use duas colunas. Acontece em celulares em paisagem e flippables abertos (Android).
- **Alvos de toque** continuam em 44 pt / 48 dp; o tablet não muda o tamanho do dedo (Apple HIG, Material; WCAG 24 px é piso).
- **Largura do texto:** limite a 80 caracteres por linha ou menos (WCAG 2.2, 1.4.8 Visual Presentation, nível AAA, 2026-11-24).
- **Não trave a orientação** e teste o app em tela dividida (Android; a Apple pede layout que se adapte a janelas redimensionáveis e multitarefa no iPad, HIG Layout, 2026-11-24).
- **Teclado e caneta:** aceite Tab, atalhos e foco visível; caneta e toque devem ser aceitos por Pointer Events (`pointerType` vale `mouse`, `pen` ou `touch`; MDN, `PointerEvent.pointerType`, 2026-11-24).
- **Alvo e hover:** `@media (hover: hover)` também vale quando o tablet tem mouse ou trackpad; não dependa dele.

## Erros comuns

- **Celular esticado:** botão de 800 px de largura e lista em uma coluna. Corrija: use duas colunas ou limite a largura.
- **Desktop espremido:** menus de 24 px e tabela com 10 colunas. Corrija: alvos de 44 px e menos colunas.
- **Travar em retrato ou paisagem.** Corrija: libere as duas.
- **Quebrar em tela dividida** (janela de 320 a 500 px). Corrija: o layout precisa cair para uma coluna.
- **Depender do hover** em tablet sem mouse. Corrija: toque ou texto visível.
- **Ignorar o teclado físico.** Corrija: Tab, Enter, Esc e atalhos básicos.
- **Esquecer o teclado virtual em paisagem:** ele cobre quase toda a altura. Corrija: formulário em modal com rolagem.

## Como aplicar

Duas colunas só quando há espaço:

```css
.split { display: grid; grid-template-columns: 1fr; }
@media (min-width: 840px) and (min-height: 480px) {
  .split { grid-template-columns: minmax(280px, 360px) 1fr; }
}
```

Limite a largura do texto e use a janela, não o aparelho:

```css
.prose { max-width: 70ch; }
```

Toque quando o ponteiro é impreciso:

```css
@media (pointer: coarse) { .btn { min-height: 48px; min-width: 48px; } }
```

Tailwind:

```html
<div class="grid grid-cols-1 min-[840px]:grid-cols-[minmax(280px,360px)_1fr]">
  <aside>Lista</aside><section>Detalhe</section>
</div>
```

Container queries ajudam quando o componente vive em painéis de largura variável:

```css
.card-wrap { container-type: inline-size; }
@container (min-width: 480px) { .card { grid-template-columns: 120px 1fr; } }
```

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md), [02-mobile.md](02-mobile.md), [04-desktop.md](04-desktop.md).
- [05-breakpoints-e-layout.md](05-breakpoints-e-layout.md): pontos de quebra e container queries.
- [06-navegacao.md](06-navegacao.md): trilho lateral.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): caneta, trackpad, teclado.
- [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md): painéis laterais.
- [13-ios-android-web.md](13-ios-android-web.md): iPad x Android.
- Skills vizinhas: `design-systems` (layouts por tipo de sistema) e `design` (UI kits e ícones).

## Decisão rápida

- **Faça:** lista + detalhe em janelas largas; uma coluna em janelas estreitas; alvos de 44 a 48 px; as duas orientações; tela dividida; teclado e caneta como bônus.
- **Evite:** esticar o celular, espremer o desktop, travar orientação, depender de hover, esquecer que o tablet é o aparelho principal em PDV, saúde e campo.
