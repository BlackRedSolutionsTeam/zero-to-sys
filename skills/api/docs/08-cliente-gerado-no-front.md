# Cliente gerado no front

> O front não escreve fetch à mão para cada rota: gera tipos e cliente do OpenAPI, e o compilador avisa quando o back quebra o contrato.

| | |
|---|---|
| **Referência** | openapi-ts.dev (openapi-typescript e openapi-fetch); orval.dev; heyapi.dev (@hey-api/openapi-ts); NSwag (github.com/RicoSuter/NSwag); Kiota (learn.microsoft.com/openapi/kiota); openapi-generator.tech; TanStack Query (tanstack.com/query) |
| **Categoria** | API |
| **Tipo** | Prática de integração front e back |
| **Vale para** | Front em TypeScript consumindo API com OpenAPI; clientes .NET/C# também |
| **Verificado em** | 2026-11-24 |

## O que é

Em vez de escrever `fetch("/appointments/" + id)` e declarar o tipo da resposta na mão, você lê o [OpenAPI](07-openapi-e-documentacao.md) e **gera** os tipos (e, em algumas ferramentas, as funções) do cliente. Se o back muda um campo, a geração muda os tipos e o `tsc` do front acusa onde o código quebrou.

## Por que usar

- **Erro em tempo de build:** o contrato quebrado aparece no compilador, não no usuário.
- **Menos código repetido:** sem tipos, URLs e parâmetros escritos duas vezes.
- **Autocomplete:** o editor sugere rotas, parâmetros e campos.

## Quando usar

- Front e back em repositórios ou times separados.
- Quando a API já gera OpenAPI do código.
- Quando há app mobile ou outros clientes que também geram código.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API própria para consumir |
| MVP de SaaS | ✅ Ótimo | Tipos gerados custam um script e evitam bugs de integração |
| SaaS em crescimento | ✅ Ótimo | Geração no CI trava PR que quebra o contrato |
| Sistema interno/corporativo | ✅ Ótimo | Back .NET ou Java com front React ganha tipos sem esforço |
| API pública/integração | ✅ Ótimo | Clientes gerados em várias linguagens facilitam a adoção |
| App mobile | 🟡 Serve | Há geradores para Swift, Kotlin e Dart; confira o suporte da ferramenta |

## Quando é bom

- **Contrato verificado pelo compilador:** o primeiro nível de defesa, antes dos testes.
- **Spec como fonte:** nada para sincronizar à mão.
- **Funciona com qualquer back:** FastAPI, .NET, Spring, Laravel, Hono, o que gerar OpenAPI.

## Quando é ruim

- **Spec ruim gera tipo ruim:** sem schemas de resposta e de erro, saem `unknown` e `any`. Corrija na spec, não no front.
- **Gerar demais:** clientes completos com muito código viram arquivos enormes e difíceis de ler. Para tipos simples, prefira só tipos mais um fetch pequeno.
- **Arquivo gerado editado à mão:** é sobrescrito na próxima geração. Nunca edite.
- **Tipos não validam em runtime:** o TypeScript confia que o back respondeu certo. Para desconfiar, use validação de resposta (Zod) ou os testes de contrato.
- **Front e back no mesmo projeto TypeScript:** tRPC ou Hono RPC já dão tipos sem OpenAPI; veja o [doc 01](01-rest-rpc-ou-graphql.md).

## Como começar

Ferramentas (confira o estado atual de cada uma antes de adotar):

| Ferramenta | O que gera | Quando escolher |
|---|---|---|
| `openapi-typescript` + `openapi-fetch` | Só tipos, mais um cliente `fetch` minúsculo e tipado | Padrão recomendado: pouco código gerado |
| Orval | Funções por rota e hooks de TanStack Query | Quer hooks prontos |
| `@hey-api/openapi-ts` | SDK, tipos e plugins (inclui TanStack Query) | Quer SDK completo configurável |
| NSwag, Kiota | Cliente C# (e TypeScript, no NSwag) | Consumidor em .NET ou back .NET gerando para o front |
| `openapi-generator` | Clientes em dezenas de linguagens | Várias linguagens ou mobile |

**Passo a passo (agendamento da clínica):**

1. O back expõe `openapi.json` (rota ou artefato do CI, veja o [doc 07](07-openapi-e-documentacao.md)).

2. No front, instale e crie o script `gen:api` no `package.json`:

```bash
npm i openapi-fetch
npm i -D openapi-typescript
```

```json
{
  "scripts": {
    "gen:api": "openapi-typescript http://localhost:3000/openapi.json -o src/api/schema.d.ts"
  }
}
```

Em CI, aponte para o artefato baixado (`./openapi.json`) em vez da URL.

3. Crie o cliente uma vez:

```ts
import createClient from "openapi-fetch";
import type { paths } from "./schema";

export const api = createClient<paths>({ baseUrl: import.meta.env.VITE_API_URL });
```

4. Use nas telas, sem escrever tipo nenhum:

```ts
const { data, error } = await api.GET("/appointments/{id}", {
  params: { path: { id: "a3f1c2d4-0000-4000-8000-000000000001" } },
});

if (error) return mostrarErro(error);
console.log(data.startsAt);
```

`data` tem o tipo `Appointment` do back. Se o back renomear `startsAt` para `startTime`, o `tsc` falha nesta linha.

5. **TanStack Query por cima:** o cliente busca, o TanStack Query cuida de cache, recarga e estado de carregamento.

```ts
export function useAppointment(id: string) {
  return useQuery({
    queryKey: ["appointments", id],
    queryFn: async () => {
      const { data, error } = await api.GET("/appointments/{id}", { params: { path: { id } } });
      if (error) throw error;
      return data;
    },
  });
}
```

6. **No CI do front:** rode `npm run gen:api` e depois `tsc --noEmit`. Se o arquivo gerado mudou e não foi commitado, falhe o job (`git diff --exit-code src/api/schema.d.ts`). Assim toda mudança de contrato aparece no PR. Rode de novo sempre que a spec mudar.

**Quem commita o arquivo gerado?** Duas opções: commitar `schema.d.ts` (o diff mostra a mudança de contrato no PR) ou gerar só no build. Para time pequeno, commitar é mais simples e transparente.

Contrato verificado também no back com Schemathesis e validação de resposta: veja [testes de API e contrato](../../quality/docs/04-testes-de-api-e-contrato.md).

## Combina com / alternativas

- [OpenAPI e documentação](07-openapi-e-documentacao.md): a spec que alimenta a geração.
- [Formato de erro](03-formato-de-erro.md): declare o schema do erro para o `error` vir tipado.
- [Paginação e filtros](04-paginacao-e-filtros.md): tipos da página saem da spec.
- [Validação na borda](../../coding/docs/06-tipos-e-validacao-na-borda.md): valide a resposta em runtime onde o risco é alto.
- Sem OpenAPI: **tRPC** ou **Hono RPC** compartilham tipos direto do código do servidor. Só servem quando front e back são TypeScript no mesmo repositório ou pacote; veja o [doc 01](01-rest-rpc-ou-graphql.md).

## Decisão rápida

- **Use se:** o front consome uma API com OpenAPI. Comece com `openapi-typescript` e `openapi-fetch`, mais TanStack Query.
- **Use Orval ou hey-api se:** quer hooks ou SDK prontos e aceita mais código gerado.
- **Evite se:** a API não tem spec confiável, ou back e front TypeScript já compartilham tipos por tRPC ou Hono RPC.
