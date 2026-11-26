# API e perfis

> Desenhar as rotas da API a partir das tabelas, dizer quem pode chamar cada uma, ligar as telas às rotas e sair com o OpenAPI.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/api e https://framia.com.br/pt-br/docs/profiles |
| **Categoria** | Contrato |
| **Ferramentas do MCP** | `generate_endpoints`, `create_api_group`, `create_endpoint`, `update_endpoint`, `delete_endpoint`, `list_endpoints`, `get_endpoint`, `link_endpoint_call`, `unlink_endpoint_call`, `export_openapi`, `create_access_profile`, `update_access_profile`, `create_access_rule`, `update_access_rule` |
| **Verificado em** | 2026-11-26 |

## O que é

Em **Produto** → **API**, o Framia guarda o desenho das rotas: método, caminho, campos da consulta e do corpo ligados às colunas, respostas, quem pode chamar e em que tela é usada. Não há servidor: o Framia não roda nem chama a API. A vista **Testar** chama do navegador da pessoa uma URL que ela informar, e o CORS pode bloquear.

Perfis de acesso são os tipos de usuário do sistema (Dono, Administrador, Membro, Cliente). Eles servem a duas coisas: restringir rotas e dizer o que cada perfil vê em cada tela.

## Passo a passo

1. **Perfis primeiro.** `create_access_profile` para cada papel levantado na `product`. Os nomes são os do cliente.
2. **Gere das tabelas.** `generate_endpoints` com `tableIds` e `language` cria listar, buscar, criar, mudar e apagar de cada tabela. Gere só para as tabelas que o MVP expõe.
3. **Corte.** `delete_endpoint` no que o MVP não usa: tabela de ligação e de auditoria raramente têm rota própria.
4. **Acrescente as ações fora do CRUD** com `create_endpoint`: `POST /appointments/:id/cancel`, login, webhook. `:id` marca parâmetro no caminho.
5. **Ajuste cada rota** com `update_endpoint`: `summary`, `description`, `query`, `body`, `responses` (status, descrição e código de erro), `isPublic` ou `profileIds`. As listas vão inteiras no `patch`.
6. **Agrupe** por recurso com `create_api_group`.
7. **Ligue as telas.** `link_endpoint_call` com `layerId`, `endpointId` e `trigger`: `open` para o que a tela carrega ao abrir, `action` para o que um botão dispara (com `elementId`).
8. **Confira** com `list_endpoints` e, numa rota, `get_endpoint`: ele devolve campos, respostas, telas e requisitos resolvidos.

## Padrão das rotas

O padrão é o da skill `api`, decidido aqui e não na hora de codar:

- Recursos no plural e ações como subrecurso ([rotas, verbos e status](../../api/docs/02-rotas-verbos-e-status.md)).
- Um formato de erro só, com os mesmos códigos em todas as rotas ([formato de erro](../../api/docs/03-formato-de-erro.md)).
- Listas com paginação, filtro e ordenação iguais ([paginação e filtros](../../api/docs/04-paginacao-e-filtros.md)).
- Toda rota com quem pode chamar: **Pública** só para login, cadastro, webhook e conteúdo aberto.

O que `generate_endpoints` cria é ponto de partida: revise respostas de erro e paginação em cada rota de lista.

## Perfis nas telas

`create_access_rule` diz o que um perfil vê numa camada: `hidden` (escondido), `visible`, `disabled` (cinza, sem clique) ou `readonly`. No editor, **Ver como** troca o perfil, e **Apresentar** abre o protótipo no perfil escolhido.

Use para o que muda por papel na mesma tela (o botão "Excluir" só para o Administrador). Tela que só um perfil acessa não precisa de regra em cada elemento: registre no requisito e na rota.

## OpenAPI

- `export_openapi` com `format` `yaml` ou `json` devolve o OpenAPI 3.1 do projeto. No editor, **Exportar OpenAPI** na barra da esquerda.
- **Importar OpenAPI** (editor) aceita JSON ou YAML de até 2 MB; cada tag vira um grupo, e `x-framia-column` liga o campo à coluna. Serve a sistema que já tem API.

## Levar para o código

O OpenAPI exportado é o **contrato alvo**: o back implementa essas rotas, e os testes de contrato conferem. Depois que o código existe, a fonte passa a ser o OpenAPI gerado do código (skill `api`, [OpenAPI e documentação](../../api/docs/07-openapi-e-documentacao.md)), e o cliente tipado do front sai dele. Detalhes em [Aprovação e passagem para o código](10-aprovacao-e-passagem-para-o-codigo.md).

## Encaixe por tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS, app mobile, sistema interno | ✅ Ótimo | Front e back partem do mesmo contrato, com as telas já ligadas às rotas |
| API para parceiros | ✅ Ótimo | O contrato é o produto; perfis viram escopos |
| Site estático | ❌ Pule | Sem API |

## Quando é bom

- **Tela e rota ligadas:** dá para ver qual botão chama o quê, e achar tela sem rota e rota sem tela.
- **Permissão decidida cedo:** quem pode chamar cada rota aparece antes do primeiro `if`.
- **Front e back em paralelo:** com o contrato fechado, os dois lados andam juntos na construção.

## Quando é ruim

- **Aceitar as rotas geradas sem cortar:** cinco rotas por tabela viram superfície de ataque e trabalho que ninguém pediu.
- **Rota sem perfil:** vira pública por descuido.
- **Manter o OpenAPI do Framia como fonte depois do código:** diverge. O contrato vivo é o do código.

## Combina com

- [Banco e enums](07-banco-e-enums.md): as tabelas de onde as rotas saem.
- [Requisitos e vínculos](09-requisitos-e-vinculos.md): cada rota ligada ao requisito.
- [Skill security](../../security/SKILL.md): papéis e permissões do sistema de verdade.
