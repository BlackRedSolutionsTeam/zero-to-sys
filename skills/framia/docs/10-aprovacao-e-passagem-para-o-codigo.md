# Aprovação e passagem para o código

> Mostrar o protótipo ao cliente, ajustar até o ok e levar para o repositório o que cada fase seguinte usa: tokens, componentes, telas, modelo de dados, contrato da API e requisitos.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/share, https://framia.com.br/pt-br/docs/branches, https://framia.com.br/pt-br/docs/import-export e https://framia.com.br/pt-br/docs/spec-to-code |
| **Categoria** | Entrega |
| **Ferramentas do MCP** | `create_share_link`, `record_prototype`, `export_layers`, `create_branch`, `list_branches`, `diff_branch`, `create_comment`, `get_design_system`, `export_frame_html`, `export_openapi`, `get_document`, `get_requirement`, `check_criteria` |
| **Verificado em** | 2026-11-26 |

## Mostrar ao cliente

| Jeito | Como | Quando |
|---|---|---|
| Apresentar ao vivo | **Apresentar** no editor, com **Ver como** para cada perfil | Reunião: o cliente clica, o time anota |
| Link de compartilhamento | `create_share_link` com `pageIds` ou `frameIds`; no editor, **Compartilhar** → **Criar link** | Cliente sem conta. Público, só leitura, cópia congelada, **vale 30 minutos** |
| Vídeo do fluxo | `record_prototype` com os passos | Mandar por mensagem; fica depois que o link expira |
| Imagens ou PDF | `export_layers` em `png`, `pdf` ou `zip` | Anexar a proposta ou a ata |
| Convite como Leitor | **Convidar** no editor | Cliente que vai acompanhar e comentar |

O link de compartilhamento não leva comentários nem memória e mostra a branch aberta como estava na criação. Como vale 30 minutos, gere na hora de mostrar; para aprovação com calma, use vídeo, PDF ou convite.

Peça o ok por fluxo, não por tela: "o agendamento, do início ao fim, é isso?". Registre o que foi aprovado e o que mudou com `save_decision` e no `README` do repositório.

## Ajustes em branch

Uma branch é uma cópia do projeto inteiro: telas, banco, enums, memória. A **Principal** não muda até alguém mesclar.

- `create_branch` para uma rodada de ajustes ou uma alternativa de visual; `diff_branch` mostra o que mudou e os conflitos.
- **Quem mescla é sempre uma pessoa**, no editor: **Revisar e mesclar** → **Mesclar N mudanças em Principal**. Em conflito, **Manter a branch** ou **Manter Principal**.
- Protótipo ainda em montagem, sem ninguém aprovando: trabalhe direto na Principal. Branch entra depois da primeira aprovação.

## O que cada fase leva

| Sai do Framia | Como pegar | Vai para | Fase seguinte |
|---|---|---|---|
| Tokens e temas | `get_design_system` com `includeCss` | Folha de tokens do app (variáveis CSS, tema do Tailwind ou do UI kit) | `design-systems`, `design` |
| Componentes | `get_design_system` com `slug` | Componentes reescritos no UI kit da stack, com os mesmos nomes e variantes | `design` |
| Telas | `export_frame_html` (página completa) ou `get_frame` com `includeCode` | Referência de estrutura, medidas e textos de cada tela | `user-experience`, `design-systems` |
| Formatos e dispositivos | `get_project`, campo `layout` | Dispositivos que o app atende | `user-experience`, `store-targets` |
| Fluxos | `get_flow_page` | Diagrama em `docs/` e a ordem das telas | `product`, `architecture` |
| Banco e enums | Vistas **SQL**, **DBML** ou **Mermaid** no editor (**Baixar**); `get_document` pelo MCP | Diagrama no `ARCHITECTURE.md` e base da primeira migration | `data` |
| Rotas | `export_openapi` | `docs/openapi-alvo.yaml`, o contrato que o back implementa | `api` |
| Perfis de acesso | `get_document` | Papéis e permissões base | `security` |
| Requisitos | `get_requirement` | Conferência de cada item do `BACKLOG.md` | Construção |
| Tamanho real do sistema | Contagem de telas, tabelas e rotas | Peso da stack e da infra | `stacks`, `infra` |

Os links de exportação (`export_layers` com `output: urls`, `export_frame_html`) valem 30 minutos: baixe na hora.

### Regras da passagem

- **Tela exportada é referência, não código do app.** O HTML do frame mostra estrutura, medidas e textos; a tela do app é escrita nos componentes da stack. Não cole o HTML exportado no projeto.
- **Tokens com os mesmos nomes.** `--color-primary` no Framia é `--color-primary` no app; mudar a marca depois é mudar um lugar em cada lado.
- **SQL do Framia não é migration.** A migration sai do ORM; o diagrama diz o que ela precisa conter.
- **OpenAPI do Framia é o alvo.** Depois que o back existe, o contrato vivo é o gerado do código.
- **Registre onde está.** No `README` (ou `ARCHITECTURE.md`): o link do projeto no Framia e a data da aprovação. No `CLAUDE.md`: "telas, banco e rotas de referência estão no projeto X do Framia; leia o requisito com `get_requirement` antes de implementar um item". O link do projeto pode ir para o repositório; o **link do MCP nunca**.

## Na construção

Cada item do backlog usa o Framia assim:

1. `get_requirement` com o número do item: história, critérios, telas e rotas.
2. Leia a tela e os estados dela; implemente dados, back e tela na ordem da skill principal.
3. Teste de verdade. Então `check_criteria` com os ids dos critérios que passaram.
4. Mudou algo em relação ao desenho (coluna, rota, campo)? Atualize o Framia no mesmo item, para o protótipo não mentir.

## Quando o protótipo deixa de mandar

| Assunto | Antes do código | Depois do código |
|---|---|---|
| Visual e tokens | Framia | Framia para telas novas; o app para o que já existe |
| Banco | Framia | Migrations |
| API | Framia | OpenAPI gerado do código |
| Escopo e critérios | `BACKLOG.md` | `BACKLOG.md` |

Tela nova ou mudança grande de fluxo volta ao Framia antes do código, numa branch. Ajuste pequeno vai direto no código e é refletido no Framia quando alterar tela, coluna ou rota.

## Quando é ruim

- **Começar o código sem o ok:** o protótipo existe para o cliente errar barato.
- **Mandar o link e esperar dias:** ele expira em 30 minutos.
- **Aprovar tela por tela:** o cliente aprova botões e não vê o fluxo quebrado.
- **Esquecer o Framia depois da fase:** em um mês o protótipo descreve outro sistema, e o próximo agente implementa pelo desenho errado.

## Combina com

- [Requisitos e vínculos](09-requisitos-e-vinculos.md): o que guia cada item.
- [Onde registrar](../../product/docs/07-onde-registrar.md): o que vai no `README` e no `CLAUDE.md`.
- [Cliente gerado no front](../../api/docs/08-cliente-gerado-no-front.md): o cliente tipado, depois que o OpenAPI sai do código.
