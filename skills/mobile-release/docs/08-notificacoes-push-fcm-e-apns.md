# Notificações push (FCM e APNs)

> Push no celular passa pelo APNs da Apple e pelo FCM do Google; no Expo, o serviço de push da Expo fica na frente dos dois.

| | |
|---|---|
| **Referência** | https://docs.expo.dev/push-notifications/push-notifications-setup/, https://docs.expo.dev/app-signing/app-credentials/ |
| **Categoria** | Notificações |
| **Tipo** | Configuração de push |
| **Vale para** | Apps Expo (caminho principal); Flutter e nativo usam FCM e APNs direto |
| **Verificado em** | 2026-11-25 |

## O que é

- **APNs** (Apple Push Notification service) entrega no iOS; exige conta Apple paga e uma chave de push.
- **FCM** (Firebase Cloud Messaging) entrega no Android; o Expo usa a API v1 com credencial de conta de serviço.
- **Expo Push Token:** o app pede permissão, obtém o token e o seu back-end o usa para enviar pela API de push da Expo.

## Por que usar

- Reengaja o usuário sem ele abrir o app.
- O serviço da Expo esconde as diferenças entre APNs e FCM.

## Quando usar

- Avisos de pedido, mensagem, lembrete e alerta do sistema.
- Não use para conteúdo que o usuário não pediu: a Apple proíbe exigir a permissão para usar o app (5.1.2).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App de pedidos, agenda, chat | ✅ Ótimo | Notificação é parte do fluxo |
| App de produto com lembretes | ✅ Ótimo | Agendamento local ou push |
| App só de consulta | 🟡 Serve | Peça só se houver motivo |
| Tela web em PWA no iOS | 🟡 Serve | Só funciona com o site na Tela de Início (user-experience, doc [13](../../user-experience/docs/13-ios-android-web.md)) |

## Quando é bom

- **Passos do Expo:** `expo-notifications` e `expo-constants`, plugin no `app.json`, `getExpoPushTokenAsync` com o `projectId`, credencial FCM V1 e chave APNs criadas pelo EAS na criação do development build (docs.expo.dev, 2026-11-25).
- **Teste rápido:** a ferramenta de push em expo.dev/notifications.
- **Chave APNs** não expira (limite de 2 por conta) e trocá-la não altera os tokens.

## Quando é ruim

- **Precisa de aparelho real** ou emulador Android com Google Play services; o simulador iOS só serve em Xcode 14+, macOS 13+ e iOS 16+.
- **Development build obrigatório:** não funciona no Expo Go.
- **Revogar a chave APNs** interrompe o push até enviar outra.
- **Android 13 (API 33) ou mais** exige a permissão `POST_NOTIFICATIONS` em tempo de execução, melhor pedida no contexto de uso (user-experience, doc [13](../../user-experience/docs/13-ios-android-web.md)).
- **Pedir permissão no primeiro segundo** derruba a taxa de aceite e a revisão pode reprovar.

## Como começar

```bash
npx expo install expo-notifications expo-constants expo-device
```

```tsx
import * as Notifications from "expo-notifications";
import Constants from "expo-constants";
import * as Device from "expo-device";

export async function registrarPush() {
  if (!Device.isDevice) return null;
  const atual = await Notifications.getPermissionsAsync();
  const final =
    atual.status === "granted"
      ? atual
      : await Notifications.requestPermissionsAsync();
  if (final.status !== "granted") return null;
  const projectId = Constants.expoConfig?.extra?.eas?.projectId;
  const token = await Notifications.getExpoPushTokenAsync({ projectId });
  return token.data;
}
```

Enviar do back-end:

```bash
curl -X POST https://exp.host/--/api/v2/push/send \
  -H "Content-Type: application/json" \
  -d '{"to":"ExponentPushToken[xxxx]","title":"Pedido a caminho","body":"Chega em 10 minutos"}'
```

Passos: criar o projeto no Firebase e subir a chave de conta de serviço do FCM no EAS; deixar o EAS criar a chave APNs ao gerar o build (ou `eas credentials`); guardar o token por usuário e aparelho no seu banco e apagar os que a API devolver como inválidos. Fila, tempo real e regras de envio: skill `integrations`, doc [08](../../integrations/docs/08-tempo-real-e-notificacoes.md).

## Combina com / alternativas

- E-mail e WhatsApp: skill `integrations`, docs [02](../../integrations/docs/02-email-transacional.md) e [03](../../integrations/docs/03-whatsapp-e-sms.md).
- Alternativas: FCM e APNs direto (Flutter com `firebase_messaging`), OneSignal.

## Decisão rápida

- **Use o push da Expo se:** o app é Expo e o volume é de produto comum.
- **Use FCM e APNs direto se:** Flutter ou nativo, ou se precisa de controle total.
- **Evite** pedir permissão antes do usuário entender o benefício.
