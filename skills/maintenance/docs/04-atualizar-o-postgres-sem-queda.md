# Atualizar o Postgres sem queda

> Versão menor é trocar o binário e reiniciar; versão maior pede pg_upgrade (queda curta) ou replicação lógica (queda de segundos), sempre com backup restaurado antes e um plano de volta.

| | |
|---|---|
| **Referência** | PostgreSQL Documentation, pg_upgrade e Logical Replication (postgresql.org/docs/current); PostgreSQL Versioning Policy (postgresql.org/support/versioning); release notes de cada versão |
| **Categoria** | Manutenção |
| **Tipo** | Prática de operação de banco |
| **Vale para** | PostgreSQL 15 em diante, em servidor próprio, VPS ou contêiner; em serviço gerenciado, o provedor tem o próprio fluxo |
| **Verificado em** | 2026-11-25 |

## O que é

Duas atualizações diferentes:

- **Versão menor** (por exemplo 18.6 para 18.7): só corrige bugs e segurança. Troca o binário e reinicia o servidor. O formato dos dados não muda.
- **Versão maior** (por exemplo 17 para 18): muda o formato interno. Não dá para só trocar o binário.

A política oficial é 5 anos de suporte por versão maior, e a recomendação é rodar sempre a menor mais recente. Em 2026-11-25, o 14 acabou de sair de suporte (2026-11-12) e o 19 acabou de ser lançado (2026-11-19); veja o [calendário](01-calendario-de-fim-de-suporte.md).

## Por que usar

- **Segurança:** sem suporte, nenhuma falha nova é corrigida.
- **Desempenho e recursos** de cada versão maior.
- **Janela curta:** com plano e ensaio, a troca vira minutos, não horas.

## Quando usar

- A versão maior chegou a menos de 6 meses do fim.
- Uma extensão ou recurso exige versão mais nova.
- Versões menores atrasadas: faça já, é de baixo risco.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Dump e restore costuma bastar |
| MVP de SaaS | ✅ Ótimo | Banco pequeno; dump e restore em minutos |
| SaaS em crescimento | ✅ Ótimo | pg_upgrade em modo link ou replicação lógica |
| Sistema interno/corporativo | ✅ Ótimo | Janela combinada fora do expediente |
| API/integração | ✅ Ótimo | Replicação lógica para quase zero de queda |
| App mobile com backend | ✅ Ótimo | Idem; app antigo segue chamando a API |
| Banco gerenciado | 🟡 Serve | Use a atualização do provedor, com o mesmo ensaio |

## Quando é bom

- **Ensaio completo** em cópia do banco de produção, com medição do tempo.
- **Backup restaurado** antes (skill `infra`, [doc 11](../../infra/docs/11-backup-e-recuperacao.md); VPS: [backup](../../vps/docs/05-backup-e-restauracao-na-vps.md)).
- **Aplicação testada** na versão nova no CI antes da troca (imagem `postgres:18` nos testes de integração).
- **Estatísticas refeitas** logo depois.

## Quando é ruim

- **Primeira vez em produção,** sem ensaio.
- **Sem backup restaurado,** só "tem backup".
- **Atualizar junto com framework** ou migration grande: se algo falha, ninguém sabe o que foi.
- **Esquecer as extensões:** os binários das extensões precisam existir na versão nova.
- **Apagar o cluster antigo** no mesmo dia.

## Como começar

### Escolher o método

| Método | Queda | Complexidade | Quando |
|---|---|---|---|
| Menor: trocar binário | Reinício (segundos) | Baixa | Sempre que sair versão menor |
| Dump e restore (`pg_dump`/`pg_restore`) | Proporcional ao tamanho | Baixa | Banco até alguns GB, queda aceitável |
| `pg_upgrade --link` | Minutos, quase independente do tamanho | Média | Banco grande, mesmo servidor, mesmo sistema de arquivos |
| Replicação lógica | Segundos (só o corte) | Alta | Banco grande e janela mínima |

### Versão menor

```bash
sudo apt update
sudo apt install --only-upgrade postgresql-18
sudo systemctl restart postgresql
psql -c "select version();"
```

No Docker, troque a tag (`postgres:18.7`) e recrie o contêiner; o volume dos dados continua o mesmo.

### Dump e restore (banco pequeno)

```bash
pg_dump -Fc -h antigo -U app -d app -f app.dump
createdb -h novo -U app app
pg_restore -h novo -U app -d app --no-owner --jobs 4 app.dump
vacuumdb -h novo -U app --all --analyze-in-stages
```

Coloque o app em modo de manutenção durante o dump para não perder escritas.

### pg_upgrade (mesmo servidor)

Executado em 2026-11-25 num Debian 13 (trixie) com os pacotes do repositório PGDG, de 18 para 19.0 (`postgresql-19` 19.0-2.pgdg13+1), com `--check --link` e depois `--link --jobs=4`; os dois terminaram com sucesso. O Debian guarda o `postgresql.conf` em `/etc/postgresql/<versão>/main`, fora do diretório de dados, por isso o `pg_upgrade` precisa de `-o` e `-O` para achar a configuração (sem eles o servidor antigo não sobe e o comando falha).

