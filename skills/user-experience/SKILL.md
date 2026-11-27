---
name: user-experience
description: 'Adapta cada tela a celular, tablet e desktop: contexto de uso, pontos de quebra, navegação, toque e teclado, formulários, tabelas, modais e folhas, densidade, transições suaves e diferenças entre iOS, Android e web. Use quando pedirem "deixar responsivo", "versão mobile", "como fica no celular" ou "a tela está seca".'
---

# user-experience

Guia de decisão para adaptar a experiência a celular, tablet e desktop. A mesma tela não é a mesma tarefa nos três: muda como a pessoa segura, com o que aponta, quanto tempo fica e quanta informação cabe. Cada tema tem um documento em `docs/` com a tabela comparativa dos três dispositivos, regras com números e fonte, erros comuns e código.

## Como usar esta skill

1. **Descubra onde o sistema será usado** antes de desenhar: quais dispositivos, qual é o principal e em que situação (mesa, rua, balcão, campo). Se o resumo do projeto não diz, pergunte. Sem resposta, assuma que os três importam e que o celular é o mais restrito.
2. **Leia [docs/01-contexto-de-uso.md](docs/01-contexto-de-uso.md)** e o documento do dispositivo principal ([02](docs/02-mobile.md), [03](docs/03-tablet.md) ou [04](docs/04-desktop.md)).
3. **Escolha os documentos de tema pela tabela abaixo**, conforme o que a tela tem (navegação, formulário, tabela, modal).
4. **Projete do menor para o maior.** Resolva a tela em 360 px primeiro; depois use o espaço extra do tablet e do desktop para mostrar mais, não só para esticar.
5. **Aplique pelas seções "Regras práticas" e "Como aplicar"** de cada documento.
6. **Dê movimento a toda troca de tela e de estado** pelo [documento 16](docs/16-movimento-e-transicoes.md). Vale para toda tela, de qualquer tipo de sistema, e para todo gesto, do toque ao arrastar; não é acabamento para depois. Leia esse documento em toda tarefa com tela, mesmo que o pedido não fale de animação. Se o projeto ainda não tem o `docs/MOTION.md`, crie-o pelo modelo do documento antes de montar a tela; se tem, siga-o.
7. **Confira nos três tamanhos**: 360 px, cerca de 768 px e 1280 px ou mais, com toque e com teclado.
8. **Explique ao usuário em uma ou duas frases** o que muda em cada dispositivo e por quê.

## Qual documento ler

| A tela tem ou o pedido envolve | Documento |
|---|---|
| Decidir para quais dispositivos projetar e qual é o principal | [01 Contexto de uso](docs/01-contexto-de-uso.md) |
| Tela usada principalmente no celular | [02 Mobile](docs/02-mobile.md) |
| Tablet (ponto de venda, campo, leitura) ou largura intermediária | [03 Tablet](docs/03-tablet.md) |
| Tela de trabalho usada o dia todo no computador | [04 Desktop](docs/04-desktop.md) |
| "Deixa responsivo", pontos de quebra, grade | [05 Breakpoints e layout](docs/05-breakpoints-e-layout.md) |
| Menu, abas, barra lateral, voltar | [06 Navegação](docs/06-navegacao.md) |
| Botões, hover, gestos, atalhos, foco | [07 Toque, mouse e teclado](docs/07-toque-mouse-teclado.md) |
| Formulário, cadastro, checkout, login | [08 Formulários](docs/08-formularios.md) |
| Tabela, lista grande, filtros, gráficos | [09 Tabelas e dados](docs/09-tabelas-e-dados.md) |
| Modal, drawer, folha inferior, tooltip, toast | [10 Modais, folhas e painéis](docs/10-modais-folhas-e-paineis.md) |
| Tamanho de fonte, espaçamento, tela "apertada" ou "vazia" | [11 Tipografia e densidade](docs/11-tipografia-e-densidade.md) |
| Lento no celular, rede ruim, offline | [12 Desempenho e rede](docs/12-desempenho-e-rede.md) |
| App nativo, PWA, diferenças de iOS e Android | [13 iOS, Android e web](docs/13-ios-android-web.md) |
| Acessibilidade, teclado, leitor de tela, contraste | [14 Acessibilidade](docs/14-acessibilidade.md) |
| Tradução, vários idiomas, datas e moedas | [15 Internacionalização](docs/15-internacionalizacao.md) |
| Toda tela: troca de tela, abrir e fechar, entrada de conteúdo, "está seco", "sem animação" | [16 Movimento e transições](docs/16-movimento-e-transicoes.md) |

## Resumo dos três dispositivos

