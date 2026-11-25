# Atualização sem loja (EAS Update) e versionamento

> EAS Update troca só o JavaScript e os assets de um app já instalado; qualquer mudança nativa continua exigindo build novo e revisão.

| | |
|---|---|
| **Referência** | https://docs.expo.dev/eas-update/introduction/, https://docs.expo.dev/eas-update/runtime-versions/, https://docs.expo.dev/build-reference/app-versions/ |
| **Categoria** | Atualização |
| **Tipo** | Prática de versionamento e entrega |
| **Vale para** | Apps Expo com `expo-updates` |
| **Verificado em** | 2026-11-25 |

## O que é

- **EAS Update** publica o bundle JavaScript e os assets; os usuários recebem na próxima abertura do app.
- **Channel:** conjunto de builds que recebe a atualização (`production`, `preview`).
- **runtimeVersion:** garante que a atualização só chegue a builds com código nativo compatível. Políticas: `appVersion`, `fingerprint` (muda sempre que algo nativo muda) ou versão fixa manual.
- **Versões:** `version` é a que o usuário vê; `android.versionCode` e `ios.buildNumber` são números de build que nunca se repetem. Com `appVersionSource: remote`, a Expo guarda esses números e `autoIncrement` os sobe.

## Por que usar

- Corrige bug de JavaScript em minutos, sem esperar revisão.
- Permite rollout gradual e testar num canal de preview antes de produção.

## Quando usar

- Correção de bug, texto, tradução, estilo e tela feitos só em JavaScript.
- Nunca para mudar permissões, dependências nativas ou versão do SDK do Expo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App Expo em produção | ✅ Ótimo | Correções rápidas |
| MVP em validação | ✅ Ótimo | Iteração sem fila de revisão |
| App que muda comportamento relevante por update | ❌ Evite | As regras das lojas se aplicam; mudança de comportamento normalmente pede revisão |
| App Flutter ou nativo | ❌ Evite | EAS Update é para React Native; Flutter tem alternativas de terceiros (Shorebird) |

## Quando é bom

- **Integra ao CI:** publica no push para a branch principal.
- **`fingerprint`** evita enviar atualização incompatível a um build antigo, ao custo de mais builds.
- **Plano Free:** 1.000 usuários ativos por mês incluídos; Starter 3.000; Production 50.000 (expo.dev/pricing, 2026-11-25).

## Quando é ruim

- **Regras das lojas valem para o update:** a Apple e a Google proíbem mudar a finalidade do app por atualização remota.
- **runtimeVersion esquecida:** com a política `appVersion`, mexer em código nativo sem subir a versão causa incompatibilidade e crash.
- **Update ruim chega a todos:** use rollout gradual e saiba reverter (publicar de novo o anterior).
- **Número de build repetido** é recusado pelas lojas.

## Como começar

```bash
npx expo install expo-updates
eas update:configure
```

`app.json`:

```json
{
  "expo": {
    "version": "1.2.0",
    "runtimeVersion": { "policy": "fingerprint" }
  }
}
```

`eas.json`:

```json
{
  "cli": { "appVersionSource": "remote" },
  "build": {
    "preview": { "distribution": "internal", "channel": "preview" },
    "production": { "channel": "production", "autoIncrement": true }
  }
}
```

Publicar:

```bash
eas update --channel preview --message "corrige botão de entrar"
eas update --channel production --message "corrige botão de entrar"
```

Sincronizar a versão remota quando já havia versões enviadas: `eas build:version:set`. Para compilar localmente com os mesmos números: `eas build:version:sync`. Com `expo-updates`, a política `nativeVersion` não funciona com versão remota; use `appVersion` ou `fingerprint`.

Regra de versão: SemVer em `version` (a cada lançamento nas lojas) e número de build automático; atualização por EAS Update não muda `version`.

## Combina com / alternativas

- Rollback e feature flag: skill `infra`, doc [14](../../infra/docs/14-feature-flags-e-rollback.md).
- Estrutura do app: skill `architecture`, doc [08](../../architecture/docs/08-react-native-expo.md).

## Decisão rápida

- **Use EAS Update se:** a correção é só JavaScript.
- **Faça novo build se:** mexeu em nativo, permissão ou SDK.
- **Use `fingerprint` se:** quer a escolha mais segura para a runtimeVersion.
