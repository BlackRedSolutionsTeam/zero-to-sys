# Pagamento: compra no app, link externo e RevenueCat

> Conteúdo e recursos digitais pagos dentro do app passam pelo sistema de compra da loja; produtos físicos e serviços consumidos fora do app podem usar Pix e cartão.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/, https://www.apple.com/br/newsroom/2026/06/apple-announces-changes-to-ios-in-brazil/, https://support.google.com/googleplay/android-developer/answer/112622, https://www.revenuecat.com/pricing/ |
| **Categoria** | Monetização |
| **Tipo** | Decisão de cobrança |
| **Vale para** | App com venda de assinatura, crédito ou conteúdo digital |
| **Verificado em** | 2026-11-25 |

## O que é

- **Compra no app (IAP, na Apple; Google Play Billing, no Google):** a loja cobra e fica com uma comissão.
- **Link externo ou pagamento alternativo:** levar o usuário a pagar no seu site ou processar por conta própria; permitido só onde e como a loja autoriza.
- **RevenueCat:** serviço que unifica assinaturas das duas lojas (e da web) com um SDK e um painel; evita validar recibos à mão.

## Por que usar

- A diretriz 3.1.1 da Apple manda usar IAP para desbloquear recursos ou conteúdo digital no app.
- Exceções do 3.1.3: apps de leitura, serviços entre pessoas em tempo real, bens e serviços consumidos fora do app (por exemplo, delivery), serviços corporativos vendidos a organizações e apps gratuitos que acompanham serviço web pago.
- RevenueCat reduz código de recibo, renovação, reembolso e teste.

## Quando usar

- IAP ou Play Billing: assinatura, crédito, desbloqueio de recurso digital.
- Cobrança própria (cartão e Pix pelo seu back-end): pedido de comida, transporte, produto físico, serviço presencial.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App com assinatura digital (conteúdo, recursos premium) | ✅ Ótimo | IAP e Play Billing, de preferência com RevenueCat |
| E-commerce, delivery, serviços físicos | ✅ Ótimo | Cobrança própria é permitida; use [pagamentos](../../integrations/docs/01-pagamentos.md) |
| App de venda B2B para empresas | 🟡 Serve | 3.1.3(c) permite cobrança fora; documente nas notas |
| App gratuito que acompanha SaaS vendido no site | 🟡 Serve | 3.1.3(f), sem botão de compra no app |
| Venda digital burlando a regra | ❌ Evite | Remoção do app |

## Quando é bom

- **Brasil, Apple (desde 18/06/2026):** acordo com o CADE permite links para pagamento externo e meios alternativos nos apps da App Store, sempre mostrados junto do IAP. Comissões segundo a Apple: 10% para a maioria dos desenvolvedores (programas Small Business, Video Partner e Mini Apps, e assinaturas após o primeiro ano) ou 21% nos demais, mais 5% de processamento quando usa o IAP; 15% de comissão de serviços de venda para compras no site vinculado (10% para membros de programas e após o primeiro ano) (apple.com/br/newsroom, 2026-11-25). O texto da Apple é ambíguo em alguns pontos: leia a página e a de distribuição no Brasil antes de decidir.
- **Restrições no Brasil:** apps da categoria infantil não podem ter links de compra, e para menores de 18 anos não pode haver link para site de transação; pagamento alternativo exige controle parental. A Apple não faz reembolso nas transações fora do sistema dela.
- **Small Business Program da Apple:** 15% (receita até US$ 1 milhão no ano anterior e no atual); inscrição pelo Account Holder.
- **Google:** 15% sobre os primeiros US$ 1 milhão por ano e 30% acima; assinaturas recorrentes 15%. Nos EUA, no EEE, no Reino Unido, na Austrália e no Japão há tarifas e programas de links externos próprios, com datas escalonadas em 2026 (support.google.com/googleplay/android-developer/answer/112622). Não encontrei programa específico do Google para o Brasil em 2026-11-25; confira no Play Console.
- **RevenueCat:** gratuito até US$ 2,5 mil de receita mensal rastreada (MTR); a partir daí cobra 1% (revenuecat.com/pricing, 2026-11-25).

## Quando é ruim

- **Comissão de 15% a 30%** em venda digital; embuta no preço.
- **Regras de link externo mudam por país** e por entitlement; sem o entitlement certo, botão ou link para pagar por fora reprova.
- **Pix dentro do app** para bem digital não substitui o IAP onde a regra exige.
- **RevenueCat é dependência externa:** o preço sobe com a receita e o SDK precisa de development build no Expo (não roda no Expo Go).

## Como começar

Com RevenueCat no Expo:

```bash
npx expo install react-native-purchases
```

```tsx
import Purchases from "react-native-purchases";
import { Platform } from "react-native";

export async function configurarCompras(userId: string) {
  const apiKey =
    Platform.OS === "ios"
      ? process.env.EXPO_PUBLIC_RC_IOS_KEY!
      : process.env.EXPO_PUBLIC_RC_ANDROID_KEY!;
  Purchases.configure({ apiKey, appUserID: userId });
}

export async function assinar() {
  const offerings = await Purchases.getOfferings();
  const pacote = offerings.current?.availablePackages[0];
  if (!pacote) return false;
  const { customerInfo } = await Purchases.purchasePackage(pacote);
  return customerInfo.entitlements.active["premium"] !== undefined;
}

export async function restaurarCompras() {
  const info = await Purchases.restorePurchases();
  return info.entitlements.active["premium"] !== undefined;
}
```

Passos: criar produtos na App Store Connect e no Play Console, ligá-los a um entitlement no RevenueCat e manter o botão "Restaurar compras" visível (exigido pela Apple). O back-end deve confiar no webhook do RevenueCat e não no app: skill `integrations`, doc [04](../../integrations/docs/04-webhooks.md).

## Combina com / alternativas

- Pagamentos de bens físicos e Pix: skill `integrations`, doc [01](../../integrations/docs/01-pagamentos.md).
- Alternativas ao RevenueCat: integrar StoreKit e Play Billing direto (mais código), ou outros serviços de assinatura.

## Decisão rápida

- **Use IAP e RevenueCat se:** o app vende assinatura ou recurso digital.
- **Use cobrança própria se:** o produto é físico ou o serviço é consumido fora do app.
- **Evite** colocar botão de pagamento por fora no app sem confirmar a regra e o entitlement para o país.
