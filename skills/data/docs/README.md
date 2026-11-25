# Dados

Um documento por prática, explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com SQL pronto para copiar. O banco padrão é PostgreSQL; cada doc mostra como fazer o mesmo nos ORMs mais usados. Recursos e comandos foram conferidos em 2026-11-24.

## Desenhar

| Prática | O que entrega | Doc |
|---|---|---|
| Modelagem de entidades | Tabelas e relações a partir das regras do produto, com diagrama ER | [01-modelagem-de-entidades.md](01-modelagem-de-entidades.md) |
| Nomes e tipos | Convenção de nomes e o tipo certo para cada coluna | [02-nomes-e-tipos.md](02-nomes-e-tipos.md) |
| Chaves e ids | Chave primária, id público e foreign keys | [03-chaves-e-ids.md](03-chaves-e-ids.md) |
| Multiempresa | Isolamento dos dados de cada cliente | [06-multiempresa.md](06-multiempresa.md) |

## Mudar com segurança

| Prática | O que entrega | Doc |
|---|---|---|
| Migrations | Mudanças versionadas, sem travar tabela | [04-migrations.md](04-migrations.md) |
| Seeds e dados de teste | Banco local recriado com um comando; testes isolados | [05-seeds-e-dados-de-teste.md](05-seeds-e-dados-de-teste.md) |
| Auditoria, histórico e soft delete | Rastro de quem mudou o quê | [07-auditoria-historico-soft-delete.md](07-auditoria-historico-soft-delete.md) |

## Operar bem

| Prática | O que entrega | Doc |
|---|---|---|
| Índices e paginação | Consultas rápidas e listas que não pulam itens | [08-indices-e-paginacao.md](08-indices-e-paginacao.md) |
| Transações e concorrência | Operações tudo ou nada, sem conflito entre usuários | [09-transacoes-e-concorrencia.md](09-transacoes-e-concorrencia.md) |
| Dados pessoais e LGPD | Dado pessoal mínimo, protegido e apagável | [10-dados-pessoais-e-lgpd.md](10-dados-pessoais-e-lgpd.md) |

## Por onde começar

- **Sistema novo:** 01 → 02 → 03 → 06 (se multiempresa) → 04 → 05, e o 10 se houver dado pessoal.
- **Tabela nova num sistema que já existe:** 01, o checklist do [SKILL.md](../SKILL.md) e o 04.
- **Consulta lenta:** 08, começando pelo `EXPLAIN ANALYZE`.
- **Dois usuários alteraram o mesmo registro, ou o mesmo horário foi pego duas vezes:** 09.
- **Cliente pediu auditoria ou "não pode apagar":** 07.
- **Pediram para exportar ou apagar os dados de uma pessoa:** 10.
