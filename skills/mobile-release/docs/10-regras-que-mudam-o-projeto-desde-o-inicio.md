# Regras das lojas mobile que mudam o projeto desde o início

> Se o app vai para a App Store ou para a Google Play, cinco decisões precisam entrar no primeiro sprint: conta da loja, login equivalente, exclusão de conta, cobrança de conteúdo digital e versões mínimas de SDK.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/, https://support.google.com/googleplay/android-developer/answer/13327111, https://support.google.com/googleplay/android-developer/answer/14151465 |
| **Categoria** | Publicação mobile |
| **Tipo** | Decisões de início de projeto |
| **Vale para** | Todo app que vai para a App Store ou para a Google Play |
| **Verificado em** | 2026-11-25 |

## O que é

O resumo mobile da matriz do [doc 02 da store-targets](../../store-targets/docs/02-regras-que-mudam-o-projeto.md). Os docs 01 a 09 explicam como publicar; este diz o que já precisa estar no projeto antes da primeira linha de código.

## As decisões

| Decisão | App Store | Google Play | Onde entra no projeto | Doc |
|---|---|---|---|---|
| Conta da loja | US$ 99/ano, D-U-N-S para empresa | US$ 25, 12 testadores por 14 dias na conta pessoal; verificação de desenvolvedor no Brasil desde 30/09/2026 | Semana 1, antes do código | [01](01-contas-apple-developer-e-google-play.md) |
| Login | Login social exige opção equivalente (4.8) | — | Auth: Sign in with Apple ou só login próprio, também na web | [05](05-regras-de-revisao-que-mais-reprovam.md) |
| Exclusão de conta | Dentro do app (5.1.1(v)) | Dentro do app e por link web | Endpoint e página web de exclusão; retenção legal (skill `security`) | [05](05-regras-de-revisao-que-mais-reprovam.md) |
| Conteúdo digital | IAP (3.1.1); no Brasil, link externo permitido desde 18/06/2026 | Play Billing | Camada de cobrança com RevenueCat; web com Stripe/Pix | [06](06-pagamento-no-app-link-externo-e-revenuecat.md) |
| SDK mínimo | Xcode 26 | API 36 | CI com versões novas e calendário anual | [03](03-builds-e-envio-eas-submit-testflight-play.md) |
| Identificador | `bundleIdentifier` para sempre | `package` para sempre | Definir com o dono da marca | [02](02-identificadores-certificados-e-assinatura.md) |
| Privacidade | Rótulos de privacidade, ATT se rastreia | Data safety | Mapa de dados real (skill `legal`) | [04](04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md) |
| Conteúdo de usuário | Denúncia, bloqueio, moderação (1.2) | Igual | Back-end de moderação | [05](05-regras-de-revisao-que-mais-reprovam.md) |
| Atualização remota | Só correção, sem mudar o app | Igual | EAS Update só para JavaScript | [07](07-atualizacao-sem-loja-eas-update-e-versionamento.md) |

## Por que usar

Mudar o login, a cobrança ou o identificador depois do primeiro envio custa semanas e pode reprovar o app.

## Quando é ruim

As regras mudam várias vezes por ano. Reconfira nas fontes antes de cada lançamento.

## Decisão rápida

- **Só um dos dois destinos:** aplique só a coluna dele, mas lembre que a conta do usuário é a mesma na web.
- **Os dois destinos:** aplique as duas colunas ao projeto inteiro.
