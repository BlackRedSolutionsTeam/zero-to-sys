# REST, RPC tipado ou GraphQL

> Use REST sobre JSON como padrão; troque por RPC tipado quando só o seu próprio front consome e tudo está em TypeScript, e por GraphQL só quando há motivo claro.

| | |
|---|---|
| **Referência** | R. Fielding, tese "Architectural Styles and the Design of Network-based Software Architectures" (2000); RFC 9110 (rfc-editor.org/rfc/rfc9110); graphql.org e spec.graphql.org; trpc.io; hono.dev (RPC); grpc.io; nextjs.org (Server Actions); tanstack.com/start (server functions) |
| **Categoria** | API |
| **Tipo** | Prática de escolha do estilo de API |
| **Vale para** | Qualquer sistema com front e back separados por rede; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

O **estilo de API** é a forma como front e back conversam. Há quatro escolhas comuns.

- **REST:** estilo descrito por Roy Fielding na tese de 2000. Você expõe **recursos** (como `/appointments`) e usa os verbos do HTTP sobre eles. Na prática, quase todo mundo faz "REST pragmático": JSON sobre HTTP, URLs de recursos, verbos e status corretos. Não implementa todas as restrições da tese (como hipermídia), e tudo bem.
- **RPC tipado:** o front chama uma função do back como se fosse local, e o tipo da função vale nos dois lados. Exemplos: tRPC, Hono RPC, server actions do Next.js e server functions do TanStack Start. RPC significa "chamada de procedimento remoto".
- **GraphQL:** uma única rota. O cliente escreve uma consulta dizendo exatamente quais campos quer, e o servidor responde só com eles.
- **gRPC:** chamadas entre serviços, com contrato em Protocol Buffers (arquivos `.proto`) e transporte binário sobre HTTP/2.

## Por que usar

- **Escolher uma vez evita retrabalho:** trocar de estilo depois muda front, back e testes.
- **REST é universal:** qualquer linguagem, ferramenta, cache e proxy entende HTTP.
- **RPC tipado corta código:** sem escrever e manter contrato à mão quando só você consome.

## Quando usar

- No começo do projeto, antes da primeira rota.
- Quando um novo tipo de consumidor aparece (app mobile, parceiro, outro serviço).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Em geral dispensa API própria; leia o conteúdo no build ou no servidor |
| MVP de SaaS | ✅ Ótimo | REST, ou RPC tipado se front e back ficam no mesmo repositório em TypeScript |
| SaaS em crescimento | ✅ Ótimo | REST com OpenAPI, pois mobile e integrações vão surgir |
| Sistema interno/corporativo | ✅ Ótimo | REST simples; RPC tipado se for um repositório só |
| API pública/integração | ✅ Ótimo | REST com OpenAPI; terceiros esperam isso |
| App mobile | 🟡 Serve | REST resolve; GraphQL só se as telas pedem dados muito diferentes |

## Quando é bom

- **REST:** cache de HTTP, ferramentas por todo lado, fácil de testar com `curl`, documentação padrão (OpenAPI).
- **RPC tipado:** erro de tipo aparece no editor quando o back muda, sem gerar cliente.
- **GraphQL:** um front traz de uma vez dados de várias entidades; clientes diferentes pedem formatos diferentes sem nova rota.
- **gRPC:** contrato rígido e desempenho entre serviços internos.

## Quando é ruim

- **REST:** telas que juntam muitos recursos geram várias chamadas ou rotas sob medida.
- **RPC tipado:** só funciona bem com TypeScript nos dois lados. Terceiros e mobile nativo não consomem. Se um dia outro cliente precisar, você terá de criar uma API REST ao lado.
- **GraphQL tem custos reais:**
  - **Cache:** tudo é `POST` na mesma URL, então o cache HTTP simples não ajuda. Exige cache no cliente.
  - **N+1:** um campo aninhado pode disparar uma consulta ao banco por item. Exige agrupamento (por exemplo, DataLoader).
  - **Segurança da consulta:** o cliente pode pedir uma consulta enorme ou muito profunda. Exige limite de profundidade, de custo e permissão por campo.
  - **Mais peças:** schema, resolvers, ferramentas próprias.
- **gRPC:** o navegador não chama gRPC direto. Não serve para o front web.

## Como começar

Pergunte quem consome a API.

| Quem consome | Estilo | Observação |
|---|---|---|
| Só o front próprio, mesmo repositório, TypeScript | RPC tipado ou REST | RPC tipado dá menos código; REST deixa a porta aberta |
| Front próprio, repositório separado ou back em outra linguagem | REST + OpenAPI | Gere o cliente tipado ([doc 08](08-cliente-gerado-no-front.md)) |
| App mobile | REST + OpenAPI | Versões antigas do app ficam em uso; veja [versionamento](05-versionamento.md) |
| Terceiros e parceiros | REST + OpenAPI | Contrato estável e documentado |
| Outros serviços internos | REST ou gRPC | gRPC se o desempenho e o contrato rígido compensam |
| Muitos clientes com necessidades de dados bem diferentes, grafo profundo | GraphQL | Só aqui; aceite os custos acima |

Exemplo de RPC tipado com Hono: o tipo da rota vai para o cliente.

```ts
const app = new Hono().get("/appointments/:id", (c) =>
  c.json({ id: c.req.param("id"), status: "scheduled" }),
);
export type AppType = typeof app;

const client = hc<AppType>("https://api.clinica.com.br");
const res = await client.appointments[":id"].$get({ param: { id: "ap_1" } });
```

Exemplo REST equivalente, que serve a qualquer cliente:

```http
GET /appointments/ap_1
```

```json
{ "id": "ap_1", "status": "scheduled", "startsAt": "2026-12-01T13:00:00Z" }
```

Misturar é permitido: REST para o que terceiros e mobile usam, RPC tipado para as telas internas. Só não duplique regra de negócio nos dois.

Dica: server actions e server functions servem para ações disparadas pela própria tela (um formulário). Se outro cliente precisar da mesma regra, ponha a regra num serviço e exponha também por REST.

## Combina com / alternativas

- [Rotas, verbos e status](02-rotas-verbos-e-status.md) para o desenho do REST.
- [OpenAPI e documentação](07-openapi-e-documentacao.md) e [cliente gerado no front](08-cliente-gerado-no-front.md) para o contrato.
- Alternativa ao GraphQL: rotas com `include` ou campos sob demanda (veja [filtros](04-paginacao-e-filtros.md)).
- A skill `stacks` escolhe o framework; esta escolhe o estilo.

## Decisão rápida

- **Use se:** REST é o padrão; RPC tipado quando só o seu front consome e tudo é TypeScript; GraphQL com vários clientes e grafo profundo; gRPC entre serviços.
- **Evite se:** GraphQL "porque é moderno" ou RPC tipado quando terceiros ou mobile nativo vão consumir.
