# Pós-lançamento: crash, avaliações e versão mínima forçada

> Depois de publicado, o trabalho é saber rápido quando o app quebra, responder às avaliações e conseguir tirar versões velhas de circulação.

| | |
|---|---|
| **Referência** | https://docs.expo.dev/eas-update/introduction/, https://developer.apple.com/help/app-store-connect/, https://support.google.com/googleplay/android-developer/ |
| **Categoria** | Operação |
| **Tipo** | Prática pós-lançamento |
| **Vale para** | Todo app já publicado |
| **Verificado em** | 2026-11-25 |

## O que é

- **Crash e erros:** relatório automático de falhas, com a versão e o aparelho. Opções: o painel de qualidade das lojas (App Store Connect e Play Console, com os dados de usuários que compartilham diagnósticos) ou uma ferramenta própria como Sentry ou Firebase Crashlytics.
- **Limites do Android vitals (Google):** a taxa de crash percebido pelo usuário de 1,09% dos usuários diários (todos os aparelhos) ou 8% em um único modelo, e a de ANR de 0,47% ou 8% por modelo, deixam o app menos descoberto na Play e podem exibir aviso na ficha (support.google.com/googleplay/android-developer/answer/9844486, lida em 2026-11-25). A Apple não publica um limite equivalente que eu tenha conferido.
- **Avaliações:** as duas lojas permitem responder publicamente a cada avaliação.
- **Versão mínima forçada:** o app consulta o seu back-end, que informa a menor versão aceita; se a instalada for menor, mostra uma tela que leva à loja. No Android, a alternativa nativa é a atualização imediata das in-app updates da Play (tela cheia que exige atualizar para continuar), disponível a partir do Android 5.0 e incompatível com apps que usam arquivos .obb (developer.android.com/guide/playcore/in-app-updates, lida em 2026-11-25); o iOS não tem equivalente, então a consulta ao back-end continua necessária.

## Por que usar

- Versões antigas deixam de funcionar quando a API muda; sem como forçar a atualização, você mantém dois mundos.
- Nota baixa derruba a posição na loja; resposta e correção rápida recuperam.

## Quando usar

- Ligue o monitor de crash antes do primeiro envio e a versão mínima desde a v1.0 (adicionar depois não alcança quem já instalou).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App com API própria | ✅ Ótimo | Versão mínima protege contra quebra de contrato |
| App sem back-end | 🟡 Serve | Crash e avaliações continuam valendo |
| Protótipo interno | ❌ Evite | Monitoramento pesado é exagero |

## Quando é bom

- **Correção de JavaScript chega por EAS Update** sem nova revisão (doc [07](07-atualizacao-sem-loja-eas-update-e-versionamento.md)).
- **Versão mínima por plataforma** deixa bloquear só o iOS ou só o Android.
- **Rollout em etapas** nas lojas limita o estrago de uma versão ruim.

## Quando é ruim

- **Crash nativo não se corrige por update de JavaScript:** exige build e revisão.
- **Bloquear sem aviso** irrita: avise antes e dê um período de transição quando possível.
- **Respostas genéricas** em avaliação pioram a imagem; responda com o problema e o que mudou.
- **Dados de crash têm dado pessoal:** declare na privacidade (doc [04](04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md)).

## Como começar

Endpoint do back-end:

```json
{
  "ios": { "versaoMinima": "1.4.0", "versaoAtual": "1.6.0" },
  "android": { "versaoMinima": "1.4.0", "versaoAtual": "1.6.0" }
}
```

Comparação no app (lógica escrita por nós, não é API oficial; o trecho não foi executado em um app real, só a comparação de versões é simples o bastante para conferir por leitura):

```tsx
import { Platform } from "react-native";
import Constants from "expo-constants";

function menorQue(a: string, b: string) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] ?? 0) !== (pb[i] ?? 0)) return (pa[i] ?? 0) < (pb[i] ?? 0);
  }
  return false;
}

export function precisaAtualizar(versaoMinima: string) {
  const instalada = Constants.expoConfig?.version ?? "0.0.0";
  return menorQue(instalada, versaoMinima);
}

export const lojaUrl =
  Platform.OS === "ios"
    ? "https://apps.apple.com/app/id1234567890"
    : "https://play.google.com/store/apps/details?id=com.suaempresa.meuapp";
```

Checklist da primeira semana: acompanhar crash por versão, responder as avaliações de 1 a 3 estrelas, conferir o painel de vitais da Play e, se houver erro grave, publicar correção por EAS Update ou novo build. Erros, alertas e observabilidade do back-end: skill `infra`, doc [10](../../infra/docs/10-observabilidade.md); incidentes: skill `operations`, doc [04](../../operations/docs/04-atender-um-incidente.md); suporte e avaliações: doc [07](../../operations/docs/07-suporte-ao-cliente.md).

## Combina com / alternativas

- Feature flags e rollback: skill `infra`, doc [14](../../infra/docs/14-feature-flags-e-rollback.md).
- Alternativas de crash: Sentry, Firebase Crashlytics.

## Decisão rápida

- **Use versão mínima forçada se:** a API muda de forma incompatível.
- **Use EAS Update se:** o crash é só de JavaScript.
- **Evite** publicar sem monitor de crash ligado.
