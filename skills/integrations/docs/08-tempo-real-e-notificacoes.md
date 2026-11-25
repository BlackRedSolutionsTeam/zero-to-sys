# Tempo real e notificações

> Escolha o canal mais simples que resolve (polling, SSE ou WebSocket), guarde as notificações no banco e deixe o usuário escolher por onde quer ser avisado.

| | |
|---|---|
| **Referência** | MDN (Server-sent events, WebSocket API, Push API, Service Worker API); RFC 6455 (WebSocket); RFC 8030 e RFC 8292 (Web Push e VAPID); documentação oficial de Pusher, Ably, Supabase Realtime, Liveblocks, Firebase Cloud Messaging e Expo Notifications; páginas de preço conferidas em 2026-11-24 |
| **Categoria** | Integrações |
| **Tipo** | Prática de comunicação em tempo real |
| **Vale para** | Node, Python, .NET, Java, Laravel, Go; navegador e app mobile |
| **Verificado em** | 2026-11-24 |

## O que é

Tempo real é o servidor avisar o cliente quando algo muda, sem o usuário recarregar a tela. Notificação é a mensagem em si, que pode aparecer dentro do app (in-app), no navegador ou no celular (push), por e-mail ou WhatsApp.

## Por que usar

- **Menos atrito:** a recepção vê o agendamento novo na hora.
- **Menos requisições:** evita consultar a API a cada segundo.
- **Retenção:** avisos certos trazem o usuário de volta.

## Quando usar

- Lista ou painel que muda sozinho (agenda do dia, fila de atendimento).
- Aviso de evento: "consulta confirmada", "paciente chegou", "exame pronto".
- Chat e edição colaborativa.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Raramente precisa; push só para quem pede boletim |
| MVP de SaaS | 🟡 Serve | Comece com polling ou SSE e notificação in-app |
| SaaS em crescimento | ✅ Ótimo | Painéis ao vivo e preferências por canal |
| Sistema interno/corporativo | ✅ Ótimo | Painel de fila e avisos de tarefa |
| API/integração | 🟡 Serve | Webhooks ([04](./04-webhooks.md)) cobrem o caso entre sistemas |
| App mobile | ✅ Ótimo | Push é o canal principal fora do app aberto |

## Quando é bom

| Técnica | Direção | Use quando |
|---|---|---|
| Polling (consultar a cada X s) | cliente pede | Mudança rara; 10 a 30 s bastam. O mais simples |
| SSE (Server-Sent Events) | servidor para cliente | Só o servidor empurra (avisos, painel). Reconecta sozinho, passa por proxies HTTP |
| WebSocket | dois sentidos | Chat, cursores, jogos: o cliente também envia com frequência |

- **Comece pelo mais simples:** SSE cobre a maioria dos avisos de um SaaS.
- **Serviço gerenciado** quando você não quer operar conexões abertas. Planos grátis (conferidos em 2026-11-24):

| Serviço | Plano grátis |
|---|---|
| Pusher Channels | 200 mil mensagens por dia e 100 conexões simultâneas |
| Ably | Até 500 usuários ativos por mês; limites de mensagens na política de uso justo |
| Supabase Realtime | 200 conexões simultâneas e 2 milhões de mensagens por mês |
| Liveblocks | 10 conexões por sala, 500 salas ativas por mês; exige a marca Liveblocks |

- **Push no navegador:** Web Push com VAPID (chave que identifica seu servidor) e um service worker (script que recebe o push com a aba fechada). No iOS, só funciona com o site instalado na tela inicial (web app), a partir do iOS e iPadOS 16.4.
- **Push no celular:** Firebase Cloud Messaging (FCM) para Android, web e iOS; o iOS entrega por APNs (serviço de push da Apple), e o FCM pode fazer a ponte. Com Expo, o Expo Push Service fala com FCM e APNs por você.
- **Notificação in-app** salva no banco: sobrevive a recarregar a página e ao usuário offline.

## Quando é ruim

- **WebSocket sem necessidade:** conexão aberta custa memória e complica o deploy.
- **Dado só no push:** push pode falhar ou ser desligado; o banco é a verdade.
- **Spam de avisos:** o usuário silencia tudo.
- **Dado sensível no texto do push:** o texto passa por terceiros (use "Você tem uma nova mensagem").
- **Serverless puro** com conexão longa: funções com tempo limite não seguram SSE ou WebSocket; use serviço gerenciado.

## Como começar

Tabela de notificações e preferências (exemplo: clínica):

```sql
create table notifications (
  id uuid primary key,
  user_id uuid not null references users(id),
  type text not null,
  title text not null,
  body text,
  link text,
  read_at timestamptz,
  created_at timestamptz not null default now()
);

create index notifications_unread_idx on notifications (user_id, created_at desc) where read_at is null;

create table notification_preferences (
  user_id uuid not null references users(id),
  type text not null,
  channel text not null,
  enabled boolean not null default true,
  primary key (user_id, type, channel)
);
```

O contador é `select count(*) from notifications where user_id = $1 and read_at is null`. Marcar como lida é um `update` de `read_at`.

SSE em Node (Express), enviando um aviso por usuário:

```ts
const clients = new Map<string, Set<import("express").Response>>();

app.get("/events", auth, (req, res) => {
  res.set({ "Content-Type": "text/event-stream", "Cache-Control": "no-cache", Connection: "keep-alive" });
  res.flushHeaders();
  const set = clients.get(req.user.id) ?? new Set();
  set.add(res);
  clients.set(req.user.id, set);
  req.on("close", () => set.delete(res));
});

export function pushToUser(userId: string, data: unknown) {
  for (const res of clients.get(userId) ?? []) res.write(`data: ${JSON.stringify(data)}\n\n`);
}
```

No navegador: `new EventSource("/events").onmessage = (e) => atualizarContador(JSON.parse(e.data))`.

Canal por tipo de aviso: ao criar o evento, consulte as preferências e dispare só pelos canais ligados.

| Tipo de aviso (clínica) | Canais sugeridos |
|---|---|
| Agendamento criado (recepção) | in-app, push |
| Lembrete de consulta (paciente) | WhatsApp ([03](./03-whatsapp-e-sms.md)), e-mail ([02](./02-email-transacional.md)) |
| Exame disponível | in-app, e-mail |

Cada envio sai como job ([05](./05-filas-e-jobs.md)), com idempotência por `(user, type, evento)`.

Escalar WebSocket ou SSE em várias instâncias: o usuário está conectado em uma instância, mas o evento nasce em outra. Duas saídas:

- **Pub/sub com Redis:** toda instância assina um canal; quem gera o evento publica; cada instância repassa aos seus clientes conectados.
- **Sticky sessions** (o balanceador manda o mesmo cliente à mesma instância): necessário para alguns clientes WebSocket com fallback; não substitui o pub/sub.

## Combina com / alternativas

- [E-mail transacional](./02-email-transacional.md) e [WhatsApp e SMS](./03-whatsapp-e-sms.md) como outros canais.
- [Filas e jobs](./05-filas-e-jobs.md) para enviar sem travar a requisição.
- [Webhooks](./04-webhooks.md) para avisar outros sistemas.
- [Transações e outbox](../../data/docs/09-transacoes-e-concorrencia.md): grave a notificação na mesma transação do fato.
- [Idempotência e retries](../../api/docs/06-idempotencia-e-retries.md).
- Alternativa simples: polling com `If-None-Match` (cache condicional).

## Decisão rápida

- **Use se:** o usuário precisa ver mudanças sem recarregar ou ser avisado fora do app.
- **Evite se:** a mudança é rara e o usuário já está olhando a tela; polling resolve.
