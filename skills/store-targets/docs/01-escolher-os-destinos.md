# Escolher os destinos de publicação

> Pergunte onde o projeto vai ser publicado antes de escolher a stack: cada loja tem exigências que mudam login, pagamento, pacote e assinatura desde o primeiro dia.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/, https://support.google.com/googleplay/android-developer/, https://learn.microsoft.com/windows/apps/publish/ |
| **Categoria** | Destinos de publicação |
| **Tipo** | Pergunta e decisão |
| **Vale para** | Todo projeto que vai virar app instalável ou site |
| **Verificado em** | 2026-11-25 |

## O que é

O destino é o lugar onde o usuário vai instalar ou abrir o produto. Um projeto pode ter vários.

| Destino | Plataforma | Quem cuida da publicação |
|---|---|---|
| App Store | iPhone e iPad | skill `mobile-release` |
| Google Play | Android | skill `mobile-release` |
| Mac App Store | macOS | skill `desktop-release` |
| Microsoft Store | Windows | skill `desktop-release` |
| Download direto no desktop | Windows (instalador assinado), macOS (DMG notarizado), Linux | skill `desktop-release` |
| Web | Navegador, com ou sem PWA | skill `infra` |

## Por que usar

- A Apple exige login equivalente quando há login social (4.8), compra pela loja para conteúdo digital (3.1.1) e exclusão de conta no app (5.1.1(v)). Descobrir isso no envio obriga a refazer auth e cobrança.
- A Mac App Store exige App Sandbox, o que pode impedir recursos que o app desktop já tinha.
- A stack escolhida pode não chegar a um destino. Exemplo: Electron não roda no celular; PWA não entra na App Store.

## Quando usar

- No começo de todo projeto, logo depois da skill `product` e antes da `stacks`.
- Quando um projeto existente ganha um destino novo ("agora queremos ir para a App Store").

## A pergunta

Faça a pergunta com múltipla escolha:

> Onde o projeto vai ser publicado? (pode marcar mais de um)
> 1. App Store (iPhone e iPad)
> 2. Google Play (Android)
> 3. Microsoft Store (Windows)
> 4. Mac App Store (macOS)
> 5. Download direto no desktop (Windows, macOS, Linux)
> 6. Web (navegador)

Depois pergunte duas coisas que mudam as regras:

- **Vende algo digital dentro do app?** (assinatura, crédito, recurso premium) Liga as regras de compra da loja.
- **Tem conta de usuário?** Liga login equivalente e exclusão de conta.

## Destino × stack

| Stack | App Store | Google Play | Microsoft Store | Mac App Store | Download desktop | Web |
|---|---|---|---|---|---|---|
| Expo / React Native | ✅ | ✅ | 🟡 react-native-windows, à parte | 🟡 react-native-macos, à parte | ❌ | ✅ com Expo web |
| Flutter | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 sem bom SEO |
| Nativo (Swift, Kotlin) | ✅ só iOS | ✅ só Android | ❌ | ✅ Swift | ✅ Swift | ❌ |
| Tauri 2 | 🟡 suporte novo | 🟡 suporte novo | ✅ | ✅ | ✅ | ❌ |
| Electron | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| .NET MAUI | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| PWA | ❌ (4.2 reprova site empacotado) | 🟡 via TWA (Bubblewrap) | ✅ PWABuilder | ❌ | ❌ | ✅ |

Use esta tabela para avisar quando a stack sugerida pela skill `stacks` não cobre os destinos. Exemplo: celular e desktop juntos pedem Flutter, ou Expo no celular com Tauri/Electron no desktop e um back-end comum.

## Quando é ruim

- **Muitos destinos de uma vez** multiplicam contas, revisões e builds. Para um MVP, comece pelo destino onde o cliente está e deixe o projeto pronto para os outros.
- **Desktop por loja** reduz o alcance de quem já distribui por download e traz o sandbox da Apple. Às vezes o download direto assinado basta.

## Como começar

1. Faça a pergunta acima.
2. Gere a lista de preparação ([doc 03](03-preparacao-por-combinacao.md)).
3. Abra as contas na primeira semana ([mobile-release doc 01](../../mobile-release/docs/01-contas-apple-developer-e-google-play.md), [desktop-release doc 01](../../desktop-release/docs/01-contas-e-custos.md)).

## Decisão rápida

- **Só web:** não precisa desta skill além da pergunta; siga para `infra`.
- **Qualquer loja:** aplique a matriz do [doc 02](02-regras-que-mudam-o-projeto.md) antes de escolher a stack.
