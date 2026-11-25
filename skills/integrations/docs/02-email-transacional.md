# E-mail transacional

> Mande e-mails disparados por ação do usuário (confirmação, recuperação de senha, recibo) por um serviço próprio, com domínio autenticado, fila e tratamento de bounce.

| | |
|---|---|
| **Referência** | Documentação oficial de Resend, Postmark, Amazon SES, Brevo e Mailgun; "Email sender guidelines" do Google (support.google.com/a/answer/81126); documentação do React Email, MJML e Mailpit |
| **Categoria** | Integrações |
| **Tipo** | Prática de integração com serviço externo |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go |
| **Verificado em** | 2026-11-25 |

## O que é

E-mail **transacional** é enviado a uma pessoa só, por causa de uma ação dela: confirmar cadastro, recuperar senha, lembrar de uma consulta, enviar recibo. E-mail de **marketing** vai de uma vez para uma lista (novidades, promoções) e exige descadastro.

A Amazon SES usa a mesma divisão ao liberar a conta: um e-mail transacional é "um para um", disparado por ação como compra ou reset de senha. A Postmark mantém as duas categorias em infraestruturas separadas, para que o marketing não prejudique a entrega do transacional.

Para enviar, você usa um serviço (Resend, Postmark, SES...) por API ou SMTP. Mandar direto do seu servidor costuma cair em spam.

## Por que usar

- **Entrega:** o serviço cuida de reputação, filas do provedor de destino e reenvio.
- **Visibilidade:** você vê se foi entregue, devolvido (bounce) ou marcado como spam.
- **Menos operação:** sem servidor de e-mail para manter.

## Quando usar

