# Vertical slice

> Cada caso de uso (criar pedido, cancelar pedido) vive em uma pasta própria com tudo o que precisa, da requisição ao banco, em vez de repartir o código em camadas horizontais.

| | |
|---|---|
| **Referência oficial** | Fonte primária do padrão: Jimmy Bogard, "Vertical Slice Architecture" (https://www.jimmybogard.com/vertical-slice-architecture/, 19/4/2018), que define a regra "minimizar o acoplamento entre fatias e maximizar dentro da fatia" (conferido em 2026-11-24). Em .NET, o app de referência da Microsoft dotnet/eShop agrupa por caso de uso (`Application/Commands`, `Application/Queries`) |
| **Categoria** | Parte 1 — Padrões que valem para qualquer stack |
| **Tipo** | Padrão de organização por caso de uso |
| **Vale para** | Back-end em qualquer linguagem; o exemplo de referência aqui é .NET (dotnet/eShop) |
| **Verificado em** | 2026-11-24 |

## O que é

Na estrutura por camadas, um pedido de "cancelar pedido" passa por `Controllers/`, `Services/`, `Repositories/` e `Models/`: quatro pastas para uma mudança. No vertical slice, a pasta `CancelOrder/` guarda a rota, a validação, a regra e o acesso a dados daquele caso de uso.

Cada slice decide sozinho como fala com o banco. Um slice simples pode ler direto; um complexo pode ter regras de domínio. O que não se faz é obrigar todos os casos de uso a passar pelas mesmas camadas.

## Por que usar

- **Acoplamento na fatia:** Bogard: "Minimize coupling between slices, and maximize coupling in a slice".
- **Menos abstração compartilhada:** segundo Bogard, com o slice "most abstractions melt away" e não se precisa de camadas compartilhadas como repositórios, serviços e controllers (algumas ainda são exigidas pelas ferramentas).
- **Nova funcionalidade só adiciona código:** "New features only add code, you're not changing shared code" (Bogard).

## Quando usar

- API com muitos casos de uso independentes.
- Quando cada mudança de caso de uso hoje atravessa várias pastas de camada (o problema que Bogard descreve).
- Dentro de cada módulo de um [monólito modular](04-monolito-modular.md).
- Projetos .NET com MediatR, como no dotnet/eShop (`Ordering.API` usa comandos e handlers).

## Para que tipo de projeto

A tabela é recomendação do guia. A base oficial é Bogard (o padrão pressupõe um time que reconhece code smells e refatora). As linhas sem esse apoio são juízo do guia.

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / back-end de negócio | ✅ Ótimo | Casos de uso claros, cada um com seu endpoint |
| SaaS / app web | ✅ Ótimo | Funciona no servidor; no front vira feature ([01](01-feature-first-colocation.md)) |
| Dashboard / painel admin | 🟡 Serve | Muita leitura simples, pouca regra; slice pequeno |
| Sistema com regras de negócio ricas e compartilhadas | 🟡 Serve | Exige modelo de domínio compartilhado entre slices |
| CRUD puro | 🟡 Serve | Funciona, mas a pasta por feature já basta |
| Landing page / site estático | ❌ Evite | Não há casos de uso |
| Biblioteca | ❌ Evite | A API pública é o recorte, não o caso de uso |

## Quando é bom

- **Liberdade por slice:** Bogard: cada slice decide por si como falar com o banco e pode começar simples (Transaction Script) e refatorar quando surgirem code smells.
- **Navegação por intenção:** no eShop, comandos, handlers e validators têm o nome do caso de uso (`CancelOrder...`).

## Quando é ruim

- **Depende do time:** Bogard avisa que o padrão pressupõe um time que entende code smells e refatoração; se o time não sabe quando um "service" faz demais e empurrar a lógica ao domínio, o padrão provavelmente não serve.
- **Lógica complexa:** é preciso saber reconhecer quando levar a lógica complexa ao domínio (Bogard).
- **Pouca convenção:** sem um modelo de slice fixo, cada um faz de um jeito (a documentação do ASP.NET Core não define um modelo de slice).

## Como começar

Exemplo .NET, na estrutura do app de referência dotnet/eShop (github.com/dotnet/eShop, `src/Ordering.API`, conferido em 2026-11-24). O eShop agrupa por caso de uso dentro do projeto: cada comando tem `XCommand`, `XCommandHandler` e `XCommandValidator`, em `Application/Commands` e `Application/Validations`.

```
src/
├── Ordering.API/
│   ├── Apis/
│   │   └── OrdersApi.cs                         # endpoints
│   ├── Application/
│   │   ├── Commands/                            # um caso de uso por par comando + handler
│   │   │   ├── CancelOrderCommand.cs
│   │   │   ├── CancelOrderCommandHandler.cs
│   │   │   ├── CreateOrderCommand.cs
│   │   │   └── CreateOrderCommandHandler.cs
│   │   ├── Queries/                             # OrderQueries.cs, OrderViewModel.cs
│   │   └── Validations/                         # CancelOrderCommandValidator.cs, ...
│   └── Program.cs                               # montagem e registro dos endpoints
├── Ordering.Domain/                             # entidades e regras (AggregatesModel, Events)
└── Ordering.Infrastructure/                     # EntityConfigurations e Migrations
tests/
└── Ordering.UnitTests/                          # Application/ e Domain/
```

Regras de nome e lugar:

- **Arquivos do caso de uso:** prefixo igual (`CancelOrderCommand`, `CancelOrderCommandHandler`, `CancelOrderCommandValidator`), assim a busca por nome acha tudo (padrão do eShop).
- **Teste:** `tests/Ordering.UnitTests/Application/` espelha a pasta `Application/` (eShop).

## Combina com / alternativas

- [Monólito modular](04-monolito-modular.md): um módulo com slices por dentro.
- [ASP.NET Core](10-aspnet-core.md), [NestJS e Node](09-nestjs-node.md).
- Alternativa: [camadas](03-camadas-clean-hexagonal.md) quando o domínio é rico e compartilhado.

## Decisão rápida

- **Use se:** a API tem muitos casos de uso independentes e você quer mudanças concentradas.
- **Evite se:** o sistema é dominado por um modelo de domínio complexo e compartilhado, ou é só um site.
