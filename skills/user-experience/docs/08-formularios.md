# Formulários por dispositivo

> No celular o formulário disputa espaço com o teclado virtual; no desktop, com a pressa de quem digita só com o teclado. Peça o mínimo e abra o teclado certo.

| | |
|---|---|
| **Tema** | Layout de campos, tipos de teclado, validação, etapas e rascunho |
| **Vale para** | Web responsiva, PWA, app nativo (a parte de teclado e validação) |
| **Referências oficiais** | MDN, `inputmode`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inputmode · MDN, `autocomplete`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete · MDN, `enterkeyhint`: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/enterkeyhint · WCAG 2.2 (3.3.x, 1.3.5): https://www.w3.org/TR/WCAG22/ · NN/g, formulários: https://www.nngroup.com/articles/web-form-design/ · web.dev, formulários: https://web.dev/learn/forms |
| **Verificado em** | 2026-11-24 |

## O que é

É o conjunto de campos, rótulos, mensagens e botões que coleta dados. Em HTML, o tipo e os atributos do campo dizem ao navegador qual teclado virtual abrir e o que preencher sozinho: `type`, `inputmode`, `autocomplete` e `enterkeyhint`.

## Por que importa

- Digitar em tela de vidro é lento e erra mais. Teclado certo (numérico, e-mail) e preenchimento automático cortam o trabalho.
- O teclado virtual ocupa parte da tela e pode cobrir o campo ou o botão de enviar (o tamanho varia por aparelho).
- Formulário é onde a conversão se perde: cadastro, checkout, pedido.

## Quando aplicar

- Em todo campo de texto: escolha o `type`, o `autocomplete` e o teclado.
- Ao decidir entre etapas e página única.
- Em formulários longos ou em campo (conexão ruim): rascunho.

## Celular, tablet e desktop

| Aspecto | Celular | Tablet | Desktop |
|---|---|---|---|
| Colunas | Uma | Uma; duas só para pares curtos (dia/mês, cidade/UF) | Uma coluna principal; campos curtos lado a lado, com largura máxima |
| Rótulo | Acima do campo (NN/g) | Acima | Acima em formulários curtos; ao lado só em formulários desktop muito longos (NN/g) |
| Teclado | Virtual: `type`, `inputmode`, `enterkeyhint` decisivos | Virtual ou físico | Físico: Tab, Shift+Tab, Enter, setas |
| Tamanho da fonte do campo | `font-size: 1rem` (16 px é o padrão dos navegadores, MDN font-size) | Idem | Idem |
| Altura do campo | 44 a 48 (ver 07) | Idem | Mínimo de 24 px (WCAG 2.5.8) |
| Data e seleção | Seletor nativo (`type="date"`, `<select>`) | Nativo ou customizado | Calendário customizado e combobox com busca são aceitáveis |
| Fluxo | Etapas curtas | Etapas ou duas colunas | Página única, seções visíveis |
| Botão de enviar | Fixo na base, acima do teclado | Fixo ou no fim | No fim do formulário, alinhado aos campos |
| Validação | Ao sair do campo; erro junto do campo | Idem | Idem; resumo no topo para formulários longos |
| Rascunho | Salvar sozinho (conexão e interrupções) | Idem | Útil em formulário longo |

## Para que tipo de projeto

| Tipo de projeto | Prioridade | Por quê |
|---|---|---|
| Landing page | Alta | Formulário de captura curto |
| E-commerce | Alta | Checkout: endereço, cartão e CPF mal preenchidos perdem a venda |
| SaaS | Alta | Cadastro e configuração em três aparelhos |
| Dashboard | Média | Filtros e edições pontuais |
| Sistema interno | Alta | Digitação massiva no desktop; Tab e Enter definem a produtividade |
| App de campo | Alta | Uso offline, uma mão, interrupções: rascunho e etapas |
| Blog/conteúdo | Baixa | Comentário e newsletter |

## Regras práticas

