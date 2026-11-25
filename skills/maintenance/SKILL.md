---
name: maintenance
description: Mantém o sistema vivo e atualizado depois que ele está no ar — calendário de fim de suporte (Node, .NET, Python, Postgres, Django, Laravel, Rails, Angular, Next.js, Spring Boot) com data conferida, atualização automática de dependências com Renovate ou Dependabot e regras de merge, atualização segura de versão maior de framework, atualização de Postgres sem queda, registro e pagamento de dívida técnica, remoção de código morto e dependências sem uso e rotina trimestral de saúde do projeto. Use sempre que o usuário perguntar "essa versão ainda tem suporte", "fim de suporte do Node/.NET/Python/Postgres", "atualizar o framework", "subir de versão maior", "configurar Renovate ou Dependabot", "atualizar o Postgres", "dívida técnica", "código morto", "dependência sem uso", "manutenção do projeto" ou "revisão trimestral". Não repete a auditoria de vulnerabilidades (skill security), a refatoração em passos (skill coding), os gates de CI (skill quality), o diagnóstico (skill audit) nem os workflows do GitHub Actions (skill infra).
---

# maintenance

Guia para manter um sistema que já está em produção: versões com suporte, dependências em dia, dívida sob controle e uma rotina que impede o projeto de envelhecer em silêncio. Atualizar pouco e sempre dói menos do que atualizar tudo depois de dois anos. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e comandos ou exemplos prontos.

## Como usar esta skill

1. **Descubra o que o projeto usa** (versão de runtime, framework, banco) lendo `package.json`, `global.json`, `pyproject.toml`, `Dockerfile`, `docker-compose.yml`. Não pergunte o que o repositório responde.
2. **Compare com o calendário** ([doc 01](docs/01-calendario-de-fim-de-suporte.md)). Quem está sem suporte, ou a menos de 6 meses disso, entra na fila primeiro.
3. **Ligue a atualização automática** ([doc 02](docs/02-atualizacao-automatica-de-dependencias.md)) antes de qualquer atualização manual: sem ela, o problema volta.
4. **Atualize versão maior de framework** em passos ([doc 03](docs/03-atualizar-versao-maior-do-framework.md)) e **versão maior do Postgres** com plano de volta ([doc 04](docs/04-atualizar-o-postgres-sem-queda.md)).
5. **Registre o que não dá para fazer agora** como dívida ([doc 05](docs/05-divida-tecnica.md)) e **apague o que ninguém usa** ([doc 06](docs/06-codigo-morto-e-dependencias-sem-uso.md)).
6. **Repita a cada trimestre** ([doc 07](docs/07-rotina-trimestral-de-saude.md)); a rotina usa a skill `audit` para o diagnóstico.

## Qual doc por situação

| Situação | Doc |
|---|---|
| "O Node 22 ainda tem suporte?" | [01](docs/01-calendario-de-fim-de-suporte.md) |
| PRs de atualização chegando ou ninguém olhando as versões | [02](docs/02-atualizacao-automatica-de-dependencias.md) |
| Subir Next.js 15 para 16, Laravel 12 para 13, .NET 8 para 10 | [03](docs/03-atualizar-versao-maior-do-framework.md) |
| Postgres 14 saiu de suporte | [04](docs/04-atualizar-o-postgres-sem-queda.md) |
| "Isso aqui está feio e ninguém mexe" | [05](docs/05-divida-tecnica.md) |
| Projeto inchado, `node_modules` enorme, pacotes que ninguém lembra | [06](docs/06-codigo-morto-e-dependencias-sem-uso.md) |
| Quer uma rotina para não esquecer de nada | [07](docs/07-rotina-trimestral-de-saude.md) |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Calendário de fim de suporte | [docs/01-calendario-de-fim-de-suporte.md](docs/01-calendario-de-fim-de-suporte.md) | Datas conferidas de Node, .NET, Python, Postgres e frameworks |
| Atualização automática | [docs/02-atualizacao-automatica-de-dependencias.md](docs/02-atualizacao-automatica-de-dependencias.md) | Renovate, Dependabot e regras de merge |
| Versão maior de framework | [docs/03-atualizar-versao-maior-do-framework.md](docs/03-atualizar-versao-maior-do-framework.md) | Passo a passo e testes de rede de proteção |
| Postgres sem queda | [docs/04-atualizar-o-postgres-sem-queda.md](docs/04-atualizar-o-postgres-sem-queda.md) | pg_upgrade, replicação lógica e plano de volta |
| Dívida técnica | [docs/05-divida-tecnica.md](docs/05-divida-tecnica.md) | Registrar, priorizar e pagar em fatias |
| Código morto | [docs/06-codigo-morto-e-dependencias-sem-uso.md](docs/06-codigo-morto-e-dependencias-sem-uso.md) | Achar e remover com segurança |
| Rotina trimestral | [docs/07-rotina-trimestral-de-saude.md](docs/07-rotina-trimestral-de-saude.md) | Checklist de saúde ligado à skill `audit` |

## Checklist

- [ ] Versão de runtime, de framework e de banco com suporte hoje e por mais 6 meses, pelo [calendário](docs/01-calendario-de-fim-de-suporte.md).
- [ ] Versão do runtime fixada em arquivo (`.nvmrc`, `engines`, `global.json`, `.python-version`, imagem Docker com tag exata).
- [ ] Renovate ou Dependabot ativo, com política de merge escrita.
- [ ] Auditoria de vulnerabilidades no CI (skill `security`, doc 08).
- [ ] Lockfile commitado e atualizado por PR, não à mão.
- [ ] Dívida técnica registrada em lista única, com dono e tamanho.
- [ ] Sem pacote sem uso nem código morto conhecido.
- [ ] Última rotina trimestral com data anotada no repositório.

## Regras de uso

- **Data só conferida.** Fim de suporte muda (Next.js 15 foi estendido, Angular e Django têm fases). Confira na fonte oficial e diga a data da conferência.
- **Atualize uma coisa por vez.** Runtime, framework e banco não sobem no mesmo PR.
- **Rede de proteção antes de subir.** Sem testes que provem o comportamento, o passo é escrever testes (skill `coding`, doc 10).
- **Versão maior nunca entra por merge automático.**
- **Backup restaurado antes de mexer no banco** (skill `infra`, doc 11).
- **Fronteiras.** Vulnerabilidade e política de severidade são da `security`; passos de refatoração da `coding`; gates obrigatórios no CI da `quality`; diagnóstico e relatório da `audit`; workflows e segredos da `infra`.

## Quando a lista não cobre

Sistemas em .NET Framework, PHP 7, Python 2, Java 8 de fornecedor pago e frameworks com suporte comercial estendido (por exemplo, o suporte pago da HeroDevs para versões fora de linha) ficam fora desta skill. Diga ao usuário e cubra com a documentação do fornecedor.

## Validade dos dados

Datas de fim de suporte foram conferidas em 2026-11-25 nas fontes oficiais de cada projeto (nodejs/Release, Microsoft, devguide.python.org, postgresql.org, Django, Laravel, Rails, Angular, Next.js); o doc 01 marca as que vieram de fonte secundária. Opções do Renovate e do Dependabot foram conferidas na mesma data. Cada documento tem a linha "Verificado em".
