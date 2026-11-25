# SPA com Vite + API separada

> Frontend React estático (Vite) conversando com uma API própria: serve quando o backend atende mais de um cliente ou tem outra linguagem.

| | |
|---|---|
| **Site** | https://vite.dev |
| **Categoria** | Área 3 — SPA + API separada |
| **Tipo** | Arquitetura de duas partes (front e back independentes) |
| **Stack/composição** | Frontend: React, Vite, TypeScript, TanStack Query, React Router (modo biblioteca), Tailwind, shadcn/ui. Backend: qualquer API do documento 05 a 10. Contrato: OpenAPI. Auth: sessão por cookie ou token, emitida pela API. Testes: Vitest, Playwright no front; testes de integração no back |
| **Preço** | Grátis |
| **Licença** | Vite: MIT; React: MIT (LICENSE nos repositórios, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

É a divisão clássica: um app React compilado em arquivos estáticos e uma API que entrega JSON. O front não tem servidor próprio. Quem guarda dados, regras e autenticação é o backend.

O contrato entre as partes pode ser escrito em OpenAPI (spec.openapis.org). O openapi-typescript converte esquemas OpenAPI 3.0/3.1 em tipos TypeScript e cria um cliente de fetch tipado (fonte: openapi-ts.dev), o que mantém os tipos do front alinhados ao contrato.

O comando de criação do Vite é `npm create vite@latest` (fonte: vite.dev/guide).

## Por que usar

- **Backend independente:** a API é um contrato HTTP, então o mesmo servidor pode atender web, mobile e integrações.
- **Linguagem livre no back:** o front só consome HTTP/OpenAPI, qualquer linguagem serve.
- **Deploy separado:** o build do Vite gera arquivos estáticos que se publicam à parte (fonte: vite.dev/guide/static-deploy).

## Quando usar

- Já existe uma API ou ela precisa servir app mobile e web.
- Backend em .NET, Java, Python, Go ou Laravel, com tela em React.
- Área logada em que SEO não importa.
- Times separados de front e back.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS / app web | ✅ Ótimo | Faz sentido se o back atende outros clientes; se a base for única, veja [Next.js](02-nextjs-saas.md) |
| Dashboard / painel admin | ✅ Ótimo | Área logada não depende de indexação; o build do Vite é estático (vite.dev/guide/static-deploy) |
| Sistema interno corporativo | ✅ Ótimo | Casa com back em [.NET](07-dotnet-aspnet-core.md) ou [Spring](08-java-spring-boot.md) |
| MVP / protótipo | 🟡 Serve | São duas partes para publicar; uma base única ([Next.js](02-nextjs-saas.md)) tem uma só |
| E-commerce | 🟡 Serve | O Google enfileira páginas JavaScript para renderização antes de indexar (developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics); para a vitrine considere renderização no servidor |
| Site institucional / blog | ❌ Evite | O Google renderiza JavaScript em uma fila à parte (mesma fonte do e-commerce); para conteúdo veja [Astro](01-astro-conteudo.md) |
| Tempo real | 🟡 Serve | O navegador tem WebSocket; o servidor de conexão fica no back |
| App mobile | ❌ Evite | É web; veja [mobile](11-mobile.md) |

## Quando é bom

- **Separação** entre tela (front) e regra de negócio (back), em projetos distintos.
- **Reuso do backend** em outros clientes, pelo contrato HTTP.
- **HMR no Vite:** atualiza o módulo sem recarregar a página (fonte: vite.dev/guide/features).
- **Tipos gerados do OpenAPI** com o openapi-typescript (fonte: openapi-ts.dev).

## Quando é ruim

- **Indexação via JavaScript:** o HTML inicial vem sem o conteúdo; o Google renderiza em fila separada (developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).
- **Dois projetos** para versionar, publicar e manter sincronizados.
- **CORS:** front e back em origens diferentes exigem cabeçalhos CORS no servidor (fonte: developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS). O Vite tem `server.proxy` para o desenvolvimento (vite.dev/config/server-options).
- **Duplicação de tipos** se o contrato não for gerado.

## Como começar

Comando de criação do Vite (versão atual do Vite no npm: 8.3.8; `create-vite` 9.3.4, conferidos em 2026-11-24; rode `npm create vite@latest --help` para ver os templates):

```bash
npm create vite@latest meu-app -- --template react-ts
```

Dados no cliente: TanStack Query, que cuida de buscar, cachear e atualizar dados do servidor (fonte: tanstack.com/query/latest/docs/framework/react/overview). Gerar o cliente da API a partir do OpenAPI: ferramentas como openapi-typescript (openapi-ts.dev). Componentes: skill design.

## Combina com / alternativas

- Back: [Node](05-node-api.md), [Python](06-python-fastapi-django.md), [.NET](07-dotnet-aspnet-core.md), [Java](08-java-spring-boot.md), [Laravel/Rails](09-laravel-rails.md), [Go](10-go-api.md).
- [Next.js](02-nextjs-saas.md) ou [React Router/TanStack Start](03-react-router-tanstack-start.md): quando uma base única basta.
- Hospedagem e proxy: skill infra.

## Decisão rápida

- **Use se:** o backend já existe, atende outros clientes ou está em outra linguagem, e a tela é uma área logada.
- **Evite se:** o produto só tem uma interface web (veja [Next.js](02-nextjs-saas.md)), ou a indexação do conteúdo importa.
