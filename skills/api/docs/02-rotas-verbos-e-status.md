# Rotas, verbos e códigos de status

> Nomeie recursos no plural, escolha o verbo pela semântica e devolva o código de status que diz o que aconteceu.

| | |
|---|---|
| **Referência** | RFC 9110 "HTTP Semantics" (rfc-editor.org/rfc/rfc9110); RFC 5789 (PATCH); RFC 6585 (429); RFC 3339 (datas); ISO 8601; R. Fielding, tese (2000) |
| **Categoria** | API |
| **Tipo** | Prática de desenho de rotas |
| **Vale para** | APIs REST/JSON em qualquer linguagem; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

Uma API REST expõe **recursos**: coisas do negócio, como agendamentos e pacientes. A URL é o nome do recurso (um substantivo), o **verbo HTTP** diz o que fazer com ele e o **código de status** diz o resultado.

Duas palavras que aparecem a seguir, definidas na RFC 9110:

- **Seguro:** o verbo não altera nada no servidor (só lê).
- **Idempotente:** repetir a mesma chamada deixa o servidor no mesmo estado que uma chamada só.

## Por que usar

- **Previsível:** quem conhece uma rota adivinha as outras.
- **Ferramentas entendem:** caches, proxies e clientes tratam `GET` e status corretamente.
- **Erros claros:** o cliente decide o que fazer (tentar de novo, pedir login, mostrar mensagem) só pelo status.

## Quando usar

- Em toda rota nova de uma API REST.
- Ao revisar rotas herdadas com nomes como `/getAppointments` ou `/doCancel`.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API de recursos para desenhar |
| MVP de SaaS | ✅ Ótimo | Padrão desde o início evita refazer rotas |
| SaaS em crescimento | ✅ Ótimo | Mobile e integrações dependem de rotas estáveis |
| Sistema interno/corporativo | ✅ Ótimo | Equipes novas entendem a API rápido |
| API pública/integração | ✅ Ótimo | Terceiros esperam o padrão HTTP |
| App mobile | ✅ Ótimo | Status corretos permitem tratar erro e retry no app |

## Quando é bom

- **Verbos pela semântica:** `GET` pode ser repetido e guardado em cache sem medo.
- **Status específico:** 409 e 422 deixam o front mostrar a mensagem certa.
- **Plural e substantivo:** `/appointments/ap_1` lê como "o agendamento ap_1".

## Quando é ruim

- **Aninhar demais:** `/clinics/1/patients/2/appointments/3/notes` fica frágil. Limite a 2 níveis.
- **Verbo na URL:** `/createAppointment` repete o que o `POST` já diz.
- **Tudo 200:** devolver 200 com `{ "error": true }` esconde a falha de caches, monitores e clientes.
- **Pureza demais:** nem toda ação cabe em CRUD. Não force.

## Como começar

**Verbos** (RFC 9110, e RFC 5789 para `PATCH`):

| Verbo | Uso | Seguro | Idempotente |
|---|---|---|---|
| `GET` | Ler um recurso ou lista | Sim | Sim |
| `POST` | Criar, ou executar uma ação | Não | Não |
| `PUT` | Substituir o recurso inteiro | Não | Sim |
| `PATCH` | Alterar só alguns campos | Não | Não garantido |
| `DELETE` | Remover | Não | Sim |

`POST` não é idempotente: repetir cria dois agendamentos. Veja [idempotência e retries](06-idempotencia-e-retries.md).

**Ações fora do CRUD:** use `POST` num sub-recurso com o nome da ação: `POST /appointments/{id}/cancel`. Cancelar não é só apagar (guarda motivo e histórico), então não use `DELETE`.

**Aninhamento:** até 2 níveis, e só quando o filho não existe sem o pai: `/patients/{id}/appointments`. Para o resto, rota própria com filtro: `/appointments?patientId=pt_1`.

**Tabela de rotas do agendamento:**

