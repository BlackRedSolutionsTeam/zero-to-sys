# Testes de API e contrato

> Teste a API como o cliente a usa (status, corpo, erro, permissão) e proteja o contrato com o OpenAPI para não quebrar o front ao mudar o back.

| | |
|---|---|
| **Referência** | Schemathesis (schemathesis.readthedocs.io); Pact (pact.io, docs sobre consumer-driven contracts); OpenAPI Specification (spec.openapis.org); Vitest (vitest.dev); M. Fowler, "ContractTest" e "TestPyramid" |
| **Categoria** | Qualidade |
| **Tipo** | Prática de teste de API |
| **Vale para** | APIs HTTP/REST em qualquer linguagem; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

Teste de API chama a rota HTTP e confere o que o cliente vê: o código de status, o corpo da resposta, o formato do erro e quem pode ou não pode acessar. Não olha o código por dentro.

**Contrato** é o acordo entre quem fornece a API e quem a consome: quais rotas existem, o que entra e o que sai. Em geral ele vive no arquivo OpenAPI (a descrição padrão de uma API REST). Teste de contrato verifica que a API de verdade cumpre esse acordo.

## Por que usar

- **Front não quebra do nada:** mudar um campo no back acende um teste, não um bug em produção.
- **Segurança verificada:** 401, 403 e 404 de outra empresa viram teste, não promessa.
- **Erros consistentes:** todo erro sai no mesmo formato.

## Quando usar

- Toda rota nova: um teste por critério de aceite, incluindo os casos de erro.
- Toda rota protegida: sem login, sem permissão, outra empresa.
- Quando o front e o back mudam em ritmos diferentes.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Sem API própria para testar |
| MVP de SaaS | ✅ Ótimo | Testes de status e permissão por rota; contrato via tipos gerados |
| SaaS em crescimento | ✅ Ótimo | Schemathesis e validação do OpenAPI no CI protegem o front |
| Sistema interno/corporativo | ✅ Ótimo | Permissões por perfil são o risco principal |
| API/integração | ✅ Ótimo | O contrato é o produto; clientes externos dependem dele |
| App mobile | ✅ Ótimo | Versões antigas do app seguem em uso; quebrar o contrato afeta quem não atualizou |

## Quando é bom

- **Olha como o cliente:** pega erro de formato que o teste de unidade não vê.
- **Casos negativos explícitos:** 401, 403, 404 e 422 têm teste próprio.
- **Contrato automático:** o OpenAPI é a fonte e a ferramenta gera os casos.

## Quando é ruim

- **Repetir o teste de unidade:** não teste cada regra de cálculo pela rota; teste os casos de borda da API.
- **Asserção frágil demais:** comparar o JSON inteiro quebra quando surge um campo novo e inofensivo. Confira o que importa.
- **Pact sem necessidade:** exige trabalho dos dois lados e um lugar para guardar os contratos; só compensa com times ou serviços diferentes.
- **OpenAPI desatualizado:** o teste de contrato passa a testar um documento velho. Gere o documento do código ou valide no CI.
- **Fuzz contra produção:** o Schemathesis cria e apaga dados; rode em ambiente de teste.

## Como começar

Formato de erro e paginação seguem a skill `api` (ainda virá). Até lá, use o padrão que o projeto já adota e teste sempre o mesmo formato.

O que testar em toda rota:

| Caso | Status | Exemplo |
|---|---|---|
| Sucesso | 200 ou 201 | Agendamento criado |
| Dado inválido | 422 (ou 400, conforme o projeto) | Horário no passado |
| Sem login | 401 | Sem token |
| Sem permissão | 403 | Perfil sem direito de agendar |
| Recurso de outra empresa | 404 | Paciente da clínica B |
| Conflito de regra | 409 | Horário já ocupado |

O 404 para outra empresa evita revelar que o recurso existe. Veja [multiempresa](../../data/docs/06-multiempresa.md).

Critério de aceite: **Dado** uma recepcionista logada, **quando** ela agenda um paciente com horário e profissional válidos, **então** o sistema cria o agendamento. Teste de API (Vitest, rota em processo):

