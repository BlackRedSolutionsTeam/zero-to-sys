# macOS: Mac App Store e notarização fora da loja

> Na Mac App Store o app roda em sandbox, empacotado pelo Xcode e atualizado só pela loja; fora dela, assine com Developer ID e notarize, ou o Gatekeeper bloqueia.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/ (2.4.5), https://support.apple.com/en-us/102445, https://developer.apple.com/documentation/security/customizing-the-notarization-workflow, https://developer.apple.com/documentation/security/hardened-runtime, https://developer.apple.com/documentation/bundleresources/entitlements/com.apple.security.app-sandbox, https://v2.tauri.app/distribute/app-store/, https://v2.tauri.app/distribute/sign/macos/, https://www.electronjs.org/docs/latest/tutorial/mac-app-store-submission-guide |
| **Categoria** | Publicação desktop |
| **Tipo** | Requisitos e assinatura |
| **Vale para** | Mac App Store e download direto no macOS |
| **Verificado em** | 2026-11-25 |

## O que é

| | Mac App Store | Download direto |
|---|---|---|
| Certificado | Apple Distribution + Mac Installer Distribution | Developer ID Application (só o titular da conta cria) |
| Pacote | `.pkg` gerado com as ferramentas do Xcode | DMG ou ZIP assinado e notarizado |
| Sandbox | Obrigatório | Opcional |
| Atualização | Só pela loja | Atualizador próprio |

## Regras da 2.4.5 (Mac App Store)

- (i) App em sandbox.
- (ii) Empacotado com o Xcode; sem instalador de terceiros.
- (iii) Não abre sozinho no login nem deixa processo rodando sem consentimento.
- (iv) Não baixa código que mude a função.
- (v) Não pede root.
- (vi) Não pede chave de licença ao abrir.
- (vii) Atualização só pela Mac App Store.
- (ix) Idiomas num único bundle.

Compras: as mesmas regras do iOS (3.1.1), com IAP para desbloquear recursos e chave de licença proibida. Política de privacidade nos metadados e dentro do app (5.1.1(i)).

## Por que usar

- Desde o Catalina o Gatekeeper exige notarização por padrão; sem ela o usuário precisa ir em Ajustes do Sistema > Privacidade e Segurança > "Abrir Mesmo Assim".
- O sandbox bloqueia acesso livre a arquivos, processos e hardware. Descubra antes de prometer o destino.

## Quando é bom

- **Tauri:** `Entitlements.plist` com App Sandbox, perfil "Mac App Store Connect", build `universal-apple-darwin`, `.pkg` com `xcrun productbuild` e envio com `altool` ou Transporter. Notarização fora da loja pelas variáveis `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH` (ou `APPLE_ID`, `APPLE_PASSWORD` com senha de app, `APPLE_TEAM_ID`).
- **Electron:** build MAS próprio (o darwin comum não abre em sandbox), `@electron/osx-sign`, envio pelo Transporter. Fora da loja, `@electron/notarize` via Forge ou Packager.

## Quando é ruim

- **Electron MAS** desliga `autoUpdater` e `crashReporter`.
- **Conta gratuita não notariza.**
- **Recursos que o sandbox impede** (acesso a qualquer pasta, ferramentas de sistema, root): fique no download direto.

## Como começar

Sandbox: a chave é `com.apple.security.app-sandbox` (Boolean), ligada pela capability App Sandbox no Xcode; acessos extras vêm de entitlements como `com.apple.security.files.user-selected.read-write`.

Hardened Runtime: obrigatório para enviar o app à notarização. Ele bloqueia JIT e injeção de código; libere só a exceção necessária (por exemplo `com.apple.security.cs.allow-jit` em apps com JavaScript JIT, caso de Electron).

Fora da loja (fluxo da Apple em "Customizing the notarization workflow"):

```bash
codesign --options runtime --sign "Developer ID Application: Empresa (TEAMID)" App.app
xcrun notarytool store-credentials "notarytool-password" --apple-id "<AppleID>" --team-id <TEAMID> --password <senha-de-app>
xcrun notarytool submit App.dmg --keychain-profile "notarytool-password" --wait
xcrun notarytool log <id> --keychain-profile "notarytool-password" log.json
xcrun stapler staple App.dmg
```

- A notarização aceita DMG (UDIF), `.pkg` assinado e ZIP; ZIP não recebe o ticket do `stapler`, então grampeie o `.app` e zipe de novo.
- O `altool` deixou de funcionar para notarização em 01/11/2023; use `notarytool`.
- A maioria termina em 5 minutos; limite de 75 notarizações por dia. Leia o log mesmo quando aprovar.

No CI, use runner macOS e a chave da API do App Store Connect como segredo.

## Decisão rápida

- **App simples, sem acesso ao sistema:** Mac App Store.
- **App que precisa de arquivos, processos ou atualização própria:** download direto notarizado.
