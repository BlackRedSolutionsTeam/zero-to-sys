# Relatório e status da auditoria

> O relatório tem resumo em 5 linhas, tabela por área com status e evidência, e achados detalhados com o risco de cada um, para que o leitor decida em dois minutos o que fazer.

| | |
|---|---|
| **Referência** | OWASP ASVS 5.0.0 (formato de referência `v<versão>-<capítulo>.<seção>.<requisito>` para citar requisitos); Google Engineering Practices, "The standard of code review" (google.github.io/eng-practices); DORA, "Software delivery performance metrics" (dora.dev/guides/dora-metrics) |
| **Categoria** | Auditoria |
| **Tipo** | Prática de comunicação do diagnóstico |
| **Vale para** | Qualquer projeto auditado pelo procedimento do [doc 01](01-como-auditar.md) |
| **Verificado em** | 2026-11-24 |

## O que é

O relatório é a entrega da auditoria. Cada área recebe um status e uma evidência. Cada problema vira um achado com o que foi visto, por que importa e qual o risco.

Os quatro status: **ok** (visto e atende), **atenção** (existe, mas incompleto ou fraco), **falta** (não existe) e **não verificado** (não deu para provar; o motivo vai escrito).

## Por que usar

- **Decisão rápida:** quem paga ou prioriza lê cinco linhas e a tabela.

## Quando usar

- Ao fim de toda auditoria, sem exceção.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Relatório curto; várias áreas "não se aplica" |
| MVP de SaaS | ✅ Ótimo | O resumo ajuda a decidir o que pagar antes do lançamento |
| SaaS em crescimento | ✅ Ótimo | Muitos achados; a tabela evita perder o fio |
| Sistema interno/corporativo | ✅ Ótimo | Serve de registro para quem assumir depois |
| API/integração | ✅ Ótimo | Áreas de contrato e erros pesam mais |
| App mobile com backend | ✅ Ótimo | Separe o que é do backend e o que é do app |
| Projeto que mudou por inteiro desde a coleta | ❌ Evite | Relatório velho engana; refaça a coleta |

## Quando é bom

- **Risco escrito em termos do negócio:** "um paciente pode ver a agenda de outra clínica", não "falha de autorização".

## Quando é ruim

- **Lista longa sem ordem.** Se tudo é urgente, nada é.
- **Achado sem evidência:** ninguém consegue conferir.
- **Misturar diagnóstico com solução detalhada.** No relatório vai só o encaminhamento ([doc 03](03-priorizacao-e-plano.md)).

## Como começar

### Modelo em Markdown

Copie e preencha. Salve fora do código do projeto, a menos que o usuário peça (por exemplo `docs/auditoria-AAAA-MM-DD.md`).

```markdown
# Auditoria de <projeto>

Data: AAAA-MM-DD | Commit: <hash curto> | Stack: <resumo>

## Resumo

1. O que o sistema faz e em que estado está (uma frase).
2. Quantas áreas: X ok, Y atenção, Z falta, W não verificado.
3. O risco mais grave, em linguagem do negócio.
4. O que fazer primeiro.
5. O que não foi possível verificar e por quê.

## Status por área

| Área | Skill | Status | Evidência |
|---|---|---|---|
| Estrutura | architecture | ok | `src/` por funcionalidade (`src/appointments/`) |
| Banco | data | falta | sem `clinic_id` em `appointment` (`prisma/schema.prisma:41`) |
| Segurança | security | não verificado | sem acesso ao painel do provedor de login |

## Achados

### A1. <título curto> (risco: alto | médio | baixo)

- **Onde:** `arquivo:linha`
- **O que foi visto:** fato, sem opinião.
- **Risco:** o que pode acontecer, em linguagem do negócio.
- **Encaminhamento:** skill e doc. **Esforço:** pequeno | médio | grande.

## Não verificado

Item, motivo e o que falta para verificar.
```

### Variante em página HTML local

Para abrir no navegador, gere um arquivo único com os mesmos blocos, numa pasta temporária fora do repositório, e abra com `open` (macOS) ou `xdg-open` (Linux).

