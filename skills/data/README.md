# data

Skill para o Claude Code que modela os dados e o banco da aplicação: entidades, tipos, chaves, migrations, seeds, multiempresa, auditoria, índices, transações e LGPD. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com SQL pronto para copiar.

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Modelagem | Entidades, relações, normalização, diagrama ER | [docs/01-modelagem-de-entidades.md](docs/01-modelagem-de-entidades.md) |
| Nomes e tipos | Convenções e o tipo certo para cada dado | [docs/02-nomes-e-tipos.md](docs/02-nomes-e-tipos.md) |
| Chaves e ids | Identity x UUID v7, id público, foreign keys | [docs/03-chaves-e-ids.md](docs/03-chaves-e-ids.md) |
| Migrations | Uma por mudança, sem travar tabela | [docs/04-migrations.md](docs/04-migrations.md) |
| Seeds e dados de teste | Referência, dados falsos, banco de teste | [docs/05-seeds-e-dados-de-teste.md](docs/05-seeds-e-dados-de-teste.md) |
| Multiempresa | Cada cliente vê só os seus dados | [docs/06-multiempresa.md](docs/06-multiempresa.md) |
| Auditoria, histórico e soft delete | Quem mudou o quê; quando não apagar | [docs/07-auditoria-historico-soft-delete.md](docs/07-auditoria-historico-soft-delete.md) |
| Índices e paginação | Consultas rápidas, offset x cursor | [docs/08-indices-e-paginacao.md](docs/08-indices-e-paginacao.md) |
| Transações e concorrência | Tudo ou nada, conflitos, outbox | [docs/09-transacoes-e-concorrencia.md](docs/09-transacoes-e-concorrencia.md) |
| Dados pessoais e LGPD | Minimizar, proteger, exportar e apagar | [docs/10-dados-pessoais-e-lgpd.md](docs/10-dados-pessoais-e-lgpd.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/data ~/.claude/skills/data
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é criar ou mudar tabelas, escrever migration, isolar dados por cliente ou resolver consulta lenta. Também dá para chamar direto com `/data`. Exemplos:

- "Modela o banco do sistema de agendamento a partir do BACKLOG.md."
- "Cada clínica precisa ver só os próprios pacientes. Como faço?"
- "/data essa listagem de pedidos está lenta, o que eu indexo?"

Com a skill carregada, o Claude:

1. lê as regras de negócio e as histórias do produto;
2. pergunta se é multiempresa, se há dado pessoal e se precisa de histórico;
3. desenha o modelo, mostra o diagrama e espera o ok;
4. gera a migration com o ORM da stack e revisa o SQL;
5. confere o checklist de cada tabela e recria o banco do zero para testar.

## Estrutura

```
data/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                                índice e "Por onde começar"
    ├── 01-modelagem-de-entidades.md
    ├── 02-nomes-e-tipos.md
    ├── 03-chaves-e-ids.md
    ├── 04-migrations.md
    ├── 05-seeds-e-dados-de-teste.md
    ├── 06-multiempresa.md
    ├── 07-auditoria-historico-soft-delete.md
    ├── 08-indices-e-paginacao.md
    ├── 09-transacoes-e-concorrencia.md
    └── 10-dados-pessoais-e-lgpd.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** recursos do Postgres e comandos dos ORMs foram conferidos em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
