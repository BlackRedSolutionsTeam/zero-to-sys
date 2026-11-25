# Página de status e comunicação com o cliente

> Um endereço público onde o cliente vê se o sistema está bem, e um jeito padronizado de avisar quando não está.

| | |
|---|---|
| **Referência** | https://www.atlassian.com/software/statuspage/pricing, https://instatus.com/pricing, https://betterstack.com/pricing, https://github.com/louislam/uptime-kuma |
| **Categoria** | Operação |
| **Tipo** | Prática de comunicação, com ferramentas de página de status |
| **Vale para** | SaaS e sistemas com cliente externo |
| **Verificado em** | 2026-11-25 |

## O que é

**Página de status** é um site simples e independente do seu sistema (outro domínio e outro servidor) que mostra o estado atual e o histórico de incidentes. O cliente consulta nela em vez de abrir chamado, o que alivia o suporte na hora de maior pressão.

## Por que usar

- Reduz chamados repetidos durante o incidente.
- Mostra transparência e dá base ao SLA.
- Permite assinatura por e-mail ou webhook.

## Quando usar

- Quando houver cliente pagante.
- Quando o suporte começar a receber o mesmo pedido várias vezes numa queda.
- Quando o contrato citar disponibilidade.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | O monitor basta |
| MVP de SaaS | ✅ Ótimo | Plano grátis ou Uptime Kuma |
| SaaS em crescimento | ✅ Ótimo | Domínio próprio e assinantes |
| Sistema interno | 🟡 Serve | Mensagem no canal da empresa basta |
| API de integração | ✅ Ótimo | Desenvolvedores clientes assinam |
| Página de status no mesmo servidor | ❌ Evite | Cai junto com o sistema |

## Quando é bom

- **Independente:** outro provedor ou outra máquina.
- **Atualizada por quem resolve** em dois cliques.
- **Honesta:** inclui quedas pequenas.

## Quando é ruim

- **Sem atualização** perde a credibilidade.
- **Verde falso:** monitor que só testa a home não vê o login quebrado.
- **Domínio abaixo do sistema** (`app.../status`) cai junto.
- **Plano grátis com poucos assinantes** e sem domínio próprio.

## Como começar

Comparação (preços e limites conferidos em 2026-11-25 nas páginas oficiais, em dólar):

| Opção | Grátis | Pago | Observação |
|---|---|---|---|
| Uptime Kuma | Sim, licença MIT, várias páginas de status e domínio próprio | Servidor próprio | Rode em outra máquina que não a do sistema |
| Atlassian Statuspage | Plano Free: 100 assinantes, 2 membros | Hobby US$ 29/mês (250 assinantes), Startup US$ 99/mês (1.000) | Padrão do mercado |
| Instatus | Starter: 15 monitores, 200 assinantes, e-mail | Pro a partir de US$ 20/mês, 5 mil assinantes e domínio próprio | Mais barato que o Statuspage |
| Better Stack | 1 página de status e 10 monitores | Página extra US$ 12/mês no anual | Junta monitor, plantão e página |

Uptime Kuma como página de status (ver a execução em [monitoramento da VPS](../../vps/docs/06-monitoramento-e-alertas.md)): crie a página, escolha os monitores e aponte `status.clinica-exemplo.com.br` por CNAME (skills `domains` e `cloudflare`). Um monitor "Fluxo de agendamento" que testa o caminho real vale mais que 10 monitores de porta.

### Modelo de mensagens de status

Em investigação:

```text
[Investigando] Problemas no agendamento
Estamos investigando falhas ao confirmar consultas desde 14:05. Outras áreas funcionam normalmente. Nova atualização até 14:35.
```

Identificado:

```text
[Identificado] Problemas no agendamento
Encontramos a causa: uma atualização das 14:03. Estamos desfazendo a mudança. Previsão de normalização até 14:50. Nova atualização até 14:35.
```

Monitorando:

```text
[Monitorando] Problemas no agendamento
A correção foi aplicada às 14:42 e o agendamento voltou. Seguimos acompanhando por 30 minutos.
```

Resolvido:

```text
[Resolvido] Problemas no agendamento
O agendamento voltou ao normal às 14:42. Entre 14:05 e 14:42, parte das confirmações falhou; nenhuma consulta foi perdida. Pedimos desculpas. Publicaremos em até 5 dias úteis o que aconteceu e o que vamos mudar.
```

E-mail para cliente direto (SEV1 ou contrato):

```text
Assunto: [clinica-exemplo] Instabilidade em 25/11 e o que fizemos

Olá, NOME.

Entre 14:05 e 14:42 de hoje, o agendamento ficou instável. Parte das confirmações falhou. Seus dados não foram perdidos.

A causa foi uma atualização nossa, já desfeita. Estamos revisando como evitar que se repita e enviaremos o resumo até 02/12.

Se você teve algum agendamento afetado, responda este e-mail com o nome do paciente e o horário que corrigimos hoje.

Equipe clinica-exemplo
```

Regras de redação: diga o impacto no que o usuário faz, não o termo técnico; dê o horário; só prometa o que controla; não culpe terceiros nem pessoas; avise de novo no horário que combinou, mesmo sem novidade.

## Combina com / alternativas

- [Atender um incidente](04-atender-um-incidente.md): a primeira mensagem sai em até 15 ou 30 minutos.
- [Suporte ao cliente](07-suporte-ao-cliente.md): ligue a página ao canal de chamados.
- Domínio e DNS: skills `domains` e `cloudflare`.

## Decisão rápida

- **Use se:** o cliente paga e pode ficar sem acesso: Uptime Kuma em outra máquina ou plano grátis do Instatus/Statuspage.
- **Evite se:** a página roda no mesmo servidor do sistema ou ninguém vai atualizá-la.
