# Runbooks: modelo e os primeiros a escrever

> Um passo a passo curto, escrito antes do problema, que qualquer pessoa do time consegue seguir de madrugada.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/incident-response/ |
| **Categoria** | Operação |
| **Tipo** | Prática de documentação operacional, com modelo |
| **Vale para** | Qualquer sistema; os exemplos assumem VPS com Docker e Postgres |
| **Verificado em** | 2026-11-25 |

## O que é

Runbook é uma página com o que fazer quando um alerta específico dispara: como confirmar, como conter, como resolver, como saber que voltou. Escreva com comandos prontos e sem teoria. Quem lê está com pressa e sono.

## Por que usar

- Quem não escreveu o sistema consegue operar.
- Resposta mais rápida e com menos erro.
- Cada [incidente](04-atender-um-incidente.md) melhora o runbook.

## Quando usar

- Para cada alerta que [acorda alguém](02-alertas-que-valem-acordar.md).
- Depois de um incidente que foi resolvido "de cabeça".
- Antes de sair de férias, para o reserva.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um runbook de "site fora" e restauração |
| MVP de SaaS | ✅ Ótimo | Os 4 primeiros cobrem a maioria das quedas |
| SaaS em crescimento | ✅ Ótimo | Um por alerta, revisado após incidente |
| Sistema interno | 🟡 Serve | Um arquivo único basta |
| Time de uma pessoa | ✅ Ótimo | Você de madrugada é outra pessoa |
| Runbook com 30 páginas de teoria | ❌ Evite | Ninguém lê durante o incidente |

## Quando é bom

- **Curto:** cabe numa tela, com comandos para copiar.
- **No repositório**, em `docs/runbooks/`, revisado como código.
- **Testado:** alguém que não escreveu o segue num ensaio.
- **Com data de validação** no topo.

## Quando é ruim

- **Comando destrutivo sem aviso** (apagar volume, `docker system prune -a`); marque em destaque.
- **Dados que mudam** (IPs, senhas) dentro do texto; aponte para o cofre.
- **Runbook desatualizado** é pior que nenhum.
- **Substitui o julgamento:** se o passo não funciona, escale.

## Como começar

Modelo de runbook (copie para `docs/runbooks/NOME.md`):

```markdown
# Runbook: NOME DO PROBLEMA

Validado em: AAAA-MM-DD por NOME
Alerta que chama este runbook: NOME DO ALERTA
Severidade provável: SEV2

## Sintoma
O que o usuário ou o monitor vê.

## Confirmar (2 min)
1. Comando ou link para confirmar que é real.
2. O que olhar para descartar falso positivo.

## Conter (reduzir o dano agora)
1. Ação rápida e reversível.

## Resolver
1. Passo com comando.
2. Passo com comando.

## Verificar que voltou
- Monitor externo verde.
- Métrica que deve normalizar.

## Escalar
Se não resolveu em 20 min: chamar NOME (telefone no cofre).

## Depois
Registrar horário e causa; abrir postmortem se SEV1 ou SEV2.
```

### 1. App fora do ar

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://app.clinica-exemplo.com.br
docker ps --format "table {{.Names}}\t{{.Status}}"
docker logs --tail 100 app
df -h /
free -h
```

Contêiner parado: `docker compose up -d app`. Último deploy suspeito: volte a versão ([rollback](../../infra/docs/14-feature-flags-e-rollback.md)). Domínio não responde com o servidor de pé: veja o DNS e a borda (skill `cloudflare`) e o proxy (skill `nginx`, diagnóstico).

### 2. Banco cheio (disco)

```bash
df -h /
docker system df
du -xh /var/lib/docker --max-depth=1 | sort -h | tail
journalctl --disk-usage
```

Libere o que é seguro e reversível: logs antigos e imagens sem uso (`docker image prune`). Nunca apague arquivos de dados do Postgres nem `pg_wal` à mão. Se o volume estiver no limite, aumente o disco no provedor e depois o sistema de arquivos. Rotação de logs do Docker: [atualizações, Docker e swap](../../vps/docs/04-atualizacoes-docker-e-swap.md). Dado perdido: [restauração](../../vps/docs/05-backup-e-restauracao-na-vps.md).

### 3. Certificado vencido

```bash
echo | openssl s_client -connect app.clinica-exemplo.com.br:443 -servername app.clinica-exemplo.com.br 2>/dev/null | openssl x509 -noout -dates
```

Com proxy do Coolify, Dokploy ou Caddy, veja o log da renovação (porta 80 aberta e DNS correto são as causas comuns de falha). Com certbot: `sudo certbot renew --dry-run` e depois `sudo certbot renew`. Atrás da Cloudflare, confira o modo SSL e o certificado de origem (skill `cloudflare`). Emissão e renovação em detalhe: skill `nginx` e skill `domains`.

### 4. Fila parada

```bash
docker logs --tail 200 worker
docker restart worker
```

Antes de reiniciar, anote o tamanho da fila e se há tarefa que trava (mensagem venenosa). Tarefa que falha sempre vai para uma fila de mortos, não fica em laço. Reinicie, acompanhe o consumo por 5 minutos e confirme que os itens atrasados foram processados sem duplicar efeito (e-mail, cobrança): tarefas precisam ser idempotentes.

## Combina com / alternativas

- [Alertas que valem acordar](02-alertas-que-valem-acordar.md): cada alerta aponta para um runbook.
- [Atender um incidente](04-atender-um-incidente.md) e [postmortem](06-postmortem-sem-culpa.md): atualize o runbook depois.
- [Backup e recuperação](../../infra/docs/11-backup-e-recuperacao.md) e [feature flags e rollback](../../infra/docs/14-feature-flags-e-rollback.md).

## Decisão rápida

- **Use se:** existe um alerta que acorda alguém; escreva o runbook dele.
- **Evite se:** o objetivo é documentar tudo "para o caso de"; escreva só o que já quebrou ou vai quebrar.
