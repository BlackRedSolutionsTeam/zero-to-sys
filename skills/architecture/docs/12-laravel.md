# Laravel

> Estrutura de pastas padrão do Laravel, com `app/`, `routes/`, `resources/` e `database/`; livre dentro de `app/` desde que o Composer consiga carregar a classe.

| | |
|---|---|
| **Referência oficial** | laravel.com/docs/13.x/structure (13.x é a versão atual do `laravel/laravel`, release v13.11.0 em 2026-11-24; a página diz que o Laravel "impõe quase nenhuma restrição" ao lugar das classes, desde que o Composer as carregue). A 12.x (laravel.com/docs/12.x/structure) tem a mesma estrutura |
| **Categoria** | Parte 2 — Estrutura recomendada por stack |
| **Tipo** | Convenção de framework |
| **Vale para** | Laravel em PHP |
| **Verificado em** | 2026-11-24 |

## O que é

O Laravel traz uma estrutura "um ótimo ponto de partida para aplicações grandes e pequenas", e a documentação diz que você pode organizar como quiser, desde que o Composer carregue a classe (`app/` usa PSR-4). A raiz tem `app`, `bootstrap`, `config`, `database`, `public`, `resources`, `routes`, `storage`, `tests` e `vendor`.

Por padrão, `app/` traz `Http`, `Models` e `Providers`. A documentação lista ainda pastas criadas pelos comandos `make:` (`Console`, `Events`, `Jobs`, `Listeners`, `Mail`, `Notifications`, `Policies`, `Rules`, `Exceptions`, `Broadcasting`), que só existem depois do primeiro comando que as gera. `Http` contém controllers, middleware e requests. `Console` e `Http` são tratadas como "formas de acessar o núcleo", sem lógica de negócio.

## Por que usar

- **Estrutura documentada** na página de estrutura (laravel.com/docs/13.x/structure).
- **Geradores `php artisan make:`** criam as classes em `app/` (fonte: a mesma página).
- **Liberdade em `app/`:** o Laravel só exige que o Composer carregue a classe (mesma página).

## Quando usar

- Sistemas web em PHP com rotas, views e banco (laravel.com/docs/13.x/structure).
- APIs: `routes/api.php` entra com `install:api` (fonte: laravel.com/docs/13.x/structure, seção `routes`).
- Apps com front-end pronto: os starter kits oferecem React, Vue e Livewire (fonte: laravel.com/docs/13.x/starter-kits).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS / app web | ✅ Ótimo | Rotas `web`, sessão, CSRF e starter kits (laravel.com/docs/13.x/starter-kits) |
| Dashboard / painel admin | 🟡 Serve | Starter kits com Livewire ou Inertia (laravel.com/docs/13.x/starter-kits) |
| API / back-end | ✅ Ótimo | `routes/api.php` stateless via `install:api` (laravel.com/docs/13.x/structure) |
| E-commerce / sistema interno | 🟡 Serve | Filas para trabalho em segundo plano (laravel.com/docs/13.x/queues); sem guia oficial de e-commerce |
| MVP / protótipo | 🟡 Serve | A estrutura padrão é "ótimo ponto de partida" (laravel.com/docs/13.x/structure) |
| Landing page / site estático | ❌ Evite | Sem base oficial para este uso; só vale com back-end |

## Quando é bom

- **Estrutura padrão pensada para projetos grandes e pequenos** (laravel.com/docs/13.x/structure).
- **Classes em qualquer pasta de `app/`,** desde que o Composer carregue (mesma página).

## Quando é ruim

- **Lógica no controller:** a documentação diz que `Http` e `Console` são formas de acessar o núcleo e não contêm lógica de aplicação (laravel.com/docs/13.x/structure).
- **Classes fora do autoload:** só carregam se o Composer as encontrar (mesma página).
- **Pastas `make:` criadas sob demanda:** várias só aparecem depois do primeiro comando (mesma página), então a árvore muda com o uso.

## Como começar

Estrutura do `laravel/laravel` (github.com/laravel/laravel, branches 12.x e 13.x iguais nas pastas listadas) e da documentação (laravel.com/docs/13.x/structure), conferidas em 2026-11-24. As pastas de `app/` criadas pelos comandos `make:` (`Http/Requests`, `Jobs`, `Policies`, `Enums`) estão em `laravel/framework`, `src/Illuminate/Foundation/Console`. O `laravel/laravel` 13.x traz só `app/Http/Controllers`, `app/Models` e `app/Providers`; `Middleware/`, `Requests/`, `Jobs/`, `Policies/` e `Enums/` abaixo são criadas depois.

```
meu-app/
├── app/                              # OFICIAL: quase todas as classes
│   ├── Http/                         # OFICIAL: porta HTTP, sem regra de negócio
│   │   ├── Controllers/
│   │   ├── Middleware/
│   │   └── Requests/                 # validação (form requests)
│   ├── Models/                       # OFICIAL: modelos Eloquent
│   ├── Providers/                    # OFICIAL: AppServiceProvider
│   ├── Jobs/                         # OFICIAL (criada por make:job)
│   ├── Policies/                     # OFICIAL (criada por make:policy)
│   └── Enums/                        # OFICIAL (make:enum usa app/Enums se a pasta existir)
├── bootstrap/                        # OFICIAL: app.php e cache
├── config/                           # OFICIAL: configuração
├── database/                         # OFICIAL: migrations, factories, seeders
├── public/                           # OFICIAL: index.php e assets
├── resources/                        # OFICIAL: views e assets brutos (CSS, JS)
├── routes/                           # OFICIAL: web.php, console.php, api.php opcional
├── storage/                          # OFICIAL: logs, cache, uploads
├── tests/                            # OFICIAL: Pest ou PHPUnit
└── vendor/                           # OFICIAL: dependências (não editar)
```

Regras de nome e lugar:

- **Classe:** um arquivo por classe, com o nome da classe (PSR-4, php-fig.org/psr/psr-4).
- **Teste:** classe com sufixo `Test`, em `tests/Feature` ou `tests/Unit` (laravel.com/docs/13.x/structure).
- **Regra de negócio** fora de `Http`: o Laravel não fixa a pasta, só exige que o Composer carregue as classes.
- **Use `make:`** para gerar as classes em `app/` (laravel.com/docs/13.x/structure).
- **Views em `resources/views`** (laravel.com/docs/13.x/structure); a subpasta por assunto é livre (ex.: `orders/index.blade.php`).

## Combina com / alternativas

- [Feature-first](01-feature-first-colocation.md): o Laravel deixa livre onde ficam as classes de assunto dentro de `app/`.
- [Monólito modular](04-monolito-modular.md): módulos como pacotes locais do Composer (o Laravel não tem guia oficial de módulos; as fontes oficiais são o capítulo de pacotes, laravel.com/docs/12.x/packages, e os repositórios `path` do Composer, getcomposer.org/doc/05-repositories.md#path).
- Alternativa: outras stacks de back-end ([Node](09-nestjs-node.md), [Python](11-python-fastapi-django.md)).

## Decisão rápida

- **Use se:** é Laravel; siga a estrutura oficial e as pastas dos comandos `make:`.
- **Evite se:** a pilha for outra.