```ts
describe("POST /agendamentos", () => {
  it("cria o agendamento e responde 201", async () => {
    const { empresa, token } = await loginComo("recepcao");
    const ana = await criarProfissional(empresa.id);
    const maria = await criarPaciente(empresa.id);

    const res = await chamar("POST", "/agendamentos", token, {
      profissionalId: ana.id,
      pacienteId: maria.id,
      inicio: "2026-12-01T09:00:00-03:00",
    });

    expect(res.status).toBe(201);
    expect(await res.json()).toMatchObject({ profissionalId: ana.id, pacienteId: maria.id });
  });

  it("responde 422 com horário no passado", async () => {
    const { empresa, token } = await loginComo("recepcao");
    const ana = await criarProfissional(empresa.id);
    const maria = await criarPaciente(empresa.id);

    const res = await chamar("POST", "/agendamentos", token, {
      profissionalId: ana.id,
      pacienteId: maria.id,
      inicio: "2020-01-01T09:00:00-03:00",
    });

    expect(res.status).toBe(422);
    expect(await res.json()).toHaveProperty("erro");
  });

  it("responde 401 sem login", async () => {
    const res = await chamar("POST", "/agendamentos", null, {});
    expect(res.status).toBe(401);
  });

  it("responde 403 para perfil sem permissão de agendar", async () => {
    const { token } = await loginComo("financeiro");
    const res = await chamar("POST", "/agendamentos", token, {});
    expect(res.status).toBe(403);
  });

  it("responde 404 para paciente de outra empresa", async () => {
    const { token } = await loginComo("recepcao");
    const outra = await criarEmpresa({ nome: "Clínica Horizonte" });
    const estranho = await criarPaciente(outra.id);

    const res = await chamar("POST", "/agendamentos", token, { pacienteId: estranho.id });

    expect(res.status).toBe(404);
  });
});
```

Aqui `chamar`, `loginComo` e as factories são helpers do projeto; `chamar` usa `supertest` ou `app.request`.

Contrato com o OpenAPI, em três camadas, da mais barata à mais cara:

1. **Tipos gerados no front:** gere os tipos TypeScript a partir do OpenAPI (por exemplo com `openapi-typescript`). Se o back muda um campo, o `tsc` do front falha. É a primeira linha de defesa.
2. **Validar a resposta contra o schema:** no teste, valide o corpo com o schema do OpenAPI usando um validador de JSON Schema (como o Ajv).
3. **Fuzz com Schemathesis:** gera chamadas a partir do OpenAPI e procura respostas fora do contrato e erros 500.

```bash
pip install schemathesis
schemathesis run ./openapi.yaml --url http://localhost:3000
```

Com autenticação: acrescente `--header 'Authorization: Bearer <token>'`. Confira as opções na documentação da versão que você instalar.

**Pact** (pact.io) é o contrato dirigido pelo consumidor: o front (consumidor) registra o que espera da API, e o back (provedor) roda esses pactos no CI. Use só quando há times ou serviços diferentes, onde o OpenAPI sozinho não basta. Com um time só, tipos gerados mais Schemathesis resolvem.

Em cada stack:

| Stack | Teste de rota | Contrato |
|---|---|---|
| TypeScript | `supertest`, `app.request` | `openapi-typescript`, Schemathesis, Pact JS |
| .NET | `WebApplicationFactory` | Schemathesis, Pact .NET |
| Python | `TestClient` (FastAPI), `pytest-django` | Schemathesis (integra com pytest) |
| PHP | Laravel HTTP tests | Schemathesis |
| Go | `net/http/httptest` | Schemathesis |
| Java | Spring Boot Test (`MockMvc`) | Schemathesis, Pact JVM |

## Combina com / alternativas

- [Pirâmide de testes](01-piramide-de-testes.md).
- [Testes de integração com banco](03-testes-de-integracao-com-banco.md): a base para o teste de rota.
- [Ponta a ponta com Playwright](05-ponta-a-ponta-com-playwright.md): cobre o fluxo pela tela, não a API.
- [Quality gates no CI](07-quality-gates-no-ci.md): rode a validação do contrato no PR.
- Skill `api` (ainda virá): formato de erro e paginação.

## Decisão rápida

- **Use se:** o sistema tem API HTTP; use tipos gerados mais Schemathesis assim que existir o OpenAPI.
- **Use Pact se:** times ou serviços diferentes evoluem a API e o consumidor de forma independente.
- **Evite se:** não há API própria, ou o teste só repete o que a unidade já cobre.
