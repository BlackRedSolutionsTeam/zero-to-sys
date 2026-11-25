# Java (Spring Boot) para sistema corporativo

> Backend em Java com Spring Boot, para sistemas corporativos com muitas integrações, segurança e mensageria.

| | |
|---|---|
| **Site** | https://spring.io/projects/spring-boot |
| **Categoria** | Áreas 4 e 5 — Backend e API; sistema corporativo/interno |
| **Tipo** | Stack completa opinativa |
| **Stack/composição** | Backend: Java e Spring Boot (Spring Web, Spring Security, Spring Data JPA). Banco: PostgreSQL ou Oracle (a doc do Spring Boot cita o pool `oracleucp`: docs.spring.io/spring-boot/reference/data/sql.html; o Testcontainers tem módulo Oracle: java.testcontainers.org). Migrações: Flyway. Frontend: React com Vite ([SPA](04-spa-vite-api.md)) ou Thymeleaf. Build: Maven ou Gradle. Testes: JUnit e Testcontainers (java.testcontainers.org: bancos em contêiner para testes de integração) |
| **Preço** | Grátis (open source). Suporte comercial é pago, à parte |
| **Licença** | Apache-2.0 (Spring Boot, repositório spring-projects/spring-boot, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Spring Boot é o framework que monta uma aplicação Java pronta para rodar, com servidor embutido e configuração por convenção. Em volta dele há suporte a web, segurança, dados, mensageria e agendamento (docs.spring.io/spring-boot/reference).

A página oficial lida na verificação mostra o Spring Boot 4.2.0 como versão atual (GA). O Maven Central também lista a 4.2.0 como última versão. O Spring Initializr (start.spring.io) oferece Java 17, 21, 25 e 27, com 17 como padrão; 17 é a versão mais antiga que ele aceita (conferido em 2026-11-24).

## Por que usar

- **Módulos oficiais** para web, segurança (Spring Security), dados, mensageria e agendamento (docs.spring.io/spring-boot/reference).
- **Monitoramento embutido:** o Actuator expõe endpoints, métricas e rastreamento (docs.spring.io/spring-boot/reference/actuator).
- **Imagem nativa GraalVM** como opção de empacotamento (docs.spring.io/spring-boot/reference/packaging/native-image).

## Quando usar

- Sistema com muitas integrações e mensageria.
- Sistema que precisa de segurança e agendamento prontos.
- Empresa que já tem time, ferramentas e servidores Java.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Sistema corporativo / regulado | ✅ Ótimo | Spring Security, Spring Data e mensageria na documentação oficial |
| API de alto volume | ✅ Ótimo | Opção de imagem nativa GraalVM, com menos memória e início mais rápido (docs.spring.io/spring-boot/reference/packaging/native-image) |
| Processamento em lote / integrações | ✅ Ótimo | Quartz e mensageria documentados (docs.spring.io/spring-boot/reference/io/quartz.html) |
| Dashboard / painel admin | 🟡 Serve | Como back de uma SPA ou com Thymeleaf |
| SaaS / app web | 🟡 Serve | Dá para fazer; sem recurso oficial específico para SaaS |
| E-commerce | 🟡 Serve | Sem recurso oficial de e-commerce; avaliar caso a caso |
| MVP / protótipo | ❌ Evite | Sem base oficial para comparar; avaliar caso a caso |
| Site de conteúdo | ❌ Evite | Não é o foco do Spring Boot |
| Dados/IA | ❌ Evite | Veja [Python](06-python-fastapi-django.md) |

## Quando é bom

- **Segurança:** Spring Security integrado (docs.spring.io/spring-boot/reference/web/spring-security.html).
- **Servidor embutido e configuração por convenção** (spring.io/projects/spring-boot).
- **Observabilidade:** Actuator com métricas e rastreamento (docs.spring.io/spring-boot/reference/actuator).

## Quando é ruim

- **Memória e início na JVM:** a documentação do Spring Boot diz que imagens nativas GraalVM têm em geral menos memória e início mais rápido, ao custo de um classpath fixo no build e de limites com reflexão e proxies (docs.spring.io/spring-boot/reference/packaging/native-image, 2026-11-24).
- **Requisitos de versão:** o Spring Boot 4.2.0 exige Java 17 ou superior e o Spring Framework 7.1 (docs.spring.io/spring-boot/system-requirements.html).
- **Front separado:** com React no front, o time mantém duas linguagens (Java e TypeScript).
- **Kotlin ou Java:** decisão extra; o Spring Boot suporta os dois (docs.spring.io/spring-boot/reference/features/kotlin.html).

## Como começar

O gerador oficial é o Spring Initializr, no site start.spring.io (o Initializr respondeu em 2026-11-24 com Boot 4.2.0 como padrão e Java 17 como padrão). Escolha Maven ou Gradle, a versão do Boot e as dependências (Web, Security, Data JPA, PostgreSQL, Flyway). Estrutura de pastas e camadas: skill architecture.

```bash
./mvnw spring-boot:run
```

O comando acima roda o projeto gerado com Maven; confira o wrapper gerado.

## Combina com / alternativas

- [SPA com Vite](04-spa-vite-api.md): React na frente.
- [.NET](07-dotnet-aspnet-core.md): alternativa equivalente.
- [Go](10-go-api.md): serviços menores e mais leves.
- Mensageria, containers e implantação: skill infra.

## Decisão rápida

- **Use se:** o ambiente é corporativo ou regulado, o time já é Java, ou há muitas integrações.
- **Evite se:** o objetivo é validar uma ideia depressa.
