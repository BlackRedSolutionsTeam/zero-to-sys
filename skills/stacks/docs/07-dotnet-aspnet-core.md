# .NET (ASP.NET Core) para sistema corporativo

> Backend em C# com ASP.NET Core e EF Core, para sistemas corporativos, internos e de longa vida, principalmente em empresas que já usam o ecossistema Microsoft.

| | |
|---|---|
| **Site** | https://dotnet.microsoft.com |
| **Categoria** | Áreas 4 e 5 — Backend e API; sistema corporativo/interno |
| **Tipo** | Stack completa opinativa |
| **Stack/composição** | Backend: C# e ASP.NET Core (Minimal APIs ou controllers). ORM: Entity Framework Core. Banco: SQL Server ou PostgreSQL. Auth: ASP.NET Core Identity ou OpenID Connect. Frontend: React com Vite ([SPA](04-spa-vite-api.md)), Razor/MVC ou Blazor. Testes: xUnit |
| **Preço** | Grátis (SDK e ASP.NET Core são open source). O Visual Studio tem edições pagas (visualstudio.microsoft.com/vs/pricing) |
| **Licença** | MIT (ASP.NET Core, LICENSE.txt do repositório dotnet/aspnetcore, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

.NET é a plataforma da Microsoft; ASP.NET Core é o framework web dela e C# a linguagem principal. O ASP.NET Core oferece Minimal APIs, controllers, Blazor, OpenAPI e Identity (learn.microsoft.com/aspnet/core).

Segundo a página oficial lida (atualizada em 2026-11-10), as versões suportadas são o .NET 10 (LTS, suporte até novembro de 2028) e o .NET 11 (STS, lançado em novembro de 2026, suporte por 24 meses). A política diz que LTS tem três anos de suporte e STS, dois; o fim do suporte do .NET 10 e do .NET 11 é 14/11/2028 (dotnet.microsoft.com/platform/support/policy/dotnet-core).

## Por que usar

- **Ciclo de suporte publicado:** versões LTS recebem suporte e correções gratuitos por três anos; as STS, por dois (.NET 10 é LTS; dotnet.microsoft.com/platform/support/policy/dotnet-core).
- **Tipos de API:** Minimal APIs (recomendadas para projetos novos) ou controllers (learn.microsoft.com/aspnet/core/fundamentals/apis).
- **Front no mesmo framework:** Blazor e Razor/MVC fazem parte do ASP.NET Core (learn.microsoft.com/aspnet/core).

## Quando usar

- Sistema interno, back-office e API para web e mobile.
- Empresa que já tem time e infraestrutura .NET.
- Projeto que precisa de um ciclo de suporte publicado (LTS de três anos).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Sistema interno corporativo | ✅ Ótimo | ASP.NET Core Identity e suporte LTS de três anos |
| API para SPA ou mobile | ✅ Ótimo | Minimal APIs com suporte a OpenAPI (learn.microsoft.com/aspnet/core/fundamentals/openapi) |
| Dashboard / painel admin | ✅ Ótimo | Blazor ou Razor/MVC no mesmo projeto, ou React na frente |
| SaaS / app web | 🟡 Serve | Dá para fazer; front em Blazor/Razor ou em SPA separada |
| E-commerce | 🟡 Serve | Sem recurso oficial de e-commerce no ASP.NET Core; avaliar caso a caso |
| MVP / protótipo | 🟡 Serve | Sem base oficial para comparar; avaliar caso a caso |
| Site de conteúdo | ❌ Evite | Astro é feito para sites de conteúdo ([Astro](01-astro-conteudo.md)) |
| Dados/IA | ❌ Evite | Veja [Python](06-python-fastapi-django.md) |
| App mobile | 🟡 Serve | Como backend; app em si, veja [mobile](11-mobile.md) |

## Quando é bom

- **Injeção de dependência embutida** no framework (learn.microsoft.com/aspnet/core/fundamentals/dependency-injection).
- **Política de ciclo de vida publicada** (dotnet.microsoft.com/platform/support/policy/dotnet-core).
- **Autenticação pronta:** ASP.NET Core Identity (learn.microsoft.com/aspnet/core/security/authentication/identity).

## Quando é ruim

- **Versão nova todo ano**, alternando LTS e STS: as STS têm só dois anos de suporte e pedem plano de atualização (dotnet.microsoft.com/platform/support/policy/dotnet-core).
- **Front separado:** com React no front, o time mantém duas linguagens (C# e TypeScript).
- **Visual Studio** tem edições pagas (visualstudio.microsoft.com/vs/pricing).

## Como começar

Comandos da CLI do .NET. O tutorial da Microsoft (learn.microsoft.com, "Tutorial: Create a minimal API with ASP.NET Core", conferido em 2026-11-24) usa `dotnet new webapi -o TodoApi`. O comando não foi executado nesta verificação.

```bash
dotnet new webapi -n MinhaApi
cd MinhaApi
dotnet run
```

Instale o SDK da linha LTS para sistemas de longa vida. EF Core: `dotnet add package Microsoft.EntityFrameworkCore`. Estrutura de pastas e camadas: skill architecture.

## Combina com / alternativas

- [SPA com Vite](04-spa-vite-api.md): React na frente de uma API .NET.
- [Java com Spring Boot](08-java-spring-boot.md): alternativa equivalente em empresas Java.
- [Go](10-go-api.md): para serviços menores e mais leves.
- Hospedagem no Azure ou em servidor próprio: skill infra.

## Decisão rápida

- **Use se:** o sistema é corporativo, de longa vida, com regras complexas, ou a empresa já tem time e infraestrutura .NET.
- **Evite se:** o time é de JavaScript e quer velocidade de MVP, ou o trabalho é de dados e IA.
