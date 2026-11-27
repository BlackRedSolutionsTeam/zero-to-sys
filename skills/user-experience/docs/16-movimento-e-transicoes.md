# Movimento e transições

> Nada aparece nem some de repente: toda troca de tela e de estado tem uma transição curta e suave, em qualquer tipo de sistema, inclusive dashboard e painel admin.

| | |
|---|---|
| **Tema** | Movimento funcional: troca de tela, abrir e fechar camadas, entrada de conteúdo, resposta ao toque e ao clique, gestos (deslizar, arrastar, puxar, pinça), listas que mudam, movimento reduzido |
| **Vale para** | Web responsiva, PWA, app nativo |
| **Referências oficiais** | NN/g, Animation Duration https://www.nngroup.com/articles/animation-duration/ · Material Design 3, Motion https://m3.material.io/styles/motion/overview · Apple HIG, Motion https://developer.apple.com/design/human-interface-guidelines/motion · MDN View Transition API https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API · MDN `@starting-style` https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style · web.dev, Baseline entry animations https://web.dev/blog/baseline-entry-animations · MDN `prefers-reduced-motion` https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion · WCAG 2.2 https://www.w3.org/TR/WCAG22/ |
| **Verificado em** | 2026-11-27 |

## O que é

Movimento funcional é a transição que liga um estado da tela ao seguinte: a tela nova entra, o modal abre, a linha salva pisca, o item excluído some. Ele mostra de onde a coisa veio e para onde foi.

É diferente de efeito decorativo (fundo animado, spotlight, texto que revela, partículas). O decorativo segue a skill `design`: só em página de marketing e portfólio. O funcional é **obrigatório em toda tela**, de qualquer tipo de sistema.

## Por que importa

- Sem transição, o conteúdo é "cuspido" na tela: a pessoa perde o que mudou e o sistema parece quebrado, barato ou travado.
- A transição explica a mudança: o painel veio da direita, então volta para a direita; o item saiu da lista porque foi excluído.
- Resposta imediata ao toque (botão que afunda, linha que acende) faz o sistema parecer rápido mesmo quando a rede demora.
- Movimento demais, longo ou em tudo cansa quem usa oito horas por dia. Suave é curto e discreto.

## Quando aplicar

- Em toda tela nova e em todo componente que muda de estado. Não é acabamento para depois: entra junto com a tela.
- No protótipo (skill `framia`): o cliente aprova o comportamento, não só a imagem parada.
- Ao revisar uma tela que "parece seca": percorra a tabela "O que anima e como".

## O que anima e como

| O que muda | Movimento | Duração |
|---|---|---|
| Hover, pressionar, foco, cor de botão e de linha | Transição de cor, fundo, borda e sombra; ao pressionar, escala de 0,97 a 0,98 | 100 a 150 ms |
| Toggle, checkbox, rádio | O indicador desliza ou preenche | Cerca de 100 ms |
| Dropdown, popover, menu, tooltip | Opacidade + deslocamento de 4 a 8 px ou escala de 0,96, saindo do elemento que abriu | 150 a 200 ms |
| Modal e confirmação | Opacidade + escala de 0,96 a 0,98; o fundo escuro entra só com opacidade | 200 a 300 ms |
| Folha inferior, drawer, painel lateral | Desliza da borda de onde vem; fecha voltando para ela | 250 a 300 ms |
| Troca de tela ou de rota | Web: crossfade, com deslocamento curto se houver hierarquia. App: o empurrão nativo da plataforma | 200 a 300 ms |
| Troca de aba, de passo de formulário, de filtro | Crossfade do conteúdo; o indicador da aba desliza | 150 a 200 ms |
| Esqueleto → conteúdo | Opacidade; o conteúdo ocupa o mesmo espaço do esqueleto, sem salto | 150 a 200 ms |
| Item entra, sai ou muda de lugar na lista | Altura + opacidade; os vizinhos deslizam para o lugar, não pulam | 200 a 250 ms |
| Acordeão, seção que expande | Altura + opacidade do conteúdo | 200 a 250 ms |
| Toast, aviso, erro de campo | Entra com opacidade + deslocamento curto; sai só com opacidade | 150 a 200 ms |
| Sucesso de uma ação (salvo, enviado, pago) | Confirmação curta no lugar da ação: ícone, cor ou destaque da linha que mudou | 200 a 400 ms |
| Gráfico e número de indicador | Entram uma vez ao carregar; não reanimam a cada atualização | Até 500 ms |

