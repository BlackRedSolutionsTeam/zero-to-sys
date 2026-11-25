# Dimensionar o servidor

> Escolha CPU, RAM e disco pelo que o app, o banco e o painel de deploy realmente usam, e meça antes de pagar por um plano maior.

| | |
|---|---|
| **Referência** | https://coolify.io/docs/get-started/installation e https://docs.dokploy.com/docs/core/installation |
| **Categoria** | Servidor |
| **Tipo** | Prática de dimensionamento de VPS |
| **Vale para** | Node, .NET, Python, Postgres e painéis Coolify e Dokploy em servidor Linux próprio |
| **Verificado em** | 2026-11-25 |

## O que é

Dimensionar é decidir quantos **vCPUs** (núcleos virtuais de processador), quanta **RAM** (memória) e quanto **disco** o servidor precisa. Um servidor pequeno demais trava e mata processos por falta de memória. Um grande demais custa dinheiro à toa.

Os únicos números firmes são os mínimos oficiais dos painéis, conferidos em 2026-11-25:

| Painel | CPU | RAM | Disco |
|---|---|---|---|
| Coolify | 2 núcleos | 2 GB | 10 GB livres, mais espaço para imagens, volumes e backups |
| Dokploy | não informado | 2 GB | 30 GB |

A documentação do Coolify diz que 1 núcleo, 512 MB de RAM e 4 GB de disco funcionam, mas não são recomendados. A do Dokploy explica que 2 GB e 30 GB evitam travamentos durante builds do Docker.

## Por que usar

- **Evita queda por falta de memória:** quando a RAM acaba, o Linux encerra processos (o app ou o banco).
- **Evita pagar demais:** quase todo projeto começa bem num plano de entrada.
- **Prevê o custo:** você sabe quando precisará subir de plano.
- **Decide a hora de separar o banco** sem achismo.

## Quando usar

- Antes de contratar o primeiro servidor.
- Quando o app começar a ficar lento ou reiniciar sozinho.
- Antes de colocar um segundo projeto no mesmo servidor.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Plano de entrada com painel basta; o tráfego pesado vai para a CDN |
| MVP de SaaS | ✅ Ótimo | App, banco e painel juntos num servidor de 4 GB já funcionam |
| SaaS em crescimento | 🟡 Serve | Chega a hora de separar o banco e medir o uso |
| Sistema interno/corporativo | ✅ Ótimo | Poucos usuários simultâneos; o disco do banco é o que cresce |
| API/integração | 🟡 Serve | Depende do volume de chamadas e de filas em segundo plano |
| App mobile com backend | 🟡 Serve | Picos de uso exigem folga de CPU e RAM |
| Produção que não pode cair | ❌ Evite | Um servidor só é ponto único de falha, por maior que seja |

## Quando é bom

- **Regra prática de partida** (ponto de partida a validar com medição, não número oficial): some a RAM do painel, do banco e de cada app, e deixe folga para o sistema e para builds.
- **Medir antes de subir de plano:** `free -h`, `htop` e `df -h` mostram o uso real.
- **Disco separado do que cresce:** logs, imagens do Docker e banco são os que enchem.

## Quando é ruim

- **Build no mesmo servidor do app:** compilar uma imagem consome CPU e RAM e pode derrubar o app. Use CI (GitHub Actions) para gerar a imagem e só baixe pronta.
- **Plano só pelo preço:** 1 GB com painel instalado vira swap o tempo todo.
- **Banco disputando RAM com o app:** o Postgres usa memória para cache; se faltar, as consultas ficam lentas.
- **Linguagem sem limite de memória:** Node, .NET e Python podem consumir tudo se não houver limite no contêiner.

## Como começar

Veja o que o servidor tem hoje:

```bash
nproc
free -h
df -h
docker stats --no-stream
```

`nproc` mostra os vCPUs, `free -h` a RAM e a swap, `df -h` o disco e `docker stats` o uso de cada contêiner.

Passo a passo para decidir:

1. Instale o painel (Coolify ou Dokploy) e anote a RAM usada por ele em repouso.
2. Suba o app e o banco do clínica-exemplo.com.br (app em `app.`, API em `api.`) e rode um teste de carga leve.
3. Anote o pico de RAM e de CPU de cada contêiner com `docker stats`.
4. Escolha o plano com folga sobre o pico somado. Se a RAM de pico passa de cerca de 80% do total, suba de plano.
5. Defina limites no Compose para um serviço não engolir os outros:

```yaml
services:
  api:
    image: ghcr.io/clinica-exemplo/api:latest
    restart: unless-stopped
    mem_limit: 512m
    cpus: 1.0
```

6. Crie [swap](04-atualizacoes-docker-e-swap.md) como rede de segurança, não como substituto de RAM.

Quando separar o banco do app (sinais, não regras fixas):

- O Postgres e o app disputam RAM e você vê swap em uso constante.
- O banco passa a ser o dado mais valioso e precisa de backup e restauração próprios.
- Você precisa reiniciar ou atualizar o app sem tocar no banco.
- O volume do banco cresce além do disco do servidor de app.

Ao separar, use uma segunda VPS na mesma rede privada ou um Postgres gerenciado (veja [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md)). O painel só roda o app.

## Combina com / alternativas

- [VPS com Coolify ou Dokploy](../../infra/docs/02-vps-coolify-dokploy.md): o painel que define o mínimo.
- [Primeiro acesso seguro](03-primeiro-acesso-seguro-ssh-e-firewall.md): o passo seguinte, antes de instalar qualquer coisa.
- [Atualizações, Docker e swap](04-atualizacoes-docker-e-swap.md): como criar a swap.
- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md): obrigatório quando o banco mora no servidor.
- Alternativa: [PaaS](../../infra/docs/01-paas.md) se ninguém quer dimensionar servidor.

## Decisão rápida

- **Use se:** você mede o uso real, começa pelo mínimo oficial do painel com folga e separa o banco quando ele disputa recursos.
- **Evite se:** quer escolher o plano só pelo preço, compila imagens no mesmo servidor do app ou usa swap como se fosse RAM.
