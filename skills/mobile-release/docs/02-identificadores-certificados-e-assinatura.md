# Identificadores, certificados e assinatura

> O identificador do app nunca muda depois do primeiro envio, e a chave de assinatura é o que impede qualquer outra pessoa de publicar no seu nome.

| | |
|---|---|
| **Referência** | https://docs.expo.dev/app-signing/app-credentials/, https://docs.expo.dev/build-reference/app-versions/, https://fastlane.tools |
| **Categoria** | Assinatura |
| **Tipo** | Prática de configuração |
| **Vale para** | Expo com EAS Build (caminho principal); Flutter e nativo com Fastlane ou ferramenta da própria stack |
| **Verificado em** | 2026-11-25 |

## O que é

- **Identificador:** `ios.bundleIdentifier` e `android.package`, em formato de domínio invertido (`com.suaempresa.app`). É a identidade do app na loja.
- **Android:** o Google exige app assinado. Com o Play App Signing (padrão), você envia um pacote assinado com a chave de upload e o Google troca pela chave de assinatura final.
- **iOS:** três credenciais ligadas à conta Apple: certificado de distribuição (limite de 3 por conta), chave de push (limite de 2) e provisioning profile (por app, expira em 12 meses sem afetar apps já em produção).
- **EAS:** guarda e gerencia essas credenciais nos servidores da Expo e as usa em cada build.

## Por que usar

- O EAS cria e renova certificados e perfis, sem Xcode nem Keychain na máquina de quem builda.
- O build sai igual na máquina de qualquer pessoa e no CI.
- Fastlane (`match`) faz o mesmo para quem não usa Expo, guardando certificados num repositório criptografado.

## Quando usar

- Antes do primeiro build de produção.
- Ao trocar de máquina, de pessoa ou de CI.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App Expo | ✅ Ótimo | EAS gerencia tudo; `eas credentials` para ajustes |
| App Flutter | 🟡 Serve | Fastlane ou Codemagic; EAS Build só cobre projetos React Native |
| App nativo | 🟡 Serve | Xcode (assinatura automática) e Gradle; Fastlane no CI |
| Protótipo que não vai à loja | ❌ Evite | Basta Expo Go ou build interno |

## Quando é bom

- **Expo:** a primeira execução de `eas build` pergunta e cria as credenciais.
- **Play App Signing:** se você perder a chave de upload, o suporte do Google recupera; a nova chave só vale 72 horas depois do envio do certificado (docs.expo.dev/app-signing/app-credentials, 2026-11-25).
- **Chave de push iOS** não expira, e uma nova chave não muda os tokens dos usuários.

## Quando é ruim

- **Identificador errado** na primeira publicação não se corrige: crie outro app, perdendo avaliações e usuários.
- **Keystore no repositório** é falha de segurança; a documentação do Expo manda mantê-lo privado, com exceção do keystore de debug.
- **Revogar a chave de push** derruba o envio de notificações até subir outra.
- **`eas credentials` remove só dos servidores da Expo**; para apagar na Apple use o Apple Developer.

## Como começar

`app.json`:

```json
{
  "expo": {
    "name": "Meu App",
    "slug": "meu-app",
    "version": "1.0.0",
    "ios": { "bundleIdentifier": "com.suaempresa.meuapp" },
    "android": { "package": "com.suaempresa.meuapp" }
  }
}
```

Comandos:

```bash
npm install --global eas-cli
eas login
eas build:configure
eas credentials
```

Baixar o keystore Android para guardar em cofre de senhas: `eas credentials`, plataforma Android, perfil, opção `credentials.json`.

Segredos (chaves de API, service account) não entram no Git: skill `infra`, doc [09](../../infra/docs/09-segredos-e-configuracao.md).

## Combina com / alternativas

- Estrutura do projeto Expo: skill `architecture`, doc [08](../../architecture/docs/08-react-native-expo.md).
- Stack mobile: skill `stacks`, doc [11](../../stacks/docs/11-mobile.md).
- Alternativas: Fastlane (fastlane.tools), Codemagic (para Flutter).

## Decisão rápida

- **Use EAS credentials se:** o projeto é Expo.
- **Use Fastlane se:** é nativo ou Flutter e você quer assinatura reproduzível no CI.
- **Antes de enviar:** confira o identificador com quem é dono da marca; ele não muda depois.
