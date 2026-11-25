# Tipografia e densidade

> Texto e espaçamento se ajustam ao aparelho: leitura confortável e alvos grandes no celular, mais informação por tela no desktop, sem travar o zoom do usuário.

| | |
|---|---|
| **Tema** | Tamanho de fonte, comprimento e altura de linha, tipografia fluida, escala do usuário, densidade, imagens nítidas, modo escuro |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | Apple HIG Typography https://developer.apple.com/design/human-interface-guidelines/typography · Material Design 3 Typography https://m3.material.io/styles/typography · MDN `clamp()` https://developer.mozilla.org/en-US/docs/Web/CSS/clamp · WCAG 2.2 (1.4.4, 1.4.10, 1.4.12, 2.5.8) https://www.w3.org/TR/WCAG22/ · web.dev https://web.dev · NN/g https://www.nngroup.com |
| **Verificado em** | 2026-11-24 |

## O que é

Tipografia é a escolha de fonte, tamanho, espaçamento e ritmo do texto. Densidade é quanta informação cabe por tela: altura de linha da tabela, altura de botão, de campo, espaço entre blocos.

Os dois se combinam. Celular pede texto de leitura confortável e alvos grandes (densidade baixa). Desktop com mouse aceita mais informação por tela (densidade média ou alta).

## Por que importa

- Texto pequeno em tela pequena, ao sol, causa erro e abandono.
- Usuários aumentam a fonte do sistema (Dynamic Type no iOS, tamanho da fonte no Android, zoom do navegador). Layout que trava isso exclui gente.
- Linhas longas cansam: o olho perde a linha seguinte.
- Densidade errada irrita: tabela de trabalho espaçada demais obriga a rolar; botão apertado no celular gera toque errado.

## Quando aplicar

- Ao definir a escala tipográfica e os tokens de espaçamento do projeto.
- Ao criar tabelas, listas e formulários que serão usados em mais de um aparelho.
- Ao revisar acessibilidade.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Fonte do texto corrido | 16 px (1rem, padrão do navegador; body de 17 pt no iOS e body large de 16 sp no Material) | 16 a 18 px | 16 px (padrão do navegador) |
| Escala de títulos | Sem número oficial por aparelho; use a escala de estilos da plataforma (HIG, Typography; Material 3, Typography) | Idem | Idem |
| Comprimento de linha | 40 a 60 caracteres em todos os breakpoints (Material 3, Breakpoints); WCAG 1.4.8 (AAA): até 80 | Idem | Idem |
| Altura de linha | O texto deve suportar 1,5 sem quebrar (WCAG 1.4.12) | Idem | Idem |
| Alvo de botão, campo e linha clicável | 44 x 44 pt padrão e 28 x 28 pt mínimo no iOS (HIG, Accessibility); 48 x 48 dp no Android (inclusive em itens de lista, Material 3, Lists) | Idem | 24 x 24 CSS px mínimo (WCAG 2.5.8) |
| Espaçamento entre alvos | 8 dp (Android, support.google.com/accessibility/android/answer/7101858); HIG: cerca de 12 pt ao redor de elementos com contorno e 24 pt sem contorno | Idem | Idem |
| Imagens e ícones | SVG para ícones, `srcset` 2x/3x | Idem | Idem; 1x e 2x |
| Escala do usuário | Respeitar Dynamic Type e fonte do Android | Idem | Zoom do navegador até 200% |

## Para que tipo de projeto

| Tipo | Densidade | Por quê |
|---|---|---|
| Landing page | ✅ Confortável | Texto grande, muito espaço, foco na leitura e no botão. |
| E-commerce | ✅ Confortável | Cartões de produto com alvos grandes; preço legível. |
| SaaS | ✅ Confortável com opção compacta | Telas mistas; dê opção de densidade para quem trabalha o dia todo. |
| Dashboard | 🟡 Compacta no desktop | Muitos números por tela; no celular, resuma e use cartões. |
| Sistema interno | 🟡 Compacta no desktop | Operadores veem muitas linhas; ofereça compacta, mas mantenha 24 px de alvo mínimo. |
| App de campo | ✅ Confortável e grande | Sol, luvas, pressa: alvos no mínimo no tamanho do toque (44 pt, 48 dp); a norma não fixa um tamanho maior. |
| Blog/conteúdo | ✅ Confortável | Leitura longa pede 16 a 20 px e linha de 60 a 75 caracteres. |

## Regras práticas

