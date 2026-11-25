# OpenAPI e documentação

> Descreva a API num arquivo OpenAPI gerado do código, publique-o, valide-o no CI e compare versões para pegar quebra antes do deploy.

| | |
|---|---|
| **Referência** | OpenAPI Specification (spec.openapis.org/oas); Spectral (github.com/stoplightio/spectral); oasdiff (github.com/oasdiff/oasdiff); docs oficiais de FastAPI, ASP.NET Core, springdoc-openapi, @hono/zod-openapi, @fastify/swagger, @nestjs/swagger, Scramble |
| **Categoria** | API |
| **Tipo** | Prática de contrato e documentação |
| **Vale para** | APIs HTTP/REST em qualquer linguagem; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

**OpenAPI** é o formato padrão (JSON ou YAML) para descrever uma API HTTP: rotas, parâmetros, corpos, respostas e erros. A especificação publicada tem as linhas 3.0, 3.1 e 3.2 (a 3.2.1 é a mais recente na página oficial). Prefira 3.1 ou 3.2, que usam JSON Schema de verdade; se a ferramenta só aceita 3.0, use 3.0.

Esse arquivo é o **contrato**: o acordo entre front e back. Dele saem a documentação navegável, o cliente tipado do front ([doc 08](08-cliente-gerado-no-front.md)) e os testes de contrato.

## Por que usar

- **Uma fonte da verdade:** docs, tipos e testes saem do mesmo arquivo.
- **Quebra visível:** uma ferramenta compara duas versões e avisa antes do deploy.
- **Onboarding rápido:** quem chega testa a API pelo navegador.
- **Integrações:** parceiros geram o próprio cliente sem perguntar a você.

## Quando usar

- Sempre que um front ou outro sistema consome a API.
- Quando front e back são feitos por pessoas ou times diferentes.
- Quando a API é pública ou usada por app mobile.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API própria para descrever |
| MVP de SaaS | ✅ Ótimo | Gerado do código sai quase de graça e alimenta o cliente do front |
| SaaS em crescimento | ✅ Ótimo | Validação e detecção de quebra no CI protegem os clientes |
| Sistema interno/corporativo | 🟡 Serve | Basta gerar e publicar; lint rígido só se houver vários consumidores |
| API pública/integração | ✅ Ótimo | A spec é o produto; precisa de exemplos, descrições e controle de quebra |
| App mobile | ✅ Ótimo | Versões antigas do app seguem em uso; o diff de spec evita quebrá-las |

## Quando é bom

- **Gerar do código:** a spec nunca fica velha, porque o código é a fonte.
- **Docs com "Try it":** testar a rota sem montar requisição à mão.
- **Revisão no PR:** o diff da spec mostra o que a mudança faz na API.

## Quando é ruim

- **Spec escrita à mão e esquecida:** vira mentira. Gere do código ou valide no CI.
- **Sem descrições e exemplos:** o arquivo existe, mas ninguém entende a rota.
- **Spec gigante com tipos genéricos:** `object` sem campos não ajuda cliente nenhum.
- **Docs expostas sem querer:** em API interna, proteja `/docs` ou desligue em produção.
- **Spec-first sem necessidade:** escrever o contrato antes é bom com times separados, mas duplica trabalho num time só.

## Como começar

**Code-first** (padrão): você escreve rotas e schemas no código, e o framework gera o OpenAPI. **Spec-first**: você escreve o OpenAPI primeiro e o código segue. Use code-first por padrão; spec-first só quando o contrato precisa ser acordado antes do código, entre times ou com parceiros.

Em cada stack (confira o nome exato na documentação da versão que você usa):

