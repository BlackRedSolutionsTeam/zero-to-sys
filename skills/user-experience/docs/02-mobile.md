# Projetar para celular

> Tela estreita, uma mão, atenção dividida: uma coluna, uma tarefa por tela e a ação principal onde o polegar alcança.

| | |
|---|---|
| **Tema** | Design de interface para celular (retrato, toque, uma mão) |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | Apple HIG, Layout e alvos de toque (https://developer.apple.com/design/human-interface-guidelines/layout); Android, classes de tamanho (https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes); WCAG 2.2, 2.5.8 e 1.4.10 (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html); MDN, `env()` (https://developer.mozilla.org/en-US/docs/Web/CSS/env) |
| **Verificado em** | 2026-11-24 |

## O que é

Projetar para celular é aceitar três limites: a tela é pequena, o dedo é impreciso e a pessoa quase sempre está fazendo outra coisa ao mesmo tempo. O desenho que funciona tem poucas coisas por tela, alvos grandes, o botão principal ao alcance do polegar e o conteúdo antes do enfeite.

Na documentação do Android, "compacta" é largura abaixo de 600 dp e cobre 99,96 % dos celulares em retrato. Em paisagem, a altura passa a ser a restrição (abaixo de 480 dp).

## Por que importa

- Quem usa com uma mão não alcança o topo da tela em aparelhos grandes.
- O teclado virtual cobre boa parte da tela; formulário mal feito fica inutilizável.
- Chamadas, notificações e troca de app interrompem a tarefa a qualquer momento.
- Notch, ilha e barra de gestos escondem o que está nas bordas.

## Quando aplicar

- Sempre: celular é o piso do design. Comece por ele e acrescente espaço depois.
- Em especial em apps de campo, e-commerce, agenda, pagamentos e qualquer tela acessada por link no WhatsApp.

## Celular, tablet e desktop

Comparação do celular com os outros dois:

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Colunas | Uma | Uma a duas (lista + detalhe) | Duas ou mais |
| Navegação | Barra inferior (3 a 5 destinos) | Trilho lateral ou barra inferior | Barra lateral ou superior, sempre visível |
| Tarefa por tela | Uma | Uma ou duas relacionadas | Várias ao mesmo tempo |
| Ação principal | Parte de baixo, ao alcance do polegar | Perto do conteúdo; os dois polegares chegam nas laterais | Perto do cursor e atalho de teclado |
| Alvo de toque | 44 a 48 px, com folga | Igual ou maior | Menor é aceitável com mouse |
| Formulário | Um campo por vez ou poucos, rolando | Duas colunas curtas | Várias colunas, tab entre campos |
| Densidade | Baixa | Média | Alta |
| Hover | Não existe | Quase nunca | Comum |
| Janela | Fixa | Pode encolher (tela dividida) | Redimensionável |

## Para que tipo de projeto

| Tipo de sistema | Prioridade | Por quê |
|---|---|---|
| Landing page | Alta | Boa parte do acesso vem de redes sociais e anúncios, no celular |
| E-commerce | Alta | Descoberta e compra no celular; checkout curto, pagamento por carteira |
| SaaS | Média | Consulta e aprovação no celular; trabalho pesado no desktop |
| Dashboard | Baixa a média | Mostre indicadores-chave; tabelas grandes ficam para o desktop |
| Sistema interno | Média | Aprovar, consultar, registrar ponto; telas simples |
| App de campo | Alta | O celular é o aparelho principal; tolerar rede ruim e sol |
| Blog / conteúdo | Alta | Leitura em uma coluna; foco em tipografia |

## Regras práticas

- **Alvo de toque:** 44 x 44 pt padrão e 28 x 28 pt mínimo (Apple HIG, Accessibility, conferido em 2026-11-24), 48 x 48 dp, cerca de 9 mm físicos (Material 3, Accessibility designing, conferido em 2026-11-24), mínimo 24 x 24 px CSS (WCAG 2.2, 2.5.8, AA). Divergem: mire em 44 a 48 px; 24 a 28 é o piso, não o ideal. A Apple sugere cerca de 12 pt de respiro em volta de controles com borda e 24 pt nos sem borda (HIG, Accessibility). O Material sugere 8 dp ou mais entre alvos (Accessibility designing).
- **Folga entre alvos:** o WCAG aceita alvo menor que 24 px se um círculo de 24 px em volta dele não toca outro alvo. Fonte: WCAG 2.2, 2.5.8. Na prática, deixe espaço entre botões vizinhos.
- **Largura mínima:** o conteúdo deve funcionar em 320 px sem rolagem lateral (WCAG 1.4.10, AA).
- **Navegação inferior:** 3 a 5 destinos, cada um com ícone e rótulo de 1 a 2 palavras; com menos de 3, use abas; com mais de 5, não use barra inferior (Material 3, Navigation bar, conferido em 2026-11-24).
- **Zona do polegar:** ações frequentes na metade de baixo. A Apple diz que é mais fácil alcançar controles no meio ou embaixo da tela (HIG, Designing for iOS, 2026-11-24). Colocar ações destrutivas ou raras longe da zona do polegar é nossa recomendação, sem diretriz oficial.
- **Fonte de campo:** use `font-size: 1rem` nos campos (16 px é o tamanho padrão dos navegadores; MDN, `font-size`, 2026-11-24).
- **Teclado virtual:** reserve espaço; o campo em foco deve ficar visível (recomendação nossa). Use o tipo de teclado certo (`inputmode`, `type`).
- **Área segura:** respeite `env(safe-area-inset-*)`; use `viewport-fit=cover` na meta viewport e as variáveis de área segura para o conteúdo não ficar fora da tela (MDN, meta viewport e `env()`, 2026-11-24).
- **Altura:** use `dvh`, não `100vh`, para altura de tela cheia com a barra do navegador que aparece e some (unidade de viewport dinâmica; caniuse: Chrome 108, Firefox 101, Safari e iOS Safari 15.4; use `100vh` como fallback antes; caniuse.com/viewport-unit-variants, 2026-11-24).

## Erros comuns

- **Menu de topo com 8 itens espremidos.** Corrija: barra inferior com 3 a 5 destinos e o resto em "Mais".
- **Botão principal no topo ou no meio da tela.** Corrija: fixe no rodapé, acima da barra de gestos.
- **Tabela larga com rolagem lateral.** Corrija: transforme linhas em cartões ou mostre só as colunas essenciais.
- **Banner e cookie cobrindo metade da tela.** Corrija: faixa fina e fechável.
- **Teclado cobrindo o botão Enviar.** Corrija: rodapé que sobe com o teclado, ou botão dentro da rolagem.
- **Pop-ups pequenos com "X" minúsculo.** Corrija: folha inferior com alvo de fechar de 44 px. Veja [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md).
- **Perder o que foi digitado ao receber uma ligação.** Corrija: salve rascunho automaticamente.
- **Layout quebrado em paisagem.** Corrija: teste a altura de 360 a 480 px.

## Como aplicar

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

Barra inferior com área segura:

```css
.tabbar {
  position: fixed; inset: auto 0 0 0;
  display: grid; grid-template-columns: repeat(4, 1fr);
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--surface);
}
.tabbar a { min-height: 48px; display: grid; place-items: center; }
main { padding-bottom: calc(56px + env(safe-area-inset-bottom)); }
```

Altura de tela cheia e fonte de campo:

```css
.screen { min-height: 100dvh; }
input, select, textarea { font-size: 1rem; }
```

Teclado certo para cada campo:

```html
<input type="email" autocomplete="email" inputmode="email">
<input inputmode="numeric" autocomplete="one-time-code">
```

Tailwind (celular primeiro, o desktop entra com prefixo):

```html
<nav class="fixed bottom-0 inset-x-0 pb-[env(safe-area-inset-bottom)] md:static md:w-64">...</nav>
```

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md), [03-tablet.md](03-tablet.md), [04-desktop.md](04-desktop.md).
- [06-navegacao.md](06-navegacao.md): barra inferior, "Mais", voltar.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): alvos e gestos.
- [08-formularios.md](08-formularios.md): campos e teclado virtual.
- [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md): folha inferior.
- [12-desempenho-e-rede.md](12-desempenho-e-rede.md): rede ruim.
- [13-ios-android-web.md](13-ios-android-web.md): gestos e convenções por plataforma.
- Skills vizinhas: `design-systems` (layouts por tipo de sistema) e `design` (UI kits e ícones).

## Decisão rápida

- **Faça:** uma coluna; uma tarefa por tela; ação principal no rodapé; alvos de 44 a 48 px; `dvh` e `env(safe-area-inset-*)`; rascunho salvo; conteúdo antes do enfeite.
- **Evite:** menu hambúrguer escondendo o essencial, tabelas largas, hover, pop-ups pequenos, teclado cobrindo o botão, `100vh` para tela cheia.
