# WhatsApp e SMS

> Para avisar o usuário por mensagem, use a API oficial do WhatsApp com template aprovado e opt-in registrado; SMS e e-mail entram como alternativas, e WhatsApp não oficial fica de fora.

| | |
|---|---|
| **Referência** | Documentação da WhatsApp Business Platform / Cloud API (developers.facebook.com/docs/whatsapp), página de preços da plataforma; documentação do WhatsApp da Twilio (twilio.com/docs/whatsapp/api); Zenvia (zenvia.com); Amazon SNS (aws.amazon.com/sns); LGPD, Lei 13.709/2018 |
| **Categoria** | Integrações |
| **Tipo** | Prática de integração de mensagens |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go; exemplos em TypeScript |
| **Verificado em** | 2026-11-24 |

## O que é

A **WhatsApp Business Platform** é a API oficial da Meta para empresas enviarem e receberem mensagens no WhatsApp. A **Cloud API** é a versão hospedada pela Meta: você chama um endpoint HTTP, sem servidor próprio do WhatsApp.

Dois tipos de mensagem, segundo a documentação de preços da Meta:

- **Template:** texto pré-aprovado, pode ser enviado a qualquer momento para iniciar contato. As categorias são marketing, utility (informativa/transacional) e authentication.
- **Sem template:** só como resposta, dentro da **janela de atendimento de 24 horas**. Ela abre quando o usuário manda mensagem e reinicia a cada nova mensagem dele.

Exemplo da clínica: lembrete de consulta na véspera é um template de utility ("Olá {{1}}, sua consulta com {{2}} é amanhã às {{3}}"). Se o paciente responder, a clínica pode conversar em texto livre por 24 horas.

## Por que usar

- **Canal que o paciente lê:** taxa de leitura maior que e-mail, na prática.
- **Reduz faltas:** lembrete e confirmação de consulta.
- **Oficial:** conta protegida contra banimento por automação.

## Quando usar

- Lembrete, confirmação e remarcação de agendamento.
- Aviso de status de pedido ou de cobrança.
- Atendimento em que o cliente já fala com você pelo WhatsApp.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Não há relação transacional com o visitante |
| MVP de SaaS | 🟡 Serve | Comece com e-mail; WhatsApp quando o público pedir |
| SaaS em crescimento | ✅ Ótimo | Reduz faltas e cobra por canal que o cliente usa |
| Sistema interno/corporativo | 🟡 Serve | Útil para avisos a clientes; para equipe, e-mail ou push |
| API/integração | ✅ Ótimo | Provedor expõe API simples; o cuidado é template e opt-in |
| App mobile | 🟡 Serve | Push costuma bastar; WhatsApp para quem não instalou o app |
| Qualquer um usando WhatsApp não oficial | ❌ Evite | Risco de banimento do número e quebra de termos |

## Quando é bom

- **Template aprovado e versionado:** o texto fica estável e auditável.
- **Opt-in registrado:** guardar quando e como o paciente aceitou. A Twilio documenta que a plataforma exige opt-in explícito e que enviar sem ele pode levar a bloqueios e à suspensão da conta.
- **Cobrança por mensagem entregue:** a Meta cobra pelas mensagens do negócio ao usuário, por categoria e país do destinatário; mensagens do usuário ao negócio e mensagens não entregues não são cobradas. Tabela de valores muda: consulte a página oficial de preços antes de calcular custo.
- **Janela gratuita de entrada:** respostas dentro de uma janela aberta por anúncio Click to WhatsApp não são cobradas (exceto Meta Business Agent), segundo a doc de preços.
- **Provedor intermediário quando simplifica:** Twilio (oferece a WhatsApp Business API pelas Messaging APIs, com taxa por mensagem mais as taxas da Meta) e Zenvia (se descreve como parceiro oficial/BSP do WhatsApp) são exemplos conferidos. Compare preço e suporte em português. Z-API, Gupshup e outros não foram conferidos aqui: valide se são oficiais antes de usar.

