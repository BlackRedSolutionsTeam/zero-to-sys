# Go para APIs e serviços

> Backend em Go: binário compilado, concorrência embutida e biblioteca padrão com servidor HTTP, para APIs, serviços de rede e ferramentas de linha de comando.

| | |
|---|---|
| **Site** | https://go.dev |
| **Categoria** | Áreas 4, 8 e 12 — Backend, tempo real e CLI |
| **Tipo** | Stack de backend |
| **Stack/composição** | Go com biblioteca padrão (`net/http`) ou um roteador leve (chi, Gin ou Echo). Banco: PostgreSQL com `pgx`. Consultas: sqlc ou GORM. Migrações: goose ou golang-migrate. Contrato: OpenAPI. Testes: pacote `testing` da biblioteca padrão. Front: [SPA](04-spa-vite-api.md) |
| **Preço** | Grátis (open source) |
| **Licença** | BSD-3-Clause (LICENSE do repositório golang/go, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Go é uma linguagem compilada, de código aberto e mantida pelo Google, com concorrência embutida e biblioteca padrão robusta (go.dev). O `go build` gera um executável (go.dev/doc/tutorial/compile-install). A biblioteca padrão traz servidor HTTP (pkg.go.dev/net/http) e testes (pkg.go.dev/testing).

A página de instalação lida não informa o número da versão atual do Go; baixe a versão estável em https://go.dev/dl. Há tutorial oficial de API com o pacote Gin (go.dev/doc/tutorial/web-service-gin).

## Por que usar

- **Concorrência embutida** e biblioteca padrão robusta (go.dev).
- **Formato único de código:** o `gofmt` padroniza a formatação (go.dev/doc/effective_go).
- **Compilação cruzada** por variáveis `GOOS` e `GOARCH` (go.dev/doc/install/source#environment).
- **Servidor HTTP na biblioteca padrão** (pkg.go.dev/net/http).

## Quando usar

- API ou microserviço com servidor HTTP da biblioteca padrão.
- Serviço de rede, proxy, gateway ou worker.
- CLI e ferramentas internas distribuídas como executável.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / microserviço | ✅ Ótimo | `net/http` na biblioteca padrão e tutorial oficial de API (go.dev/doc/tutorial/web-service-gin) |
| Tempo real (WebSocket, streaming) | ✅ Ótimo | Concorrência embutida na linguagem (go.dev) |
| CLI / ferramenta de desenvolvedor | ✅ Ótimo | `go build` e compilação cruzada (go.dev/doc/install/source#environment) |
| Sistema interno corporativo | 🟡 Serve | Como serviço; sem framework de telas na biblioteca padrão |
| SaaS / app web | 🟡 Serve | Como API; telas ficam em outro projeto |
| E-commerce | 🟡 Serve | Bom para serviços de pedido e estoque; vitrine é outra stack |
| MVP / protótipo | ❌ Evite | Biblioteca padrão não traz admin, auth nem filas |
| Site de conteúdo | ❌ Evite | Não é o foco da linguagem |
| Dados/IA | ❌ Evite | Veja [Python](06-python-fastapi-django.md) |
| App mobile | ❌ Evite | Só como backend |

## Quando é bom

- **Formato padronizado** pelo `gofmt` (go.dev/doc/effective_go).
- **Testes na própria linguagem:** pacote `testing` e comando `go test` (pkg.go.dev/testing).
- **Aprendizado:** o site oficial descreve a linguagem como "fácil de aprender e ótima para times" (go.dev).

## Quando é ruim

- **Sem ORM, admin nem framework na biblioteca padrão:** você escolhe pacotes de terceiros (chi, Gin, Echo, sqlc, GORM).
- **Erros são valores:** a linguagem não tem exceções e o tratamento é explícito (go.dev/doc/faq#exceptions).
- **Sem front:** não traz framework de telas.

## Como começar

Instalação pela página oficial (https://go.dev/doc/install) e depois, comandos usuais do Go (versão atual em go.dev/dl em 2026-11-24: go1.27.4):

```bash
mkdir minha-api && cd minha-api
go mod init exemplo.com/minha-api
go run .
```

Estrutura de pastas é da skill architecture. Imagem de container e hospedagem são da skill infra.

## Combina com / alternativas

- [SPA com Vite](04-spa-vite-api.md): front React consumindo a API Go.
- [Node](05-node-api.md): quando o time é só JavaScript.
- [.NET](07-dotnet-aspnet-core.md) e [Java](08-java-spring-boot.md): quando o sistema tem muita regra de negócio.
- Alternativa de fora: Rust para CLI e serviços (rust-lang.org).

## Decisão rápida

- **Use se:** precisa de serviço de rede com biblioteca padrão robusta, ou ferramenta de linha de comando distribuída como executável.
- **Evite se:** o projeto é um sistema de cadastros com muita tela e a equipe espera admin e auth prontos.