- Use `font-size: 1rem` nos campos (16 px é o tamanho padrão dos navegadores, MDN font-size).
- Rótulo visível, ligado ao campo (`<label for>`). NN/g diz que o placeholder causa muitos problemas de usabilidade e é melhor evitá-lo (nngroup.com/articles/web-form-design, 2026-11-24).
- Alvo do campo e do botão de 44 a 48 (ver [07](07-toque-mouse-teclado.md)).
- `inputmode` aceita `none`, `text`, `decimal`, `numeric`, `tel`, `search`, `email` e `url` (confirmado na MDN). Quando existe `type` equivalente (`tel`, `email`, `url`, `search`), a MDN recomenda o `type`. O `inputmode` não valida nada.
- `enterkeyhint` muda o rótulo da tecla Enter do teclado virtual: valores `enter`, `done`, `go`, `next`, `previous`, `search`, `send` (MDN, enterkeyhint, 2026-11-24).
- `autocomplete` com os tokens padrão (`name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`…) atende ao critério 1.3.5 do WCAG 2.2 (finalidade do campo).
- Para número que não é quantidade (CPF, CEP, código), use `type="text"` com `inputmode="numeric"`: a MDN diz que `type="number"` não serve para valores só de dígitos que não são números, como CEP ou cartão (developer.mozilla.org, input/number, 2026-11-24).
- Valide ao sair do campo (blur) e reexiba ao digitar quando já há erro; não mostre erro antes de o usuário tentar. Mensagem diz o que fazer, junto do campo, com texto e não só cor (WCAG 3.3.1).
- Não peça de novo o que já foi informado (WCAG 3.3.7, Entrada redundante, novo no 2.2).

## Erros comuns

- **Teclado de texto para telefone e CEP.** Corrija: `type="tel"`, `inputmode="numeric"`.
- **Botão de enviar escondido pelo teclado.** Corrija: botão fixo acima do teclado e `scroll-margin` / `scrollIntoView` no campo focado.
- **Erro mostrado a cada tecla.** Corrija: validar no blur.
- **Formulário longo numa tela só no celular.** Corrija: etapas, com barra de progresso e botão Voltar.
- **`autocomplete="off"` em tudo**, matando o preenchimento. Corrija: use os tokens certos.
- **Perder tudo ao voltar.** Corrija: guardar rascunho.

## Como aplicar

```html
<form novalidate>
  <label for="cep">CEP</label>
  <input id="cep" name="cep" type="text" inputmode="numeric" autocomplete="postal-code"
         enterkeyhint="next" pattern="\d{5}-?\d{3}" required>

  <label for="tel">Celular</label>
  <input id="tel" name="tel" type="tel" autocomplete="tel" enterkeyhint="next">

  <label for="email">E-mail</label>
  <input id="email" name="email" type="email" autocomplete="email" enterkeyhint="send">

  <label for="nasc">Nascimento</label>
  <input id="nasc" name="nasc" type="date" autocomplete="bday">
  <button type="submit">Continuar</button>
</form>
```

```css
input, select, textarea { font-size: 1rem; min-height: 2.75rem; width: 100%; max-width: 32rem; } /* 1rem, 44 px */
@media (pointer: fine) { input, select { min-height: 2.25rem; } }
input:user-invalid { border-color: var(--erro); }   /* erro só após interação */
.form-actions { position: sticky; bottom: 0; padding-bottom: env(safe-area-inset-bottom); }
```

```js
// Rascunho simples
form.addEventListener('input', () => localStorage.setItem('rascunho', JSON.stringify(Object.fromEntries(new FormData(form)))));
```

## Combina com / alternativas

- [02-mobile](02-mobile.md), [04-desktop](04-desktop.md), [05-breakpoints-e-layout](05-breakpoints-e-layout.md), [07-toque-mouse-teclado](07-toque-mouse-teclado.md), [10-modais-folhas-e-paineis](10-modais-folhas-e-paineis.md), [11-tipografia-e-densidade](11-tipografia-e-densidade.md), [12-desempenho-e-rede](12-desempenho-e-rede.md)
- Skills vizinhas: **design-systems** (layouts prontos por tipo de sistema) e **design** (UI kits e ícones).

## Decisão rápida

- **Faça:** uma coluna, rótulo acima, `type` + `autocomplete` + `enterkeyhint`, `font-size: 1rem`, seletores nativos no celular, validação no blur, etapas no celular, rascunho.
- **Evite:** placeholder como rótulo, `type="number"` para CPF, erro a cada tecla, botão atrás do teclado, `autocomplete="off"` em tudo.