- Todo sistema com cadastro, login por e-mail ou aviso ao usuário.
- Na clínica: confirmação de agendamento, lembrete 24h antes, recibo de pagamento ([01-pagamentos.md](01-pagamentos.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Formulário de contato e newsletter; marketing tem ferramenta própria |
| MVP de SaaS | ✅ Ótimo | Verificação de e-mail e recuperação de senha são obrigatórias |
| SaaS em crescimento | ✅ Ótimo | Volume, reputação e webhooks de bounce passam a importar |
| Sistema interno/corporativo | 🟡 Serve | Se a empresa tem servidor SMTP próprio, use-o por SMTP |
| API/integração | ✅ Ótimo | Notificação e alerta por e-mail |
| App mobile | 🟡 Serve | Push cobre avisos ([08-tempo-real-e-notificacoes.md](08-tempo-real-e-notificacoes.md)); e-mail fica para conta e recibo |
| Qualquer um, usando o Gmail pessoal ou SMTP de hospedagem compartilhada | ❌ Evite | Limite baixo, sem métricas, domínio sem reputação |

## Quando é bom

- **Domínio próprio:** `agenda@clinica.com.br`, nunca `@gmail.com`.
- **Autenticação do domínio:** o Google exige SPF, DKIM e DMARC de quem manda mais de 5.000 mensagens por dia ao Gmail. Faça desde o dia 1 mesmo com volume baixo.
- **Fila:** o envio roda em segundo plano, com retry ([05-filas-e-jobs.md](05-filas-e-jobs.md)).
- **Webhook de bounce e complaint:** o serviço avisa quando o endereço não existe ou o destinatário marcou spam.
- **Fluxos separados:** o remetente do transacional não é o do marketing.

## Quando é ruim

- **Enviar na requisição:** se o serviço demorar ou cair, o usuário fica esperando ou o cadastro falha.
- **Reenviar para endereço que devolveu:** destrói a reputação do domínio.
- **Marketing e transacional no mesmo domínio e remetente:** uma campanha ruim derruba o e-mail de senha.
- **Token de recuperação em log ou em fila sem cuidado:** quem lê o log vira dono da conta.
- **Depender do plano grátis em produção sem olhar os limites** (veja a tabela abaixo).

## Como começar

### Qual serviço

Limites mudam: confira a página oficial antes de decidir.

| Serviço | Plano grátis (conferido em 2026-11-25) | Observação |
|---|---|---|
| Resend | 3.000 e-mails por mês, 100 por dia, 3 domínios, 1 endpoint de webhook | Mesma equipe do React Email |
| Postmark | 100 e-mails por mês, sem excedente; plano Basic pago a partir de US$ 15 por mês com 10.000 e-mails | Separa transacional e broadcast |
| Amazon SES | Não há cota de e-mails grátis na página de preços; contas novas recebem até US$ 200 em créditos, com plano grátis por 6 meses e créditos usáveis em até 12 meses. Depois, US$ 0,16 por 1.000 e-mails no plano Essentials (até 10 milhões por mês) | Conta nova nasce em sandbox |
| Mailgun | 100 por dia, 1 domínio, logs por 1 dia | API e SMTP |
| Brevo | 300 e-mails por dia, segundo páginas do próprio Brevo; a página de preços não expôs o valor, então confirme lá | Envio liberado após aprovação da conta |

**Sandbox da SES:** conta nova só envia para endereços verificados, até 200 mensagens por 24 horas e 1 por segundo. É preciso pedir acesso de produção (resposta inicial em até 96 horas).

### DNS: SPF, DKIM e DMARC

- **SPF:** registro TXT dizendo quais servidores podem enviar pelo seu domínio.
- **DKIM:** assinatura criptográfica em cada e-mail, validada por uma chave pública no DNS.
- **DMARC:** diz ao destino o que fazer quando SPF e DKIM falham; o Google aceita a política `none` no começo.

O serviço mostra os registros exatos ao adicionar o domínio. Copie-os no seu DNS (por exemplo, Cloudflare), espere propagar e clique em verificar. Depois, o remetente (`From`) deve estar no mesmo domínio.

### Envio, com fila (Node, TypeScript)

```ts
import { Resend } from "resend";
import { render } from "@react-email/render";
import { ConfirmacaoAgendamento } from "./emails/confirmacao-agendamento";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function enviarConfirmacao(agendamentoId: string) {
  const ag = await db.agendamento.buscarComPaciente(agendamentoId);
  if (!ag.paciente.emailValido) return;

  const html = await render(ConfirmacaoAgendamento({ nome: ag.paciente.nome, quando: ag.inicio }));
  const { error } = await resend.emails.send(
    { from: "Clínica <agenda@clinica.com.br>", to: ag.paciente.email, subject: "Consulta confirmada", html },
    { idempotencyKey: `confirmacao-${ag.id}` },
  );
  if (error) throw new Error(error.message);
}
```

O `throw` faz a fila tentar de novo com espera crescente. No Resend a chave tem de 1 a 256 caracteres e é guardada por 24 horas; confira na documentação do SDK que a opção existe na sua versão. Na rota, só enfileire: `await fila.enfileirar("enviar-confirmacao", { agendamentoId })`.

### Bounce e complaint

- **Bounce:** o endereço não existe ou a caixa está cheia. Marque `emailValido = false` e pare de enviar.
- **Complaint:** o destinatário apertou "é spam". Pare de enviar mensagens opcionais para ele.

Cada serviço tem webhooks para esses eventos; cadastre uma rota, verifique a assinatura e trate como em [04-webhooks.md](04-webhooks.md). No Resend os eventos são `email.bounced` e `email.complained`; na Postmark há webhooks próprios de bounce e de spam complaint; na SES, os eventos `Bounce` e `Complaint` chegam por SNS (campo `eventType`, ou `notificationType` sem event publishing), e só os bounces `Permanent` pedem remover o endereço. Nos demais, confira os nomes na documentação. A SES exige um processo para tratar bounce e complaint já no pedido de produção.

### Templates

- **React Email:** componentes React que viram HTML compatível com clientes de e-mail. Combina com Node.
- **MJML:** linguagem de marcação que gera HTML responsivo; funciona em qualquer stack.
- **Nas outras stacks:** Blade/Mailables (Laravel), Razor (.NET), Thymeleaf (Java), Jinja2 (Python), `html/template` (Go).

Sempre inclua uma versão em texto puro e teste em vários clientes.

### Link de verificação e recuperação

O link leva um token aleatório, de uso único e com validade curta. Grave apenas o hash do token no banco. A regra completa está em [recuperação e 2FA](../../security/docs/03-recuperacao-e-2fa.md). A resposta de "esqueci a senha" deve ser igual exista ou não o e-mail, para não revelar quem tem conta.

### Desenvolvimento local

Não mande e-mail de verdade em dev. Use um servidor SMTP falso que captura tudo:

| Ferramenta | Estado (conferido em 2026-11-25) |
|---|---|
| Mailpit | Ativo: último push em 2026-11-23, versão v1.34.0 de 2026-11-17. SMTP na porta 1025, interface web na 8025, imagem Docker `axllent/mailpit` |
| MailHog | Parado: última versão v1.0.1 em 2020-08-11, último push em 2024-02-13. Prefira o Mailpit |

```yaml
services:
  mailpit:
    image: axllent/mailpit
    ports:
      - "1025:1025"
      - "8025:8025"
```

Aponte o SMTP do app para `localhost:1025` em dev e abra `http://localhost:8025` para ver as mensagens. Nos testes automáticos, mocke o cliente ([testes de API](../../quality/docs/04-testes-de-api-e-contrato.md)).

## Combina com / alternativas

- [05-filas-e-jobs.md](05-filas-e-jobs.md) e [04-webhooks.md](04-webhooks.md): envio assíncrono e eventos de bounce.
- [06-rotinas-agendadas.md](06-rotinas-agendadas.md): lembrete 24h antes da consulta.
- [03-whatsapp-e-sms.md](03-whatsapp-e-sms.md): quando o e-mail não é lido; [08-tempo-real-e-notificacoes.md](08-tempo-real-e-notificacoes.md): push.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).

## Decisão rápida

- **Use se:** o sistema avisa ou autentica pessoas por e-mail; comece com Resend ou Mailgun no plano grátis e avalie SES com volume.
- **Evite se:** é só campanha em massa (use ferramenta de marketing) ou se pretende enviar direto do seu servidor sem SPF, DKIM e DMARC.
