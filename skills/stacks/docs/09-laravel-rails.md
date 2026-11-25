# Laravel e Rails (monólito produtivo)

> Frameworks full-stack "com tudo incluído": Laravel (PHP) como recomendação principal, Rails (Ruby) como alternativa equivalente. Trazem rotas, banco, autenticação, filas, e-mail e testes no próprio framework.

| | |
|---|---|
| **Site** | https://laravel.com e https://rubyonrails.org |
| **Categoria** | Áreas 2, 4 e 10 — Full-stack, backend e e-commerce |
| **Tipo** | Stack completa opinativa (monólito) |
| **Stack/composição** | Laravel: PHP, Eloquent, Blade com Livewire ou React/Vue com Inertia, MySQL ou PostgreSQL (SQLite por padrão em dev), filas, Sanctum e starter kits de auth (React, Vue ou Livewire), Pest ou PHPUnit. Rails: Ruby, Active Record, Hotwire, PostgreSQL, Minitest ou RSpec |
| **Preço** | Grátis (open source). Laravel tem produtos pagos à parte, nenhum necessário (preços lidos em 2026-11-24): Cloud a partir de US$ 5/mês mais uso, com primeiro mês grátis (laravel.com/cloud/pricing); Forge de US$ 12 a US$ 39/mês (laravel.com/forge/pricing); Nova a US$ 99 (licença única de projeto) ou US$ 299 (ilimitada) (nova.laravel.com); Herd Pro a US$ 69/ano, com versão Free sem custo (herd.laravel.com) |
| **Licença** | Laravel (framework): MIT; Rails: MIT (repositório laravel/framework e RubyGems, conferidos em 2026-11-24). O repositório inicial laravel/laravel não tem arquivo de licença reconhecido pela API do GitHub (`gh api repos/laravel/laravel/license` retorna 404); o `composer.json` dele declara MIT (conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Laravel e Rails trazem em um pacote só: rotas, banco com migrações, autenticação, filas, e-mail, validação, testes e cache. Fontes: laravel.com/docs/13.x e guides.rubyonrails.org.

A documentação lida mostra o Laravel 13.x como atual (o `composer.json` do laravel/laravel pede PHP ^8.3; a documentação cita o PHP 8.5 no script de instalação). O guia de Rails lido é do Rails 8.1 (última versão 8.1.4.1) e pede Ruby 3.2 ou superior (guides.rubyonrails.org/getting_started.html).

Os dois permitem tela no servidor (Blade/Livewire, Hotwire) ou funcionam só como API para uma SPA.

## Por que usar

- **Peças prontas no Laravel:** filas (laravel.com/docs/13.x/queues), e-mail (/mail), agendador (/scheduling) e testes com Pest ou PHPUnit (/testing).
- **Peças prontas no Rails:** Active Job, Action Mailer e Action Cable nos guias oficiais (guides.rubyonrails.org).
- **Documentação oficial versionada:** laravel.com/docs/13.x e o guia do Rails 8.1.
- **Popularidade:** cerca de 85,4 mil estrelas no GitHub (laravel/laravel, 2026-11-24).

## Quando usar

- Aplicação web que precisa de banco, auth, filas e e-mail no mesmo framework.
- Time que já conhece PHP ou Ruby.
- Aplicação com tela no servidor (Blade/Livewire, Hotwire) ou API para SPA.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Sistema de negócio / back-office | ✅ Ótimo | Filas, e-mail e agendador no framework |
| SaaS / app web | ✅ Ótimo | Starter kits de auth, Cashier para cobrança (laravel.com/docs/13.x/billing) e Hotwire no Rails |
| E-commerce próprio | ✅ Ótimo | Sem recurso oficial de e-commerce; só pagamento via Cashier (Stripe) |
| MVP / protótipo | ✅ Ótimo | Banco SQLite e migrações já configurados ao criar o projeto (laravel.com/docs/13.x/installation) |
| API para SPA ou mobile | 🟡 Serve | Sanctum no Laravel (laravel.com/docs/13.x/sanctum); outras opções: [Hono](05-node-api.md) ou [FastAPI](06-python-fastapi-django.md) |
| Dashboard / painel admin | 🟡 Serve | Tela no servidor com Blade/Livewire ou Hotwire |
| Site de conteúdo | 🟡 Serve | [Astro](01-astro-conteudo.md) é feito para sites de conteúdo |
| Tempo real | 🟡 Serve | Laravel tem Reverb (laravel.com/docs/13.x/reverb); Rails tem Action Cable (guides.rubyonrails.org/action_cable_overview.html) |
| Dados/IA, CPU pesada | ❌ Evite | Sem recurso oficial nessas áreas |
| App mobile | ❌ Evite | Só como backend |

## Quando é bom

- **Tudo no mesmo lugar:** banco, filas, e-mail e testes (laravel.com/docs/13.x).
- **Convenções para IA:** a documentação do Laravel afirma que a estrutura previsível ajuda agentes de IA (laravel.com/docs/13.x/installation).
- **Guia de upgrade** a cada versão (laravel.com/docs/13.x/upgrade).

## Quando é ruim

- **Linguagem do back diferente do front TypeScript:** não compartilha tipos com o front.
- **Ruby ou PHP:** o time que não conhece a linguagem precisa aprender.
- **Ferramentas pagas do Laravel** (opcionais) pertencem à empresa por trás do framework.

## Como começar

Laravel (documentação oficial):

```bash
composer global require laravel/installer
laravel new example-app
cd example-app
composer run dev
```

Rails (guia oficial):

```bash
rails new store
```

Os starter kits do Laravel entregam login e cadastro prontos. Estrutura de pastas é da skill architecture; hospedagem é da skill infra.

## Combina com / alternativas

- [Next.js](02-nextjs-saas.md): se o time prefere TypeScript de ponta a ponta.
- [Python/Django](06-python-fastapi-django.md): equivalente em Python, com admin forte.
- [SPA + API](04-spa-vite-api.md): Laravel como backend de um front React.
- Componentes para Blade: [HyperUI](../../design/docs/04-hyperui.md) (skill design).

## Decisão rápida

- **Use se:** quer um framework full-stack com banco, auth, filas e e-mail, e o time conhece PHP (ou Ruby).
- **Evite se:** o projeto é de dados e IA ou a empresa padronizou outra linguagem.