| | Celular | Tablet | Desktop |
|---|---|---|---|
| Entrada | Toque, um polegar | Toque com duas mãos; às vezes teclado e caneta | Mouse e teclado |
| Sessão | Curta, com interrupção | Média | Longa e focada |
| Layout | Uma coluna, uma tarefa por tela | Duas colunas (lista + detalhe) | Várias colunas e painéis |
| Navegação | Barra inferior | Trilho lateral | Barra lateral ou topo |
| Densidade | Baixa, alvos grandes | Média | Alta, se a tarefa pede |
| Hover | Não existe | Não conte com ele | Existe; use para revelar, não para esconder o essencial |
| Camada | Folha inferior ou tela cheia | Folha ou painel lateral | Modal central ou painel lateral |
| Tabela | Vira lista de cartões ou colunas prioritárias | Menos colunas | Completa |
| Troca de tela | Empurrão lateral nativo | Só o painel de detalhe troca | Crossfade curto do conteúdo |

Os números e as fontes de cada linha estão nos documentos.

## Checklist de toda tela nova

- [ ] O dispositivo principal e os demais foram definidos e registrados no resumo do projeto (`grep -ri 'dispositivo' README.md docs`).
- [ ] A tela foi conferida em 360 px, cerca de 768 px e 1280 px ou mais (abrir no navegador com as larguras).
- [ ] Não há rolagem horizontal no celular (inspecionar a 360 px).
- [ ] O CSS base é do celular e cresce com `min-width` (`grep -rn 'max-width' src --include=*.css`).
- [ ] Nenhuma ação essencial depende só de hover ou de gesto (`grep -rn ':hover' src`; conferir se há alternativa visível).
- [ ] Alvos de toque têm o tamanho mínimo do documento 07 (inspecionar botões e links no celular).
- [ ] Cada campo tem `type`, `inputmode` e `autocomplete` certos (`grep -rn '<input' src`).
- [ ] O viewport não trava o zoom (`grep -rn 'user-scalable' .`; deve voltar vazio).
- [ ] Tabelas viram lista de cartões ou colunas prioritárias no celular, e modais viram folha ou tela cheia (abrir a tela a 360 px).
- [ ] Troca de tela, modal, menu, folha, aba e conteúdo que carrega entram e saem com transição; nada aparece ou some de uma vez (navegar pelo fluxo clicando, não só olhar a tela parada).
- [ ] Todo gesto da tela (pressionar, deslizar, arrastar, puxar, rolar) responde na hora, segue o dedo e termina com transição (usar a tela no toque, conforme a tabela de gestos do documento 16).
- [ ] O projeto tem o `docs/MOTION.md` e a tela o segue (`ls docs/MOTION.md`).
- [ ] Duração e curva vêm de tokens e `prefers-reduced-motion` troca o movimento por opacidade (`grep -rnE 'transition|animation|prefers-reduced-motion' src`).

## Regras de uso

- **Dispositivo não é largura de tela.** Decida pelo que a pessoa consegue fazer: tem hover? o ponteiro é fino ou grosso? Use `@media (hover)` e `(pointer)`, não só `min-width`.
- **Do menor para o maior.** CSS base para o celular, `min-width` para crescer. O que não cabe no celular precisa de justificativa para existir.
- **Adaptar não é esconder.** Toda tarefa possível no desktop deve ser possível no celular, mesmo que por outro caminho. Não remova função por falta de espaço: mude o componente.
- **Tablet não é celular esticado nem desktop espremido.** Use o espaço para duas colunas.
- **Nada essencial atrás de hover ou de gesto.** Tooltip, menu que só abre ao passar o mouse e ação só por deslizar precisam de alternativa visível.
- **Alvo de toque grande, com respiro.** Siga os mínimos do [documento 07](docs/07-toque-mouse-teclado.md). No desktop pode ser menor, mas não minúsculo.
- **Ação principal ao alcance.** No celular, embaixo, na zona do polegar. No desktop, perto do conteúdo que ela afeta.
- **O teclado certo para cada campo** (`type`, `inputmode`, `autocomplete`) e nunca travar o zoom do usuário (`user-scalable=no` impede quem tem baixa visão de ler; MDN, meta viewport, 2026-11-24).
- **Desktop merece densidade e atalhos.** Sistema de trabalho com botões gigantes e muito espaço vazio cansa quem usa oito horas por dia.
- **Suave sempre.** Toda troca de tela e de estado tem transição curta (100 a 300 ms), em qualquer sistema, inclusive dashboard e painel admin. Conteúdo jogado na tela de uma vez é defeito, não estilo. O que fica restrito a marketing é o efeito decorativo (skill `design`), não o movimento funcional ([documento 16](docs/16-movimento-e-transicoes.md)).
- **Teste em aparelho ou emulação real.** Redimensionar a janela do navegador não mostra teclado virtual, área segura, toque nem CPU lenta.

## Quando a lista não cobre

TV, relógio, carro, óculos de realidade mista, totem e interface por voz estão fora desta skill: têm diretrizes próprias de cada plataforma. Diga isso ao usuário e consulte a documentação oficial. Os layouts prontos por tipo de sistema ficam na skill `design-systems`; os componentes, na `design`; a escolha entre tecnologia web e nativa, na `stacks`.

## Validade dos dados

Tamanhos de alvo, pontos de quebra, limites de desempenho e suporte de navegador foram conferidos nas fontes oficiais em 2026-11-24. Cada documento diz o que não tem fonte oficial. Antes de afirmar um número decisivo, confira na fonte citada.