| Rota | Verbo | Sucesso | Função |
|---|---|---|---|
| `/appointments` | `GET` | 200 | Lista (com [paginação](04-paginacao-e-filtros.md)) |
| `/appointments` | `POST` | 201 | Cria o agendamento |
| `/appointments/{id}` | `GET` | 200 | Detalha |
| `/appointments/{id}` | `PATCH` | 200 | Remarca ou altera observação |
| `/appointments/{id}/cancel` | `POST` | 200 | Cancela, com motivo |
| `/appointments/{id}/confirm` | `POST` | 200 | Confirma presença |
| `/patients` | `GET`, `POST` | 200, 201 | Lista e cadastra |
| `/patients/{id}` | `GET`, `PATCH` | 200 | Detalha e altera |
| `/patients/{id}/appointments` | `GET` | 200 | Histórico do paciente |

**Códigos de status:**

| Código | Quando usar |
|---|---|
| 200 | Deu certo e há corpo na resposta |
| 201 | Criou algo; envie o cabeçalho `Location` com a URL do novo recurso |
| 204 | Deu certo e não há corpo (ex.: `DELETE`) |
| 400 | Requisição malformada (JSON quebrado, parâmetro ilegível) |
| 401 | Sem login ou token inválido |
| 403 | Logado, mas sem permissão |
| 404 | Recurso não existe, ou é de outra empresa |
| 409 | Conflito com o estado atual (horário já ocupado) |
| 422 | Corpo legível, mas dados inválidos (horário no passado) |
| 429 | Muitas requisições; envie `Retry-After` |
| 500 | Erro nosso, inesperado |

**401 x 403:** 401 quer dizer "não sei quem você é" (faça login). 403 quer dizer "sei quem é, mas não pode". O nome do 401 na RFC é "Unauthorized", mas o sentido é de autenticação.

**404 para outra empresa:** se a recepcionista da clínica A pede o paciente da clínica B, responda 404, não 403. Assim não se revela que ele existe. Veja [multiempresa](../../data/docs/06-multiempresa.md).

Criação:

```http
POST /appointments
{ "patientId": "pt_1", "professionalId": "pr_7", "startsAt": "2026-12-01T13:00:00Z" }
```

```http
HTTP/1.1 201 Created
Location: /appointments/ap_9
```

```json
{ "id": "ap_9", "status": "scheduled", "startsAt": "2026-12-01T13:00:00Z", "price": 15000 }
```

**Formato de sucesso e campos:** devolva o recurso direto, sem envelope inútil; para listas, um objeto com `items` e dados de página. Use um só padrão de nome (camelCase aqui), o mesmo `id` e o mesmo `status` em todas as rotas. O formato de erro está em [formato de erro](03-formato-de-erro.md).

**Datas:** ISO 8601 em UTC com `Z` (`2026-12-01T13:00:00Z`; a RFC 3339 é um perfil dele). O front converte para o fuso do usuário. **Dinheiro:** inteiro em centavos (`15000` = R$ 150,00) ou string decimal (`"150.00"`). Nunca `number` com vírgula flutuante.

Em cada stack, o desenho é o mesmo; muda só como registrar a rota:

| Stack | Rota |
|---|---|
| Hono / Fastify | `app.post("/appointments", ...)` |
| NestJS / Spring Boot | `@Post("appointments")` / `@PostMapping` |
| FastAPI / ASP.NET Core | `@app.post(...)` / `MapPost(...)` |
| Laravel / Rails / Django | `Route::post` / `resources :appointments` / `path(...)` |

## Combina com / alternativas

- [Estilo da API](01-rest-rpc-ou-graphql.md) antes de desenhar rotas.
- [Idempotência](06-idempotencia-e-retries.md) para `POST` que o cliente pode repetir.
- Testes por status: `skills/quality/docs/04-testes-de-api-e-contrato.md`.

## Decisão rápida

- **Use se:** a API é REST; recursos no plural, verbo certo, status exato, 404 para outra empresa.
- **Evite se:** verbos na URL, aninhamento acima de 2 níveis ou sucesso sempre com 200.
