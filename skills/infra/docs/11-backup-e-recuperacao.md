# Backup e recuperação

> Cópias dos dados feitas de forma automática, guardadas fora do lugar original e com restauração testada.

| | |
|---|---|
| **Site** | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html |
| **Categoria** | Continuidade |
| **Tipo** | Prática, com recursos do provedor e de ferramentas |
| **Stack** | Independente; `pg_dump` e recursos de banco gerenciado, armazenamento de objetos compatível com S3 |
| **Preço** | Prática: sem custo próprio; custo de armazenamento. RDS: 100% do armazenamento provisionado em backup é gratuito por região. Supabase: backup diário só no Pro. Render: Postgres grátis sem backup |
| **Licença** | Não se aplica |
| **Verificado em** | 2026-11-24 |

## O que é

Backup é uma cópia que permite voltar ao estado anterior depois de apagar algo, errar uma migração, sofrer ataque ou perder o servidor. Recuperação é o processo de restaurar, e só existe de verdade quando já foi testado.

Duas metas guiam a escolha: **RPO** (quanto dado você aceita perder, por exemplo 24 horas ou 5 minutos) e **RTO** (quanto tempo aceita ficar fora). Backup diário dá RPO de até um dia. Recuperação por ponto no tempo reduz isso para minutos. No RDS, a recuperação por ponto no tempo vale para qualquer instante dentro do período de retenção configurado.

## Por que usar

- **Erro humano acontece:** uma consulta errada em produção apaga dados.
- **Ataque de ransomware** e falha de disco ou de conta.
- **Exigência de cliente e de lei** sobre continuidade.
- **Tranquilidade para migrar** e testar mudanças arriscadas.
- **Metas claras** de perda e de tempo fora do ar.

## Quando usar

- Em qualquer sistema com dados de usuário, antes do primeiro cliente pagante.
- Antes de migrações de banco e atualizações grandes.
- Ao usar servidor próprio, onde nada é automático.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | O Git já é o backup; basta o conteúdo externo |
| MVP / protótipo | 🟡 Serve | Dump periódico; dados ainda valem pouco |
| SaaS pequeno | ✅ Ótimo | Backup diário e restauração testada, no mínimo |
| SaaS em crescimento | ✅ Ótimo | Recuperação por ponto no tempo e cópia em outra região |
| Sistema corporativo | ✅ Ótimo | RPO e RTO formais, retenção longa e teste periódico |
| Servidor próprio (VPS) | ✅ Ótimo | Tudo depende de você; copie para fora do servidor |
| Banco no plano grátis | ❌ Evite | Sem backup em alguns casos; faça o seu |
| Backup na mesma conta e região do banco | ❌ Evite | Uma falha de conta ou de região leva os dois |

## Quando é bom

- **Backup automático do provedor** poupa trabalho (RDS, Supabase Pro).
- **Recuperação por ponto no tempo** limita a perda a minutos.
- **Cópia externa e imutável** protege contra ataque e erro de conta.
- **Teste periódico** transforma esperança em fato.

## Quando é ruim

- **Backup sem teste:** só se descobre que não restaura quando é tarde.
- **Mesmo lugar do dado:** snapshot na mesma conta e região não protege de falha da conta.
- **RDS apaga backups automáticos** junto com a instância, se você não marcar para retê-los; snapshots manuais ficam.
- **Plano grátis sem cópia:** Supabase grátis e Render grátis não incluem backup automático.
- **Dump com segredos e dados pessoais** precisa de criptografia e acesso restrito.
- **Retenção curta demais:** um erro percebido tarde já passou da janela (Supabase Pro guarda 7 dias).
- **Recuperação por ponto no tempo pode ser paga à parte** (Supabase: complemento pago).

## Como começar

Backup manual de Postgres, a ser agendado:

```bash
pg_dump "$DATABASE_URL" -Fc -f "backup-$(date +%F).dump"
```

Enviar para armazenamento de objetos em outra conta ou região, com criptografia e versionamento. O comando depende do provedor; exemplo com a AWS CLI (confira a sintaxe na documentação):

```bash
aws s3 cp backup.dump s3://seu-bucket-de-backup/
```

Teste de restauração, feito em banco separado:

```bash
createdb teste_restore
pg_restore -d teste_restore backup.dump
```

Defina RPO e RTO por escrito, agende o teste (por exemplo, a cada trimestre) e crie alerta para backup que falhou.

## Combina com / alternativas

- [Postgres gerenciado](05-postgres-gerenciado.md): backup do provedor como primeira camada.
- [Coolify e Dokploy](02-vps-coolify-dokploy.md): backup agendado para S3.
- [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md): recriar a infra, enquanto o backup recria os dados.
- Alternativas: replicação para outra região (nuvem grande); snapshots de disco do VPS (complemento, não substituto de backup de banco).

## Decisão rápida

- **Use se:** o sistema guarda qualquer dado que não possa ser recriado (ou seja, quase sempre).
- **Evite se:** a ideia é "o provedor já cuida disso" sem ter lido o que o plano cobre e sem ter restaurado ao menos uma vez.
