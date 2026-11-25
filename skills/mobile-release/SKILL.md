---
name: mobile-release
description: Leva um app Expo, Flutter ou nativo até a App Store e a Play Store sem tropeçar nas regras de revisão — contas Apple Developer e Google Play (custo, D-U-N-S, teste de 12 testadores por 14 dias na conta pessoal), identificadores e assinatura (EAS Build, Fastlane), envio com EAS Submit, TestFlight e trilhas da Play, ficha da loja (capturas, classificação etária, privacidade), regras que mais reprovam (login social, compra no app, exclusão de conta), pagamento (IAP, link externo no Brasil, RevenueCat), EAS Update e versionamento, push (FCM e APNs) e pós-lançamento (crash, avaliações, versão mínima forçada). Use sempre que o usuário pedir "publicar na App Store", "publicar na Play Store", "subir o app nas lojas", "o app foi reprovado", "conta de desenvolvedor Apple", "TestFlight", "EAS Submit", "eas build", "atualização OTA", "push notification no app", "IAP", "RevenueCat" ou "versão mínima do app". Não escolhe a stack mobile (skill stacks), não define pastas do app (architecture) nem escreve a política de privacidade (legal).
---

# mobile-release

Guia para quem tem um app de celular pronto (ou quase) e precisa colocá-lo nas lojas e mantê-lo no ar. O que mais atrasa não é o código: são a conta de organização, a ficha da loja e as regras de revisão. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e comandos prontos.

## Como usar esta skill

0. **Projeto ainda no começo?** Aplique o [doc 10](docs/10-regras-que-mudam-o-projeto-desde-o-inicio.md) e a skill `store-targets` antes do código.
1. **Abra as contas primeiro** ([doc 01](docs/01-contas-apple-developer-e-google-play.md)): D-U-N-S leva tempo e a conta pessoal da Google exige 12 testadores por 14 dias antes da produção.
2. **Defina o identificador e a assinatura** ([doc 02](docs/02-identificadores-certificados-e-assinatura.md)); o identificador não muda depois.
3. **Gere o build e envie** ([doc 03](docs/03-builds-e-envio-eas-submit-testflight-play.md)); teste no TestFlight e na trilha interna.
4. **Preencha a ficha da loja** ([doc 04](docs/04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md)).
5. **Passe pela lista de regras de revisão** ([doc 05](docs/05-regras-de-revisao-que-mais-reprovam.md)) antes de pedir revisão.
6. **Se o app vende algo digital**, decida a cobrança no [doc 06](docs/06-pagamento-no-app-link-externo-e-revenuecat.md) antes do envio.
7. **Depois de publicado**, configure atualização, push e monitoramento ([doc 07](docs/07-atualizacao-sem-loja-eas-update-e-versionamento.md), [08](docs/08-notificacoes-push-fcm-e-apns.md), [09](docs/09-pos-lancamento-crash-avaliacoes-e-versao-minima.md)).

## O que escolher por situação

