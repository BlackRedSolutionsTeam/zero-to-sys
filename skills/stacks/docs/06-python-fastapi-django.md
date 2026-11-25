# Python (FastAPI, Django e dados/IA)

> Backend em Python: FastAPI para APIs e serviços de dados e IA, Django para sistemas com admin, banco e regras prontos.

| | |
|---|---|
| **Site** | https://fastapi.tiangolo.com e https://www.djangoproject.com |
| **Categoria** | Áreas 4 e 9 — Backend e API; dados e IA |
| **Tipo** | Stack de backend, com dois frameworks |
| **Stack/composição** | FastAPI: Python, Pydantic, SQLAlchemy ou SQLModel, Alembic, PostgreSQL, uv. Django: ORM, migrações, admin e auth embutidos, PostgreSQL. Testes: pytest. Dados/IA: pandas, NumPy, bibliotecas de modelos, filas para trabalho longo. Front: separado ([SPA](04-spa-vite-api.md)) ou templates do Django |
| **Preço** | Grátis (open source) |
| **Licença** | FastAPI: MIT; Django: BSD-3-Clause (LICENSE nos repositórios, conferidos em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

FastAPI usa as anotações de tipo do Python (com Pydantic) para validar dados e gera o esquema OpenAPI e a documentação interativa (fonte: fastapi.tiangolo.com e fastapi.tiangolo.com/tutorial/first-steps). Django traz ORM (docs.djangoproject.com/en/6.1/intro/overview), migrações (topics/migrations), interface de admin (ref/contrib/admin), autenticação (topics/auth) e formulários (topics/forms) no próprio framework.

A documentação do Django lida mostra a versão 6.1 como atual, compatível com Python 3.12 a 3.15. A documentação do FastAPI recomenda instalar com `uv`; a versão atual dele no PyPI é a 0.165.0, com Python 3.11 ou superior (conferido em 2026-11-24). O Django está na 6.1.3 no PyPI, com Python 3.12 ou superior.

O FastAPI roda de forma independente do produto principal; o front pode ser separado ([SPA](04-spa-vite-api.md)).

## Por que usar

- **Mesma linguagem das bibliotecas de dados:** pandas e NumPy são pacotes Python (fonte: pandas.pydata.org, numpy.org), então o serviço os importa direto.
- **FastAPI:** documentação interativa e validação a partir dos tipos (fonte: fastapi.tiangolo.com).
- **Django:** ORM, migrações, admin e autenticação no próprio framework (fontes em "O que é").

## Quando usar

- Serviço que expõe modelo, pipeline ou análise de dados.
- API com validação rica de entrada.
- Sistema de cadastros com painel de gestão (Django).
- Time que já usa pandas, NumPy ou modelos em Python e quer expor isso como API.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Dados / IA / automação | ✅ Ótimo | pandas e NumPy são bibliotecas Python; FastAPI expõe como API |
| API para SPA ou mobile | ✅ Ótimo | FastAPI gera o esquema OpenAPI e valida pelos tipos (fastapi.tiangolo.com/tutorial/first-steps) |
| Sistema interno / cadastros | ✅ Ótimo | Django traz a interface de admin no framework (docs.djangoproject.com/en/6.1/ref/contrib/admin) |
| SaaS / app web | 🟡 Serve | Django com templates ou back de uma SPA; o front em TypeScript fica em projeto separado |
| E-commerce | 🟡 Serve | Sem recurso oficial específico de loja; compare com [Laravel/Rails](09-laravel-rails.md) |
| Tempo real | 🟡 Serve | FastAPI documenta WebSockets (fastapi.tiangolo.com/advanced/websockets) e Django suporta ASGI (docs.djangoproject.com/en/6.1/howto/deployment/asgi) |
| Site de conteúdo | ❌ Evite | Para conteúdo veja [Astro](01-astro-conteudo.md) |
| App mobile / desktop | ❌ Evite | Python serve aqui como backend; veja [mobile](11-mobile.md) |
| Alta concorrência com CPU | 🟡 Serve | A doc do FastAPI separa trabalho I/O bound (async) de CPU bound, que pede processos em paralelo (fastapi.tiangolo.com/async); veja também [Go](10-go-api.md) |

## Quando é bom

- **Django admin:** interface de gestão dos modelos já no framework (docs.djangoproject.com/en/6.1/ref/contrib/admin).
- **Dicas de tipo no FastAPI:** usadas para validar e documentar (fastapi.tiangolo.com).
- **Dados e IA na mesma linguagem:** pandas e NumPy são pacotes Python.

## Quando é ruim

- **Tipos não são checados em execução:** o runtime do Python não impõe as anotações de tipo; quem as usa são ferramentas de terceiros (fonte: docs.python.org/3/library/typing.html). O FastAPI valida a entrada, mas o resto do código precisa de testes e verificador de tipos.
- **FastAPI sem ORM nem admin:** o tutorial de banco usa SQLModel (sobre SQLAlchemy e Pydantic) e cita o Alembic para migrações (fastapi.tiangolo.com/tutorial/sql-databases); a segurança vem como ferramentas (fastapi.tiangolo.com/tutorial/security), não como painel pronto.
- **Dois projetos se o front for separado:** a API em Python e o front em outra stack.
- **Trabalho CPU bound:** exige processos em paralelo (multiprocessing), segundo fastapi.tiangolo.com/async.

## Como começar

FastAPI (comandos da documentação oficial):

```bash
uv add "fastapi[standard]"
uv run fastapi dev
```

Django (instalação da documentação oficial, docs.djangoproject.com/en/6.1/topics/install; versão atual 6.1.3 no PyPI):

```bash
python -m pip install Django
django-admin startproject meusite
```

O `django-admin startproject` é o comando oficial do Django para criar o projeto (tutorial oficial em docs.djangoproject.com, conferido em 2026-11-24). O tutorial usa `django-admin startproject mysite djangotutorial`: o segundo argumento é o diretório de destino; sem ele, o comando cria o diretório do nome do projeto.

## Combina com / alternativas

- [SPA + API](04-spa-vite-api.md): front React consumindo FastAPI.
- [Next.js](02-nextjs-saas.md) como produto principal e FastAPI como serviço à parte, quando há dados ou IA em Python.
- [Node](05-node-api.md): quando o time é só de JavaScript.
- [Laravel/Rails](09-laravel-rails.md): alternativas de monólito; veja o documento.
- Jobs longos e filas: skill infra.

## Decisão rápida

- **Use se:** o projeto envolve dados, IA ou automação, ou é um sistema de cadastros que se beneficia do admin do Django.
- **Evite se:** quer TypeScript de ponta a ponta, ou o projeto é um site de conteúdo.