```bash
sudo apt install postgresql-19
sudo systemctl stop postgresql
pg_lsclusters
sudo pg_dropcluster 19 main
sudo pg_createcluster 19 main --start-conf=manual
sudo -u postgres /usr/lib/postgresql/19/bin/pg_upgrade \
  -b /usr/lib/postgresql/18/bin -B /usr/lib/postgresql/19/bin \
  -d /var/lib/postgresql/18/main -D /var/lib/postgresql/19/main \
  -o "-c config_file=/etc/postgresql/18/main/postgresql.conf" \
  -O "-c config_file=/etc/postgresql/19/main/postgresql.conf" \
  --check --link
sudo -u postgres /usr/lib/postgresql/19/bin/pg_upgrade \
  -b /usr/lib/postgresql/18/bin -B /usr/lib/postgresql/19/bin \
  -d /var/lib/postgresql/18/main -D /var/lib/postgresql/19/main \
  -o "-c config_file=/etc/postgresql/18/main/postgresql.conf" \
  -O "-c config_file=/etc/postgresql/19/main/postgresql.conf" \
  --link --jobs=4
sudo systemctl start postgresql
vacuumdb --all --analyze-in-stages --missing-stats-only --jobs=4
vacuumdb --all --analyze-only --jobs=4
```

Os caminhos acima seguem o layout de pacotes do Debian e do Ubuntu (confirmados no teste); ajuste para a sua instalação. Notas do teste:

- Se o `pg_lsclusters` não listar o cluster `19 main`, pule o `pg_dropcluster`: no teste, instalar o pacote com um cluster 18 já existente não criou o 19, e o comando falhou com "specified cluster does not exist". Se listar, o `pg_dropcluster` é necessário para o `pg_upgrade` receber um cluster vazio.
- O `pg_createcluster 19 main` escolheu a porta 5433, porque a 5432 estava ocupada. Depois do upgrade, ajuste `port = 5432` em `/etc/postgresql/19/main/postgresql.conf` antes de religar o app, ou o app não conecta.
- O Debian também tem o `pg_upgradecluster`, que faz o mesmo de forma assistida; este doc usa o `pg_upgrade` por ser o comando da documentação do Postgres.
- O `--check` terminou com "Clusters are compatible". No teste, a verificação posterior com `psql` e os dois `vacuumdb` não rodaram (a porta ficou em 5433), então esse trecho segue a documentação do Postgres e não foi executado por mim.

Pontos da documentação:

- `--check` não altera nada; rode antes e com o mesmo modo (`--link`).
- Com `--link`, os arquivos são ligados, não copiados: rápido, mas depois de iniciar o cluster novo o antigo não pode mais ser usado. Se algo falhar antes de iniciar o novo, remova o sufixo `.old` de `global/pg_control` do cluster antigo e ele volta. Depois de iniciado, a única volta é o backup.
- `--clone` (sistema de arquivos com reflink, como Btrfs, XFS ou APFS) é quase tão rápido e mantém o cluster antigo utilizável.
- As estatísticas do otimizador são transferidas em geral, mas as estatísticas acumuladas não: rode os dois `vacuumdb` acima.
- Instale as extensões na versão nova (apenas os binários); não rode `CREATE EXTENSION`.
- Apague o cluster antigo só depois de dias de operação estável.

### Replicação lógica (janela mínima)

Resumo do fluxo; o procedimento completo está na seção de atualização da documentação oficial de replicação lógica.

1. Suba o servidor novo, vazio, na versão de destino.
2. Copie o esquema: `pg_dump --schema-only` do antigo, restore no novo.
3. No antigo (`wal_level = logical`): `CREATE PUBLICATION migracao FOR ALL TABLES;`
4. No novo: `CREATE SUBSCRIPTION migracao CONNECTION '...' PUBLICATION migracao;`
5. Espere a sincronização e confirme as contagens.
6. No corte: pare as escritas do app, espere o atraso zerar, acerte as sequences no novo (a replicação lógica não leva o valor delas; confira a versão da documentação), troque a connection string e religue.
7. Tabelas sem chave primária precisam de `REPLICA IDENTITY` explícita; mudanças de esquema (DDL) e objetos grandes não são replicados.

### Plano de volta

| Momento | Como voltar |
|---|---|
| Antes de iniciar o cluster novo (`--link`) | Restaurar o `pg_control` do antigo |
| Depois | Restaurar o backup, ou voltar o app para o servidor antigo (replicação lógica deixa o antigo intacto) |
| Aplicação com erro pós-corte | Reverter a connection string; só funciona se nenhuma escrita foi feita no novo |

### Checklist do dia

- [ ] Backup feito e restauração testada nos últimos 7 dias.
- [ ] Ensaio feito com o tempo medido.
- [ ] Aviso aos usuários e página de manutenção prontas.
- [ ] Extensões instaladas na versão nova.
- [ ] Testes de integração do CI rodando na versão nova.
- [ ] Alguém monitorando erros e latência depois (skill `infra`, doc 10).

## Combina com / alternativas

- Skill `infra`: [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md) e [backup](../../infra/docs/11-backup-e-recuperacao.md).
- Skill `data`: [migrations](../../data/docs/04-migrations.md).
- Skill `vps`: [backup na VPS](../../vps/docs/05-backup-e-restauracao-na-vps.md).
- [Calendário de fim de suporte](01-calendario-de-fim-de-suporte.md).
- Alternativa: banco gerenciado, em que o provedor faz parte do trabalho.

## Decisão rápida

- **Use dump e restore se:** o banco é pequeno e uma queda de minutos é aceitável.
- **Use pg_upgrade se:** é um servidor só e a queda deve ser de minutos.
- **Use replicação lógica se:** a janela precisa ser de segundos e o time aguenta a complexidade.
