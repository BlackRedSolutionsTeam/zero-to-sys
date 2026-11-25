# Pagamento e atualização automática no desktop

> Na Microsoft Store, app que não é jogo pode cobrar com checkout próprio e ficar com 100%; na Mac App Store vale o IAP. Atualizador próprio só nos builds fora das lojas.

| | |
|---|---|
| **Referência** | https://learn.microsoft.com/en-us/windows/apps/publish/get-started, https://developer.apple.com/app-store/review/guidelines/ (3.1.1, 2.4.5), https://v2.tauri.app/plugin/updater/, https://www.electronjs.org/docs/latest/tutorial/updates |
| **Categoria** | Publicação desktop |
| **Tipo** | Decisão de cobrança e de atualização |
| **Vale para** | Apps desktop pagos ou com versões frequentes |
| **Verificado em** | 2026-11-25 |

## Pagamento

| Destino | Conteúdo digital | Comissão |
|---|---|---|
| Microsoft Store (app) | Checkout próprio ou o comércio da Microsoft | 0% no próprio; 15% no da Microsoft |
| Microsoft Store (jogo) | Só a API da Store | 12% |
| Mac App Store | IAP; chave de licença proibida | Como no iOS (ver mobile-release doc 06) |
| Download direto | Livre (Stripe, Pix, chave de licença) | 0% para a loja |

## Atualização automática

| Destino | Como atualiza |
|---|---|
| Microsoft Store MSIX | A Store |
| Microsoft Store MSI/EXE | Nova URL versionada enviada ao Partner Center |
| Mac App Store | Só a loja (2.4.5(vii)) |
| Download direto | Tauri updater, `autoUpdater` do Electron (Squirrel) ou update.electronjs.org |

## Quando é bom

- **Tauri updater:** assinatura obrigatória (`TAURI_SIGNING_PRIVATE_KEY`), endpoint com TLS e resposta 204 quando não há versão nova.
- **update.electronjs.org:** gratuito para repositório público no GitHub, com app assinado no macOS.

## Quando é ruim

- **Perder a chave do Tauri updater** impede atualizar quem já instalou. Guarde em cofre.
- **O guia do Tauri** diz que o instalador da Store deve usar o updater, mas a Microsoft pede URL versionada a cada versão. Teste antes de depender disso.
- **Electron MAS** não tem `autoUpdater`.

## Como começar

1. Uma flag de build por destino (`STORE=msstore|mas|direct`).
2. Nos builds de loja, desligue o updater e a cobrança proibida.
3. No download direto, ligue o updater com a chave de assinatura no CI.

## Decisão rápida

- **SaaS com app desktop no Windows:** checkout próprio na web, app só faz login.
- **App pago no Mac pela loja:** IAP, sem chave de licença.
