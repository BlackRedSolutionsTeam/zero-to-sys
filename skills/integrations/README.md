# integrations

Skill para o Claude Code que liga o sistema a serviços externos e a trabalho em segundo plano: pagamentos, e-mail, WhatsApp, webhooks, filas, rotinas agendadas, arquivos, tempo real e planilhas. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Pagamentos | Stripe, Mercado Pago, Asaas, AbacatePay, Pix | [docs/01-pagamentos.md](docs/01-pagamentos.md) |
| E-mail transacional | Entrega, domínio, bounce | [docs/02-email-transacional.md](docs/02-email-transacional.md) |
| WhatsApp e SMS | Mensagens ativas, templates, consentimento | [docs/03-whatsapp-e-sms.md](docs/03-whatsapp-e-sms.md) |
| Webhooks | Assinatura, idempotência, reprocessamento | [docs/04-webhooks.md](docs/04-webhooks.md) |
| Filas e jobs | Segundo plano com retry | [docs/05-filas-e-jobs.md](docs/05-filas-e-jobs.md) |
| Rotinas agendadas | Cron, fuso, não rodar duas vezes | [docs/06-rotinas-agendadas.md](docs/06-rotinas-agendadas.md) |
| Arquivos | Object storage e URL assinada | [docs/07-armazenamento-de-arquivos.md](docs/07-armazenamento-de-arquivos.md) |
| Tempo real e notificações | SSE, WebSocket, push | [docs/08-tempo-real-e-notificacoes.md](docs/08-tempo-real-e-notificacoes.md) |
| Planilhas | Importar e exportar sem travar | [docs/09-importar-e-exportar-planilhas.md](docs/09-importar-e-exportar-planilhas.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/integrations ~/.claude/skills/integrations
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/integrations`. Exemplos:

- "Integra o Asaas para cobrar com Pix e boleto."
- "Manda um lembrete por WhatsApp 24 horas antes da consulta."
- "/integrations o webhook do pagamento está chegando duplicado."

Com a skill carregada, o Claude:

1. levanta as integrações que o produto pede;
2. escolhe o serviço e confere preço e plano grátis na página oficial;
3. isola a integração num módulo e põe os eventos de fora em fila;
4. torna tudo idempotente e testa com sandbox;
5. confere o checklist de integração.

## Estrutura

```
integrations/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-pagamentos.md
    ├── 02-email-transacional.md
    ├── 03-whatsapp-e-sms.md
    ├── 04-webhooks.md
    ├── 05-filas-e-jobs.md
    ├── 06-rotinas-agendadas.md
    ├── 07-armazenamento-de-arquivos.md
    ├── 08-tempo-real-e-notificacoes.md
    └── 09-importar-e-exportar-planilhas.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Preços, planos e limites mudam com frequência e foram conferidos em 2026-11-24 quando citados. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