- Fonte base de 16 px (1rem; é o padrão dos navegadores, e o Material 3 converte 16 px = 1rem em m3.material.io/styles/typography/type-scale-tokens, 2026-11-24). Apple: body de 17 pt e mínimo de 11 pt no iOS e iPadOS, 13 pt e 10 pt no macOS (HIG, Typography, 2026-11-24); a HIG, em Accessibility, pede ampliar o texto em pelo menos 200%. Material 3: body large de 16 sp (tokens da escala de tipos). Fontes divergem em 1 ponto; 16 a 17 serve.
- Use `rem` para fonte e espaçamentos e não trave o zoom. WCAG 1.4.4: texto redimensionável até 200% sem perda de conteúdo. Não use `user-scalable=no` nem `maximum-scale=1`.
- Reflow sem rolagem horizontal em 320 CSS px de largura (WCAG 1.4.10).
- Espaçamento de texto ajustável sem quebra: altura de linha 1,5, parágrafo 2x a fonte, letra 0,12 e palavra 0,16 da fonte (WCAG 1.4.12).
- Comprimento de linha: o WCAG 1.4.8 (nível AAA) fala em até 80 caracteres por linha (40 em CJK). O Material 3 cita 40 a 60 caracteres como comprimento ideal de linha de texto (m3.material.io/components/snackbar/guidelines, 2026-11-24). Não é número de norma de nível AA; `65ch` não vem de norma.
- Tipografia fluida: `font-size: clamp(1rem, 0.9rem + 0.5vw, 1.25rem)`. Inclua `rem` no meio da expressão para que o tamanho respeite a preferência de fonte do usuário e o zoom de texto (WCAG 1.4.4); só `vw` não tem esse componente. `clamp()` é suportado desde Chrome 79 e Safari 13.1 (MDN/BCD, 2026-11-24).
- Alvo mínimo: 24 x 24 CSS px (WCAG 2.5.8, AA); no toque, 44 x 44 pt padrão e 28 x 28 pt mínimo no iOS (Apple HIG, Accessibility) e 48 x 48 dp no Android, com 8 dp entre alvos (support.google.com/accessibility/android/answer/7101858). No desktop compacto, 24 px atende a WCAG 2.5.8.
- Fonte do sistema (`system-ui`) é rápida e familiar; fonte web custa download. Se usar, `font-display: swap` e subconjunto (`font-display`: MDN).
- Contraste: texto normal 4,5:1, texto grande 3:1 (WCAG 1.4.3, AA).
- Imagem raster para telas 2x/3x via `srcset`; ícones e logos em SVG.
- Modo escuro: teste o contraste nos dois temas (Apple HIG, Accessibility). O Android Developers diz que o tema escuro reduz o consumo de energia de forma significativa, conforme a tecnologia da tela (developer.android.com/develop/ui/views/theming/darktheme, 2026-11-24).

## Erros comuns

- **Fonte em `px` fixo e zoom travado:** troque por `rem`, remova `user-scalable=no`.
- **`vw` puro em fonte:** use `clamp()` com `rem`.
- **Parágrafo de 140 caracteres no desktop:** `max-width: 65ch`.
- **Tabela do desktop espremida no celular:** vire cartões ou rolagem controlada (doc 09).
- **Texto cinza claro sobre branco:** meça o contraste.
- **Campo com fonte pequena (12 px):** use `font-size: 1rem` nos campos (16 px é o tamanho padrão dos navegadores, MDN `font-size`; ver doc 08).
- **Densidade única:** ofereça compacta/confortável em telas de trabalho.

## Como aplicar

```css
:root { font-size: 100%; }
body { font: 1rem/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
h1 { font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem); line-height: 1.15; }
.prose { max-width: 65ch; }
:root { --controle: 3rem; }              /* 48 px: alvo de toque do Android */
@media (hover: hover) and (pointer: fine) { :root { --controle: 1.5rem; } } /* 24 px: mínimo da WCAG 2.5.8 */
button, input, select { min-height: var(--controle); font-size: 1rem; }
```

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
<img src="foto-800.jpg" srcset="foto-800.jpg 800w, foto-1600.jpg 1600w"
     sizes="(min-width: 1024px) 50vw, 100vw" width="800" height="600" alt="...">
```

```css
:root { color-scheme: light dark; }
@media (prefers-color-scheme: dark) { body { background: #121212; color: #e6e6e6; } }
```

## Combina com / alternativas

- [01-contexto-de-uso.md](01-contexto-de-uso.md): sol, pressa, luvas.
- [05-breakpoints-e-layout.md](05-breakpoints-e-layout.md): onde a escala muda.
- [07-toque-mouse-teclado.md](07-toque-mouse-teclado.md): tamanho de alvo.
- [08-formularios.md](08-formularios.md) e [09-tabelas-e-dados.md](09-tabelas-e-dados.md): altura de campo e de linha.
- [12-desempenho-e-rede.md](12-desempenho-e-rede.md): custo de fontes e imagens.
- [13-ios-android-web.md](13-ios-android-web.md): Dynamic Type e fontes do sistema.
- Skills vizinhas: design (UI kits e ícones), design-systems (layouts prontos), stacks.

## Decisão rápida

**Faça**
- 16 px base em `rem`, `clamp()` com `rem`, linha de até 65ch, altura de linha 1,5.
- Alvos de 44 pt (iOS) e 48 dp (Android) no toque; mínimo de 24 px com mouse (WCAG 2.5.8).
- Opção de densidade compacta só para telas de trabalho no desktop.

**Evite**
- Travar zoom, `px` fixo, `vw` puro.
- Campo com fonte menor que `1rem`.
- Alvo abaixo de 24 px.
