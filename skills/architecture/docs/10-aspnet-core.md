# ASP.NET Core (solução e projetos)

> Uma solução com um projeto por fronteira e pastas por funcionalidade dentro da API, como no app de referência dotnet/eShop.

| | |
|---|---|
| **Referência oficial** | learn.microsoft.com/aspnet/core. A visão geral de fundamentos (learn.microsoft.com/aspnet/core/fundamentals) trata de `Program.cs`, DI, middleware e `wwwroot`, não de pastas da solução. Para a estrutura da solução, a Microsoft mostra o e-book [Architect Modern Web Applications with ASP.NET Core and Azure](https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) (um projeto, ou três: Application Core, Infrastructure e UI/Web) e o app de referência [dotnet/eShop](https://github.com/dotnet/eShop) (`src/` e `tests/`, projetos `X.API`, `X.Domain`, `X.Infrastructure`, mais `eShop.AppHost` do .NET Aspire). Nenhum deles mostra monólito modular com vertical slice, então a árvore abaixo segue só a estrutura do eShop |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção da Microsoft (e-book e dotnet/eShop) |
| **Vale para** | ASP.NET Core Web API, MVC e Razor Pages em C# |
| **Verificado em** | 2026-11-24 |

## O que é

O .NET separa em soluções que reúnem projetos (`.csproj`). Um projeto só usa o código de outro se tiver uma referência de projeto (fonte: learn.microsoft.com/visualstudio/ide/managing-references-in-a-project). Por isso a solução pode marcar as fronteiras de um [monólito modular](04-monolito-modular.md).

Os templates trazem pastas conhecidas (`Controllers`, `Models`, `Views`, `Pages`, `wwwroot`, `Program.cs`, `appsettings.json`). Elas servem para começar, mas o e-book da Microsoft lista a desvantagem: com o crescimento, os arquivos de UI ficam espalhados por pastas de tipo e a lógica de negócio se dispersa entre `Models` e `Services` (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures). O eShop organiza a API por caso de uso (`Application/Commands`, `Queries`), próximo do [vertical slice](02-vertical-slice.md).

## Por que usar

- **Fronteira por referência de projeto:** um projeto só usa outro se referenciar (fonte: learn.microsoft.com/visualstudio/ide/managing-references-in-a-project).
- **`src/` e `tests/`** na raiz, como no dotnet/eShop.
- **Testes por projeto:** o eShop tem `Ordering.UnitTests` e `Ordering.FunctionalTests` ao lado de `Ordering.API` (fonte: github.com/dotnet/eShop).

## Quando usar

- Web APIs em C# (fonte: learn.microsoft.com/aspnet/core/fundamentals/apis).
- Sistemas com mais de uma área de funcionalidade, onde o e-book mostra a separação em projetos (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / back-end de negócio | ✅ Ótimo | Web API é o foco do eShop (`Ordering.API`, `Catalog.API`) e a Microsoft documenta APIs em learn.microsoft.com/aspnet/core/fundamentals/apis |
| Sistema interno / SaaS / e-commerce | ✅ Ótimo | O eShop é um e-commerce de referência com serviços em projetos separados (github.com/dotnet/eShop) |
| Dashboard / painel admin | 🟡 Serve | MVC e Razor Pages com `Areas` para partes distintas (fonte: learn.microsoft.com/aspnet/core/mvc/controllers/areas) |
| MVP / protótipo | 🟡 Serve | O e-book mostra a opção de um projeto só (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures) |
| Landing page / site estático | ❌ Evite | A documentação não trata esse uso; ASP.NET Core serve páginas, mas o uso aqui é de back-end |

## Quando é bom

- **Módulo só vê o outro por referência de projeto** (fonte: learn.microsoft.com/visualstudio/ide/managing-references-in-a-project).
- **O e-book prevê a evolução:** de um projeto para a divisão em Application Core, Infrastructure e Web (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).

## Quando é ruim

- **Pasta por tipo no template:** o e-book aponta que a lógica se espalha entre `Models` e `Services` e que as pastas de UI crescem (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).
- **Mais projetos, mais manutenção:** o e-book mostra a solução de um projeto como opção para aplicações simples (mesma fonte).
- **Namespace diferente da pasta:** a regra IDE0130 do analisador acusa (fonte: learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide0130).

## Como começar

Estrutura do dotnet/eShop (github.com/dotnet/eShop, conferido em 2026-11-24): `src/` e `tests/` na raiz, `Directory.Build.props`, e um projeto por camada em cada serviço (`Ordering.API`, `Ordering.Domain`, `Ordering.Infrastructure`). Dentro de `Ordering.API`, `Apis/`, `Application/Commands`, `Application/Queries` e `Application/Validations`. `Program.cs` e `appsettings.json` também estão no eShop.

```
eShop/                                  # raiz do repositório
├── eShop.slnx                          # solução
├── Directory.Build.props               # regras comuns dos projetos
├── src/
│   ├── Ordering.API/                   # projeto: rotas e casos de uso
│   │   ├── Apis/                       # OrdersApi.cs: endpoints
│   │   ├── Application/
│   │   │   ├── Commands/               # CreateOrderCommand.cs, CreateOrderCommandHandler.cs
│   │   │   ├── Queries/                # OrderQueries.cs, OrderViewModel.cs
│   │   │   └── Validations/            # CreateOrderCommandValidator.cs
│   │   ├── Program.cs                  # montagem
│   │   └── appsettings.json
│   ├── Ordering.Domain/                # projeto: entidades e regras (AggregatesModel, Events)
│   ├── Ordering.Infrastructure/        # projeto: EntityConfigurations e Migrations
│   ├── Basket.API/                     # outro serviço, mesma forma
│   └── Catalog.API/
└── tests/
    ├── Ordering.UnitTests/             # Application/ e Domain/
    └── Ordering.FunctionalTests/
```

Regras de nome e lugar:

- **Arquivo:** `PascalCase.cs` com o nome do tipo, como no eShop (`CreateOrderCommand.cs`).
- **Namespace igual ao caminho da pasta** (regra IDE0130, learn.microsoft.com/dotnet/fundamentals/code-analysis/style-rules/ide0130).
- **Projeto:** `Servico.Camada` (`Ordering.API`), pasta com o mesmo nome (padrão do eShop).
- **Em projeto pequeno:** um projeto só; o e-book da Microsoft mostra a opção de um projeto e a de três (Application Core, Infrastructure e Web).
- **Razor Pages e MVC:** `Pages/`, `Views/`, `wwwroot/` seguem o template; agrupe por `Areas/` quando o sistema tiver partes distintas.

## Combina com / alternativas

- [Vertical slice](02-vertical-slice.md) e [monólito modular](04-monolito-modular.md).
- [Camadas](03-camadas-clean-hexagonal.md) dentro de módulos de domínio rico.
- Alternativas: um projeto por camada no sistema todo (`Domain`, `Application`, `Infrastructure`), que cresce mal por tipo.

## Decisão rápida

- **Use se:** é API ou sistema em C# com vários assuntos; use projetos como fronteira (fonte: e-book da Microsoft e dotnet/eShop).
- **Evite se:** é uma aplicação simples: o e-book mostra a opção de um projeto só.
