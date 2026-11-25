# Python (FastAPI e Django)

> FastAPI: um pacote `app` com routers por assunto; Django: um projeto com várias apps, uma por domínio, cada uma com seus modelos, rotas, templates e testes.

| | |
|---|---|
| **Referência oficial** | fastapi.tiangolo.com/tutorial/bigger-applications/ (FastAPI); github.com/fastapi/full-stack-fastapi-template (template oficial do FastAPI, pasta `backend/`); docs.djangoproject.com/en/stable/intro/tutorial01/ e tutorial07 (Django) |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção de framework (FastAPI, Django) e template oficial full-stack-fastapi-template |
| **Vale para** | FastAPI e Django |
| **Verificado em** | 2026-11-24 |

## O que é

O guia "Bigger Applications" do FastAPI mostra um pacote `app` com `main.py`, `dependencies.py`, uma pasta `routers/` (um arquivo por assunto, cada um com um `APIRouter`) e `internal/`. Os `__init__.py` marcam pacotes. O `main.py` cria o app e inclui os routers. O template oficial `full-stack-fastapi-template` (`backend/app`) segue a mesma ideia, com `api/routes/`, `core/`, `models.py` e `crud.py`.

No Django, uma app é um pacote de um assunto, que o `startapp` cria com `admin.py`, `apps.py`, `migrations/`, `models.py`, `tests.py` e `views.py` (fonte: tutorial01). O `urls.py` e as pastas `templates/<app>/` e `static/<app>/` o tutorial cria à mão. O tutorial 3 explica o namespacing de templates pelo nome da app: o Django usa o primeiro template com aquele nome, e sem o prefixo pode haver choque entre apps (docs.djangoproject.com/en/stable/intro/tutorial03/). O layout `src` (código dentro de `src/`) é descrito pelo Python Packaging User Guide da PyPA, que compara os dois formatos (packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout, conferido em 2026-11-24); não é obrigatório.

## Por que usar

- **Convenção na documentação oficial** de ambos (FastAPI: tutorial "Bigger Applications"; Django: tutoriais 1 e 7).
- **Django:** a app é um pacote com modelos, views, templates e testes juntos (docs.djangoproject.com/en/stable/intro/tutorial01/).
- **FastAPI:** `APIRouter` divide as rotas em arquivos (fastapi.tiangolo.com/tutorial/bigger-applications/).

## Quando usar

- FastAPI: web APIs em Python (fastapi.tiangolo.com).
- Django: sistemas com modelos, admin e templates, como mostram os tutoriais (docs.djangoproject.com/en/stable/intro/tutorial01/ e tutorial07).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| API / back-end de negócio | ✅ Ótimo | FastAPI é feito para web APIs, com `APIRouter` para dividir (fastapi.tiangolo.com/tutorial/bigger-applications/) |
| Sistema interno / SaaS / app web | ✅ Ótimo | Django traz admin e apps por assunto (docs.djangoproject.com/en/stable/intro/tutorial07/); o template oficial pareia FastAPI com front separado (github.com/fastapi/full-stack-fastapi-template) |
| MVP / protótipo | 🟡 Serve | O tutorial do FastAPI começa com um `main.py` (fastapi.tiangolo.com/tutorial/first-steps/) |
| Blog / conteúdo / e-commerce | 🟡 Serve | Sem guia oficial para este uso; o Django tem modelos, admin e templates |
| Landing page / site estático | ❌ Evite | Sem base oficial para este uso |
| App mobile | ❌ Evite | Só como API |

## Quando é bom

- **Estrutura documentada** nos guias oficiais dos dois.
- **App Django:** modelo, view, template e teste no mesmo pacote (docs.djangoproject.com/en/stable/intro/tutorial01/ e tutorial03).

## Quando é ruim

- **Poucos routers no guia:** o "Bigger Applications" é um exemplo mínimo (`routers/`, `internal/`); o template oficial acrescenta `api/routes/`, `core/` e `models.py` único (github.com/fastapi/full-stack-fastapi-template).
- **Referência entre apps Django:** a chave estrangeira aceita o modelo como texto `"app.Modelo"`, uma referência preguiçosa (docs.djangoproject.com/en/stable/ref/models/fields/#foreignkey).
- **Rótulo repetido:** o rótulo da app deve ser único no projeto (docs.djangoproject.com/en/stable/ref/applications/).
- **`__init__.py`:** o guia do FastAPI usa um em cada pasta para formar pacotes (fastapi.tiangolo.com/tutorial/bigger-applications/).

## Como começar

FastAPI, na árvore de `backend/` do template oficial full-stack-fastapi-template (github.com/fastapi/full-stack-fastapi-template, conferido em 2026-11-24). O guia "Bigger Applications" mostra a versão mínima: `app/` com `main.py`, `dependencies.py`, `routers/` e `internal/`.

```
backend/
├── pyproject.toml
├── alembic.ini
├── app/                            # pacote Python
│   ├── __init__.py
│   ├── main.py                     # cria o FastAPI e inclui o router da API
│   ├── models.py                   # modelos
│   ├── crud.py                     # acesso a dados
│   ├── utils.py
│   ├── api/
│   │   ├── main.py                 # junta os routers
│   │   ├── deps.py                 # dependências comuns
│   │   └── routes/                 # um arquivo por assunto: items.py, users.py, login.py
│   ├── core/                       # config.py, db.py, security.py
│   └── alembic/                    # migrações
└── tests/
    └── api/routes/                 # test_items.py
```

Django (tutorial oficial, partes 1 e 7, conferido em 2026-11-24; `polls` vira `orders`):

```
djangotutorial/
├── manage.py
├── mysite/                         # projeto: settings, urls raiz, wsgi/asgi
├── orders/                         # uma app por assunto (startapp)
│   ├── models.py, views.py, urls.py, admin.py, apps.py, tests.py
│   ├── migrations/
│   ├── templates/orders/           # OFICIAL: templates com o nome da app
│   ├── static/orders/              # OFICIAL: estáticos com o nome da app
└── templates/                      # OFICIAL (tutorial, parte 7): templates do projeto todo
```

Regras de nome e lugar:

- **Testes:** `backend/tests/` espelhando `app/` no template do FastAPI; `tests.py` na app Django.
- **Em Django,** `templates/<app>/` com o nome da app (tutorial 3); o mesmo vale para `static/<app>/` (tutorial 6, docs.djangoproject.com/en/stable/intro/tutorial06/).

## Combina com / alternativas

- [Feature-first](01-feature-first-colocation.md) e [monólito modular](04-monolito-modular.md).
- [Camadas](03-camadas-clean-hexagonal.md) só em domínio rico.
- Alternativa: Flask sem convenção (mesmo conselho: blueprints por assunto; a documentação do Flask 3.1 diz que blueprints servem para fatorar aplicações maiores, mas não prescreve pastas).

## Decisão rápida

- **Use se:** o back-end é em Python; FastAPI com `APIRouter`, ou Django com uma app por assunto.
- **Evite se:** é um site estático.