As durações seguem a NN/g: a maior parte das animações de interface fica entre 100 e 500 ms; resposta simples (checkbox, toggle) perto de 100 ms e mudança grande de tela (modal) entre 200 e 300 ms (nngroup.com/articles/animation-duration, 2026-11-27). A divisão por linha da tabela é prática do plugin dentro dessa faixa, sem fonte oficial linha a linha. O Material 3 publica tokens próprios de duração e curva (m3.material.io/styles/motion/easing-and-duration/tokens-specs); os valores exatos não foram conferidos nesta data: confira na página antes de citar.

## Gestos, do simples ao avançado

Vale para tudo em que a pessoa encosta, do toque num botão ao arrastar de um cartão. Quatro regras servem a todos: a interface responde no mesmo quadro do contato; o que é arrastado segue o dedo ou o ponteiro sem atraso; ao soltar, o elemento termina o caminho com a velocidade que tinha (ou volta ao lugar, se não passou do limite); e o gesto pode ser cancelado no meio. As linhas abaixo são prática do plugin; cada plataforma tem o comportamento nativo, que ganha quando existe.

| Gesto | Enquanto acontece | Ao soltar ou terminar |
|---|---|---|
| Toque e clique | Estado pressionado na hora (cor ou escala de 0,97 a 0,98) | Volta em 100 a 150 ms; a ação começa sem esperar a animação |
| Hover e foco por teclado | Cor, fundo ou sombra em transição; o anel de foco aparece sem atraso | Volta na mesma duração |
| Toque longo | Leve escala ou elevação crescente mostra que algo vai abrir | Menu de contexto sai do item tocado |
| Rolagem | Inércia nativa, nunca rolagem reescrita em JavaScript; cabeçalho que encolhe acompanha a rolagem | Para sozinha; limite com o efeito nativo da plataforma |
| Carrossel e páginas laterais | Conteúdo segue o dedo | Encaixa no item mais próximo (`scroll-snap`); o indicador acompanha |
| Puxar para atualizar | O indicador desce junto com o dedo, com resistência crescente | Passou do limite: gira até carregar e recolhe; não passou: volta |
| Deslizar item da lista (arquivar, excluir) | A linha segue o dedo e revela a ação por baixo; a cor firma ao passar do limite | Passou: a linha sai e os vizinhos fecham o espaço; não passou: volta. Oferece "Desfazer" |
| Arrastar folha inferior ou drawer | A folha segue o dedo; o fundo escurece ou clareia na mesma proporção | Encaixa na parada mais próxima ou fecha, conforme posição e velocidade |
| Voltar por gesto de borda | A tela atual desliza e mostra a anterior por baixo | Completa ou cancela conforme a distância; use o gesto nativo, não o reescreva |
| Arrastar e soltar, reordenar | O item sobe (sombra, leve escala) e segue o ponteiro; os vizinhos abrem espaço deslizando | Pousa no lugar com transição curta; solto fora, volta à origem |
| Redimensionar painel ou coluna | O tamanho segue o ponteiro, sem animação no meio | Fica onde soltou; duplo clique volta ao padrão com transição |
| Pinça e zoom (imagem, mapa) | Escala segue os dedos a partir do ponto entre eles | Passou do mínimo ou do máximo: volta ao limite com transição |
| Atalho de teclado e Esc | O mesmo movimento do clique equivalente | Idem; teclado nunca fica com a versão seca |

