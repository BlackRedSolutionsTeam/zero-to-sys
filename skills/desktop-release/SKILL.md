---
name: desktop-release
description: 'Leva um app desktop à Microsoft Store, à Mac App Store e ao download assinado: contas, MSIX ou MSI/EXE, assinatura de código, sandbox e notarização, regras de certificação, pagamento, atualização e Linux. Use quando pedirem "publicar na Microsoft Store", "notarizar" ou "SmartScreen bloqueia".'
---

# desktop-release

Guia para colocar um app desktop nas lojas ou num download confiável. O que mais atrasa: certificado de assinatura (no Brasil não dá para usar o Azure Artifact Signing), o sandbox da Mac App Store e as regras de instalador da Microsoft. Cada tópico tem um documento em `docs/`.

## Como usar esta skill

1. **Confira os destinos** no `docs/STORES.md` do projeto (skill `store-targets`).
2. **Abra as contas** ([doc 01](docs/01-contas-e-custos.md)).
3. **Windows:** pacote e assinatura no [doc 02](docs/02-windows-pacote-e-assinatura.md).
4. **macOS:** sandbox ou notarização no [doc 03](docs/03-macos-mac-app-store-e-notarizacao.md).
5. **Antes do envio:** regras de certificação e ficha no [doc 04](docs/04-regras-de-certificacao-e-ficha.md).
6. **Cobrança e atualização** por destino no [doc 05](docs/05-pagamento-e-atualizacao.md).
7. **Linux**, se houver: [doc 06](docs/06-linux-flathub-e-snap.md).

## O que escolher por situação

| Situação | Caminho | Por quê |
|---|---|---|
| Microsoft Store, app novo | MSIX | A Store assina; sem certificado |
| Tauri ou Electron na Microsoft Store | MSI/EXE offline, silencioso e assinado com OV | Tauri só gera EXE e MSI |
| Download no Windows, empresa no Brasil | Certificado OV com chave em HSM na nuvem | Artifact Signing não atende o Brasil |
| Mac sem acesso ao sistema | Mac App Store | Sandbox e IAP |
| Mac com arquivos, processos ou updater | DMG com Developer ID e notarização | Sandbox impediria |
| SaaS com app de Windows | Checkout próprio na web | Microsoft permite 0% para app que não é jogo |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Contas | [docs/01-contas-e-custos.md](docs/01-contas-e-custos.md) | Partner Center e Apple Developer |
| Windows | [docs/02-windows-pacote-e-assinatura.md](docs/02-windows-pacote-e-assinatura.md) | MSIX, MSI/EXE, certificado, SmartScreen, winget |
| macOS | [docs/03-macos-mac-app-store-e-notarizacao.md](docs/03-macos-mac-app-store-e-notarizacao.md) | Sandbox, 2.4.5, Developer ID, notarização |
| Regras | [docs/04-regras-de-certificacao-e-ficha.md](docs/04-regras-de-certificacao-e-ficha.md) | Políticas 10.x, IARC, testes |
| Pagamento e atualização | [docs/05-pagamento-e-atualizacao.md](docs/05-pagamento-e-atualizacao.md) | Checkout, IAP, updater por destino |
| Linux | [docs/06-linux-flathub-e-snap.md](docs/06-linux-flathub-e-snap.md) | Flathub e Snap |

## Checklist

- [ ] Contas abertas, Company/organização se for empresa.
- [ ] Certificado OV (Windows) e Developer ID (macOS) no cofre e no CI.
- [ ] Instalador do Windows offline, silencioso e com desinstalação limpa.
- [ ] Recursos do app testados em sandbox, se for Mac App Store.
- [ ] Builds de loja sem atualizador próprio e sem cobrança proibida.
- [ ] Política de privacidade e classificação IARC preenchidas.
- [ ] Conta demo nas notas de certificação.

## Regras de uso

- **Regra de loja só conferida na fonte.** Diga a data da conferência.
- **Assine desde o primeiro build de teste.** Reputação no SmartScreen vem de versões seguidas com a mesma identidade.
- **Um build por destino.** Updater e cobrança mudam por loja.
- **Fronteiras.** Destinos e matriz de regras da `store-targets`; celular da `mobile-release`; stack da `stacks`; política de privacidade da `legal`; CI da `infra`.

## Quando a lista não cobre

Steam, Epic, consoles, distribuição corporativa (Intune, MDM, Apple Business Manager) e apps de kernel ou driver ficam fora. Use a documentação oficial.

## Validade dos dados

Conferido em 2026-11-25 nas páginas oficiais da Microsoft (incluindo a de preços do Artifact Signing), da Apple (notarização, Hardened Runtime, entitlement do sandbox), do Tauri, do Electron, do Flathub e do Snapcraft. Cada documento tem a linha "Verificado em".