```html
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auditoria do projeto</title>
<style>
body { font-family: system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; }
td, th { border: 1px solid #ccc; padding: .4rem; }
.ok { background: #d9f2dd; }
.falta { background: #f8d4d4; }
</style>
</head>
<body>
<table>
<tr class="falta"><td>Testes</td><td>falta</td><td>sem e2e</td></tr>
</table>
</body>
</html>
```

O status aparece em texto e em cor. Nunca só em cor.

### Exemplo preenchido: Next.js com Postgres, sem testes e2e

Projeto: sistema de agendamento de clínica. Next.js (App Router), Prisma, Postgres, hospedado em uma VPS.

**Resumo**

1. Sistema de agendamento em produção há 6 meses, com 4 pessoas no código nos últimos 90 dias.
2. 8 áreas: 1 ok, 3 atenção, 3 falta, 1 não verificado.
3. Risco mais grave: a lista de agendamentos não filtra por clínica, então um usuário pode ver agendamentos de outra.
4. Primeiro: filtro por clínica e backup do banco.
5. Não verificado: configuração do login (sem acesso ao painel).

**Status por área**

| Área | Status | Evidência |
|---|---|---|
| Estrutura (`architecture`) | ok | `src/app/(agenda)/` e `src/features/appointments/` seguem a organização por funcionalidade |
| Código (`coding`) | atenção | `src/features/billing/calc.ts` com 480 linhas; ESLint configurado, mas sem `lint` no CI |
| Banco (`data`) | falta | `appointment` sem `clinic_id` (`prisma/schema.prisma:41`); sem índice em `scheduled_at` |
| API (`api`) | atenção | rotas com `{ error: "..." }` livre em vez do formato único (`src/app/api/patients/route.ts:22`) |
| Testes (`quality`) | falta | 12 testes de unidade, nenhum de integração com banco, nenhum e2e (`rg -l "playwright"` sem resultado) |
| Segurança (`security`) | não verificado | sem acesso ao provedor de login; `.env.example` existe e `.env` não está no Git (`git ls-files .env` vazio) |
| Telas (`user-experience`) | atenção | tabela de agendamentos sem versão para celular (`src/features/appointments/table.tsx`) |
| Produção (`infra`) | falta | nenhum job de backup em `.github/workflows/` nem no `docker-compose.yml` |

**Achado A1 (risco: alto)**

- **Onde:** `src/app/api/appointments/route.ts:18`
- **O que foi visto:** `prisma.appointment.findMany()` sem `where` por clínica.
- **Risco:** a clínica A pode ver nome e horário de pacientes da clínica B (dado pessoal, LGPD).
- **Encaminhamento:** `data`, [doc 06](../../data/docs/06-multiempresa.md) e [doc 10](../../data/docs/10-dados-pessoais-e-lgpd.md).
- **Esforço:** médio (migration, backfill e teste).

**Achado A2 (risco: alto)**

- **Onde:** `docker-compose.yml`, `.github/workflows/`
- **O que foi visto:** sem rotina de backup do Postgres nem teste de restauração.
- **Risco:** erro de disco ou migration ruim perde a agenda inteira.
- **Encaminhamento:** `infra`, [doc 11](../../infra/docs/11-backup-e-recuperacao.md).
- **Esforço:** pequeno.

**Achado A3 (risco: médio):** sem teste e2e do fluxo "agendar consulta"; o formulário pode quebrar sem ninguém perceber. Encaminhamento: `quality`, [doc 05](../../quality/docs/05-ponta-a-ponta-com-playwright.md). Esforço: médio.

## Combina com / alternativas

- [01-como-auditar.md](01-como-auditar.md): como coletar o que entra aqui.
- [03-priorizacao-e-plano.md](03-priorizacao-e-plano.md): como ordenar os achados e virar PRs.

## Decisão rápida

- **Use se:** a auditoria terminou e alguém precisa decidir o que corrigir.
- **Evite se:** a coleta está incompleta e você ainda não sabe o que ficou "não verificado".
