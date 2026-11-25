# Camadas, Clean, Onion e hexagonal

> Separar o código em anéis em que o domínio fica no centro e não depende de banco, framework ou interface, ao custo de mais pastas, mais interfaces e mais mapeamento.

| | |
|---|---|
| **Referência oficial** | Sem padrão oficial de framework. Origens: Alistair Cockburn (hexagonal, 2005), Jeffrey Palermo (Onion, 2008), Robert C. Martin (Clean, 2012). Datas conferidas em 2026-11-24 nos textos originais: Cockburn, 4/9/2005 (alistair.cockburn.us/hexagonal-architecture); Palermo, 29/7/2008 (jeffreypalermo.com/2008/07/the-onion-architecture-part-1); Martin, 13/8/2012 (blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) |
| **Categoria** | Parte 1 — Padrões que valem para qualquer stack |
| **Tipo** | Padrão de arquitetura em camadas |
| **Vale para** | Back-end em qualquer linguagem; raro no front |
| **Verificado em** | 2026-11-24 |

## O que é

As três ideias são parentes. O domínio (entidades e regras) fica no centro. Em volta vêm os casos de uso (aplicação). Na borda ficam banco, HTTP, filas e e-mail (infraestrutura). A dependência aponta sempre para dentro: a infraestrutura conhece o domínio; o domínio não conhece ninguém.

No e-book da Microsoft, as interfaces ficam no Application Core e a infraestrutura as implementa; o Application Core não depende de outras camadas da aplicação (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures). Aqui a árvore usa quatro pastas: `Domain`, `Application`, `Infrastructure` e `Api` (organização deste documento). O dotnet/eShop tem `Ordering.Domain`, `Ordering.Infrastructure` e `Ordering.API` (conferido em github.com/dotnet/eShop, pasta `src/`).

Fonte oficial mais próxima: o e-book da Microsoft "Architect Modern Web Applications with ASP.NET Core and Azure" (learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures), que descreve Clean Architecture com os projetos Application Core, Infrastructure e UI. Os nomes `Domain`, `Infrastructure` e `Api` seguem o dotnet/eShop (`Ordering.Domain`, `Ordering.Infrastructure`, `Ordering.API`); `Application` é a divisão deste documento, sem pasta equivalente no eShop. Tem custo real, por isso entra aqui com critério.

## Por que usar

- **Infraestrutura depende do núcleo, não o contrário:** detalhes de acesso a dados implementam abstrações definidas no Application Core (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).
- **Núcleo sem dependência de outras camadas da aplicação** (mesma fonte).

## Quando usar

- Sistema com regras de negócio ricas e vida longa.
- Quando já houve dor real de regra misturada com banco ou HTTP.

(Critério deste documento; a Microsoft apresenta a Clean Architecture como uma das arquiteturas comuns de aplicações web, sem fixar porte de time.)

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Sistema de negócio com regras ricas | 🟡 Serve | Há domínio a isolar (critério deste documento) |
| SaaS / app web médio | 🟡 Serve | Use dentro de cada módulo, não no sistema todo |
| CRUD simples | ❌ Evite | Sem regra de negócio, o domínio não tem o que proteger |
| Landing page / site estático | ❌ Evite | Não há domínio |
| App mobile / front | ❌ Evite | Fora do escopo: o e-book trata de aplicações ASP.NET Core |

Outros tipos (painel admin, MVP, API grande): a documentação oficial não trata esses casos; avalie pelo critério acima.

## Quando é bom

- **Dependências invertidas:** infraestrutura e detalhes de implementação dependem do Application Core (fonte: learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures).
- **Modelo documentado:** o e-book da Microsoft e o eShopOnWeb servem de referência.

## Quando é ruim

- **Mais projetos e interfaces:** o eShop separa `Domain`, `Infrastructure` e `API` em projetos distintos; cada camada a mais é uma pasta, uma interface e um mapeamento a manter.
- **Pasta por tipo disfarçada:** `Services/`, `Repositories/`, `Dtos/` gigantes, com todos os assuntos misturados. É o pior resultado.
- **Abstração sem segundo uso:** interface com uma implementação só, "para o caso de trocar" o banco que nunca troca.
- **Regra no lugar errado:** serviço "anêmico" que só chama o repositório.

## Como começar

Estrutura por camadas dentro de um módulo (base: e-book da Microsoft e dotnet/eShop, ver acima). Em .NET costuma ser um projeto por camada; em outras stacks, uma pasta.

```
src/Orders/                         # um módulo (veja o monólito modular)
├── Domain/                         # centro: não importa nada de fora
│   ├── Order.cs                    # entidade com as regras
│   ├── OrderStatus.cs              # tipos de valor e enums
│   └── IOrderRepository.cs         # contrato que o domínio exige
├── Application/                    # casos de uso, orquestra o domínio
│   ├── CreateOrder/                # um caso de uso por pasta (veja vertical slice)
│   └── CancelOrder/
├── Infrastructure/                 # implementa os contratos
│   ├── OrderRepository.cs          # banco
│   └── OrderMapping.cs
└── Api/                            # borda HTTP
    └── OrdersEndpoints.cs
```

Regras de nome e lugar:

- **Regra de dependência:** `Api` e `Infrastructure` apontam para `Application`, que aponta para `Domain`. `Domain` não importa de ninguém.
- **Organize por assunto primeiro, camada depois.** `Orders/Domain`, não `Domain/Orders` com todos os assuntos.
- **Nada de pasta `Interfaces/` global.** O contrato mora ao lado de quem o exige.
- **Sem camada vazia:** se `Application` só repassa, junte com `Api` até a regra aparecer.
- **Comece enxuto:** duas pastas (domínio e o resto) e divida quando doer.

## Combina com / alternativas

- [Monólito modular](04-monolito-modular.md): camadas por módulo, não no sistema inteiro.
- [Vertical slice](02-vertical-slice.md): slices dentro de `Application`.
- Alternativa: [feature-first](01-feature-first-colocation.md), mais simples, para a maioria dos projetos.

## Decisão rápida

- **Use se:** o domínio é rico, o sistema vai durar anos e já houve dor de regra misturada com infraestrutura.
- **Evite se:** é CRUD, MVP, painel ou site. Comece por feature e adote camadas quando doer.
