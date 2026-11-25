# Atualizar versão maior do framework com segurança

> Suba uma versão maior de cada vez, sobre uma rede de testes, em um PR só dessa atualização, seguindo o guia oficial de migração, com plano de volta pronto.

| | |
|---|---|
| **Referência** | Guias oficiais de migração de cada framework (Next.js upgrade guides em nextjs.org/docs, Laravel Upgrade Guide em laravel.com/docs, Django release notes em docs.djangoproject.com, Angular Update Guide em angular.dev/update-guide, Microsoft Learn "Migrate from ASP.NET Core"); Working Effectively with Legacy Code (M. Feathers, 2004); Fowler, "StranglerFigApplication" |
| **Categoria** | Manutenção |
| **Tipo** | Prática de processo |
| **Vale para** | Qualquer framework com guia de migração: Next.js, Laravel, Rails, Django, Angular, ASP.NET Core, Spring Boot |
| **Verificado em** | 2026-11-25 |

## O que é

Uma versão maior pode quebrar compatibilidade de propósito: APIs removidas, configuração nova, requisito de runtime maior. Atualizar com segurança é separar o risco em partes que se conferem sozinhas: testes antes, uma versão por vez, mudanças de comportamento isoladas e um jeito de voltar.

Os passos de refatoração em si estão na skill `coding` ([doc 10](../../coding/docs/10-refatoracao-segura.md)); aqui vai a sequência específica de subir versão.

## Por que usar

- **Erro pequeno é achável:** se quebrou, foi a atualização, não dez mudanças misturadas.
- **Evita o salto triplo:** subir 12 para 13 é um dia; 10 para 13 é um projeto.
- **Previsível:** o time sabe quando termina e quando dá para voltar.

## Quando usar

- A versão do framework chegou a menos de 6 meses do fim de suporte ([doc 01](01-calendario-de-fim-de-suporte.md)).
- Um PR do robô trouxe uma versão maior ([doc 02](02-atualizacao-automatica-de-dependencias.md)).
- Uma biblioteca nova exige o framework mais novo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Pouco código próprio, migração costuma ser rápida |
| MVP de SaaS | ✅ Ótimo | Base pequena; atualizar cedo custa pouco |
| SaaS em crescimento | ✅ Ótimo | Precisa de plano, janela e ambiente de teste |
| Sistema interno/corporativo | 🟡 Serve | Muitas vezes sem testes: escreva primeiro a rede mínima |
| API/integração | ✅ Ótimo | Contrato testado detecta regressão |
| App mobile com backend | 🟡 Serve | Backend sobe, mas versões antigas do app seguem chamando a API |
| Projeto sem testes e sem ninguém que conheça o código | ❌ Evite começar pela atualização | Escreva testes de caracterização antes |

## Quando é bom

- **Um salto de cada vez,** na ordem das versões maiores (não pule de 12 para 14).
- **Rede de proteção antes:** testes que cobrem login, o fluxo principal de dinheiro ou dados e as rotas da API.
- **PR só de atualização,** sem funcionalidade nova junto.
- **Ferramenta oficial primeiro:** codemods e comandos de migração do próprio framework.
- **Ambiente de staging** igual à produção, com dados de teste.

## Quando é ruim

- **Atualizar tudo no mesmo PR:** runtime, framework e libs juntos escondem a causa.
- **Sem teste:** "abriu a tela" não é prova.
- **Pular o changelog:** o que mudou de comportamento sem erro de compilação é o mais perigoso (padrões trocados, ordem de middleware).
- **Fork de biblioteca para segurar a versão:** vira dívida maior que a migração.
- **Atualizar no dia do deploy grande** ou numa sexta.

## Como começar

### Passo a passo

1. **Leia o guia oficial** da versão de destino e liste o que afeta o projeto. Anote o requisito de runtime (por exemplo, o PHP mínimo do Laravel 13 é 8.3 e o do Laravel 12 é 8.2, segundo a página de suporte conferida em 2026-11-25).
2. **Suba o runtime antes,** se o framework novo pedir (um PR só disso, [doc 01](01-calendario-de-fim-de-suporte.md)).
3. **Monte a rede de proteção** (abaixo). Rode tudo na versão atual e confirme verde.
4. **Crie a branch** `chore/upgrade-<framework>-<versão>` a partir da principal.
5. **Atualize o pacote e rode a ferramenta de migração** oficial. Commit.
6. **Corrija os erros de compilação e de teste,** um tipo de erro por commit.
7. **Revise avisos de depreciação** e remova o uso de API que sumirá na próxima versão.
8. **Teste em staging** com um backup recente da produção (dados anonimizados) e percorra o fluxo principal à mão.
9. **Planeje a volta:** o PR é revertível, migrations de banco são compatíveis nos dois sentidos ou separadas (skill `data`, [doc 04](../../data/docs/04-migrations.md)), e a versão anterior da imagem continua publicada.
10. **Faça o deploy fora do pico,** com alguém olhando erros e latência por 24 horas (skill `infra`, [doc 10](../../infra/docs/10-observabilidade.md)).

