# Requisitos e vínculos

> Registrar cada item do backlog como requisito com critérios de aceite, ligado às telas, rotas e fluxos, e ligar os campos das telas às colunas do banco.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/requirements, https://framia.com.br/pt-br/docs/bindings e https://framia.com.br/pt-br/docs/spec-to-code |
| **Categoria** | Rastreabilidade |
| **Ferramentas do MCP** | `create_requirement_group`, `create_requirement`, `update_requirement`, `list_requirements`, `get_requirement`, `check_criteria`, `get_coverage`, `create_binding`, `update_binding`, `delete_binding` |
| **Verificado em** | 2026-11-26 |

## O que é

Um requisito é uma história com critérios de aceite, numerada `REQ-n`, com status (A fazer, Em andamento, Pronto), prioridade e ligações com as telas, as rotas e os fluxos que o entregam. Não tem prazo nem sprint e não substitui o Jira: no editor, exporta em Markdown ou CSV.

Um vínculo (binding) registra qual coluna do banco, ou qual enum, alimenta uma camada da tela. Ele não muda o desenho: é a anotação que diz ao desenvolvedor de onde vem cada campo.

## Passo a passo

1. Um épico por módulo ou jornada: `create_requirement_group`.
2. Um requisito por item do `BACKLOG.md`: `create_requirement` com `title`, `story` (Como / quero / para), `criteria`, `priority`, `groupId`, e as ligações `layerIds`, `endpointIds` e `flowPageIds`.
3. Escreva o número do requisito no item do `BACKLOG.md` (`REQ-7`), para os dois lados se acharem.
4. Vincule os campos: `create_binding` com `layerId` e `target` (a coluna, ou o enum e o valor) em cada campo de formulário, coluna de tabela e selo de status.
5. `get_coverage`: lista as telas e as rotas sem requisito. Para cada sobra, ou falta um requisito, ou a tela ou rota está fora do escopo e sai.
6. `list_requirements` para conferir que todo item do MVP está lá.

## Critérios de aceite

Os critérios são os da `product` ([histórias e critérios de aceite](../../product/docs/04-historias-e-criterios-de-aceite.md)), copiados com o mesmo texto: verificáveis, em Dado / Quando / Então, sem "rápido" nem "fácil".

- O título da tela ligada ganha um selo como `0/3`, que fica verde quando todos os critérios são marcados.
- `check_criteria` marca critérios e assina quem marcou. **No protótipo, não marque:** critério se marca quando o código existe e o comportamento foi testado.
- A fonte dos critérios é o `BACKLOG.md`. Mudou lá, atualize o requisito no mesmo item (`update_requirement`).

## Vínculos

- Vincular de novo a mesma camada substitui o vínculo anterior.
- O vínculo de enum não muda o texto da camada: escreva o rótulo que a pessoa vê.
- Na coluna, o editor mostra "Usada por N camadas": coluna sem uso em tela nenhuma é candidata a sair do MVP; campo de tela sem coluna é coluna que faltou.
- Vincule o que carrega ou grava dado. Título, rótulo e ícone fixos não levam vínculo.

## Do requisito ao código

Na construção, cada item começa pelo requisito:

1. Pedido: "Implemente o REQ-1 do projeto X no Framia".
2. `get_requirement` com `number` devolve a história, os critérios com ids, as telas e as rotas resolvidas, com campos e respostas.
3. O agente lê a tela (`get_frame`, `export_frame_html`) e os vínculos, e implementa na stack do projeto.
4. Depois de testar de verdade, `check_criteria` com os ids do que passou. O selo vai a `3/3` e o requisito pode ir para **Pronto**.

O ciclo completo está em [Aprovação e passagem para o código](10-aprovacao-e-passagem-para-o-codigo.md).

## Encaixe por tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| MVP de SaaS, sistema interno, app | ✅ Ótimo | Um requisito por item do backlog, com tela e rota à mão |
| API, integração | ✅ Ótimo | Um requisito por operação, ligado à rota e ao fluxo |
| Landing | 🟡 Serve | Só para formulário e integração |

## Quando é bom

- **O agente recebe tudo de uma vez:** história, critérios, tela e rota numa chamada.
- **Cobertura visível:** tela sem requisito e requisito sem tela aparecem antes do código.
- **Pronto com dono:** cada critério marcado tem quem marcou.

## Quando é ruim

- **Dois backlogs:** o `BACKLOG.md` manda; o requisito no Framia é o espelho ligado às telas. Texto diferente nos dois é erro.
- **Marcar critério no protótipo:** desenho não cumpre critério de aceite.
- **Requisito sem ligação:** vira lista de desejos; ligue ao menos uma tela ou uma rota.
- **Vincular tudo:** vínculo em texto fixo polui a contagem de uso das colunas.

## Combina com

- [Backlog e ordem de construção](../../product/docs/06-backlog-e-ordem-de-construcao.md): a origem dos requisitos.
- [API e perfis](08-api-e-perfis.md) e [Telas e protótipo](05-telas-e-prototipo.md): o que o requisito liga.
- [Definição de pronto](../../quality/docs/08-definition-of-done.md): quando o critério pode ser marcado.
