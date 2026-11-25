# Atender um incidente: detectar, conter, comunicar, resolver

> Um roteiro fixo para o pior momento, em que decidir o que fazer primeiro custa mais que fazer.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/managing-incidents/, https://sre.google/sre-book/incident-response/ |
| **Categoria** | Operação |
| **Tipo** | Prática de resposta a incidente |
| **Vale para** | Qualquer sistema em produção, de uma pessoa a um time de plantão |
| **Verificado em** | 2026-11-25 |

## O que é

Incidente é qualquer evento que degrada o serviço para o usuário. A resposta tem quatro fases: **detectar** (saber), **conter** (parar o dano), **comunicar** (avisar quem precisa) e **resolver** (corrigir a causa). A ordem importa: contenha primeiro, investigue depois. Voltar a versão anterior vale mais que descobrir o porquê com o cliente parado.

## Por que usar

- Reduz o tempo de queda ao tirar a decisão do improviso.
- Evita dois fazendo a mesma coisa e ninguém avisando o cliente.
- Gera o registro que alimenta o [postmortem](06-postmortem-sem-culpa.md).

## Quando usar

- Em todo SEV1 e SEV2 ([definições](01-slo-severidade-e-plantao.md)).
- SEV3 e SEV4 seguem o [suporte](07-suporte-ao-cliente.md), sem cerimônia.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um item de lista basta |
| MVP de SaaS | ✅ Ótimo | Uma pessoa acumula os papéis, mas segue o roteiro |
| SaaS em crescimento | ✅ Ótimo | Separe quem conserta de quem comunica |
| Sistema interno | 🟡 Serve | Avisar o gestor e resolver |
| Sistema com dado sensível | ✅ Ótimo | Vazamento tem prazo legal de comunicação (skill `security`) |
| Investigar a causa com o sistema fora | ❌ Evite | Contenha antes |

## Quando é bom

- **Papéis claros:** comandante (decide e coordena), quem conserta, quem comunica. Em time pequeno uma pessoa acumula, mas nomeie quem comunica.
- **Linha do tempo anotada** durante, não de memória depois.
- **Contenção reversível primeiro:** rollback, flag desligada, escalar recursos.

## Quando é ruim

- **Herói solitário:** peça ajuda em 20 a 30 minutos sem progresso.
- **Mudanças em cascata:** cada correção sem registro vira nova incógnita.
- **Silêncio:** o cliente descobre sozinho e a confiança cai mais que pela queda.
- **Culpar no meio do incidente:** fica para o postmortem, e lá sem culpa.

## Como começar

Roteiro (copie para um canal de mensagens do incidente):

```text
1. DETECTAR
   - Confirme com uma segunda fonte (monitor externo, teste manual).
   - Defina a severidade e abra o canal #inc-AAAA-MM-DD.
   - Anote o horário de início (quando o usuário começou a sentir, não quando você viu).

2. DESIGNAR
   - Comandante: NOME. Quem conserta: NOME. Quem comunica: NOME.

3. CONTER
   - Houve deploy ou mudança nas últimas 2 horas? Volte.
   - Desligue a flag da funcionalidade suspeita.
   - Escale recurso ou reinicie só se for reversível.
   - Anote cada ação com horário.

4. COMUNICAR
   - Primeira mensagem de status em até 15 min (SEV1) ou 30 min (SEV2).
   - Atualização a cada 30 min, mesmo sem novidade.

5. RESOLVER
   - Siga o runbook; se não houver, escreva um depois.
   - Verifique: monitor externo verde e teste manual do fluxo principal.

6. ENCERRAR
   - Mensagem final de resolvido.
   - Agende o postmortem em até 5 dias úteis.
```

Perguntas rápidas de diagnóstico, nesta ordem:

| Pergunta | Onde olhar |
|---|---|
| Mudou algo? | Último deploy, migração, configuração, DNS, certificado |
| Está só em um lugar? | Região, rede, uma versão do app |
| Falta recurso? | Disco, memória, conexões do banco, limites de API de terceiros |
| É dependência externa? | Página de status do provedor |
| Voltar resolve? | Rollback ([feature flags e rollback](../../infra/docs/14-feature-flags-e-rollback.md)) |

Comandos de primeira resposta em VPS:

```bash
uptime
df -h /
free -h
docker ps --format "table {{.Names}}\t{{.Status}}"
docker logs --since 30m --tail 200 app
```

Diagnóstico do proxy e da borda: skills `nginx` e `cloudflare`.

## Combina com / alternativas

- [Runbooks](03-runbooks-modelo-e-primeiros.md) para os passos de cada problema.
- [Página de status e comunicação](05-pagina-de-status-e-comunicacao.md) para as mensagens.
- [Postmortem](06-postmortem-sem-culpa.md) ao encerrar.
- Dado vazado ou conta invadida: skill `security`.

## Decisão rápida

- **Use se:** é SEV1 ou SEV2: confirme, designe, contenha, comunique de 30 em 30 minutos, resolva e registre.
- **Evite se:** a tentação é caçar a causa raiz com o serviço fora; volte a versão antes.