### Rede de proteção

| Camada | O que cobrir | Skill |
|---|---|---|
| Testes de unidade | Regras de negócio puras | `quality`, doc 02 |
| Testes de integração com banco | Consultas, transações e migrations | `quality`, doc 03 |
| Testes de contrato da API | Formato de resposta que os clientes esperam | `quality`, doc 04 |
| Ponta a ponta | Login, o fluxo de dinheiro ou dado principal | `quality`, doc 05 |
| Testes de caracterização (legado) | Comportamento atual, mesmo feio | `coding`, doc 10 |

Sem nada disso, a primeira tarefa é escrever o mínimo: um teste ponta a ponta do fluxo principal e um de contrato por endpoint crítico.

### Comandos de apoio por stack

Next.js (guia de codemods, página atualizada em 2026-10-02): o argumento aceita `patch`, `minor`, `major`, uma dist-tag (`latest`, `canary`, `rc`) ou uma versão exata; o padrão é `minor`. O comando abaixo atualiza o Next.js, o React e o React DOM e roda os codemods; a forma antiga `@next/codemod@canary upgrade latest` não é a que a página documenta hoje.

```bash
npx @next/codemod upgrade major
```

Laravel (guia de upgrade do 13.x): o guia pede `laravel/framework` em `^13.0`, `laravel/boost` em `^2.0`, `laravel/tinker` em `^3.0`, `phpunit/phpunit` em `^12.0` e `pestphp/pest` em `^4.0`, e cita o Laravel Boost (`/upgrade-laravel-v13`) e o Shift como automação. O `-W` é o `--with-all-dependencies` do Composer 2.11.3 (flag conferida no `--help`):

```bash
composer require laravel/framework:^13.0 -W
composer outdated --direct
```

Django (guia oficial de upgrade): os avisos de depreciação ficam silenciados por padrão e o guia manda ligar com `-Wa`. O `-W error::DeprecationWarning` é opção do próprio Python (executada com Python 3.x em 2026-11-25) e faz o aviso virar erro.

```bash
python -Wa manage.py test
python -W error::DeprecationWarning -m pytest
python -m pip install -U Django
```

.NET (Microsoft Learn): a partir do SDK 10 a forma é `dotnet package list`; no SDK 9 ou anterior, use `dotnet list package`. As opções `--outdated`, `--deprecated` e `--vulnerable` existem nas duas (a `--vulnerable` pede SDK 9.0.300 ou mais e não combina com as outras duas).

```bash
dotnet package list --outdated
dotnet package list --deprecated
dotnet package list --vulnerable
```

Angular (referência do `ng update`): o comando básico leva os dois pacotes; para uma maior específica, fixe com `@angular/core@^21`. `--create-commits` (`-C`) cria um commit por migração.

```bash
ng update @angular/cli @angular/core --create-commits
```

Lido nas páginas oficiais em 2026-11-25; o `ng update`, o `dotnet` e o `composer require` do Laravel não foram executados num projeto real (só a flag `-W` e a página). Confira o comando exato no guia da versão de destino: nomes de pacote e flags mudam entre versões.

### Subir o runtime e a imagem

Troque a tag exata em um PR isolado:

```dockerfile
FROM node:24-bookworm-slim
```

E em `package.json`:

```json
{
  "engines": {
    "node": ">=24 <25"
  }
}
```

### Quando o salto é grande

Se faltam três versões maiores ou o código é legado sem testes, use o padrão estrangulador (Fowler): rode a versão nova em paralelo (um módulo ou rota por vez) e migre aos poucos, em vez de um PR gigante.

## Combina com / alternativas

- [Calendário de fim de suporte](01-calendario-de-fim-de-suporte.md): decide quando.
- [Atualização automática](02-atualizacao-automatica-de-dependencias.md): mantém as minors em dia, o que reduz o salto.
- Skill `coding`, [refatoração segura](../../coding/docs/10-refatoracao-segura.md) e [testes](../../coding/docs/08-testes.md).
- Skill `quality`, [pirâmide de testes](../../quality/docs/01-piramide-de-testes.md) e [gates no CI](../../quality/docs/07-quality-gates-no-ci.md).
- Alternativa: reescrever; arriscada, só vale quando a migração custa mais que o sistema novo.

## Decisão rápida

- **Use se:** há testes ou dá para escrever o mínimo.
- **Evite se:** a única validação é abrir o sistema no navegador; escreva a rede antes.