| Stack | Como gerar | Onde sai |
|---|---|---|
| FastAPI | Nativo, via modelos Pydantic | `/openapi.json`, `/docs`, `/redoc` |
| Django | `drf-spectacular` (com DRF) | rota configurada por você |
| ASP.NET Core | Pacote `Microsoft.AspNetCore.OpenApi` (.NET 9+): `AddOpenApi()` e `MapOpenApi()` | `/openapi/v1.json` |
| Spring Boot | `springdoc-openapi` | `/v3/api-docs` |
| Hono | `@hono/zod-openapi` (rotas com `createRoute` e Zod) | rota do `app.doc(...)` |
| Fastify | `@fastify/swagger` (usa os schemas das rotas) | rota do plugin |
| NestJS | `@nestjs/swagger` (`SwaggerModule`) | rota que você define |
| Laravel | Scramble (`dedoc/scramble`) ou L5-Swagger | rota do pacote |
| Rails | `rswag` (gera a partir dos specs de teste) | arquivo no repositório |
| Go | `huma` (code-first) ou `swaggo/swag` (por comentários) | rota ou arquivo |

Exemplo com Hono, o agendamento da clínica com descrição e exemplo:

```ts
import { OpenAPIHono, createRoute, z } from "@hono/zod-openapi";

const Appointment = z
  .object({
    id: z.string().uuid(),
    patientId: z.string().uuid(),
    startsAt: z.string().datetime().openapi({ example: "2026-12-01T12:00:00Z" }),
    status: z.enum(["scheduled", "cancelled"]),
  })
  .openapi("Appointment");

const getAppointment = createRoute({
  method: "get",
  path: "/appointments/{id}",
  summary: "Busca um agendamento",
  request: { params: z.object({ id: z.string().uuid() }) },
  responses: {
    200: { description: "Agendamento encontrado", content: { "application/json": { schema: Appointment } } },
    404: { description: "Agendamento não existe" },
  },
});

const app = new OpenAPIHono();
app.openapi(getAppointment, (c) => c.json(buscar(c.req.valid("param").id), 200));
app.doc("/openapi.json", { openapi: "3.1.0", info: { title: "Clínica API", version: "1.0.0" } });
```

Respostas de erro seguem o [formato de erro](03-formato-de-erro.md); declare o schema do problema em toda rota que pode falhar.

**Publicar:** sirva o `openapi.json` numa rota e salve também como artefato do CI, para o front baixar sem subir o back.

**Documentação navegável:** Scalar, Swagger UI e Redoc leem o `openapi.json`. Scalar tem visual moderno e cliente de teste embutido; Swagger UI é o mais conhecido; Redoc é bom para leitura. Muitos frameworks já trazem um deles.

**Validar a spec no CI** com Spectral, que aplica regras (descrição obrigatória, `operationId` único):

```bash
npx @stoplight/spectral-cli lint openapi.json
```

**Detectar quebra** com oasdiff, comparando a spec da branch `main` com a do PR:

```bash
oasdiff breaking main-openapi.json pr-openapi.json
```

Remover campo, tornar campo opcional em obrigatório e mudar tipo são quebras. Se há quebra, siga o [versionamento](05-versionamento.md). O oasdiff tem uma GitHub Action (`oasdiff-action`) para isso.

## Combina com / alternativas

- [Cliente gerado no front](08-cliente-gerado-no-front.md): o principal consumidor da spec.
- [Testes de API e contrato](../../quality/docs/04-testes-de-api-e-contrato.md): Schemathesis e validação de resposta usam a spec.
- [Versionamento](05-versionamento.md): o que fazer quando o diff aponta quebra.
- [Validação na borda](../../coding/docs/06-tipos-e-validacao-na-borda.md): o mesmo schema valida a entrada e descreve a rota.
- Alternativa sem OpenAPI: tRPC ou Hono RPC, veja o [doc 01](01-rest-rpc-ou-graphql.md). GraphQL tem schema próprio.

## Decisão rápida

- **Use se:** há consumidor da API além do próprio código. Gere do código, publique, valide e compare no CI.
- **Evite se:** não há API HTTP, ou o front e o back são o mesmo processo (server actions) e ninguém mais consome.