| Situação | Caminho | Por quê |
|---|---|---|
| App Expo, primeira publicação | EAS Build + EAS Submit | Sem Xcode nem Android Studio, mesmo comando no CI |
| App Flutter ou nativo | Fastlane ou CI da stack, mesmas trilhas das lojas | EAS Build e Update são para React Native |
| Projeto solo, conta pessoal | Aceitar 14 dias de teste fechado na Google | Regra para contas criadas depois de 13/11/2023 |
| Empresa ou app de finanças, saúde, VPN | Conta de organização com D-U-N-S | Exigida pela Google nessas categorias |
| Venda de assinatura ou conteúdo digital | IAP e Play Billing, com RevenueCat | Regra 3.1.1 da Apple |
| Produto físico, delivery, serviço presencial | Cobrança própria (Pix e cartão) | Exceção do 3.1.3(e) |
| Correção só de JavaScript | EAS Update | Sem nova revisão |
| Mudança nativa ou de permissão | Build novo e revisão | Update remoto não cobre |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Contas | [docs/01-contas-apple-developer-e-google-play.md](docs/01-contas-apple-developer-e-google-play.md) | Custo, D-U-N-S, verificação, teste da conta pessoal |
| Assinatura | [docs/02-identificadores-certificados-e-assinatura.md](docs/02-identificadores-certificados-e-assinatura.md) | Bundle ID, package, EAS credentials, Fastlane |
| Builds e envio | [docs/03-builds-e-envio-eas-submit-testflight-play.md](docs/03-builds-e-envio-eas-submit-testflight-play.md) | eas build, eas submit, TestFlight, trilhas |
| Ficha da loja | [docs/04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md](docs/04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md) | Capturas, classificação etária, Data safety |
| Regras de revisão | [docs/05-regras-de-revisao-que-mais-reprovam.md](docs/05-regras-de-revisao-que-mais-reprovam.md) | Login, compra, exclusão de conta |
| Pagamento | [docs/06-pagamento-no-app-link-externo-e-revenuecat.md](docs/06-pagamento-no-app-link-externo-e-revenuecat.md) | IAP, link externo no Brasil, RevenueCat |
| Atualização | [docs/07-atualizacao-sem-loja-eas-update-e-versionamento.md](docs/07-atualizacao-sem-loja-eas-update-e-versionamento.md) | EAS Update, runtimeVersion, versões |
| Push | [docs/08-notificacoes-push-fcm-e-apns.md](docs/08-notificacoes-push-fcm-e-apns.md) | expo-notifications, FCM, APNs |
| Pós-lançamento | [docs/09-pos-lancamento-crash-avaliacoes-e-versao-minima.md](docs/09-pos-lancamento-crash-avaliacoes-e-versao-minima.md) | Crash, avaliações, versão mínima |
| Início do projeto | [docs/10-regras-que-mudam-o-projeto-desde-o-inicio.md](docs/10-regras-que-mudam-o-projeto-desde-o-inicio.md) | O que entra no primeiro sprint |

## Checklist

- [ ] Contas criadas com 2FA e e-mail de domínio próprio; membros com acesso por papel, sem senha compartilhada.
- [ ] Na Google com conta pessoal: trilha fechada com 12 testadores por 14 dias seguidos.
- [ ] `ios.bundleIdentifier` e `android.package` definidos e confirmados com o dono da marca.
- [ ] Keystore e chaves fora do Git; backup em cofre de senhas.
- [ ] Build de produção testado em aparelho real pelo TestFlight e pela trilha interna.
- [ ] Xcode 26 ou mais novo e alvo Android API 36 (`eas build` com SDK recente).
- [ ] Ficha completa: capturas, descrição, política de privacidade, classificação etária, Data safety.
- [ ] Exclusão de conta no app (e URL web para a Google); login social com alternativa equivalente.
- [ ] Compra digital pelo IAP e Play Billing; botão "Restaurar compras".
- [ ] Conta demo e back-end no ar nas notas para a revisão.
- [ ] Crash monitorado e versão mínima forçada desde a v1.0.

## Regras de uso

- **Regra de loja só conferida na fonte.** Diretrizes, preços e prazos mudam; leia a página oficial antes de afirmar e diga a data da conferência.
- **Conta antes de código.** Comece as contas na primeira semana do projeto.
- **Identificador é para sempre.** Confirme `bundleIdentifier` e `package` antes do primeiro envio.
- **Nada de venda digital por fora sem checar a regra do país.** Brasil tem regras próprias da Apple desde 18/06/2026.
- **Atualização remota não muda o app.** EAS Update corrige; mudança de comportamento volta para a revisão.
- **Fronteiras.** Stack mobile é da `stacks`; pastas do app da `architecture`; telas por plataforma da `user-experience`; desktop da `desktop-release`; destinos da `store-targets`; pagamentos, webhooks e push no servidor da `integrations`; política de privacidade da `legal`; LGPD da `security`; pipeline da `infra`.

## Quando a lista não cobre

Distribuição privada (Apple Business Manager, Play privado), lojas alternativas, jogos (Game Center, Play Games), app para TV, relógio e carro, apps para crianças e de saúde regulados ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial.

## Validade dos dados

Preços (Apple US$ 99 por ano, Google US$ 25 uma vez, planos do EAS e do RevenueCat), prazos (Xcode 26 desde 28/04/2026, API 36 desde 31/08/2026, verificação de desenvolvedor Android desde 30/09/2026 no Brasil, link externo da Apple no Brasil desde 18/06/2026) e regras de revisão foram conferidos em 2026-11-25 nas páginas oficiais; cada documento tem a linha "Verificado em".
