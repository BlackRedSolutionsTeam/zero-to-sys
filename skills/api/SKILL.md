---
name: api
description: 'Define o contrato da API entre front e back: REST, RPC ou GraphQL, rotas e status, formato de erro, paginação e filtros, versionamento, idempotência, OpenAPI e cliente gerado. Use quando for criar ou mudar rotas ou pedirem "desenhar a API" ou "padrão de erro".'
---

# api

Guia para que front e back conversem por um contrato único, previsível e verificável. Sem padrão, cada rota nasce de um jeito: erro em formatos diferentes, lista sem limite, campo renomeado que quebra a tela. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos do agendamento de uma clínica.

## Como usar esta skill

1. **Descubra quem consome a API:** só o front do próprio sistema, um app mobile em loja, parceiros ou outros serviços. Isso decide o estilo e o quanto versionar ([doc 01](docs/01-rest-rpc-ou-graphql.md)).
2. **Defina as rotas a partir das histórias** do `BACKLOG.md` (skill `product`): recursos no plural, ações fora do CRUD como `POST /appointments/{id}/cancel` ([doc 02](docs/02-rotas-verbos-e-status.md)).
3. **Fixe o formato de erro e o de lista** antes da primeira rota ([doc 03](docs/03-formato-de-erro.md) e [doc 04](docs/04-paginacao-e-filtros.md)). É o que mais custa mudar depois.
4. **Proteja o que não pode repetir:** pagamento, agendamento e webhook ([doc 06](docs/06-idempotencia-e-retries.md)).
5. **Gere o OpenAPI do código** e publique a documentação ([doc 07](docs/07-openapi-e-documentacao.md)).
6. **Gere o cliente tipado do front** a partir do OpenAPI ([doc 08](docs/08-cliente-gerado-no-front.md)).
7. **Peça os testes** de status, erro e contrato à skill `quality` ([doc 04 dela](../quality/docs/04-testes-de-api-e-contrato.md)).

## Qual estilo usar

| Quem consome | Estilo recomendado | Observação |
|---|---|---|
| Só o front do mesmo repositório, em TypeScript | RPC tipado (tRPC, Hono RPC, server actions) ou REST | Menos código; trocar de estilo depois custa |
| Front separado do back, ou back em outra linguagem | REST com OpenAPI e cliente gerado | Padrão do plugin |
| App mobile em loja | REST com OpenAPI, versionado | Usuário demora a atualizar o app |
| Parceiros e terceiros | REST com OpenAPI, versão estável e deprecação com prazo | Contrato é promessa |
| Muitos clientes que pedem dados diferentes | GraphQL, só com esse motivo | Custo em cache, segurança e N+1 |
| Entre serviços internos | REST ou gRPC | gRPC só com time para operar |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Estilo | [docs/01-rest-rpc-ou-graphql.md](docs/01-rest-rpc-ou-graphql.md) | REST, RPC tipado ou GraphQL |
| Rotas, verbos e status | [docs/02-rotas-verbos-e-status.md](docs/02-rotas-verbos-e-status.md) | Nomes, métodos e códigos HTTP |
| Formato de erro | [docs/03-formato-de-erro.md](docs/03-formato-de-erro.md) | Problem Details, erros por campo |
| Paginação e filtros | [docs/04-paginacao-e-filtros.md](docs/04-paginacao-e-filtros.md) | Listas com limite, cursor, filtros e ordenação |
| Versionamento | [docs/05-versionamento.md](docs/05-versionamento.md) | Mudar sem quebrar quem consome |
| Idempotência e retries | [docs/06-idempotencia-e-retries.md](docs/06-idempotencia-e-retries.md) | Clique duplo, rede ruim, webhook repetido |
| OpenAPI e documentação | [docs/07-openapi-e-documentacao.md](docs/07-openapi-e-documentacao.md) | Contrato gerado do código |
| Cliente gerado no front | [docs/08-cliente-gerado-no-front.md](docs/08-cliente-gerado-no-front.md) | Tipos e chamadas geradas |

## Checklist de toda rota nova

- [ ] Nome no plural, verbo e status certos ([02](docs/02-rotas-verbos-e-status.md)).
- [ ] Entrada validada na borda, com erro 422 por campo ([03](docs/03-formato-de-erro.md)).
- [ ] Erros no formato único, sem vazar detalhe interno.
- [ ] Lista com limite máximo e ordenação estável ([04](docs/04-paginacao-e-filtros.md)).
- [ ] Recurso de outra empresa responde 404, não 403 (liga com `data`, doc 06).
- [ ] `POST` que não pode repetir aceita chave de idempotência ([06](docs/06-idempotencia-e-retries.md)).
- [ ] Rota aparece no OpenAPI com exemplo e o cliente do front foi regenerado ([07](docs/07-openapi-e-documentacao.md), [08](docs/08-cliente-gerado-no-front.md)).
- [ ] Teste de status e de erro escrito (skill `quality`).

## Regras de uso

- **Um formato de erro e um de lista para a API inteira.** Quem consome escreve um tratamento só.
- **Contrato primeiro, depois o código.** Pense na resposta antes de escrever a rota; gere o OpenAPI do código para ele nunca ficar desatualizado.
- **Mudança compatível por padrão.** Acrescentar campo opcional é seguro; remover ou renomear quebra. Quebra exige versão ou migração em duas etapas.
- **Nunca devolva o modelo do banco direto.** Devolva só o que a tela precisa; senão cada coluna nova vira contrato e vaza dado.
- **Limite em toda lista.** Sem `limit` máximo, uma consulta derruba o servidor.
- **Erro não vaza detalhe.** Sem stack trace, SQL nem nome de tabela na resposta; o detalhe vai para o log, com um id de requisição.
- **O front usa cliente gerado.** Fetch escrito à mão em cada tela é onde o contrato quebra sem ninguém ver.
- **Fronteiras.** Framework é da `stacks`, pastas das rotas da `architecture`, login e permissões da `security`, regra de negócio e tabelas da `product` e da `data`, testes da `quality`. Esta skill cuida do formato do que trafega.

## Quando a lista não cobre

WebSockets e eventos em tempo real, filas e mensageria, webhooks enviados, upload de arquivos grandes, GraphQL avançado (federação) e API pública com planos e cotas ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial da ferramenta.

## Validade dos dados

RFCs, versões de especificações e nomes de bibliotecas foram conferidos em 2026-11-24. Cada documento tem a linha "Verificado em"; confira a versão do OpenAPI e da biblioteca do projeto antes de copiar uma configuração.
