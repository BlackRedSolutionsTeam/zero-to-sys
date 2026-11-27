# Design system

> Fechar tokens, temas, fontes, componentes e regras no Framia antes da primeira tela, para todas as telas saírem iguais e o app herdar o mesmo visual.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/tokens, https://framia.com.br/pt-br/docs/components e https://framia.com.br/pt-br/docs/memory |
| **Categoria** | Visual |
| **Ferramentas do MCP** | `get_design_system`, `set_design_tokens`, `edit_theme`, `set_design_system`, `save_component`, `create_component_group`, `review_component`, `delete_component`, `upload_file`, `set_guidelines`, `list_guidelines`, `get_guidelines`, `pin_reference`, `get_reference`, `save_decision`, `propose_rule` |
| **Verificado em** | 2026-11-26 |

## As peças

| Peça | O que é | Onde fica no editor |
|---|---|---|
| Tokens | Valores com nome, como `--color-primary: #2743ee` e `--space-4: 16px`; telas e componentes usam `var(--nome)` | Aba **Tokens** do painel da direita |
| Temas | Conjunto que troca alguns tokens; os demais vêm do **Padrão** | Aba **Tokens**, seção **Temas** |
| Fontes | Arquivos enviados, que viram `@font-face` na folha global | Aba **Tokens**, seção **Fontes** |
| Folha de estilos global | O CSS do projeto, com os tokens | **Editar folha de estilos e regras** |
| Regras de uso | Markdown que todo agente lê antes de desenhar | Mesma janela, aba **Regras de uso** |
| Componentes | Peças com HTML, CSS e JS próprios, usadas em várias telas | Aba **Componentes** → **Biblioteca** |
| Memória | Regras, referências de estilo e decisões da branch | Aba **Memória** |

## Passo a passo

1. `get_design_system`: veja o que o projeto já tem (o design system inicial ou o do modelo).
2. Levante a marca do cliente: cores, fonte, logotipo, raio, densidade. Sem marca, proponha uma e espere o ok.
3. `set_design_tokens`: grave cores, espaçamento, raio, tipografia e movimento (`--dur-fast`, `--dur`, `--dur-slow`, `--ease`, `--ease-exit`). Nomes pelo papel (`--color-primary`, `--color-danger`), não pela cor (`--azul`).
4. `edit_theme` com `create` para o tema escuro ou de marca, e `set_design_tokens` com `theme` para os tokens que mudam nele.
5. Fontes: `upload_file` sem `data` devolve um link para enviar o arquivo do disco; depois declare o `@font-face` na folha global. Fonte só carrega por `<link>` ou `@font-face` no HTML.
6. `set_design_system`: escreva a folha global (`globalCss`) e as regras de uso (`notes`).
7. Componentes: confira a biblioteca antes de criar. Falta um? `save_component`.
8. Depois da primeira tela aprovada, `pin_reference` nela: vira a referência de estilo das seguintes.

## Tokens e temas

- Cada tema é publicado como um bloco `[data-theme="<nome>"]`. Um frame usa o tema com `<html data-theme="noite-azul">`; sem o atributo, vale o Padrão.
- O nome do tema vira slug: "Noite Azul" vira `noite-azul`. O Padrão não se renomeia nem se apaga.
- Renomear um token troca o nome em todos os temas e na folha global, mas não no CSS dos componentes: confira os usos.
- Os valores seguem as regras da skill `design-systems` ([fundamentos](../../design-systems/docs/01-fundamentos.md)): escala de espaçamento, contraste, hierarquia tipográfica.

## Componentes

Um componente tem **Nome**, **Slug**, **Grupo**, **Tipo**, **Quando usar** (texto que pessoas e agentes leem), HTML, CSS, JS e **Variantes** (Secondary, Ghost…).

- A raiz do HTML leva `data-framia-component="<slug>"`.
- O CSS do componente guarda só o que é dele; cor e espaço vêm dos tokens.
- A tela guarda só a marcação. Mudar o componente muda todas as telas que o usam, o protótipo e a exportação.
- O Framia traz 73 modelos de componente em 15 grupos (botões, formulários, navegação, exibição de dados, feedback…). Com a biblioteca vazia, **Começar com componentes prontos** no editor.
- Componente salvo por agente entra em **Componentes para revisar**: uma pessoa marca **Está certo** ou **Precisa revisar**. O agente não aprova o próprio componente.
- Cada branch tem a sua biblioteca; mesclar leva os componentes.

Crie componente para o que se repete em três telas ou mais (botão, campo, cartão, linha de tabela, cabeçalho, menu lateral). Bloco usado numa tela só fica no HTML dela.

## Regras e memória

- **Regras de uso** (`set_design_system`, campo `notes`): o que vale para o projeto todo. Exemplo: "Botão primário só um por tela", "Tabela com mais de 6 colunas vira cartão no celular".
- **Documentos de regras** (`set_guidelines`): até 20 por branch, 24.000 caracteres cada. Use um por assunto: tom de texto, formulários, tabelas.
- **Referências** (`pin_reference`): até 12 frames por branch, fixados como exemplo de estilo.
- **Decisões** (`save_decision`): "o cliente pediu mais espaço em branco". Ficam na memória da branch.
- **Regra proposta** (`propose_rule`): o agente propõe, com o motivo e em que se baseou; só vale quando uma pessoa clica em **Adicionar às regras**. Uma proposta aberta por vez.

Quando o usuário corrige o visual ("menos sombra", "título menor"), aplique e registre com `save_decision`; se a correção vale para todas as telas, `propose_rule`.

## Levar para o código

O Framia não exporta tokens em JSON nem componentes como código de framework. O caminho:

- `get_design_system` com `includeCss`: a folha global, com os tokens em variáveis CSS e os blocos de tema. Ela é a fonte dos tokens do app.
- `get_design_system` com `slug`: HTML, CSS e variantes de um componente, para reescrever no UI kit da stack.
- Detalhes em [Aprovação e passagem para o código](10-aprovacao-e-passagem-para-o-codigo.md).

## Quando é ruim

- **Primeira tela antes dos tokens:** cada tela sai com um azul diferente, e arrumar depois é tela por tela.
- **Cor escrita no HTML da tela:** trocar a marca deixa de ser uma mudança de token.
- **Componente para tudo:** biblioteca de 80 peças que ninguém acha; no Starter, o limite é 10.
- **Regra na conversa:** o próximo agente não vê. Regra vai para as regras de uso ou para a memória.

## Combina com

- [Design systems](../../design-systems/SKILL.md): a estrutura de cada tipo de tela e as medidas.
- [Design](../../design/SKILL.md): o UI kit e os ícones em que os componentes serão reescritos no app.
- [Telas e protótipo](05-telas-e-prototipo.md): o passo seguinte.
