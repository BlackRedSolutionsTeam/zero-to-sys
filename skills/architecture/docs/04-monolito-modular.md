# Monólito modular

> Um só sistema implantável, dividido em módulos por assunto com fronteiras explícitas, para ter a organização dos microserviços sem o custo de rede e operação.

| | |
|---|---|
| **Referência oficial** | NestJS: "Modules" (docs.nestjs.com/modules), que define módulos por feature. Para .NET, a Microsoft descreve o monólito em camadas (Application Core, Infrastructure, UI) no e-book "Architect Modern Web Applications with ASP.NET Core and Azure" (learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures). Em Java, o projeto oficial Spring Modulith define o módulo de aplicação como um pacote com API exposta a outros módulos e implementação interna que eles não acessam (https://docs.spring.io/spring-modulith/reference/fundamentals.html, conferido em 2026-11-24); a regra de módulos deste documento segue essa definição |
| **Categoria** | Parte 1 — Padrões que valem para qualquer stack |
| **Tipo** | Padrão de organização do sistema |
| **Vale para** | Back-end em qualquer stack; também front grande |
| **Verificado em** | 2026-11-24 |

## O que é

O sistema é um único processo e um único deploy, mas o código é cortado em módulos: `Orders`, `Billing`, `Users`. Cada módulo tem uma API pública pequena e esconde o resto. Um módulo só fala com outro pela API pública ou por eventos; nunca importa arquivos internos (regra deste documento, na linha do Spring Modulith: tipos internos não são acessíveis a outros módulos).

O NestJS faz isso de forma nativa: um módulo declara o que exporta (`exports`) e quem o importa só enxerga isso. Em outras stacks a fronteira é separação em projetos (.NET), pacotes (Python, Go `internal/`) ou regra de lint.

## Por que usar

- **Encapsulamento por módulo:** o NestJS só expõe a quem importa o que o módulo exporta em `exports` (docs.nestjs.com/modules); o Spring Modulith esconde tipos internos pelo escopo de pacote do Java (docs.spring.io/spring-modulith/reference/fundamentals.html).
- **Um processo e um deploy:** definição deste padrão (sem rede entre módulos).

## Quando usar

- Sistema de negócio com vários assuntos distintos.
- Quando a pasta única `src/` já não cabe, mas microserviços seriam exagero (critério deste documento).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / back-end de negócio | ✅ Ótimo | Módulos NestJS (`exports`) e Spring Modulith são feitos para isso |
| SaaS / app web / sistema interno | 🟡 Serve | Se tiver vários assuntos de negócio (critério deste documento) |
| Landing page / site estático | ❌ Evite | Não há módulos de negócio |

Outros tipos (e-commerce, painel admin, MVP, biblioteca): a documentação oficial não trata esses casos.

## Quando é bom

- **Fronteira imposta pela ferramenta:** `exports` no NestJS (docs.nestjs.com/modules), escopo de pacote no Java (Spring Modulith) e `internal/` no Go (go.dev/doc/go1.4#internalpackages).

## Quando é ruim

- **Fronteira só no papel:** sem lint ou projeto separado, alguém importa o interno e o módulo vira bola de lama.
- **Banco compartilhado sem regra:** módulos fazendo `JOIN` nas tabelas uns dos outros. Dê a cada módulo suas tabelas (schema ou prefixo).
- **Módulos recortados errado:** `Common` ou `Core` com tudo dentro.
- **Burocracia em projeto pequeno:** três módulos para 12 endpoints.

## Como começar

Exemplo agnóstico de stack. Em NestJS, cada módulo é uma pasta com `x.module.ts` (docs.nestjs.com/modules); em Java, cada módulo é um subpacote direto do pacote da aplicação (Spring Modulith); nas demais stacks a árvore aplica a mesma regra: API pública do módulo e o resto interno.

```
src/
├── modules/
│   ├── orders/                    # módulo: um assunto do negócio
│   │   ├── api/                   # a ÚNICA porta de entrada para outros módulos
│   │   │   └── orders.api.ts      # funções e tipos públicos
│   │   ├── features/              # casos de uso (veja vertical slice)
│   │   │   ├── create-order/
│   │   │   └── cancel-order/
│   │   ├── domain/                # entidades e regras do módulo
│   │   ├── data/                  # tabelas, repositórios, migrações do módulo
│   │   ├── events/                # eventos que o módulo publica
│   │   └── orders.module.ts       # registro do módulo
│   ├── billing/                   # mesma forma
│   └── users/
├── shared/                        # kernel pequeno: tipos base, erros, utilitários
├── host/                          # montagem: registra módulos, config, main
└── main.ts
```

Regras de nome e lugar:

- **Um módulo = um assunto de negócio**, nome no plural e em minúsculas (`orders`).
- **Só `api/` e `events/` são públicos.** Todo o resto é interno e proibido para os outros módulos.
- **Reforce por ferramenta:** `exports` no NestJS, projetos separados no .NET, `internal/` no Go, regra do ESLint ou `import-linter` no Python.
- **Cada módulo tem seus dados.** Referência entre módulos é por id, nunca por chave estrangeira cruzada.
- **`shared/` pequeno:** só tipos base e utilitários sem negócio.
- **Teste de módulo:** em `modules/orders/` ao lado; teste de integração do sistema em `tests/`.

## Combina com / alternativas

- [Vertical slice](02-vertical-slice.md) por dentro do módulo; [camadas](03-camadas-clean-hexagonal.md) só nos módulos com domínio rico.
- [NestJS](09-nestjs-node.md) e [ASP.NET Core](10-aspnet-core.md): suporte natural.
- [Monorepo](05-monorepo.md): quando os módulos viram pacotes.
- Alternativa: microserviços, que só valem com times independentes e escala diferente por parte (veja "O que saiu da lista").

## Decisão rápida

- **Use se:** o sistema tem vários assuntos de negócio, um time e um deploy.
- **Evite se:** o projeto é pequeno (pasta por feature basta) ou se ninguém vai manter as fronteiras.