- **Durante o arrasto, zero transição.** A posição vem direto do dedo; transição só ao soltar. Animar durante o arrasto cria atraso.
- **Ao soltar, mola ou curva de saída.** No nativo, mola com a velocidade do gesto (Reanimated `withSpring`, física do Flutter). Na web, transição de 200 a 300 ms com `--ease`.
- **Resistência nos limites.** Arrastar além do fim anda menos que o dedo e volta ao soltar, em vez de travar seco.
- **Todo gesto tem botão equivalente** (WCAG 2.5.1; [doc 07](07-toque-mouse-teclado.md)), e o botão dispara a mesma animação.
- **Resposta tátil no app nativo** ao passar de um limite ou concluir uma ação, discreta e pela API da plataforma.
- **Na web:** `touch-action` para o navegador não disputar o gesto, `overscroll-behavior` para a rolagem não vazar, `scroll-snap` em vez de carrossel em JavaScript, Pointer Events para arrasto. **No React Native:** Gesture Handler com Reanimated. **No Flutter:** `Dismissible`, `ReorderableListView`, `DraggableScrollableSheet`, `InteractiveViewer`.
- **Movimento reduzido:** o arrasto continua seguindo o dedo (é resposta direta); some o que é automático ao soltar, que vira troca com opacidade.

## Celular, tablet e desktop

| | Celular | Tablet | Desktop |
|---|---|---|---|
| Troca de tela | Empurrão lateral ao avançar e voltar; aba troca com crossfade | Idem; em lista + detalhe, só o painel de detalhe troca | Crossfade curto do conteúdo; a moldura (menu, cabeçalho) fica parada |
| Camada | Folha sobe de baixo e acompanha o dedo ao arrastar | Folha ou painel lateral deslizando | Modal com opacidade + escala; drawer desliza da lateral |
| Resposta ao toque | Estado pressionado visível na hora (não existe hover) | Idem | Hover e pressionado |
| Distância e duração | Tela pequena, percurso curto: fique no começo da faixa | Meio da faixa | Percurso maior pode usar o fim da faixa; sistema de trabalho usa o começo |
| Gestos | A animação segue o dedo e pode ser cancelada no meio | Idem | Não se aplica |
| Desempenho | CPU fraca: só `transform` e `opacity`, teste em aparelho real | Idem | Mais folga, mesma regra |

## Para que tipo de projeto

| Tipo | Prioridade | Por quê |
|---|---|---|
| Landing page | Alta | Movimento funcional na navegação e nos formulários; o decorativo segue a skill `design` |
| E-commerce | Alta | Carrinho, filtros e checkout com retorno visível passam confiança na compra |
| SaaS | Alta | Muitas trocas de tela e de estado por sessão; sem transição parece protótipo |
| Dashboard | Alta | Movimento curto e discreto: troca de período, filtro e esqueleto sem salto |
| Sistema interno | Alta | Use o começo da faixa de duração; quem repete a ação cem vezes ao dia não pode esperar |
| App de campo | Alta | Retorno imediato ao toque confirma que o comando entrou, mesmo com rede ruim |
| Blog/conteúdo | Média | Troca de página, menu e imagem que carrega sem salto |

## Regras práticas

