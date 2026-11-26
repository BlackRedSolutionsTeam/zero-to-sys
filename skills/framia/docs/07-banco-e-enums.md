# Banco e enums

> Desenhar tabelas, colunas, relações e enums no Framia a partir das regras de negócio, e sair com SQL, DBML ou Mermaid para o modelo de dados do app.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/database, https://framia.com.br/pt-br/docs/enums e https://framia.com.br/pt-br/docs/product |
| **Categoria** | Dados |
| **Ferramentas do MCP** | `create_db_table`, `update_db_table`, `delete_db_table`, `add_db_column`, `update_db_column`, `delete_db_column`, `create_db_relation`, `update_db_relation`, `delete_db_relation`, `create_db_group`, `create_db_note`, `create_enum`, `update_enum`, `delete_enum`, `get_document` |
| **Verificado em** | 2026-11-26 |

## O que é

Na aba **Produto** → **Banco**, o Framia guarda um diagrama de schemas, tabelas, colunas e relações. Ele **não se conecta a banco nenhum**: é o desenho. Do desenho saem três visões, com **Copiar** e **Baixar**: **SQL** (PostgreSQL, MySQL ou SQLite, escolhidos em **Motor SQL**), **DBML** e **Mermaid**.

**Produto** → **Enums** guarda as listas fechadas de valores, como `booking_status`.

## Passo a passo

1. Leia `docs/regras-de-negocio.md` e as histórias. Os substantivos viram tabelas; os estados viram enum.
2. Responda as três perguntas da skill `data` antes de desenhar: é multiempresa? Guarda dado pessoal ou sensível? Precisa de histórico de quem mudou o quê?
3. `create_enum` para cada lista fechada, com `values` (valor real, como `confirmed`, e rótulo opcional).
4. `create_db_table` com `name`, `comment` e as `columns` de uma vez; use `groupId` para agrupar por módulo (`create_db_group`).
5. `create_db_relation` para cada chave estrangeira, com `kind` (`many-to-one`, `one-to-many`, `one-to-one`, `many-to-many`) e `onDelete`.
6. `create_db_note` para a regra que o diagrama não diz ("um agendamento por horário e profissional").
7. Mostre o diagrama ao usuário antes de seguir para as rotas.

## Colunas

Cada coluna tem nome, tipo (texto livre: `uuid`, `text`, `timestamptz`), **Nulo**, **Chave primária**, **Único**, **Padrão**, **Enum** e **Máscara** (o editor sugere pelo nome: CPF, CNPJ, e-mail).

- Nomes e tipos pelas regras da skill `data` ([nomes e tipos](../../data/docs/02-nomes-e-tipos.md) e [chaves e ids](../../data/docs/03-chaves-e-ids.md)): os mesmos nomes vão para o código.
- Ligar a coluna a um enum troca o tipo dela pelo nome do enum.
- `delete_db_column` também apaga as relações e os vínculos de tela que usam a coluna: confira antes.
- Relação **Apenas documentada** fica fora do SQL; tabela marcada "Ainda não está no banco de dados" (`offDb`) serve para o que é do depois.

## Enums no SQL

| Motor | Como sai |
|---|---|
| PostgreSQL | `CREATE TYPE … AS ENUM` |
| MySQL | `ENUM(…)` na coluna |
| SQLite | `TEXT` |

## Importar o que já existe

Com um DBML pronto (de outro projeto ou gerado de um banco), **Importar** na barra de cima do editor: cole, confira o resumo e importe. O Framia combina por nome e trata tudo como uma mudança só. Além do limite de tabelas do plano, nada é criado.

## Levar para o código

O SQL do Framia é **referência**, não migration. O banco do app nasce da migration do ORM (skill `data`, [migrations](../../data/docs/04-migrations.md)); o diagrama diz quais tabelas, colunas, relações e enums ela precisa ter. O DBML ou o Mermaid entra no `ARCHITECTURE.md` como diagrama do modelo. Detalhes em [Aprovação e passagem para o código](10-aprovacao-e-passagem-para-o-codigo.md).

## Encaixe por tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS, sistema interno, app mobile | ✅ Ótimo | As telas se ligam às colunas, e as rotas saem das tabelas |
| API, integração | ✅ Ótimo | Banco e rotas são o protótipo inteiro |
| Landing, site de conteúdo | ❌ Pule | Sem banco; no máximo a tabela do formulário |

## Quando é bom

- **Muda barato:** mover uma coluna aqui custa segundos; depois da migration, custa uma migration.
- **Cliente e time olham a mesma coisa:** o diagrama fica ao lado das telas.
- **Dá origem às rotas:** `generate_endpoints` parte das tabelas ([doc 08](08-api-e-perfis.md)).

## Quando é ruim

- **Tratar o SQL exportado como schema final:** índices, constraints de regra e ajustes do ORM são da skill `data`.
- **Desenhar o banco do sistema inteiro:** só as tabelas do MVP; o resto fica como "ainda não está no banco" ou fora.
- **Dois lugares mandando:** depois da primeira migration, a fonte é a migration. Mudou o banco no código? Atualize o diagrama no mesmo item.
- **Plano Starter:** 10 tabelas por projeto.

## Combina com

- [API e perfis](08-api-e-perfis.md): rotas geradas das tabelas.
- [Requisitos e vínculos](09-requisitos-e-vinculos.md): campo da tela ligado à coluna.
- [Modelagem de entidades](../../data/docs/01-modelagem-de-entidades.md): o critério do desenho.
