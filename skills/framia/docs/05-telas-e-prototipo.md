# Telas e protótipo

> Montar cada tela como um frame de HTML, por seções, com os estados, conferir renderizada e ligar tudo num protótipo clicável.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/html-frames, https://framia.com.br/pt-br/docs/prototype e https://framia.com.br/pt-br/docs/mcp-tools |
| **Categoria** | Telas |
| **Ferramentas do MCP** | `create_screen`, `create_frame_from_html`, `append_frame_html`, `duplicate_frame`, `find_elements`, `get_frame_elements`, `get_element_code`, `update_element`, `insert_element`, `replace_in_frame`, `update_frame`, `get_frame`, `render_layer`, `upload_file`, `set_prototype_links`, `set_prototype_start`, `get_prototype`, `record_prototype` |
| **Verificado em** | 2026-11-26 |

## O que é um frame de HTML

Um frame que guarda uma página HTML completa, com CSS e JS. Cada elemento é uma camada: dá para ler, selecionar e trocar um elemento sem reescrever a tela. O HTML roda isolado, sem sessão, cookies nem rede; as exceções são Google Fonts, jsDelivr, Iconify, Simple Icons e Fontshare.

## Ordem das telas

Siga o fluxo principal da `product`, na ordem do backlog. A primeira tela de cada tipo (lista, formulário, detalhe, painel) vai ao usuário antes das outras do mesmo tipo: corrigir uma é barato, corrigir dez não.

## Montar uma tela

1. `create_screen` com o nome da tela e o `flowName` da jornada. Ele cria a página e a casa de cada formato.
2. Escolha o layout pelo tipo de tela na skill `design-systems`.
3. `create_frame_from_html` com `screenId` e `format`, os estilos e **só a primeira seção**. Em tela que segue outra, `copyStyleFrom` leva os estilos e as fontes do frame de origem.
4. Um `append_frame_html` por seção seguinte, na ordem da página, com `done: true` na última.
5. `render_layer` para conferir. Ele avisa se o conteúdo sai do frame (ajuste `h` para `suggestedH`) ou sobra espaço (`minH` bem menor que `h`: ajuste para `minH`).
6. Guarde os ids que as ferramentas de escrita devolvem em `elements`, em vez de ler o frame de novo.

No HTML:

- Cor, espaço, raio e fonte por `var(--token)`; blocos repetidos pelos componentes da biblioteca ([doc 04](04-design-system.md)).
- `data-name` ou `aria-label` nos elementos que serão ligados, vinculados ou editados depois.
- Texto real do negócio, nas palavras do cliente, e dados plausíveis. Nada de "Lorem ipsum".
- Imagem: `upload_file` sem `data` devolve o link para enviar do disco e o `path` para usar no HTML.

## Mudar uma tela

| Mudança | Ferramenta |
|---|---|
| Achar um elemento pelo texto, rótulo ou tag | `find_elements` |
| Trocar um elemento | `update_element` |
| Pôr marcação antes, depois ou dentro de um elemento | `insert_element` |
| Trocar uma regra de CSS ou uma palavra, em uma ou várias telas | `replace_in_frame` (com `layerIds` para várias) |
| Mudar marcação, CSS e script de uma vez | Um `update_frame` |
| Ler só uma parte do código | `get_frame` com `codePart`: `style`, `body`, `head` ou `script` |

Não reescreva a tela para mudar um botão.

## Estados e formatos

Outro estado da mesma tela (vazio, carregando, erro, sem permissão, menu aberto, diálogo) e outro formato (Tablet, Mobile) são **um `duplicate_frame`** que já leva as mudanças (`elements`, `insert`, `edits`, `css`, `js`). Use `below` ou `rightOf` com o id de um frame para posicionar, ou `screenId` e `format` para cair na casa certa.

- Estados que toda tela com dados precisa: vazio, carregando, erro. Tela com permissão: sem permissão. Detalhes em [estados de tela](../../design-systems/docs/13-estados-de-tela.md).
- Formato menor não é a tela grande encolhida: siga a skill `user-experience` para navegação, tabelas e formulários.
- Conferir vários frames de uma vez: `render_layer` com `layerIds` devolve uma folha de contato. `actions` (clicar, digitar, rolar) mostra a tela depois da interação; `image: false` devolve só o relatório.

## Protótipo clicável

Telas viram protótipo por links: o clique num elemento abre outro frame de nível principal.

1. Com duas ou mais telas de um fluxo prontas, **um** `set_prototype_links` liga todas, por nome: cada link é `{ layerId, elementName, toFrameName }` (ou `toFrameId`). `elementName` é o que o controle diz, como "Confirmar".
2. Nome repetido no mesmo controle (um "Criar conta" no topo e outro no rodapé) liga todas as cópias. Nome que serve a elementos diferentes é recusado com os candidatos: passe `elementId`, que `find_elements` com `clickable` devolve.
3. `set_prototype_start` escolhe a primeira tela de cada página.
4. `get_prototype` mostra todos os links e os inícios: confira que o fluxo principal não tem beco sem saída.

No HTML escrito pelo agente, `data-framia-link="<id do frame>"` é o mesmo link, e `data-framia-link="name:<nome do frame>"` liga uma tela que ainda não existe. Ligue o controle de verdade (o botão, a aba, a linha), não o invólucro.

`record_prototype` grava um vídeo do fluxo sendo clicado (WebM, até 50 cliques e cerca de 1 minuto). No editor, **Apresentar** abre o protótipo, com **Ver como** para trocar de perfil de acesso.

## Encaixe por tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS, sistema interno, painel | ✅ Ótimo | Muitas telas do mesmo tipo; o protótipo fecha o visual e o fluxo antes do código |
| App mobile | ✅ Ótimo | O cliente clica no formato do celular antes de existir build |
| Landing, site de conteúdo | ✅ Ótimo | A página aprovada vira o HTML de referência |
| API, worker | ❌ Pule | Sem tela; fique com banco, rotas e fluxos |

## Quando é ruim

- **Tela inteira num `create_frame_from_html` só:** ninguém acompanha, e um erro no fim perde tudo.
- **Só o caminho feliz:** sem os estados de vazio e erro, o protótipo aprova uma tela que o sistema quase nunca mostra assim.
- **Protótipo sem links:** o cliente vê telas soltas e não percebe o passo que falta.
- **Pixel perfeito antes do fluxo:** primeiro o fluxo clicável inteiro, depois o acabamento.
- **Não conferir renderizado:** conteúdo cortado só aparece para quem abre o editor.

## Combina com

- [Design system](04-design-system.md): tokens e componentes usados aqui.
- [Fluxos](06-fluxos.md): o fluxograma de cada jornada, ligado a estas telas.
- [Requisitos e vínculos](09-requisitos-e-vinculos.md): cada tela ligada ao requisito e às colunas.
- [Design systems](../../design-systems/SKILL.md) e [Experiência do usuário](../../user-experience/SKILL.md): layout por tipo de tela e adaptação por dispositivo.