- **Toda mudança de estado visível tem transição.** Montar ou desmontar um bloco (`if`, renderização condicional, `display: none`) sem animar entrada e saída é o erro que deixa a tela seca.
- **Curto.** Dentro da faixa de 100 a 500 ms da NN/g; em sistema de trabalho, raramente acima de 300 ms.
- **Sair é mais rápido que entrar.** Fechar, dispensar e recolher usam a duração de baixo da faixa: a pessoa já decidiu, não a faça esperar (prática do plugin).
- **Curva, nunca linear, para o que se move.** Quem entra desacelera no fim (`ease-out`); quem sai acelera (`ease-in`). Linear só para opacidade pura e para o que gira sem parar (prática do plugin; Material 3 e Apple HIG descrevem a mesma ideia).
- **Só `transform` e `opacity`** no que se move; cor, fundo, borda e sombra podem transicionar em hover e foco. Animar `width`, `height`, `top` ou `left` refaz o layout a cada quadro ([doc 12](12-desempenho-e-rede.md)).
- **Tokens, não valor solto.** Duração e curva ficam em variáveis (`--dur-fast`, `--dur`, `--dur-slow`, `--ease`, `--ease-exit`), junto dos tokens de cor e espaço da skill `design-systems`. Todas as telas usam os mesmos.
- **O movimento tem origem.** O menu sai do botão que o abriu; o painel volta para a borda de onde veio; avançar empurra para um lado e voltar, para o outro.
- **Nunca trave a pessoa.** A interface aceita clique, toque e teclado durante a transição, e uma animação nova interrompe a anterior em vez de esperar o fim.
- **Sem salto de layout.** Esqueleto com a forma e o tamanho do conteúdo; imagem com `width` e `height`; aviso que entra empurra o resto com transição ([doc 12](12-desempenho-e-rede.md), CLS).
- **Retorno na hora.** O estado pressionado aparece no mesmo quadro do toque; o botão que envia mostra carregando no próprio botão; a lista atualiza de forma otimista quando é seguro.
- **Muitos itens: anime o grupo.** Tabela de 50 linhas entra como um bloco só. Escalonar item a item só em listas curtas (até uns 6 itens, 30 a 50 ms entre eles; prática do plugin).
- **Movimento reduzido: troque, não apague.** Com `prefers-reduced-motion: reduce`, tire deslocamento, escala, parallax e autoplay e mantenha uma opacidade curta: a pessoa pediu menos movimento, não uma tela que pisca (MDN `prefers-reduced-motion`; WCAG 2.3.3). Movimento automático por mais de 5 segundos precisa de pausa (WCAG 2.2.2).
- **Nada decorativo aqui.** Fundo animado, brilho que persegue o mouse, texto que digita sozinho: skill `design`, só em marketing.

## Erros comuns

- **Tela trocada de uma vez:** a rota muda e o conteúdo novo estoura na tela. Corrija com View Transitions ou com a transição do roteador da stack.
- **Modal e menu que aparecem e somem secos:** entrada animada, saída não. Anime as duas (`@starting-style` e `allow-discrete`, ou o estado de saída da biblioteca).
- **Spinner que pisca:** resposta em 80 ms mostra e esconde o carregando. Mantenha o conteúdo anterior e só mostre o carregando se a espera passar de algumas centenas de milissegundos (prática do plugin).
- **Conteúdo que pula:** o esqueleto tem outra altura, a imagem chega sem dimensão, o aviso empurra tudo de repente.
- **Animação longa em ação repetida:** 600 ms para abrir um menu usado o dia todo. Fique no começo da faixa.
- **Tudo anima ao mesmo tempo:** cada cartão com efeito próprio vira ruído. Um movimento por mudança.
- **Durações e curvas diferentes em cada componente:** falta de tokens.
- **Animar `height: auto` com JavaScript medindo pixel:** use `grid-template-rows: 0fr → 1fr` ou o componente de acordeão do UI kit.
- **Sem `prefers-reduced-motion`**, ou com ele desligando até a opacidade.

## O `docs/MOTION.md` do projeto

Todo projeto com tela tem um `docs/MOTION.md`, criado junto com o `ARCHITECTURE.md` (fase 3 da skill principal), antes da primeira tela. O `ARCHITECTURE.md` (ou o `README`) e o `CLAUDE.md`/`AGENTS.md` apontam para ele em uma linha. Em projeto existente sem o arquivo, crie-o na primeira tarefa com tela. Ajuste os valores e a coluna "Como" à stack; não corte linhas. Padrão novo de movimento que surgir numa tela entra no arquivo no mesmo PR.