## Quando é ruim

- **WhatsApp não oficial** (bibliotecas que automatizam o WhatsApp Web): viola os termos e o número pode ser banido. Não use em produção.
- **Marketing sem consentimento:** denúncias derrubam a qualidade do número e podem suspender a conta.
- **Texto livre fora da janela de 24 horas:** a Meta só aceita template.
- **SMS como canal padrão:** costuma custar mais por mensagem que e-mail e tem pouco espaço de texto.
- **Mandar dado sensível no texto:** mensagem fica no celular e em backups; envie só o necessário e um link.

## Como começar

1. Crie conta Meta Business, registre o número (ou contrate um provedor).
2. Cadastre o template e espere a aprovação.
3. Guarde o consentimento (ver [LGPD na prática](../../security/docs/09-lgpd-na-pratica.md)).
4. Envie pela fila ([05](05-filas-e-jobs.md)), não dentro da requisição do usuário.

Tabela de consentimento:

```sql
create table contact_consent (
  id uuid primary key,
  patient_id uuid not null references patient(id),
  channel text not null,
  purpose text not null,
  granted_at timestamptz not null,
  revoked_at timestamptz,
  source text not null
);
```

Envio de lembrete (a Cloud API recebe `POST /<PHONE_NUMBER_ID>/messages` em `graph.facebook.com`, com `messaging_product: "whatsapp"`, `to`, `type: "template"` e o objeto `template`; confira o formato do objeto na referência da Messages API):

```typescript
async function sendReminder(patient: Patient, appointment: Appointment) {
  const consent = await consents.findActive(patient.id, "whatsapp", "reminder");
  if (!consent) return { skipped: "no_consent" };

  const response = await fetch(
    `https://graph.facebook.com/${process.env.WA_API_VERSION}/${process.env.WA_PHONE_NUMBER_ID}/messages`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.WA_TOKEN}`,
        "Content-Type": "application/json",
      },
      signal: AbortSignal.timeout(10_000),
      body: JSON.stringify(buildReminderPayload(patient, appointment)),
    },
  );

  if (!response.ok) throw new Error(`whatsapp_${response.status}`);
  return response.json();
}
```

Cada envio fica em log com o id da mensagem. O status (entregue, lido, falhou) chega por [webhook](04-webhooks.md).

Escolha do canal, em ordem de custo para o lembrete:

| Canal | Custo | Observação |
|---|---|---|
| E-mail ([02](02-email-transacional.md)) | Mais baixo | Tente primeiro; leitura menor |
| WhatsApp (template utility) | Por mensagem entregue | Melhor resultado; exige opt-in |
| SMS (Twilio, Zenvia, Amazon SNS) | Por mensagem, varia por país | Reserva para quem não usa WhatsApp; veja a tabela de cada provedor |

Em cada stack: o cliente é uma classe isolada com `fetch`/HTTP client e a fila decide o retry.

| Stack | Cliente HTTP |
|---|---|
| Node | `fetch` ou SDK do provedor |
| Python | `httpx` |
| .NET | `HttpClient` tipado |
| Java | `HttpClient` do JDK |
| Laravel | `Http::` facade |
| Go | `net/http` |

## Combina com / alternativas

- [Pagamentos](01-pagamentos.md), para aviso de cobrança.
- [E-mail transacional](02-email-transacional.md): alternativa mais barata.
- [Webhooks](04-webhooks.md): status de entrega e respostas chegam assim.
- [Filas e jobs](05-filas-e-jobs.md): envio assíncrono com retry.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md): não mandar o mesmo lembrete duas vezes.
- [LGPD na prática](../../security/docs/09-lgpd-na-pratica.md): base legal e revogação.

## Decisão rápida

- **Use se:** o usuário já usa WhatsApp e você tem opt-in; use template utility para lembretes.
- **Evite se:** não houver consentimento, ou se a ideia for automatizar um WhatsApp comum sem API oficial; nesse caso prefira e-mail.
