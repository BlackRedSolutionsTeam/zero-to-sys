# Postmortem sem culpa: modelo

> Depois do incidente, escreva o que aconteceu, por quê e o que muda, sem apontar culpado.

| | |
|---|---|
| **Referência** | https://sre.google/sre-book/postmortem-culture/, https://www.pagerduty.com/pricing/incident-management/ |
| **Categoria** | Operação |
| **Tipo** | Prática de aprendizado, com modelo |
| **Vale para** | Qualquer time que tenha tido um incidente relevante |
| **Verificado em** | 2026-11-25 |

## O que é

Postmortem é o relatório curto de um incidente: impacto, linha do tempo, causas, o que funcionou, o que faltou e ações com dono e prazo. "Sem culpa" quer dizer que se assume que todos agiram bem com a informação que tinham; o alvo é o sistema e o processo. Segundo o livro de SRE do Google, culpar leva a esconder incidentes.

## Por que usar

- O erro de hoje vira melhoria permanente.
- O time perde o medo de reportar.
- Serve de prova para o cliente de que o problema foi tratado.

## Quando usar

Defina os gatilhos antes (a mesma fonte lista alguns):

- Qualquer SEV1 ou SEV2.
- Perda de dado.
- Queda acima do limite combinado (por exemplo, 30 minutos).
- Quando precisou de rollback ou ação manual urgente.
- Quando o problema foi descoberto pelo cliente, não pelo monitor.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Meia página, só se houve perda |
| MVP de SaaS | ✅ Ótimo | Poucos incidentes, muito aprendizado |
| SaaS em crescimento | ✅ Ótimo | Padrões aparecem na [revisão mensal](08-revisao-operacional-mensal.md) |
| Sistema interno | 🟡 Serve | Versão curta no wiki |
| Contrato com SLA | ✅ Ótimo | O cliente pode pedir o relatório |
| Postmortem para achar culpado | ❌ Evite | Mata a honestidade |

## Quando é bom

- **Em até 5 dias úteis**, com a memória fresca.
- **Ações pequenas e verificáveis**, com dono e data.
- **Compartilhado** no time e, resumido, com o cliente.

## Quando é ruim

- **Causa única "erro humano":** pergunte por que o sistema deixou o erro chegar à produção.
- **Lista de 20 ações** que ninguém faz; escolha até 5.
- **Sem acompanhamento:** ação sem dono é desejo.
- **Dados sensíveis** de usuário no texto; mascare.

## Como começar

Modelo (copie para `docs/postmortems/AAAA-MM-DD-titulo.md`):

```markdown
# Postmortem: TÍTULO CURTO

Data do incidente: AAAA-MM-DD
Severidade: SEV_
Autores: NOMES
Status: rascunho | revisado | ações em andamento | encerrado

## Resumo
Duas frases: o que quebrou, quem foi afetado e por quanto tempo.

## Impacto
- Duração: de HH:MM a HH:MM (X min).
- Usuários ou clientes afetados: N ou %.
- Dados perdidos ou incorretos: sim/não, quais.
- Consumo do orçamento de erro do mês: X%.

## Linha do tempo (horário local)
| Hora | Evento |
|---|---|
| 14:03 | Deploy da versão 1.42 |
| 14:05 | Primeiras falhas |
| 14:11 | Alerta disparou |
| 14:20 | Incidente declarado, canal aberto |
| 14:42 | Rollback concluído, serviço normal |

## Causas
- Causa imediata:
- Causas contribuintes (processo, teste, alerta, documentação):
- Por quê? (repita 5 vezes até chegar a algo que o time controla)

## O que funcionou
-

## O que não funcionou
-

## Onde tivemos sorte
-

## Ações
| Ação | Tipo (prevenir, detectar, mitigar) | Dono | Prazo | Link |
|---|---|---|---|---|
| Alerta de erro 5xx por rota | detectar | NOME | AAAA-MM-DD | |

## Lições e pontos para o runbook
-
```

Reunião de revisão: 30 a 45 minutos, lendo a linha do tempo em voz alta. Regras: sem "fulano errou"; use "o deploy foi feito sem teste de X"; pergunte "o que tornou o erro fácil?". Para o cliente, mande um resumo de 5 linhas (impacto, causa, o que muda, prazo).

## Combina com / alternativas

- [Atender um incidente](04-atender-um-incidente.md): a linha do tempo vem do canal do incidente.
- [Revisão operacional mensal](08-revisao-operacional-mensal.md): confere se as ações foram feitas.
- O PagerDuty Professional inclui revisão pós-incidente (plano Free não); em outros casos o documento no Git basta.

## Decisão rápida

- **Use se:** houve SEV1 ou SEV2: escreva em até 5 dias úteis, com até 5 ações com dono.
- **Evite se:** a intenção é descobrir quem errou; troque a pergunta para "o que facilitou o erro".
