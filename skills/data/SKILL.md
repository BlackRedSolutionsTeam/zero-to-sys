---
name: data
description: 'Modela os dados e o banco: entidades e relações, nomes e tipos, chaves e ids, migrations seguras, seeds, multiempresa com RLS, auditoria e soft delete, índices, paginação, transações e LGPD no banco. Use quando pedirem "modelar o banco", "criar tabelas" ou "migration".'
---

# data

Guia para transformar as regras de negócio em tabelas que aguentam o sistema crescer. O modelo de dados é a parte mais cara de mudar depois: tabela errada vira migration arriscada, dado duplicado e bug de vazamento entre clientes. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e SQL pronto para copiar. O banco padrão do plugin é PostgreSQL; o que muda em outros bancos está dito no doc.

## Como usar esta skill

1. **Parta do produto.** Leia as histórias, as regras de negócio e a máquina de estados da skill `product` (`BACKLOG.md`, `docs/regras-de-negocio.md`). Os substantivos viram entidades; os estados viram coluna de status. Se o projeto foi prototipado no Framia (skill `framia`), o diagrama do banco aprovado lá é o ponto de partida.
2. **Responda antes de desenhar:** o sistema é multiempresa? Guarda dado pessoal ou sensível? Precisa de histórico de quem mudou o quê? Essas três respostas mudam todas as tabelas.
3. **Desenhe o modelo** com o [doc 01](docs/01-modelagem-de-entidades.md) e um diagrama em Mermaid, e mostre ao usuário antes de gerar migration.
4. **Aplique nomes, tipos e chaves** pelos docs [02](docs/02-nomes-e-tipos.md) e [03](docs/03-chaves-e-ids.md).
5. **Gere a migration** com a ferramenta do ORM da stack e revise o SQL gerado ([doc 04](docs/04-migrations.md)).
6. **Crie o seed** de referência e de desenvolvimento ([doc 05](docs/05-seeds-e-dados-de-teste.md)).
7. **Confira o checklist** abaixo para cada tabela nova.
8. **Rode de verdade:** recrie o banco local do zero (reset, migrate, seed) e rode os testes antes de dar por pronto.

## Decisões por porte

| Decisão | MVP | SaaS pequeno ou em crescimento | Sistema corporativo |
|---|---|---|---|
| Multiempresa | Coluna `tenant_id` desde o início, se houver mais de um cliente | `tenant_id` + Row Level Security | `tenant_id` + RLS; schema ou banco por cliente só se o contrato exigir |
| Chave primária | `bigint` identity ou UUID v7 | UUID v7 quando o id aparece na URL ou vem de fora | Padrão da empresa; UUID v7 se não houver |
| Auditoria | `created_at`, `updated_at` | + `created_by`, `updated_by` e histórico de status | + tabela de auditoria com antes e depois |
| Exclusão | Apagar de verdade | Soft delete só onde a regra pede | Conforme retenção e LGPD |
| Paginação | Offset | Cursor nas listas grandes e infinitas | Cursor |
| Concorrência | Constraint `unique` nas regras críticas | + lock otimista nas edições | + níveis de isolamento revisados |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Modelagem | [docs/01-modelagem-de-entidades.md](docs/01-modelagem-de-entidades.md) | Entidades, relações, normalização, diagrama ER |
| Nomes e tipos | [docs/02-nomes-e-tipos.md](docs/02-nomes-e-tipos.md) | Convenções e o tipo certo para dinheiro, data, texto e enum |
| Chaves e ids | [docs/03-chaves-e-ids.md](docs/03-chaves-e-ids.md) | Identity x UUID v7, id público, foreign keys |
| Migrations | [docs/04-migrations.md](docs/04-migrations.md) | Uma por mudança, sem travar tabela, comando por stack |
| Seeds e dados de teste | [docs/05-seeds-e-dados-de-teste.md](docs/05-seeds-e-dados-de-teste.md) | Dados de referência, dados falsos e banco de teste |
| Multiempresa | [docs/06-multiempresa.md](docs/06-multiempresa.md) | Cada cliente vê só os seus dados; RLS |
| Auditoria, histórico e soft delete | [docs/07-auditoria-historico-soft-delete.md](docs/07-auditoria-historico-soft-delete.md) | Quem mudou o quê; quando não apagar |
| Índices e paginação | [docs/08-indices-e-paginacao.md](docs/08-indices-e-paginacao.md) | Consultas rápidas, offset x cursor, N+1 |
| Transações e concorrência | [docs/09-transacoes-e-concorrencia.md](docs/09-transacoes-e-concorrencia.md) | Tudo ou nada, dois usuários no mesmo registro, outbox |
| Dados pessoais e LGPD | [docs/10-dados-pessoais-e-lgpd.md](docs/10-dados-pessoais-e-lgpd.md) | Minimizar, proteger, exportar e apagar |

