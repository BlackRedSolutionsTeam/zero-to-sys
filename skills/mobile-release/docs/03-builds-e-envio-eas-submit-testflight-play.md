# Builds e envio: EAS Submit, TestFlight e Play

> Gere o build de produção com `eas build`, envie com `eas submit` e teste em TestFlight e na trilha interna antes de pedir revisão.

| | |
|---|---|
| **Referência** | https://docs.expo.dev/build/eas-json/, https://docs.expo.dev/submit/introduction/, https://docs.expo.dev/submit/android/, https://docs.expo.dev/submit/ios/, https://developer.apple.com/help/app-store-connect/test-a-beta-version/testflight-overview |
| **Categoria** | Build e distribuição |
| **Tipo** | Fluxo de publicação |
| **Vale para** | Expo (EAS); Flutter e nativo usam o mesmo caminho das lojas com ferramentas próprias |
| **Verificado em** | 2026-11-25 |

## O que é

- **EAS Build** compila na nuvem da Expo. O perfil `production` gera `.aab` no Android (a Play não aceita `.apk`) e `.ipa` no iOS.
- **EAS Submit** envia o binário às lojas. No iOS ele cai no TestFlight depois do processamento (10 a 15 minutos) e não vai à App Store sozinho; no Android a primeira submissão cria o release na trilha de teste interno.
- **TestFlight:** até 100 testadores internos e até 10.000 externos; cada build vale 90 dias. O primeiro build para testadores externos passa por revisão da Apple.
- **Play:** trilhas interna, fechada e aberta antes da produção. A interna não tem requisito; a fechada exige a ficha de configuração do app concluída.

Preços do EAS conferidos em 2026-11-25 (expo.dev/pricing): Free com 15 builds Android e 15 iOS por mês em fila de baixa prioridade, que pode passar de 90 minutos no pico; Starter US$ 19 mais uso; Production US$ 199 mais uso.

## Por que usar

- Um comando por etapa, o mesmo no seu computador e no CI.
- Perfis separam build de teste (`preview`, instalável direto no aparelho) do de loja (`production`).

## Quando usar

- Todo lançamento e toda atualização que muda código nativo (doc [07](07-atualizacao-sem-loja-eas-update-e-versionamento.md)).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App Expo | ✅ Ótimo | Fluxo oficial, sem Xcode nem Android Studio |
| App Flutter ou nativo | 🟡 Serve | Mesmas trilhas das lojas; build e envio por Fastlane ou CI |
| MVP com poucos lançamentos | ✅ Ótimo | Plano Free cobre os 15 builds por plataforma |
| Time com muitos lançamentos por semana | 🟡 Serve | Fila de baixa prioridade atrasa; considere plano pago ou build local (`--local`) |

## Quando é bom

- **TestFlight e trilha interna** pegam crash e erro de configuração antes da revisão.
- **`--non-interactive`** roda em CI; exige App Store Connect API Key e service account do Google configuradas antes.
- **Versão remota:** `appVersionSource: remote` com `autoIncrement` evita número de build repetido, que as lojas rejeitam.

## Quando é ruim

- **Fila gratuita lenta** em horário de pico.
- **Número de build repetido** é recusado: `android.versionCode` e `ios.buildNumber` sobem a cada envio.
- **Build iOS exige Xcode atual:** desde 28/04/2026 a Apple só aceita apps compilados com Xcode 26 ou mais novo (iOS 26 SDK) (developer.apple.com/news/upcoming-requirements). Em 09/09/2026 passou a exigir alvo mínimo iOS 13.
- **Android:** apps novos e atualizações devem mirar Android 16 (API 36) desde 31/08/2026; apps existentes precisam de API 35 para continuar visíveis a novos usuários (support.google.com/googleplay/android-developer/answer/11926878, 2026-11-25). Use um SDK do Expo recente, que já traz o alvo certo, e confira ao atualizar.

## Como começar

`eas.json`:

```json
{
  "cli": { "appVersionSource": "remote" },
  "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview": { "distribution": "internal" },
    "production": { "autoIncrement": true }
  },
  "submit": {
    "production": {
      "ios": { "ascAppId": "1234567890" },
      "android": { "track": "internal", "releaseStatus": "draft" }
    }
  }
}
```

Fluxo:

```bash
eas build --platform all --profile preview
eas build --platform all --profile production
eas submit --platform ios --latest
eas submit --platform android --latest
```

CI:

```bash
eas submit --platform android --latest --non-interactive
```

Passos fora do comando:

1. Crie o app no Play Console (`Create app`) e envie a chave JSON da service account com `eas credentials --platform android`.
2. No App Store Connect, crie o app e copie o Apple ID para `ascAppId`.
3. Na Google com conta pessoal, rode a trilha fechada com 12 testadores por 14 dias seguidos antes de pedir produção (clique em `Apply for production` no Painel).
4. No iOS, depois de testar no TestFlight, envie o build para App Review pelo App Store Connect.

## Combina com / alternativas

- Pipeline: skill `infra`, doc [07](../../infra/docs/07-github-actions.md).
- Alternativas: Fastlane, Codemagic, Bitrise.

## Decisão rápida

- **Use `preview` e TestFlight/trilha interna se:** é a primeira vez que o app sai do seu computador.
- **Use `--non-interactive` se:** o envio roda no CI.
- **Evite** pedir revisão sem ter testado o build de produção em aparelho real.