```markdown
# Movimento e transições

Regra do projeto, sem exceção por tipo de tela: nada aparece nem some de uma vez. Toda troca de tela, toda mudança de estado e todo gesto têm transição curta e suave. Tela ou componente novo que não segue este documento não está pronto.

## Tokens

| Token | Valor | Uso |
|---|---|---|
| `--dur-fast` | 120 ms | Hover, pressionar, foco, toggle, saída de camada |
| `--dur` | 200 ms | Menu, popover, aba, entrada de conteúdo, toast, lista |
| `--dur-slow` | 280 ms | Modal, folha, drawer, troca de tela |
| `--ease` | `cubic-bezier(.2, 0, 0, 1)` | O que entra ou se move |
| `--ease-exit` | `cubic-bezier(.4, 0, 1, 1)` | O que sai |

Ficam em `<arquivo de tokens do projeto>`. Duração ou curva solta no código é erro.

## Padrões

| Situação | Como neste projeto |
|---|---|
| Troca de tela ou rota | `<View Transitions, transição do roteador ou pilha nativa>` |
| Modal, folha, drawer, menu, popover, toast | `<componente ou biblioteca>`, com entrada e saída animadas |
| Conteúdo que carrega | Esqueleto do tamanho do conteúdo, depois opacidade; sem salto de layout |
| Item que entra, sai ou muda de lugar em lista | `<como>`; os vizinhos deslizam |
| Pressionar, hover e foco | Transição pelos tokens; estado pressionado na hora |
| Gestos (deslizar, arrastar, puxar, pinça) | Segue o dedo, termina com a velocidade do gesto, pode ser cancelado, tem botão equivalente |
| Movimento reduzido | `prefers-reduced-motion`: sai o deslocamento, fica opacidade curta |

## Regras

- Só `transform` e `opacity` no que se move.
- Sair é mais rápido que entrar; nunca travar clique, toque ou teclado durante a transição.
- Efeito decorativo (fundo animado, brilho, texto que revela) só em página de marketing.
- Antes de entregar uma tela: usar o fluxo clicando e com gestos, com rede lenta e com movimento reduzido.
```

## Como conferir

Tela parada não mostra movimento. Antes de dar a tela por pronta, use-a:

1. Navegue pelo fluxo inteiro clicando e, no toque, com os gestos da tabela acima.
2. Abra e feche cada camada pelo botão, por Esc, pelo clique fora e pelo gesto.
3. Force os estados: rede lenta (esqueleto → conteúdo), erro, lista vazia, item criado e excluído.
4. Repita com `prefers-reduced-motion: reduce` ligado (emulação do navegador ou ajuste do sistema).
5. Liste na entrega as transições e os gestos da tela e os tokens usados. O que apareceu ou sumiu de uma vez volta para correção.

## Como aplicar

Tokens e base, uma vez, na folha global:

```css
:root {
  --dur-fast: 120ms; --dur: 200ms; --dur-slow: 280ms;
  --ease: cubic-bezier(.2, 0, 0, 1);      /* entra e se move: desacelera no fim */
  --ease-exit: cubic-bezier(.4, 0, 1, 1); /* sai: acelera */
}
button, a, input, select, textarea, [role="button"], tr {
  transition: background-color var(--dur-fast) var(--ease), border-color var(--dur-fast) var(--ease),
              color var(--dur-fast) var(--ease), box-shadow var(--dur-fast) var(--ease), transform var(--dur-fast) var(--ease);
}
button:active, [role="button"]:active { transform: scale(.98); }
```

Troca de tela na web. Em navegação entre páginas (MPA), uma regra de CSS; em SPA, envolva a atualização do DOM:

```css
@view-transition { navigation: auto; }
::view-transition-old(root) { animation-duration: var(--dur-fast); }
::view-transition-new(root) { animation-duration: var(--dur); }
```

```js
const trocar = (atualizar) => document.startViewTransition ? document.startViewTransition(atualizar) : atualizar();
```

A API no mesmo documento (`document.startViewTransition`) é Baseline desde outubro de 2025 (Chrome 111, Safari 18, Firefox 144). A regra `@view-transition` entre documentos funciona no Chrome e no Edge 126 e no Safari 18.2; o Firefox ainda não a suporta e carrega a página sem transição, o que é um degrau aceitável (MDN, 2026-11-27). Dê `view-transition-name` ao elemento que continua de uma tela para a outra (a capa do produto, o título) para ele se mover em vez de piscar.

Camada que entra e sai animada, sem JavaScript:

