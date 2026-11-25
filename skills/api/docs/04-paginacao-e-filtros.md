# Paginação e filtros

> Toda lista devolve o mesmo envelope, com limite máximo, cursor opaco, filtros por query string e ordenação explícita.

| | |
|---|---|
| **Referência** | RFC 8288, "Web Linking" (rfc-editor.org/rfc/rfc8288); RFC 3339 (datas); "Use The Index, Luke", Markus Winand (use-the-index-luke.com), seção sobre seek method; docs de PostgreSQL sobre índices |
| **Categoria** | API |
| **Tipo** | Prática de contrato de listas |
| **Vale para** | APIs REST/JSON em qualquer stack; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

**Paginação** é devolver uma lista em pedaços. **Filtro** reduz a lista (`?status=confirmed`). **Ordenação** define a ordem (`?sort=-startsAt`). Tudo isso entra pela **query string**, a parte da URL depois do `?`.

Existem dois estilos de página: **offset** ("pule 40, traga 20") e **cursor** ("traga 20 depois deste ponto"). O SQL e o motivo da diferença estão em [índices e paginação](../../data/docs/08-indices-e-paginacao.md).

## Por que usar

- **Resposta rápida e leve:** ninguém baixa 50 mil agendamentos de uma vez.
- **Front simples:** um componente de lista serve para todas as telas.
- **Banco protegido:** limite máximo impede o pedido que derruba o servidor.
- **Contrato estável:** a lista não muda de forma quando você troca offset por cursor, só o `pageInfo`.

## Quando usar

- Em toda rota que devolve coleção, mesmo que hoje tenha 10 itens.
- Cursor para listas que crescem e mudam (agendamentos, mensagens, pedidos).
- Offset para cadastros pequenos com "ir para a página 3" (pacientes de uma clínica pequena).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas listas; offset com `limit` basta |
| MVP de SaaS | ✅ Ótimo | Envelope e limite desde o início evitam quebrar o front depois |
| SaaS em crescimento | ✅ Ótimo | Cursor e filtros indexados sustentam tabelas grandes |
| Sistema interno/corporativo | ✅ Ótimo | Telas de grade pedem filtro, ordenação e às vezes total |
| API pública/integração | ✅ Ótimo | Clientes varrem tudo; cursor é o padrão seguro |
| App mobile | ✅ Ótimo | Rolagem infinita casa com cursor |
| Rota que devolve a tabela inteira "porque é pouca coisa" | ❌ Evite | Hoje são 50 linhas, amanhã são 50 mil |

## Quando é bom

- **Envelope único:** `items` e `pageInfo` em toda lista.
- **Cursor opaco:** o servidor pode mudar o que há dentro sem quebrar clientes.
- **Filtros nomeados como o campo:** `status`, `professionalId`, fáceis de adivinhar.

## Quando é ruim

- **Total sempre:** `count(*)` em tabela grande é caro. Devolva `total` só quando pedido (`?include=total`) ou em tabelas pequenas.
- **Sem ordenação estável:** cursor exige ordem total. Sempre desempate pelo `id` (`startsAt`, depois `id`).
- **Filtro livre demais:** aceitar qualquer campo vira busca sem índice. Aceite só os filtros listados no contrato.
- **Cursor tratado como ID:** o front não deve montar nem ler o cursor; é um texto opaco.
- **`limit` sem teto:** o cliente pede `limit=1000000`.

## Como começar

Parâmetros padrão:

| Parâmetro | Exemplo | Regra |
|---|---|---|
| `limit` | `limit=20` | Padrão 20, máximo 100; acima disso, use 100 ou responda 422 |
| `cursor` | `cursor=eyJzIjoi...` | Texto opaco devolvido em `nextCursor` |
| `sort` | `sort=-startsAt` | `-` na frente é decrescente; só campos permitidos |
| `q` | `q=maria` | Busca de texto livre, em campos definidos pelo servidor |
| `from`, `to` | `from=2026-12-01&to=2026-12-31` | Intervalo de datas em ISO 8601 (RFC 3339), `from` incluso, `to` exclusivo |
| filtros | `status=confirmed&professionalId=pro_12` | Um parâmetro por campo; vários valores com vírgula |

Pedido e resposta (agendamentos confirmados de um profissional, em dezembro):

```http
GET /appointments?status=confirmed&professionalId=pro_12&from=2026-12-01&to=2027-01-01&sort=startsAt&limit=2
```

```json
{
  "items": [
    { "id": "apt_101", "startsAt": "2026-12-02T12:00:00Z", "status": "confirmed", "patientId": "pat_7" },
    { "id": "apt_108", "startsAt": "2026-12-02T13:00:00Z", "status": "confirmed", "patientId": "pat_9" }
  ],
  "pageInfo": {
    "limit": 2,
    "hasNextPage": true,
    "nextCursor": "eyJzIjoiMjAyNi0xMi0wMlQxMDowMDowMC0wMzowMCIsImlkIjoiYXB0XzEwOCJ9"
  }
}
```

Próxima página: o mesmo pedido com `&cursor=<nextCursor>`. Na última página, `hasNextPage` é `false` e `nextCursor` é `null`.

Cursor opaco em TypeScript (base64url do último item visto):

```ts
const encode = (last: { startsAt: string; id: string }) =>
  Buffer.from(JSON.stringify({ s: last.startsAt, id: last.id })).toString("base64url")

const decode = (cursor: string) => {
  try {
    return JSON.parse(Buffer.from(cursor, "base64url").toString())
  } catch {
    throw new AppError(400, "invalid_cursor", "Cursor inválido")
  }
}

const limit = Math.min(Number(query.limit ?? 20), 100)
const rows = await listAppointments({ ...filters, after: cursor && decode(cursor), take: limit + 1 })
const hasNextPage = rows.length > limit
const items = rows.slice(0, limit)
```

Buscar `limit + 1` linhas diz se há próxima página sem fazer `count`. Cursor adulterado ou vencido devolve erro no [formato padrão](03-formato-de-erro.md).

Offset, quando fizer sentido:

```json
{ "items": [], "pageInfo": { "page": 3, "pageSize": 20, "total": 143 } }
```

Header `Link` (RFC 8288) é opcional e útil para clientes genéricos:

```http
Link: </appointments?cursor=eyJz...&limit=20>; rel="next"
```

Regras para a lista não ficar gigante: `limit` com teto, filtros só em campos com índice, `from`/`to` com janela máxima (por exemplo, 366 dias) e exportação grande em rota própria, assíncrona.

## Combina com / alternativas

- [Índices e paginação](../../data/docs/08-indices-e-paginacao.md): o índice que sustenta filtro e ordem.
- [Formato de erro](03-formato-de-erro.md): filtro ou cursor inválido vira 422 ou 400.
- [OpenAPI](07-openapi-e-documentacao.md): declare os parâmetros e o schema do envelope uma vez.
- Alternativa: GraphQL com conexões (`edges`, `pageInfo`), no mesmo espírito; veja [REST, RPC ou GraphQL](01-rest-rpc-ou-graphql.md).

## Decisão rápida

- **Use se:** a rota devolve uma coleção que pode crescer.
- **Evite se:** o recurso é único (um agendamento por id) ou a lista é fixa e minúscula (os 4 status possíveis).
