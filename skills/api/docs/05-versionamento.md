# Versionamento de API

> Só crie versões da API quando existe cliente que você não controla; no resto, evolua de forma compatível e avise antes de remover.

| | |
|---|---|
| **Referência** | RFC 9745 (cabeçalho Deprecation) e RFC 8594 (cabeçalho Sunset) em rfc-editor.org; documentação de versionamento da Stripe (docs.stripe.com/api/versioning); OpenAPI Specification (spec.openapis.org); Pact (pact.io) |
| **Categoria** | API |
| **Tipo** | Prática de evolução de contrato |
| **Vale para** | APIs HTTP/REST em qualquer linguagem; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

Versionar uma API é deixar mais de uma forma do contrato (rotas, campos, erros) disponível ao mesmo tempo, para que quem usa a forma antiga continue funcionando enquanto outros migram.

Mudança **compatível** não quebra quem já usa a API. Mudança de **quebra** (breaking change) faz o cliente antigo falhar ou entender errado.

## Por que usar

- **Cliente antigo continua funcionando:** o app que ficou no celular de alguém não para de uma hora para outra.
- **Migração com prazo:** o parceiro tem tempo de atualizar.
- **Você evolui sem medo:** a quebra vai para a versão nova.

## Quando usar

- Há cliente que você não atualiza junto com o servidor: app mobile em loja, parceiro que integra com sua API, sistema de terceiros.
- A API é pública ou paga.
- Não use quando front e back saem no mesmo deploy: só um cliente, que muda junto. Nesse caso evolua com expand and contract e pronto.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API própria consumida por terceiros |
| MVP de SaaS | ❌ Evite | Front e back no mesmo deploy; compatibilidade basta |
| SaaS em crescimento | 🟡 Serve | Só se abrir API para integrações de clientes |
| Sistema interno/corporativo | 🟡 Serve | Só quando outros sistemas da empresa consomem a API |
| API pública/integração | ✅ Ótimo | Você não controla quando o parceiro atualiza |
| App mobile | ✅ Ótimo | Versões antigas do app ficam em uso por meses |

## Quando é bom

- **Quebra com rede de proteção:** a versão antiga segue de pé.
- **Regra clara:** todo mundo sabe o que é quebra e o que não é.
- **Remoção previsível:** aviso, prazo e data de desligamento.

## Quando é ruim

- **Versão cedo demais:** manter v1 e v2 dobra teste, documentação e suporte.
- **Versão por qualquer mudança:** a maioria das mudanças é compatível e dispensa versão.
- **Versões que nunca morrem:** sem prazo de desligamento, você mantém tudo para sempre.

## Como começar

**O que é compatível e o que quebra**

| Mudança | Tipo |
|---|---|
| Nova rota | Compatível |
| Campo novo opcional na resposta | Compatível |
| Parâmetro novo opcional na requisição | Compatível |
| Remover ou renomear campo | Quebra |
| Mudar o tipo de um campo (`"12"` para `12`) | Quebra |
| Tornar obrigatório um campo que era opcional | Quebra |
| Novo valor em enum que o cliente trata com `switch` fechado | Quebra para quem não prevê valor novo |

Por isso, peça aos clientes para **ignorar campos que não conhecem**. Assim, acrescentar campo nunca quebra.

**Onde pôr a versão**

| Forma | Exemplo | Quando serve |
|---|---|---|
| Na URL | `/v1/appointments` | Padrão para a maioria; fácil de ver, testar e cachear |
| Em cabeçalho | `Accept: application/vnd.clinica.v2+json` | Quando a URL deve ficar estável; mais difícil de testar no navegador |
| Por data | `Stripe-Version: <data>` | API pública com muitas mudanças pequenas |

A Stripe usa cabeçalho `Stripe-Version` com a versão da conta como padrão, e hoje lança versões mensais sem quebra e um lançamento maior com quebras duas vezes por ano. É um modelo caro de manter; só copie com equipe para isso.

**Versão na URL, no Hono**

```ts
import { Hono } from "hono";
import { v1 } from "./v1/routes";
import { v2 } from "./v2/routes";

const app = new Hono();
app.route("/v1", v1);
app.route("/v2", v2);
```

**Avisar a deprecação**

Marque a rota antiga com os cabeçalhos padrão. `Deprecation` (RFC 9745) diz que a rota está obsoleta; seu valor é uma data estruturada, como `@1688169599` (segundos desde 1970). `Sunset` (RFC 8594) diz quando ela deixa de responder e usa data HTTP. O `Link` com `rel="deprecation"` aponta para o guia de migração.

```ts
app.use("/v1/*", async (c, next) => {
  await next();
  c.header("Deprecation", "@1767225599");
  c.header("Sunset", "Thu, 31 Dec 2026 23:59:59 GMT");
  c.header("Link", '<https://api.clinica.com.br/docs/migracao-v2>; rel="deprecation"; type="text/html"');
});
```

Combine um prazo (por exemplo, 6 meses para parceiros, mais para app mobile), avise por e-mail quem ainda usa a rota (registre o uso por cliente) e só desligue depois da data.

**Expand and contract na API**

É o mesmo passo a passo das migrations do banco (veja [../../data/docs/04-migrations.md](../../data/docs/04-migrations.md)). Exemplo: trocar `name` por `fullName` em `/patients`.

1. **Expandir:** a resposta passa a trazer `name` e `fullName`; a requisição aceita os dois.
2. **Migrar:** clientes passam a usar `fullName`; você mede quem ainda usa `name`.
3. **Contrair:** com o uso zerado (ou após o Sunset), remova `name`.

**Detectar quebra antes de publicar**

Compare o OpenAPI novo com o da versão publicada no CI e falhe se houver quebra; ferramentas de diff de OpenAPI fazem isso. Teste de contrato com os clientes reais (Pact) também pega. Veja [../../quality/docs/04-testes-de-api-e-contrato.md](../../quality/docs/04-testes-de-api-e-contrato.md).

## Combina com / alternativas

- [02-rotas-verbos-e-status.md](02-rotas-verbos-e-status.md) e [07-openapi-e-documentacao.md](07-openapi-e-documentacao.md): o OpenAPI é a base para comparar versões.
- [08-cliente-gerado-no-front.md](08-cliente-gerado-no-front.md): o cliente gerado quebra o build do front quando o contrato muda.
- Alternativa sem versão: só mudanças compatíveis, com expand and contract, para quando você controla todos os clientes.
- GraphQL evolui marcando campos como obsoletos em vez de criar versões (veja [01-rest-rpc-ou-graphql.md](01-rest-rpc-ou-graphql.md)).

## Decisão rápida

- **Use se:** há app em loja, parceiro ou sistema de terceiros que você não atualiza junto.
- **Evite se:** front e back saem no mesmo deploy; use mudanças compatíveis e expand and contract.
