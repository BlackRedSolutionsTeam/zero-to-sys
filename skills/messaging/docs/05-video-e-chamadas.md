# Vídeo e chamadas

> Para chamadas de vídeo e áudio dentro do app, use uma plataforma WebRTC pronta (LiveKit, Daily ou Twilio) e calcule o custo por minuto de participante antes de decidir.

| | |
|---|---|
| **Referência** | https://livekit.com/pricing, https://docs.livekit.io/home/self-hosting/deployment/, https://www.daily.co/pricing/video-sdk/, https://www.twilio.com/en-us/video/pricing, MDN (WebRTC API) |
| **Categoria** | Mensageria |
| **Tipo** | Prática de comunicação em tempo real com mídia |
| **Vale para** | Web, iOS, Android, React Native e Flutter |
| **Verificado em** | 2026-11-25 |

## O que é

WebRTC é a tecnologia do navegador para áudio e vídeo em tempo real. Entre duas pessoas, a conexão pode ser direta (P2P). Com três ou mais, ou com gravação, é preciso um servidor de mídia: o **SFU** recebe o vídeo de cada pessoa e o repassa aos outros. Também há **TURN** para quem está atrás de firewall rígido.

Montar isso do zero leva meses. As plataformas entregam SFU, TURN, SDKs, gravação e componentes de tela prontos.

Cobrança comum: **minuto de participante** (cada pessoa conectada por minuto) e banda de saída.

## Por que usar

- Chamada funcionando em dias, não meses.
- SDKs para web e mobile.
- Gravação, transmissão ao vivo e transcrição como opção.

## Quando usar

- Teleconsulta, aula ao vivo, reunião dentro do sistema.
- Suporte com vídeo ou compartilhamento de tela.
- Agente de voz com IA na chamada (LiveKit tem suporte próprio).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Link para Google Meet ou Zoom resolve |
| MVP de SaaS | 🟡 Serve | Só se a chamada é o produto; senão, link externo |
| SaaS em crescimento | ✅ Ótimo | Teleconsulta, aula e reunião integradas |
| Sistema interno/corporativo | 🟡 Serve | Reunião externa costuma bastar |
| API/integração | ❌ Evite | Sem mídia |
| App mobile com backend | ✅ Ótimo | SDKs nativos e push de chamada |

## Quando é bom

Preços conferidos nas páginas oficiais em 2026-11-25; mudam, confirme antes de contratar.

| Plataforma | Plano grátis | Preço depois | Notas |
|---|---|---|---|
| LiveKit Cloud | Build: US$ 0, 5.000 minutos WebRTC, 50 GB de banda, 100 conexões simultâneas | Ship: US$ 50/mês com 150 mil minutos, US$ 0,0005 por minuto extra; Scale: US$ 500/mês com 1,5 milhão de minutos, US$ 0,0004 por minuto extra | Código aberto: dá para hospedar por conta própria |
| Daily | 10.000 minutos de participante por mês | US$ 0,004 por minuto de vídeo; US$ 0,00099 por minuto só de áudio | Gravação em nuvem US$ 0,01349 por minuto gravado; RTMP US$ 0,015 e HLS US$ 0,03 por minuto codificado |
| Twilio Video | Sem custo inicial | US$ 0,004 por minuto de participante; gravação US$ 0,004 por participante por minuto; composição US$ 0,01 por minuto | Página de preços de outubro de 2026 |

Exemplo de conta: uma teleconsulta de 30 minutos com 2 pessoas gasta 60 minutos de participante. Mil consultas por mês são 60 mil minutos: a US$ 0,004 daria US$ 240 (o Daily desconta os 10 mil grátis); no LiveKit Ship caberia nos 150 mil incluídos, por US$ 50.

- **LiveKit auto-hospedado:** exige domínio com TLS válido, portas 7880 (HTTPS e WebSocket), 7881 (RTC sobre TCP) e a faixa UDP de 50000 a 60000, Redis para produção, e TURN opcional. A documentação recomenda instâncias otimizadas para CPU com pelo menos 10 Gbps de rede e rede em modo host no Docker. Na VPS comum, a banda vira o limite ([vps](../../vps/SKILL.md)).
- **Link de reunião externo** (Google Meet, Zoom) custa zero de desenvolvimento.

## Quando é ruim

- **Chamada rara:** um link externo basta.
- **Auto-hospedar sem time de infra:** portas UDP, TURN e banda dão trabalho.
- **Custo ignorado:** sala com 20 pessoas por 1 hora são 1.200 minutos de participante.
- **Câmera aberta de quem só assiste:** espectador paga como participante; use transmissão ([06](./06-transmissao-e-upload-de-video.md)).
- **Gravação sem aviso:** exija consentimento (LGPD).
- **Navegador em rede corporativa fechada:** sem TURN a chamada não conecta.

## Como começar

Token de acesso no servidor (LiveKit, Node):

```ts
import { AccessToken } from "livekit-server-sdk";

export async function gerarToken(sala: string, usuarioId: string, nome: string) {
  const token = new AccessToken(process.env.LIVEKIT_API_KEY!, process.env.LIVEKIT_API_SECRET!, {
    identity: usuarioId,
    name: nome,
    ttl: "1h",
  });
  token.addGrant({ roomJoin: true, room: sala });
  return await token.toJwt();
}
```

Entrar na sala no navegador:

```ts
import { Room } from "livekit-client";

const room = new Room();
await room.connect(process.env.NEXT_PUBLIC_LIVEKIT_URL!, token);
await room.localParticipant.setCameraEnabled(true);
await room.localParticipant.setMicrophoneEnabled(true);
```

Regras do dia a dia:

- O token sai do seu backend, depois de checar se a pessoa pode entrar naquela sala; a chave secreta nunca vai ao navegador.
- Token de vida curta e uma sala por consulta ou aula.
- Peça permissão de câmera e microfone com uma tela explicando o porquê.
- Teste com rede lenta e no celular; adapte a qualidade ao sinal.
- Webhook da plataforma avisa quando a sala começa e termina ([webhooks](../../integrations/docs/04-webhooks.md)), útil para cobrar por minuto.
- Alerta de gasto no painel da plataforma.

## Combina com / alternativas

- [06 Transmissão e upload de vídeo](./06-transmissao-e-upload-de-video.md): para muita gente só assistindo.
- [Tempo real e notificações](../../integrations/docs/08-tempo-real-e-notificacoes.md): chat e avisos sem mídia.
- [Armazenamento de arquivos](../../integrations/docs/07-armazenamento-de-arquivos.md): onde ficam as gravações.
- Alternativas: Google Meet ou Zoom por link; Jitsi auto-hospedado.

## Decisão rápida

- **Use se:** a chamada é parte do produto e você quer lançá-la rápido.
- **Evite se:** um link de reunião externo atende ou o volume de minutos ainda não foi calculado.
