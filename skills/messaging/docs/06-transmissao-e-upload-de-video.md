# Transmissão e upload de vídeo

> Para o usuário enviar um vídeo e outras pessoas assistirem, deixe uma plataforma de vídeo (Mux ou Cloudflare Stream) transcodificar e entregar; não sirva o arquivo bruto do seu servidor.

| | |
|---|---|
| **Referência** | https://www.mux.com/pricing, https://docs.mux.com, https://developers.cloudflare.com/stream/pricing/, https://developers.cloudflare.com/stream/ |
| **Categoria** | Mensageria |
| **Tipo** | Prática de vídeo sob demanda e ao vivo |
| **Vale para** | Web e mobile |
| **Verificado em** | 2026-11-25 |

## O que é

Vídeo cru de celular é grande e só toca bem em poucos aparelhos. A plataforma recebe o arquivo, **transcodifica** em várias qualidades, gera um formato de streaming adaptativo (HLS) e entrega por CDN, com um player. O espectador recebe a qualidade que a conexão aguenta.

Diferença para a [doc 05](./05-video-e-chamadas.md): lá todos falam; aqui poucos enviam e muitos assistem.

## Por que usar

- Reprodução sem travar em qualquer rede.
- Você não opera transcodificação nem CDN.
- Transmissão ao vivo e miniaturas prontas.

## Quando usar

- Cursos e aulas gravadas, vídeos de produto, depoimentos.
- Usuário envia vídeo (perfil, evidência, laudo).
- Transmissão ao vivo com muitos espectadores.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Um vídeo do YouTube embutido costuma bastar |
| MVP de SaaS | 🟡 Serve | Só se o vídeo é o produto |
| SaaS em crescimento | ✅ Ótimo | Cursos e treinamentos com controle de acesso |
| Sistema interno/corporativo | 🟡 Serve | Treinamento interno privado |
| API/integração | ❌ Evite | Sem vídeo |
| App mobile com backend | ✅ Ótimo | Upload do celular e reprodução adaptativa |

## Quando é bom

Preços conferidos nas páginas oficiais em 2026-11-25.

| Plataforma | Como cobra | Valores |
|---|---|---|
| Mux Video | Pague pelo uso, sem mensalidade nem cartão para começar, com US$ 20 de crédito de uso por mês | Vídeo sob demanda (1080p, básico): codificação grátis; armazenamento US$ 0,003 por minuto por mês; entrega US$ 0,001 por minuto, com 100 mil minutos de entrega grátis por mês. Ao vivo: US$ 0,03125 por minuto na entrada |
| Cloudflare Stream | Armazenamento pré-pago e entrega por uso | US$ 5 por mês a cada 1.000 minutos de capacidade; US$ 1 por 1.000 minutos entregues; entrada ao vivo e codificação sem custo; arquivos de até 30 GB |

Exemplo: 200 minutos de curso gravado e 500 mil minutos assistidos por mês. No Cloudflare Stream: armazenamento 200 min = US$ 5 e entrega 500 mil min = US$ 500. No Mux: armazenamento 200 × 0,003 = US$ 0,60; entrega (500 mil − 100 mil grátis) × 0,001 = US$ 400.

- **Upload direto:** o navegador envia o arquivo à plataforma por uma URL assinada, sem passar pelo seu servidor.
- **Proteção:** URLs assinadas e com prazo para vídeos pagos ou privados.
- **Mux** avisa por webhook quando o vídeo está pronto; **Stream** também.

## Quando é ruim

- **Servir MP4 do seu servidor ou bucket:** sem qualidade adaptativa e com banda cara.
- **Aceitar upload sem limite:** defina tamanho e duração máximos.
- **Esquecer o armazenamento:** no Mux ele acumula enquanto você não apaga; apague o que não usa.
- **Vídeo pago sem assinatura de URL:** o link vaza e circula.
- **Vídeo curto e raro:** o YouTube não listado ou o armazenamento comum resolve.

## Como começar

Upload direto no Mux: o backend cria a URL de envio.

```ts
import Mux from "@mux/mux-node";

const mux = new Mux();

export async function criarUpload() {
  const upload = await mux.video.uploads.create({
    cors_origin: process.env.APP_URL!,
    new_asset_settings: { playback_policy: ["signed"] },
  });
  return { id: upload.id, url: upload.url };
}
```

O navegador envia o arquivo para a `url`. Quando o vídeo termina o processamento, o Mux chama o seu webhook com `video.asset.ready`; guarde o `playback_id`.

```ts
export async function tratarWebhook(evento: { type: string; data: { id: string; playback_ids?: { id: string }[] } }) {
  if (evento.type !== "video.asset.ready") return;
  await db.video.update({
    where: { muxAssetId: evento.data.id },
    data: { playbackId: evento.data.playback_ids?.[0]?.id, status: "pronto" },
  });
}
```

Verifique a assinatura do webhook, como em [webhooks](../../integrations/docs/04-webhooks.md).

Regras do dia a dia:

- Estado do vídeo no banco: `enviando`, `processando`, `pronto`, `erro`.
- Player da própria plataforma (Mux Player, player do Stream) para ter qualidade adaptativa e legenda.
- Apague o vídeo na plataforma quando apagar no seu sistema.
- Monitore o custo mensal de entrega.
- Para arquivos que não são vídeo para streaming, veja [armazenamento de arquivos](../../integrations/docs/07-armazenamento-de-arquivos.md).

## Combina com / alternativas

- [05 Vídeo e chamadas](./05-video-e-chamadas.md): conversa em tempo real.
- [Webhooks](../../integrations/docs/04-webhooks.md) e [filas e jobs](../../integrations/docs/05-filas-e-jobs.md): receber o aviso de "pronto".
- Alternativas: YouTube não listado, Vimeo, ou transcodificar por conta própria com FFmpeg num worker (só com volume e time).

## Decisão rápida

- **Use se:** o vídeo faz parte do produto e muitas pessoas assistem.
- **Evite se:** um vídeo do YouTube embutido resolve.
