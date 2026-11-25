# Escalar: vertical, horizontal e réplica de leitura

> Escalar é o último passo, não o primeiro: confirme com números que o gargalo é capacidade e escolha a forma mais simples que resolve.

| | |
|---|---|
| **Referência** | PostgreSQL docs: High Availability, Load Balancing, and Replication (postgresql.org/docs/current/warm-standby.html); The Twelve-Factor App (12factor.net); skill `vps`, doc 02 e doc 08; skill `infra` |
| **Categoria** | Desempenho |
| **Tipo** | Guia de decisão |
| **Vale para** | Qualquer back-end; exemplos de banco em PostgreSQL |
| **Verificado em** | 2026-11-25 |

## O que é

Três jeitos de aumentar a capacidade:

- **Vertical (scale up):** um servidor maior (mais CPU e RAM). Não muda o código.
- **Horizontal (scale out):** mais instâncias da aplicação atrás de um balanceador. Exige app **sem estado** (sessão no banco ou no Redis, arquivos em armazenamento de objetos).
- **Réplica de leitura:** uma cópia do banco que recebe as mudanças da principal e atende só consultas de leitura.

## Por que usar

- **Vertical:** a mudança mais rápida e barata de fazer; resolve muito problema de MVP.
- **Horizontal:** passa do limite de uma máquina e tolera a queda de uma instância.
- **Réplica:** tira relatórios e listagens pesadas da instância que recebe escrita.

## Quando usar

Antes de escalar, confirme com o [doc 01](01-medir-primeiro.md) e o [doc 04](04-teste-de-carga-com-k6.md):

| Sintoma medido | Primeiro passo | Escalar só se |
|---|---|---|
| CPU da API em 80% ou mais e perfil sem desperdício | Perfil ([doc 05](05-profiling-por-stack.md)) | A função quente já está otimizada |
| Consultas lentas | Plano e índice ([doc 02](02-banco-explain-n-mais-1-e-pool.md)) | Plano bom e CPU ou RAM do banco no limite |
| Leitura repetida demais | Cache ([doc 03](03-cache-http-aplicacao-e-redis.md)) | Cache com boa taxa de acerto e a leitura ainda pesa |
| Tarefas lentas dentro da requisição | Fila ([doc 06](06-trabalho-pesado-fora-da-requisicao.md)) | O worker satura |
| RAM acabando | Procurar vazamento ([doc 05](05-profiling-por-stack.md)) | Uso estável e legítimo |

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | CDN e cache; vertical simples se a origem sofrer |
| MVP de SaaS | ✅ Ótimo | Vertical primeiro; horizontal só com pico comprovado |
| SaaS em crescimento | ✅ Ótimo | Duas ou mais instâncias da API, worker separado e réplica de leitura para relatórios |
| Sistema interno/corporativo | 🟡 Serve | Uma máquina folgada costuma bastar; vertical |
| API/integração | ✅ Ótimo | Horizontal atrás de balanceador para absorver rajadas |
| App mobile com backend | ✅ Ótimo | Picos por notificação empurrada pedem instâncias extras |
| Escalar "porque vai crescer" | ❌ Evite | Complexidade e custo hoje por uma demanda que talvez nunca venha |

## Quando é bom

- **Vertical:** nenhuma mudança de código, resultado imediato; em VPS e em nuvem basta trocar o plano (pode exigir reinício).
- **Horizontal:** ganho quase linear para a camada de aplicação, mais tolerância a falha.
- **Réplica:** alivia o banco principal em cargas de leitura.

## Quando é ruim

- **Vertical tem teto** e, em muitos provedores, exige reinício ou migração. A máquina continua sendo ponto único de falha ([vps](../../vps/SKILL.md)).
- **Horizontal pressupõe app sem estado:** sessão em memória, arquivo em disco local e tarefas agendadas em cada instância quebram quando há duas cópias.
- **Mais instâncias, mais conexões no banco:** cada uma abre seu pool. Some tudo e use PgBouncer ([doc 02](02-banco-explain-n-mais-1-e-pool.md)).
- **Réplica atrasada:** a replicação do PostgreSQL é assíncrona por padrão; a doc oficial fala em atraso tipicamente menor que 1 segundo, mas uma leitura logo após uma escrita pode não ver a mudança. A réplica serve para telas que toleram dado levemente atrasado.
- **Escalar o app sem olhar o banco:** o banco costuma ser o gargalo; mais instâncias só aumentam a fila para ele.