```css
dialog {
  opacity: 0; transform: translateY(8px) scale(.98);
  transition: opacity var(--dur) var(--ease-exit), transform var(--dur) var(--ease-exit),
              overlay var(--dur) allow-discrete, display var(--dur) allow-discrete;
}
dialog[open] { opacity: 1; transform: none; transition-timing-function: var(--ease); transition-duration: var(--dur-slow); }
@starting-style { dialog[open] { opacity: 0; transform: translateY(8px) scale(.98); } }
dialog::backdrop { opacity: 0; transition: opacity var(--dur) linear, overlay var(--dur) allow-discrete, display var(--dur) allow-discrete; }
dialog[open]::backdrop { opacity: 1; }
@starting-style { dialog[open]::backdrop { opacity: 0; } }
```

`@starting-style` e `transition-behavior: allow-discrete` são Baseline desde agosto de 2024 (web.dev, Baseline entry animations). A saída depende também de `overlay`, que na data daquele artigo não era Baseline: onde falta, a camada fecha sem animar. Confira o suporte atual no MDN antes de contar com a saída.

Conteúdo que chega e seção que expande:

```css
.conteudo { animation: entrar var(--dur) var(--ease) both; }
@keyframes entrar { from { opacity: 0; transform: translateY(4px); } }
.expande { display: grid; grid-template-rows: 0fr; transition: grid-template-rows var(--dur) var(--ease); }
.expande[data-aberto="true"] { grid-template-rows: 1fr; }
.expande > * { overflow: hidden; }
```

Movimento reduzido: mantém a opacidade, tira o deslocamento.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: var(--dur-fast) !important; animation-iteration-count: 1 !important; scroll-behavior: auto !important; }
  .conteudo { animation-name: aparecer; }
  dialog, dialog[open] { transform: none; }
  button:active, [role="button"]:active { transform: none; }
  ::view-transition-group(*) { animation: none; }
}
@keyframes aparecer { from { opacity: 0; } }
```

Pela stack do projeto (confira a API na documentação oficial de cada uma antes de escrever):

| Stack | Troca de tela | Camadas e listas |
|---|---|---|
| HTML e CSS, Astro, MPA | `@view-transition`; no Astro, o roteador de transições do framework | `@starting-style`, `<dialog>`, CSS acima |
| React (Vite, Next.js, React Router) | View Transitions pelo roteador do framework, quando ele oferece; senão `document.startViewTransition` | Estados `data-state` dos componentes do shadcn/ui (Radix) já trazem entrada e saída: não remova; Motion com `AnimatePresence` para o que monta e desmonta |
| Vue, Svelte | View Transitions ou as transições nativas do framework (`<Transition>`, `transition:`) | Idem, nativas do framework |
| React Native / Expo | Pilha nativa do Expo Router e do React Navigation: mantenha a animação padrão da plataforma | Reanimated (`entering`, `exiting`, `layout`) |
| Flutter | Rotas de página padrão da plataforma; `Hero` para o elemento que continua | Widgets implícitos (`AnimatedSwitcher`, `AnimatedContainer`, `AnimatedSize`) |
| Tauri, Electron | Igual à web | Igual à web |

## Combina com / alternativas

- [10-modais-folhas-e-paineis.md](10-modais-folhas-e-paineis.md): a forma de cada camada por dispositivo.
- [12-desempenho-e-rede.md](12-desempenho-e-rede.md): esqueleto, interface otimista, CLS, custo de animação.
- [13-ios-android-web.md](13-ios-android-web.md): transições nativas de cada plataforma.
- [14-acessibilidade.md](14-acessibilidade.md): movimento reduzido.
- Skills vizinhas: design-systems (tokens e estados de tela), design (efeito decorativo e bibliotecas animadas), framia (movimento no protótipo).

## Decisão rápida

**Faça**
- Transição em toda troca de tela, toda camada e todo bloco que entra ou sai.
- Gesto que segue o dedo, termina com a velocidade do gesto e pode ser cancelado.
- Tokens de duração e curva; 100 a 300 ms; sair mais rápido que entrar.
- `transform` e `opacity`; estado pressionado na hora; esqueleto sem salto.
- Opacidade curta no lugar do movimento com `prefers-reduced-motion`.

**Evite**
- Conteúdo que aparece ou some de uma vez.
- Animação longa, decorativa ou escalonada em tela de trabalho.
- Travar o clique durante a transição.