## Checklist de toda tabela nova

- [ ] Nome no padrão do projeto e chave primária definida ([02](docs/02-nomes-e-tipos.md), [03](docs/03-chaves-e-ids.md)).
- [ ] `tenant_id` com foreign key e índice, se o sistema for multiempresa ([06](docs/06-multiempresa.md)).
- [ ] `created_at` e `updated_at` em `timestamptz` ([07](docs/07-auditoria-historico-soft-delete.md)).
- [ ] Colunas `NOT NULL` por padrão; dinheiro sem `float`; data com fuso.
- [ ] Foreign keys declaradas, com `on delete` escolhido de propósito, e índice em cada uma ([08](docs/08-indices-e-paginacao.md)).
- [ ] Regras de unicidade do produto viraram `unique` ou constraint no banco, não só validação na tela.
- [ ] Índice para cada busca e ordenação que a tela ou a API faz.
- [ ] Dado pessoal identificado e, se sensível, protegido ([10](docs/10-dados-pessoais-e-lgpd.md)).
- [ ] Migration revisada, reversível quando possível e testada num banco recriado do zero ([04](docs/04-migrations.md)).
- [ ] Seed atualizado, se a tabela tem dado de referência ([05](docs/05-seeds-e-dados-de-teste.md)).

## Regras de uso

- **Regra de negócio importante mora no banco também.** Unicidade, obrigatoriedade e faixas válidas viram constraint. A validação na aplicação dá a mensagem bonita; a constraint impede o dado errado quando dois pedidos chegam juntos.
- **Multiempresa se decide no primeiro dia.** Acrescentar `tenant_id` depois, com dados de vários clientes misturados, é uma das migrations mais caras que existem.
- **Nunca edite migration já aplicada.** Crie uma nova. O histórico de migrations é o histórico do banco.
- **Revise o SQL que o ORM gera.** Principalmente em tabela grande: um `ALTER` inocente pode travar a tabela em produção.
- **Dinheiro nunca em `float`, data nunca sem fuso.** Use `numeric` ou centavos em inteiro, e `timestamptz`.
- **Sem chamada externa dentro de transação.** Pagamento, e-mail e webhook ficam fora; use outbox ([doc 09](docs/09-transacoes-e-concorrencia.md)).
- **Produção não vai para o banco de desenvolvimento.** Dados de teste são falsos ou anonimizados.
- **Meça antes de otimizar.** Use `EXPLAIN ANALYZE` na consulta lenta antes de criar índice ou cache.
- **Fronteiras.** Banco gerenciado, backup e réplica são da skill `infra`; a escolha do ORM é da `stacks`; o formato de lista e de erro na API é da `api`; login, papéis e permissões são da `security`. Esta skill cuida do que fica dentro do banco.

## Quando a lista não cobre

Data warehouse, analytics, busca textual avançada (Elasticsearch, Meilisearch), banco de grafos, séries temporais em grande volume, sharding e bancos NoSQL como base principal ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial da ferramenta.

## Validade dos dados

Recursos de banco e comandos de ORM foram conferidos em 2026-11-24. Cada documento tem a linha "Verificado em"; confira a versão do Postgres e do ORM do projeto antes de usar um recurso novo.