## Como começar

### Ordem sugerida

1. Medir, corrigir banco, cache e código, tirar o trabalho pesado da requisição.
2. Vertical: subir o plano e repetir o teste de carga. Se o p95 voltou à meta, parar.
3. Tornar a app sem estado e subir a segunda instância atrás do balanceador (proxy do Coolify ou Dokploy, nginx `upstream` ou balanceador da nuvem; veja [nginx](../../nginx/SKILL.md) e [infra](../../infra/SKILL.md)).
4. Separar o banco e o worker da máquina da API ([vps, doc 02](../../vps/docs/02-dimensionar-o-servidor.md)).
5. Só então, réplica de leitura para o que tolera atraso.

### Lista de verificação de app sem estado

| Item | Como deve estar |
|---|---|
| Sessão e login | Token assinado ou sessão no banco ou no Redis, não na memória do processo |
| Arquivos enviados | Armazenamento de objetos ([integrations, doc 07](../../integrations/docs/07-armazenamento-de-arquivos.md)) |
| Rotinas agendadas | Um só executor ou trava no banco ([integrations, doc 06](../../integrations/docs/06-rotinas-agendadas.md)) |
| Cache local | Compartilhado (Redis) ou aceitar que cada instância tem o seu |
| Configuração | Variáveis de ambiente iguais em todas as instâncias ([infra, doc 09](../../infra/docs/09-segredos-e-configuracao.md)) |
| Saúde | Rota `/saude` para o balanceador tirar a instância ruim |

### Réplica de leitura

Medir o atraso na principal e na réplica (visões conferidas na doc em 2026-11-25):

```sql
select client_addr, state, replay_lag from pg_stat_replication;
```

Regras de uso na aplicação:

- Duas conexões configuradas: `DATABASE_URL` (escrita) e `DATABASE_REPLICA_URL` (leitura).
- Mande para a réplica relatórios, buscas e listagens que toleram alguns segundos de atraso.
- Depois de uma escrita, leia da principal na mesma requisição e nas seguintes do mesmo usuário por um breve período.
- A doc atual do PostgreSQL descreve `synchronous_commit = remote_apply` como forma de ter leitura consistente na réplica, ao custo de latência maior nas escritas. Pondere antes de ligar.

Provedores gerenciados oferecem réplica por um clique ([infra, doc 05](../../infra/docs/05-postgres-gerenciado.md)); montar a sua na VPS é trabalho de operação que só vale com equipe para isso.

### Quando o servidor único deixa de bastar

Sinais de que é hora de ir além da VPS única: o plano vertical mais caro ainda satura, a queda de uma máquina não é tolerável, ou o banco precisa de réplica e failover. Os caminhos estão em [migrar ou sair da VPS](../../vps/docs/08-migrar-ou-sair-da-vps.md) e [nuvem grande](../../infra/docs/03-nuvem-grande.md).

## Combina com / alternativas

- [Custo x desempenho](08-custo-x-desempenho.md) para pesar o preço de cada passo.
- [Docker e Kubernetes](../../infra/docs/04-docker-kubernetes.md) quando a quantidade de instâncias justificar orquestração.
- Alternativas ao escalonamento: CDN e cache para tirar carga da origem; otimização do que já existe.
- Particionamento e sharding do banco ficam fora deste guia; use a documentação oficial.

## Decisão rápida

- **Vertical** é o primeiro passo e costuma bastar para MVP.
- **Horizontal** exige app sem estado e conta de conexões do banco.
- **Réplica** só para leituras que aceitam atraso.
- **Evite:** escalar sem número que prove capacidade no limite.
