# Seeds e dados de teste no ambiente local

> Quem clona o projeto roda um comando e vê o sistema com telas cheias, sem dado real e sem montar nada à mão.

| | |
|---|---|
| **Referência** | Skill `data`, doc 05; https://fakerjs.dev e https://faker.readthedocs.io |
| **Categoria** | Dados locais |
| **Tipo** | Prática de ambiente local |
| **Vale para** | Qualquer projeto com banco |
| **Verificado em** | 2026-11-25 |

## O que é

Esta prática liga o ambiente local ao que a skill `data` ensina. Os três tipos de seed (referência, desenvolvimento e dados de teste), as receitas por ORM e os comandos de recriação estão em `skills/data/docs/05-seeds-e-dados-de-teste.md`; não se repetem aqui. O que este doc acrescenta é o **fluxo do dia 1**: como o seed entra no passo a passo de quem chega.

## Por que usar

- **Dia 1 produtivo:** a pessoa vê uma tela de listagem com 50 itens, não uma tela vazia.
- **Sem dado real:** nada de copiar produção para o notebook (LGPD, skill `data`, doc 10).
- **Mesmo estado para todos:** o bug que um vê, o outro reproduz.

## Quando usar

- Assim que existir a primeira tela de listagem.
- Quando o README de onboarding passar de cinco passos.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Sem banco |
| MVP / protótipo | ✅ Ótimo | Um usuário admin e alguns registros bastam |
| SaaS | ✅ Ótimo | Duas empresas de demonstração testam o multiempresa |
| Sistema interno/corporativo | ✅ Ótimo | Cargos, filiais e usuários de cada papel |
| API/integração | ✅ Ótimo | Contas de teste para cada cliente da API |
| App mobile com backend | ✅ Ótimo | Conta de teste e dados para demonstração |

## Quando é bom

- **Um comando só** (`make reset`, `just reset` ou `npm run db:reset`) que apaga, migra e popula.
- **Idempotente e determinístico** (semente fixa do Faker).
- **Usuários conhecidos:** um por papel, com e-mail e senha de desenvolvimento no README (`admin@exemplo.com` / `senha-local`).
- **Seed de desenvolvimento protegido** por checagem de ambiente.
- **Volume realista:** algumas centenas de linhas revelam paginação e consulta lenta.

## Quando é ruim

- **Seed lento:** passou de um minuto, ninguém roda; gere em lote.
- **Senha de seed igual à de produção** ou usuário de seed que chega a produção.
- **Seed que depende de ordem manual** ou de passos fora do script.
- **Dados falsos que parecem reais** (CPF, e-mail e telefone de pessoas de verdade): use geradores e domínios reservados (`example.com`).
- **Dump de produção sem anonimizar.**

## Como começar

O fluxo de dia 1 no script de onboarding, depois de subir o Compose (doc 01) e copiar o `.env` (doc 03):

```bash
docker compose up -d --wait
npm run db:reset
```

`db:reset` fica definido como na skill `data` (migrations mais seed). Para o Prisma 7, o seed não roda sozinho no `migrate reset`: encadeie `prisma db seed`, como no doc 05 da `data`.

Proteja o seed de desenvolvimento:

```ts
if (process.env.NODE_ENV === 'production') {
  throw new Error('Seed de desenvolvimento não roda em produção')
}
```

Liste no README os usuários criados:

| Papel | E-mail | Senha |
|---|---|---|
| Administrador | `admin@exemplo.com` | `senha-local` |
| Atendente | `atendente@exemplo.com` | `senha-local` |

## Combina com / alternativas

- Skill `data`: seeds (doc 05), migrations (doc 04), multiempresa (doc 06), LGPD (doc 10).
- [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md): banco que recebe o seed.
- [05-scripts-de-uma-linha.md](05-scripts-de-uma-linha.md): o atalho `reset`.
- Alternativa: dump anonimizado quando o volume real importa (skill `infra`, doc 11, para o backup de onde sai o dump).

## Decisão rápida

- **Use se:** o sistema tem banco e telas que listam dados.
- **Evite se:** o projeto não tem persistência.
