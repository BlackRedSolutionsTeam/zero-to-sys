# Backup e restauração na VPS

> Na VPS nada é automático: combine snapshot do provedor com dump agendado do banco, copie para fora do servidor e restaure de verdade ao menos uma vez.

| | |
|---|---|
| **Referência** | https://restic.readthedocs.io, https://developers.cloudflare.com/r2/pricing/, https://www.postgresql.org/docs/current/app-pgdump.html, https://coolify.io/docs/databases/backups |
| **Categoria** | Servidor |
| **Tipo** | Prática de backup e restauração em servidor próprio |
| **Vale para** | VPS com Docker, Coolify ou Dokploy e Postgres no mesmo servidor ou em contêiner |
| **Verificado em** | 2026-11-25 |

## O que é

Em VPS, você é o responsável pelo backup. Há duas camadas que não se substituem:

- **Snapshot do provedor:** foto do disco inteiro da máquina. Restaura o servidor todo, rápido, mas fica na mesma conta do provedor. Quanto custa e se existe varia por plano: consulte a página do seu provedor.
- **Dump do banco:** arquivo gerado por `pg_dump`, pequeno e consistente. Restaura só os dados, em qualquer servidor.

Depois vem a **cópia externa**: o arquivo vai para um armazenamento de objetos compatível com S3 (como o Cloudflare R2) em outra conta. Ferramentas comuns: **restic** (cópia criptografada e deduplicada, licença BSD 2-Clause) e **rclone** (copia arquivos para S3 e R2).

Metas: **RPO** é quanto dado você aceita perder; **RTO** é quanto tempo aceita ficar fora. Detalhes em [backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md).

## Por que usar

- Snapshot sozinho some junto com a conta ou o servidor.
- Dump é pequeno, restaura em qualquer lugar e dá para testar em minutos.
- Cópia externa protege de erro de conta, ataque e falha do provedor.
- R2 não cobra saída de dados (egress) para a internet, então restaurar não gera conta extra (conferido em 2026-11-25).

## Quando usar

- Antes do primeiro cliente pagante.
- Antes de migração de banco ou atualização grande.
- Em todo servidor com banco no mesmo disco do app.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | O Git guarda o código; copie só uploads e banco, se houver |
| MVP de SaaS | ✅ Ótimo | Dump diário para R2 custa quase nada |
| SaaS em crescimento | ✅ Ótimo | Dump mais frequente, retenção longa e teste agendado |
| Sistema interno/corporativo | ✅ Ótimo | Exige RPO e RTO escritos e prova de restauração |
| API/integração | ✅ Ótimo | Estado crítico em banco e filas precisa de cópia |
| App mobile com backend | ✅ Ótimo | Perder dados de usuário quebra o app em todos os aparelhos |
| Banco com recuperação por ponto no tempo exigida | ❌ Evite | Dump diário não cobre; use banco gerenciado ou WAL contínuo |

## Quando é bom

- **Dois níveis:** snapshot para servidor inteiro, dump para dados.
- **Barato:** no R2, 10 GB-mês, 1 milhão de operações classe A e 10 milhões de classe B são grátis por mês; acima disso são US$ 0,015 por GB-mês (conferido em 2026-11-25).
- **Coolify:** agenda dump de Postgres, envia para S3 e guarda retenção por destino (conferido em 2026-11-25).
- **restic:** criptografa e só guarda o que mudou.

## Quando é ruim

- Dump diário perde até 24 horas de dados.
- Snapshot de disco com banco ligado pode ficar inconsistente; não o use como único backup do banco.
- Backup que nunca foi restaurado é esperança, não backup.
- Chaves do R2 no próprio servidor: quem invadir a VPS apaga também a cópia. Use chave só de escrita e ative versionamento ou bloqueio de objeto, se o provedor oferecer.
- Dump contém dados pessoais: criptografe e restrinja o acesso (LGPD).

## Como começar

Variáveis em `/etc/backup.env`, com permissão 600:

```bash
AWS_ACCESS_KEY_ID=chave-do-r2
AWS_SECRET_ACCESS_KEY=segredo-do-r2
RESTIC_REPOSITORY=s3:https://CONTA.r2.cloudflarestorage.com/clinica-backup
RESTIC_PASSWORD=senha-forte-do-repositorio
```

Criar o repositório (uma vez):

```bash
set -a; . /etc/backup.env; set +a
restic init
```

Script `/usr/local/bin/backup-db.sh` para a clínica de exemplo, com o Postgres em contêiner:

```bash
#!/usr/bin/env bash
set -euo pipefail
set -a; . /etc/backup.env; set +a
mkdir -p /var/backups/db
arquivo="/var/backups/db/clinica-$(date +%F-%H%M).dump"
docker exec clinica-db pg_dump -U clinica -Fc clinica > "$arquivo"
restic backup /var/backups/db
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune
find /var/backups/db -type f -mtime +2 -delete
```

Agendar às 03:00 e avisar se falhar:

```bash
echo '0 3 * * * root /usr/local/bin/backup-db.sh || curl -fsS https://hc-ping.exemplo/falhou' > /etc/cron.d/backup-db
```

Com rclone, a configuração do R2 usa `provider = Cloudflare`, o endpoint `https://CONTA.r2.cloudflarestorage.com` e `acl = private`; exige rclone 1.59 ou mais novo (conferido em 2026-11-25):

```bash
rclone copy /var/backups/db r2:clinica-backup/db
```

**Teste de restauração**, mensal e em outra máquina ou banco descartável:

```bash
set -a; . /etc/backup.env; set +a
restic restore latest --target /tmp/restore
createdb teste_restore
pg_restore -d teste_restore /tmp/restore/var/backups/db/clinica-*.dump
psql -d teste_restore -c "select count(*) from consultas"
restic check
```

Anote quanto tempo levou: esse é o seu RTO real. Para banco no Coolify, use o agendamento nativo e restaure em banco descartável antes de confiar.

## Combina com / alternativas

- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md) e [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md), quando a recuperação por ponto no tempo for exigida.
- [Monitoramento e alertas](06-monitoramento-e-alertas.md): alerte quando o backup não rodar.
- [Migrar ou sair da VPS](08-migrar-ou-sair-da-vps.md): o dump é a base da migração.
- Alternativas: Backblaze B2, Wasabi ou S3 como destino; `wal-g` ou `pgBackRest` para ponto no tempo.

## Decisão rápida

- **Use se:** o banco está na VPS e há dados que não dá para recriar.
- **Evite se:** a ideia é depender só do snapshot do provedor, ou guardar a cópia no mesmo servidor ou na mesma conta.
