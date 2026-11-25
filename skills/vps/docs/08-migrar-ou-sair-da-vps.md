# Migrar de VPS ou sair para a nuvem grande

> Migre com TTL de DNS baixo, banco copiado ou replicado e a VPS antiga viva até o fim; saia da VPS quando carga, equipe ou contrato exigirem mais.

| | |
|---|---|
| **Referência** | https://www.postgresql.org/docs/current/logical-replication.html, https://www.postgresql.org/docs/current/app-pgdump.html, https://datatracker.ietf.org/doc/html/rfc1035 |
| **Categoria** | Servidor |
| **Tipo** | Prática de migração e decisão de arquitetura |
| **Vale para** | VPS com Docker, Postgres e domínio próprio |
| **Verificado em** | 2026-11-25 |

## O que é

Migrar é mover o sistema de uma VPS para outra (outro provedor, plano maior, datacenter mais perto) sem o usuário perceber. **Sair da VPS** é trocar o servidor único por nuvem grande, com banco gerenciado, várias máquinas e SLA.

Peças da migração:

- **TTL** (time to live): tempo que os resolvedores guardam a resposta do DNS. TTL baixo (por exemplo 300 segundos) faz a troca de IP se espalhar rápido.
- **Corte** (cutover): o momento em que o domínio passa a apontar para o servidor novo.
- **Janela de manutenção:** período curto combinado em que o sistema fica só leitura ou fora do ar enquanto o banco é copiado.
- **Replicação lógica:** o Postgres novo recebe as mudanças do antigo em tempo quase real, e o corte é rápido.

## Por que usar

- Trocar de provedor por preço, suporte ou latência sem derrubar o site.
- Aumentar o plano quando o servidor ficou pequeno.
- Sair da VPS no momento certo, e não no meio de uma crise.

## Quando usar

- Contrato, preço ou desempenho do provedor deixou de servir.
- Disco ou RAM chegaram no limite ([monitoramento](06-monitoramento-e-alertas.md)).
- Cliente exige SLA, região específica ou certificação.
- Precisa de alta disponibilidade e não aceita servidor único.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Migra em minutos; basta copiar arquivos e trocar o DNS |
| MVP de SaaS | ✅ Ótimo | Dump e janela de poucos minutos de madrugada resolvem |
| SaaS em crescimento | ✅ Ótimo | Replicação lógica e corte rápido; avalie banco gerenciado |
| Sistema interno/corporativo | ✅ Ótimo | Janela combinada com a área e plano de volta escrito |
| API/integração | 🟡 Serve | Clientes que fixam IP precisam ser avisados antes |
| App mobile com backend | 🟡 Serve | Apps antigos seguem usando o domínio; nunca mude o domínio da API |
| Migrar sem backup restaurado e sem plano de volta | ❌ Evite | Um erro vira perda de dados |

## Quando é bom

- **Corte reversível:** a VPS antiga fica ligada e o DNS volta se algo falhar.
- **DNS no Cloudflare ou provedor com TTL baixo:** troca rápida (veja [migrar DNS sem queda](../../domains/docs/07-migrar-dns-sem-queda.md)).
- **Banco replicado:** o corte leva segundos, sem perder escrita.
- **Teste prévio:** o servidor novo roda a cópia antes de receber tráfego.

## Quando é ruim

- **Janela com dump** deixa o sistema em manutenção durante a cópia; cresce com o tamanho do banco.
- **Replicação lógica** não copia esquema, sequences e alguns objetos automaticamente: exige cuidado e ensaio (conferir a documentação do Postgres da sua versão).
- **IP fixo em integrações** (webhooks, listas de permissão de clientes) quebra com a troca de IP.
- **Cache de DNS** de alguns provedores ignora o TTL; espere minutos extras.
- **Nuvem grande custa mais** e traz complexidade (rede, permissões, cobrança por uso). Não saia só por moda.

## Como começar

Plano de migração, em ordem:

1. Dois a três dias antes, baixe o TTL dos registros `app`, `api` e `staging` para 300 segundos.
2. Prepare o servidor novo com [primeiro acesso seguro](03-primeiro-acesso-seguro-ssh-e-firewall.md) e [Docker](04-atualizacoes-docker-e-swap.md).
3. Copie `.env`, volumes e `docker-compose.yml`; suba a aplicação apontando para um banco restaurado de teste.
4. Teste pelo arquivo `hosts` local, sem mexer no DNS.
5. Corte: ponha o sistema em modo manutenção, faça o dump final, restaure, troque o DNS.
6. Mantenha a VPS antiga ligada por 7 dias, sem escrita, e só então a desligue.
7. Suba o TTL de volta.

Dump e restauração na janela:

```bash
docker exec clinica-db pg_dump -U clinica -Fc clinica > final.dump
scp final.dump deploy@IP_NOVO:/tmp/
ssh deploy@IP_NOVO "docker exec -i clinica-db pg_restore -U clinica -d clinica --clean --if-exists < /tmp/final.dump"
```

Teste local sem DNS (Linux ou macOS), apontando o domínio para o IP novo apenas na sua máquina:

```bash
echo "IP_NOVO app.clinica-exemplo.com.br api.clinica-exemplo.com.br" | sudo tee -a /etc/hosts
curl -I https://api.clinica-exemplo.com.br/saude
```

Verifique a propagação depois do corte:

```bash
dig +short api.clinica-exemplo.com.br
```

Remova a linha do `hosts` ao terminar. O certificado do servidor novo precisa estar emitido antes do corte: com Cloudflare e certificado de origem, ou emita antes por desafio DNS.

**Quando sair da VPS para a nuvem grande**, sinais claros:

| Sinal | Ação |
|---|---|
| Banco disputa RAM com o app | Mova só o banco para [Postgres gerenciado](../../infra/docs/05-postgres-gerenciado.md) |
| Servidor único é risco inaceitável | Várias máquinas e balanceador |
| Contrato exige SLA, certificação ou região | [Nuvem grande](../../infra/docs/03-nuvem-grande.md) |
| Carga muda muito durante o dia | Escala automática |
| Equipe cresceu e precisa de permissões e auditoria | Contas e papéis da nuvem |

Mova o banco primeiro: costuma ser o ganho maior com o menor risco.

## Combina com / alternativas

- [Backup e restauração](05-backup-e-restauracao-na-vps.md): o dump restaurado em teste é o ensaio da migração.
- [Migrar DNS sem queda](../../domains/docs/07-migrar-dns-sem-queda.md) e [nuvem grande](../../infra/docs/03-nuvem-grande.md).
- [Deploy na VPS](07-deploy-na-vps.md): atualize o `SSH_HOST` e a chave depois do corte.
- Alternativas: PaaS gerenciado, sem migrar servidor; Cloudflare Tunnel para trocar o servidor sem mudar o IP público.

## Decisão rápida

- **Use se:** o provedor ou o tamanho da VPS deixou de atender, e há backup restaurado e plano de volta.
- **Evite se:** o motivo é só curiosidade por nuvem grande, ou não dá para ensaiar a restauração antes.
