# Postgres gerenciado (Neon, Supabase e RDS)

> Banco PostgreSQL operado por um provedor, com backup, atualização e alta disponibilidade, para você não administrar o servidor de dados.

| | |
|---|---|
| **Site** | https://neon.com, https://supabase.com, https://aws.amazon.com/rds |
| **Categoria** | Dados |
| **Tipo** | Banco de dados gerenciado |
| **Stack** | PostgreSQL; Supabase inclui autenticação, armazenamento e funções |
| **Preço** | Neon: grátis (100 projetos, 1 GB por projeto), Launch pago por uso (US$ 0,106 por CU-hora, US$ 0,35 por GB-mês). Supabase: grátis (2 projetos, 500 MB), Pro a partir de US$ 25/mês. RDS: pago por uso; no PostgreSQL Single-AZ sob demanda em us-east-1, db.t4g.micro custa US$ 0,016 por hora (cerca de US$ 11,70 por mês) e db.t3.micro US$ 0,018 por hora; armazenamento gp3 a US$ 0,115 por GB-mês (lista de preços da AWS, conferido em 2026-11-24) |
| **Licença** | PostgreSQL é open source; os serviços são proprietários (Supabase e Neon publicam código aberto sob Apache 2.0 nos repositórios supabase/supabase e neondatabase/neon, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

O dado é a parte mais difícil de recuperar numa falha. Um Postgres gerenciado entrega backup, patches, monitoramento e, nos planos maiores, réplicas.

**Neon** separa computação e armazenamento, desliga a computação quando não há uso (no grátis, após 5 minutos) e cria branches de banco por cópia na escrita, úteis para homologação e previews. **Supabase** é o Postgres com autenticação, storage e funções; no plano grátis o projeto pausa após uma semana sem atividade e não há backup automático. **RDS** é o Postgres da AWS: sem plano grátis perpétuo, com backups automáticos e recuperação para qualquer ponto dentro do período de retenção.

## Por que usar

- **Backup e recuperação** sem montar nada (nos planos que os incluem).
- **Menos operação:** atualização e monitoramento do provedor.
- **Padrão aberto:** é Postgres comum, dá para migrar com `pg_dump`.
- **Neon:** branches de banco por pull request.
- **Supabase:** autenticação e API prontas, reduzem código.

## Quando usar

- Qualquer sistema com dados relacionais, do MVP ao corporativo.
- Quando ninguém quer ser DBA.
- Neon ou Supabase no começo e RDS (ou equivalente) em nuvem grande.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Não precisa de banco |
| MVP / protótipo | ✅ Ótimo | Neon ou Supabase grátis para validar |
| SaaS pequeno | ✅ Ótimo | Plano pago com backup; Supabase Pro inclui 7 dias de backup diário |
| SaaS em crescimento | ✅ Ótimo | Neon Scale, Supabase maior ou RDS com réplica |
| Sistema corporativo | ✅ Ótimo | RDS ou equivalente, com rede privada e criptografia |
| App com carga constante e alta | 🟡 Serve | Computação que dorme (Neon) é ruim aqui; prefira instância fixa |
| Dados muito sensíveis | 🟡 Serve | Confira região, criptografia e contrato antes |
| Produção em plano grátis | ❌ Evite | Pausa, limites e sem backup (Supabase) |

## Quando é bom

- **Neon:** escala a zero, branching barato e conexão estável após o despertar (em geral algumas centenas de milissegundos, segundo o site).
- **Supabase:** tudo num lugar, com painel e SQL no navegador.
- **RDS:** maduro, integrado à rede e ao IAM da AWS.
- **Dados portáveis:** por ser Postgres, a saída é possível.

## Quando é ruim

- **Plano grátis não é produção:** Supabase pausa e não faz backup; Neon suspende a computação ao passar do limite do plano.
- **Cold start (Neon):** a primeira consulta após dormir tem latência extra.
- **Custo cresce com dados e computação:** acompanhe armazenamento e consumo.
- **Recursos próprios geram lock-in:** funções e autenticação do Supabase ou branching do Neon dificultam trocar.
- **Conexões limitadas:** use pool de conexão em ambientes de funções.
- **RDS:** custo e configuração de rede maiores; sem plano grátis perpétuo.
- **Recuperação por ponto no tempo no Supabase** é complemento pago (US$ 100/mês por 7 dias de retenção, no momento da verificação).

## Como começar

Crie o projeto pelo painel e guarde a string de conexão no gerenciador de segredos do projeto ([doc 09](09-segredos-e-configuracao.md)). Teste a conexão:

```bash
psql "$DATABASE_URL" -c "select version();"
```

Backup manual de qualquer um deles:

```bash
pg_dump "$DATABASE_URL" -Fc -f backup.dump
```

Prefira conexão com TLS e usuário da aplicação sem permissão de administrador (veja [segurança base](12-seguranca-base.md)).

## Combina com / alternativas

- [Backup e recuperação](11-backup-e-recuperacao.md): complementa o do provedor.
- [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md): RDS e Neon podem ser descritos em código.
- [PaaS](01-paas.md): bancos próprios do Railway e do Render são outra opção.
- Alternativas: Cloud SQL (GCP): instância compartilhada db-f1-micro a US$ 0,0105 por hora e db-g1-small a US$ 0,035 por hora em us-central1, sem SLA; SSD a US$ 0,000232877 por GiB-hora, cerca de US$ 0,17 por GiB-mês (cloud.google.com/sql/pricing, conferido em 2026-11-24); Azure Database for PostgreSQL Flexible Server: Burstable B1ms a US$ 0,017 por hora, cerca de US$ 12,40 por mês só de computação, em East US (API de preços da Azure, conferido em 2026-11-24); Postgres autohospedado só com quem saiba operá-lo.

## Decisão rápida

- **Use se:** o sistema guarda dados relacionais e o time não quer administrar banco.
- **Evite se:** quer produção em plano grátis, tem carga constante e alta em computação que dorme, ou precisa de algo além do Postgres (avalie outro tipo de banco).
