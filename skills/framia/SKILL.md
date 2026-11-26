---
name: framia
description: 'Protótipo completo do sistema no Framia pelo MCP, antes de qualquer código: conta, link do MCP no Claude, design system, telas clicáveis, fluxos, banco, API e requisitos, com aprovação do cliente e passagem para o código. Use logo depois do planejamento (product) ou quando pedirem "prototipa no Framia", "conecta o Framia", "desenha as telas antes de programar".'
---

# framia

O [Framia](https://framia.com.br/pt-br/docs) é uma mesa de design multiusuário em que o agente, pelo MCP, monta o sistema inteiro **desenhado**: telas em HTML, protótipo clicável, fluxos, banco de dados, rotas da API, requisitos e design system. Nada roda: é o desenho do sistema, não o sistema.

Esta skill é a **primeira execução depois do planejamento**. Com o escopo e o backlog da skill `product` em mãos, o sistema é prototipado no Framia e aprovado pelo cliente antes de escolher stack e antes de escrever a primeira linha de código. O que sai daqui alimenta as fases seguintes: os tokens e os componentes viram o design system do app, o diagrama vira o modelo de dados, o OpenAPI vira o contrato da API e os requisitos viram a conferência de cada item do backlog.

## Como usar esta skill

1. **Confira a conexão.** Chame `list_workspaces`. Se as ferramentas `mcp__framia__*` não existirem ou a chamada falhar, pare e conduza o usuário pelo [doc 01](docs/01-conta-equipe-e-planos.md) (conta) e pelo [doc 02](docs/02-conectar-o-mcp.md) (link do MCP). O agente não cria a conta nem o link: quem faz é a pessoa.
2. **Leia o planejamento.** `README`, `BACKLOG.md` e `docs/regras-de-negocio.md` (skill `product`). Sem escopo aprovado, volte à `product`: esta skill não inventa funcionalidade.
3. **Crie o projeto** de um modelo, quando o negócio bate com um, ou em branco; escolha o design system inicial e a organização das telas ([doc 03](docs/03-comecar-o-projeto.md)). Mostre a escolha e espere o ok: projeto conta no plano.
4. **Feche o design system antes da primeira tela:** tokens da marca, temas, fontes, componentes e as regras que os agentes seguem ([doc 04](docs/04-design-system.md)). Layout de cada tipo de tela vem da skill `design-systems`; dispositivos, da `user-experience`.
5. **Desenhe o banco e os enums** a partir das regras de negócio ([doc 07](docs/07-banco-e-enums.md)), com os critérios da skill `data`.
6. **Gere e ajuste as rotas da API** a partir das tabelas e crie os perfis de acesso ([doc 08](docs/08-api-e-perfis.md)), com os critérios da skill `api`.
7. **Monte as telas do fluxo principal**, uma por vez, por seções, com os estados vazio, carregando, erro e sem permissão, e confira cada uma renderizada ([doc 05](docs/05-telas-e-prototipo.md)).
8. **Ligue as telas num protótipo clicável** e desenhe o fluxo de cada jornada ([doc 05](docs/05-telas-e-prototipo.md) e [doc 06](docs/06-fluxos.md)).
9. **Registre os requisitos** do backlog como REQ-n, ligados às telas, rotas e fluxos, e vincule os campos das telas às colunas ([doc 09](docs/09-requisitos-e-vinculos.md)). Feche com `get_coverage`: nenhuma tela ou rota do MVP sem requisito.
10. **Mostre ao cliente e colha o ok** (apresentação, link de 30 minutos ou vídeo do protótipo) e ajuste numa branch ([doc 10](docs/10-aprovacao-e-passagem-para-o-codigo.md)).
11. **Passe para o código.** Exporte OpenAPI e HTML das telas, leia tokens e componentes, baixe o SQL ou DBML, e registre no repositório onde está o projeto do Framia ([doc 10](docs/10-aprovacao-e-passagem-para-o-codigo.md)). Só então seguem `store-targets`, `stacks` e as demais fases.

## Quanto aprofundar

| Projeto | Telas | Banco e API | Fluxos e requisitos |
|---|---|---|---|
| Site de conteúdo, landing | Todas as páginas, em desktop e celular | Pule, salvo formulário com dados | Um fluxo até a conversão; requisitos só de formulário e integração |
| MVP de SaaS | Fluxo principal completo e uma tela de cada tipo (lista, formulário, detalhe, configuração) | Tabelas e rotas do MVP | Um fluxo por jornada; um REQ por item do backlog |
| SaaS em crescimento, sistema corporativo | Todas as telas do escopo, por perfil de acesso | Modelo completo, com perfis nas rotas | Fluxos com aprovações; cobertura total |
| App mobile | Todas, no formato Mobile; Tablet se o app roda em tablet | Tabelas e rotas do MVP | Fluxos com offline e notificação anotados |
| API, worker | Pule | Tabelas, enums e rotas completos | Fluxo da sequência de chamadas; um REQ por operação |
| CLI, biblioteca | Pule a skill | | |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Conta, equipe e planos | [docs/01-conta-equipe-e-planos.md](docs/01-conta-equipe-e-planos.md) | Cadastro, equipes, papéis e os limites de cada plano |
| Conectar o MCP | [docs/02-conectar-o-mcp.md](docs/02-conectar-o-mcp.md) | Criar o link do MCP e ligar no Claude Code, no app do Claude e no Codex |
| Começar o projeto | [docs/03-comecar-o-projeto.md](docs/03-comecar-o-projeto.md) | Modelo ou em branco, design system inicial, organização das telas |
| Design system | [docs/04-design-system.md](docs/04-design-system.md) | Tokens, temas, fontes, componentes, memória e regras |
| Telas e protótipo | [docs/05-telas-e-prototipo.md](docs/05-telas-e-prototipo.md) | Frames de HTML por seções, estados, conferência e protótipo clicável |
| Fluxos | [docs/06-fluxos.md](docs/06-fluxos.md) | Fluxograma de cada jornada, ligado às telas |
| Banco e enums | [docs/07-banco-e-enums.md](docs/07-banco-e-enums.md) | Tabelas, colunas, relações, enums e exportação em SQL, DBML e Mermaid |
| API e perfis | [docs/08-api-e-perfis.md](docs/08-api-e-perfis.md) | Rotas geradas das tabelas, quem pode chamar, telas que chamam, OpenAPI |
| Requisitos e vínculos | [docs/09-requisitos-e-vinculos.md](docs/09-requisitos-e-vinculos.md) | REQ-n com critérios, ligações, cobertura e campo ligado à coluna |
| Aprovação e passagem para o código | [docs/10-aprovacao-e-passagem-para-o-codigo.md](docs/10-aprovacao-e-passagem-para-o-codigo.md) | Mostrar ao cliente, branches e o que cada fase seguinte leva do Framia |

## Checklist antes de sair para o código

- [ ] O projeto existe e o link dele está no `README` ou no `CLAUDE.md` do repositório (`grep -n 'framia' README.md CLAUDE.md`).
- [ ] Tokens da marca, tema e fontes definidos, e as regras de uso escritas (`get_design_system`).
- [ ] Toda tela do fluxo principal existe em cada formato do projeto, sem casa vazia (`get_project`, campo `layout`).
- [ ] Cada tela foi conferida renderizada, sem conteúdo saindo do frame (`render_layer`).
- [ ] As telas têm os estados vazio, carregando, erro e sem permissão onde isso se aplica.
- [ ] O protótipo abre na primeira tela e o fluxo principal se clica até o fim (`get_prototype`).
- [ ] Cada jornada tem um fluxo com os caminhos de erro (`get_flow_page`).
- [ ] Tabelas, relações e enums cobrem as regras de negócio; multiempresa decidida.
- [ ] Toda rota tem quem pode chamar, e as telas estão ligadas às rotas que chamam (`list_endpoints`, `get_endpoint`).
- [ ] Cada item do `BACKLOG.md` tem um REQ com critérios, ligado a tela e rota, e a cobertura não mostra sobra (`list_requirements`, `get_coverage`).
- [ ] O cliente viu o protótipo e aprovou; os ajustes pedidos estão na branch principal.
- [ ] OpenAPI, SQL ou DBML e os tokens foram levados para o repositório, nos lugares do [doc 10](docs/10-aprovacao-e-passagem-para-o-codigo.md).

## Regras de uso

- **Framia antes de código.** Nenhuma pasta de app, migration ou componente é criado antes do protótipo aprovado. A única exceção é o que o usuário mandar fazer fora de ordem.
- **O link do MCP é uma senha.** Quem tem o link age como a pessoa. Vai em `--scope user`, nunca em `.mcp.json` versionado, em commit, em issue ou em print. Vazou: revogue em **Ajustes → Chaves MCP**.
- **`get_project` antes de editar.** Ele traz as branches e o `layout` (como o projeto organiza as telas). Quando a pessoa mandar o link do editor, passe-o como `url`: ele diz a branch, a página e o frame abertos.
- **Tela pela organização do projeto.** Crie telas com `create_screen` e frames com `screenId` e `format`, não com `x` e `y` soltos.
- **Monte por seções.** `create_frame_from_html` com os estilos e a primeira seção, depois um `append_frame_html` por seção, com `done: true` na última. As pessoas veem a tela nascer.
- **Mude a parte, não a tela.** `find_elements` e `update_element` para um trecho; `replace_in_frame` para uma regra de CSS ou um texto em várias telas; `update_frame` quando muda marcação, CSS e script juntos.
- **Estado e tamanho são cópia.** Menu aberto, erro, vazio ou outro dispositivo é um `duplicate_frame` com as mudanças, não uma tela nova do zero.
- **Cor e espaço vêm dos tokens.** Nada de cor solta no HTML da tela: use `var(--nome)` e os componentes da biblioteca.
- **Confira renderizado.** Depois de cada tela, `render_layer`; ajuste a altura quando o conteúdo sobra ou falta.
- **Só marque o que testou.** `check_criteria` é assinado por quem marcou; no protótipo, critério de aceite fica aberto até o código existir.
- **Quem decide é uma pessoa.** Mesclar branch, aprovar componente salvo por agente e aceitar regra proposta são ações humanas no editor.
- **Respeite o limite.** O MCP aceita 300 chamadas por minuto; o plano limita projetos, páginas, tabelas e componentes. No limite, pare e avise, não contorne.
- **Fronteiras.** Esta skill não decide o escopo (`product`), o critério de modelagem (`data`), o padrão das rotas (`api`), o layout de cada tipo de tela (`design-systems`) nem a stack (`stacks`). Ela aplica essas decisões no Framia e devolve o protótipo.

## Quando a lista não cobre

Importar telas de um arquivo do Figma (`import_figma`), capturar as telas de um app que já roda (`create_capture_key`, `import_webpage`) e desenhar a partir do código de um repositório vinculado (`repo_screens`) servem a projeto existente e estão na documentação oficial (Importar do Figma, Captura do app, Repositórios). O assistente dentro do editor, que usa chave de API do provedor, também fica fora: esta skill trabalha pelo MCP.

## Validade dos dados

Passos, nomes de botões, ferramentas, limites e preços foram conferidos em framia.com.br/pt-br/docs em 2026-11-26. O Framia muda rápido: confira a linha "Verificado em" de cada documento e a página oficial antes de afirmar preço ou limite.
