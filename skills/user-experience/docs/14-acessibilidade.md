# Acessibilidade (WCAG 2.2 AA)

> Acessibilidade é fazer a tela funcionar para quem usa teclado, leitor de tela, zoom ou tem baixa visão; o nível AA da WCAG 2.2 é o alvo prático.

| | |
|---|---|
| **Referência** | WCAG 2.2 (w3.org/TR/WCAG22) · MDN, `prefers-reduced-motion` (developer.mozilla.org) · WAI-ARIA Authoring Practices (w3.org/WAI/ARIA/apg) · Lei 13.146/2015, art. 63 (planalto.gov.br) |
| **Categoria** | Experiência do usuário |
| **Tipo** | Prática de acessibilidade aplicada a telas |
| **Vale para** | Web responsiva, PWA, a parte web de apps híbridos |
| **Verificado em** | 2026-11-24 |

## O que é

**WCAG** (Web Content Accessibility Guidelines) é o padrão do W3C com critérios testáveis. Cada critério tem um nível: A, AA ou AAA. O **AA** é o que a maioria dos projetos adota. A versão 2.2 acrescentou critérios como foco não encoberto (2.4.11) e tamanho mínimo de alvo (2.5.8).

## Por que usar

- Quem usa só o teclado, o leitor de tela ou o zoom consegue agendar uma consulta, e não só quem usa mouse.
- Quase tudo ajuda todo mundo: contraste no sol, teclado em formulário longo, legenda sem som.
- No Brasil, a Lei Brasileira de Inclusão (Lei 13.146/2015, art. 63) torna obrigatória a acessibilidade em sites de empresas com sede ou representação comercial no país e de órgãos de governo. Isto é contexto, não parecer jurídico. O **eMAG** (modelo do governo federal para sites públicos) não foi conferido aqui; consulte gov.br antes de citá-lo.

## Quando usar

- Em toda tela nova, desde o desenho (cores, tamanhos, rótulos), não só no fim.
- Em todo componente próprio (menu, modal, abas) antes de publicar.
- Em revisão de PR e antes de entregar.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Títulos, alt e contraste são a base do site |
| MVP de SaaS | ✅ Ótimo | Custa pouco no começo e muito para corrigir depois |
| SaaS em crescimento | ✅ Ótimo | Contratos de clientes grandes costumam pedir conformidade |
| Sistema interno/corporativo | ✅ Ótimo | Quem usa o dia todo depende do teclado e do foco |
| API/integração | ❌ Evite | Sem interface; vale para o painel que a acompanha |
| App mobile | 🟡 Serve | A WCAG vale para web; no nativo use VoiceOver e TalkBack (ver [13](13-ios-android-web.md)) |

## Quando é bom

- **Corrige na origem:** HTML semântico resolve a maior parte sem código extra.
- **Testável:** cada critério tem um jeito de conferir.
- **Barato no começo:** um `<button>` já vem com foco, teclado e papel certo.

## Quando é ruim

- **Ferramenta automática como prova:** ela acha só parte dos problemas; teclado e leitor de tela são manuais.
- **ARIA em excesso:** ARIA errado piora a experiência; use só quando o HTML não basta.
- **Overlay "de acessibilidade":** um widget colado no site não substitui o código correto.

## Como começar

Checklist AA aplicado (critério entre parênteses):

| Item | O que fazer |
|---|---|
| Contraste de texto | 4,5:1 (3:1 para texto grande) (1.4.3) |
| Contraste de componentes | Borda de campo, ícone e foco com 3:1 contra o fundo (1.4.11) |
| Foco visível | Nunca `outline: none` sem substituto (2.4.7) |
| Foco não encoberto | Cabeçalho ou barra fixa não cobre o campo focado (2.4.11) |
| Teclado | Tudo operável sem mouse, sem armadilha (2.1.1) |
| Ordem de foco | Segue a ordem visual e a de leitura (2.4.3) |
| Rótulos | Todo campo com `<label>` ligado (1.3.1, 3.3.2) |
| Imagem | `alt` descritivo; `alt=""` se decorativa (1.1.1) |
| Títulos | Um `h1`, sem pular nível (1.3.1, 2.4.6) |
| Landmarks | `header`, `nav`, `main`, `footer`; link "pular para o conteúdo" (2.4.1) |
| Alvo de toque | Mínimo de 24 x 24 px CSS (2.5.8); recomendado 44 px (ver [07](07-toque-mouse-teclado.md)) |
| Não só cor | Erro e status também com texto ou ícone (1.4.1) |
| Movimento | Respeitar `prefers-reduced-motion` |
| Erro de formulário | Texto junto do campo e anunciado (3.3.1, 4.1.3) |

```html
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
<main id="conteudo">
  <h1>Novo agendamento</h1>
  <form novalidate>
    <label for="paciente">Paciente</label>
    <input id="paciente" name="paciente" aria-describedby="paciente-erro" aria-invalid="true">
    <p id="paciente-erro" role="alert">Informe o nome do paciente.</p>
    <button type="submit">Agendar</button>
  </form>
</main>
```

```css
:focus-visible { outline: 3px solid var(--foco); outline-offset: 2px; }
.pular:not(:focus) { position: absolute; left: -9999px; }
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

**ARIA só quando o HTML não basta.** `<button>`, `<a>`, `<nav>`, `<dialog>` e `<label>` já trazem papel e teclado. Um `<div onclick>` não traz. Use `aria-describedby`, `aria-invalid`, `aria-expanded` e `role="alert"` para o que o HTML não diz.

**Como testar**

1. **Teclado:** desligue o mouse; use Tab, Shift+Tab, Enter, Espaço e Esc em todo o fluxo de agendar. Veja o foco o tempo todo.
2. **Automático:** axe no CI (ver [quality 06](../../quality/docs/06-acessibilidade-e-desempenho-automaticos.md)) e Lighthouse no Chrome.
3. **Leitor de tela:** NVDA (Windows), VoiceOver (macOS e iOS), TalkBack (Android). Ouça o formulário com um erro.
4. **Zoom:** 200% e texto maior sem perder função.

## Combina com / alternativas

- [07-toque-mouse-teclado](07-toque-mouse-teclado.md), [08-formularios](08-formularios.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [11-tipografia-e-densidade](11-tipografia-e-densidade.md)
- [15-internacionalizacao](15-internacionalizacao.md): `lang` certo no `<html>` e em trechos em outro idioma.
- Skills vizinhas: **quality** (axe e Lighthouse no CI), **design** (contraste das cores e ícones).

## Decisão rápida

- **Use se:** a tela tem formulário, navegação ou qualquer interação, ou seja, quase sempre.
- **Evite:** tratar como etapa final, `div` clicável no lugar de `button`, `outline: none` sem substituto, ARIA sem necessidade e confiar só em teste automático.
