# Regras que mudam o projeto desde o início

> Matriz das regras de cada loja que afetam auth, pagamento, dados, pacote e CI. Marque as dos destinos escolhidos e aplique a mais exigente ao projeto inteiro.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/, https://support.google.com/googleplay/android-developer/answer/13327111, https://learn.microsoft.com/en-us/windows/apps/publish/store-policies, https://learn.microsoft.com/en-us/windows/apps/publish/get-started |
| **Categoria** | Destinos de publicação |
| **Tipo** | Matriz de regras × destinos |
| **Vale para** | Projetos com ao menos uma loja |
| **Verificado em** | 2026-11-25 |

## O que é

Uma regra por linha. As colunas são App Store (iOS), Google Play (Android), Microsoft Store (Win) e Mac App Store (Mac). Download direto no desktop está na última coluna (Fora). ✅ exige, 🟡 exige em parte ou depende, — não exige.

## Conta e prazo

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Conta paga | ✅ US$ 99/ano | ✅ US$ 25 uma vez | — gratuita no fluxo novo | ✅ mesma conta do iOS | 🟡 Apple Developer para notarizar | Abrir na semana 1 |
| D-U-N-S para empresa | ✅ | ✅ | 🟡 recomendado | ✅ | — | Pedir junto com o CNPJ |
| Teste fechado antes da produção | — | ✅ 12 testadores por 14 dias (conta pessoal) | — | — | — | Recrutar testadores cedo |
| Conta de empresa obrigatória | — | 🟡 finanças, saúde, VPN, governo | 🟡 app que pede dados financeiros (10.14) | — | — | Usar CNPJ nesses casos |

## Login e conta

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Login social exige opção equivalente (4.8) | ✅ | — | — | ✅ | — | Sign in with Apple ou só login próprio; vale para a conta toda, inclusive na web |
| Exclusão de conta dentro do app | ✅ 5.1.1(v) | ✅ e também por link web | — | ✅ | — | Endpoint de exclusão e página web desde o início |
| Conta demo para a revisão | ✅ | ✅ | ✅ 10.3.1 | ✅ | — | Seed de conta demo no ambiente de produção |

## Pagamento

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Conteúdo digital pela loja | ✅ 3.1.1 (link externo no Brasil desde 18/06/2026) | ✅ Play Billing | — app não-jogo pode usar checkout próprio, 0% | ✅ 3.1.1, proibido chave de licença | — | Camada de cobrança com um provedor por destino (RevenueCat no celular, Stripe/Pix na web e no desktop) |
| Comissão | 15–30% (Brasil: ver mobile-release doc 06) | 15–30% | 15% apps, 12% jogos, só se usar a Microsoft | 15–30% | 0% | Embutir no preço |

## Privacidade e dados

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Política de privacidade em URL pública | ✅ e dentro do app | ✅ | ✅ se coleta dados (10.5) | ✅ e dentro do app | 🟡 LGPD exige igual | Página pública na semana 1 (skill `legal`) |
| Formulário de dados coletados | ✅ rótulos de privacidade | ✅ Data safety | — | ✅ | — | Mapa de dados real (skill `legal`, doc 02) |
| Permissões pedidas no uso, com finalidade | ✅ | ✅ | 🟡 | ✅ | — | Sem pedir tudo na abertura |
| Rastreamento com consentimento | ✅ ATT | 🟡 | — | ✅ | — | Analytics sem rastreamento entre apps, ou ATT |

## Conteúdo

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Conteúdo de usuário com denúncia e bloqueio | ✅ 1.2 | ✅ | 🟡 | ✅ | — | Moderação mínima no back-end |
| Classificação etária | ✅ | ✅ IARC | ✅ IARC (11.11) | ✅ | — | Responder o questionário antes do envio |
| App não pode ser só um site | ✅ 4.2 | 🟡 | 🟡 10.1 valor claro | ✅ | — | Recursos nativos; PWA só na Play e na Microsoft |
| Metadados fiéis, sem palavra-chave no nome | ✅ | ✅ | ✅ 10.1 | ✅ | — | Nome e descrição revisados |

## Pacote, código e atualização

| Regra | iOS | Android | Win | Mac | Fora | O que fazer no projeto |
|---|---|---|---|---|---|---|
| Não baixar código que mude o app | ✅ 2.5.2 | ✅ | ✅ 10.2.2 | ✅ 2.4.5(iv) | — | EAS Update só para correção |
| SDK ou alvo mínimo | ✅ Xcode 26 | ✅ API 36 | — | ✅ | — | CI com versões novas; calendário anual |
| Formato do pacote | IPA | AAB | MSIX ou MSI/EXE offline e silencioso | `.pkg` do Xcode, sandbox obrigatório (2.4.5) | instalador assinado, DMG notarizado | Escolher a stack sabendo disso |
| Assinatura de código | ✅ Apple | ✅ Play App Signing | 🟡 MSIX a Store assina; MSI/EXE com CA confiável | ✅ Apple | ✅ Windows (OV ou Artifact Signing) e macOS (Developer ID + notarização) | Certificados e segredos no CI desde o primeiro build |
| Atualizador próprio | ❌ | ❌ | ❌ MSI/EXE manda nova URL versionada | ❌ 2.4.5(vii) | ✅ Tauri updater, Squirrel | Desligar o updater nos builds de loja |
| Sem root, sem abrir sozinho no login | — | — | — | ✅ 2.4.5(iii, v) | — | Planejar recursos de segundo plano |

## Por que usar

As linhas marcadas para algum destino escolhido viram tarefas do backlog desde o primeiro sprint. É mais barato do que refazer auth, cobrança ou empacotamento no fim.

## Quando é ruim

- As regras mudam várias vezes por ano. Antes de cada lançamento, confira nas fontes da tabela de referência e nos docs de `mobile-release` e `desktop-release`.
- Os valores de comissão do Brasil na Apple e as regras de link externo mudam por país; use o [doc 06 da mobile-release](../../mobile-release/docs/06-pagamento-no-app-link-externo-e-revenuecat.md).

## Decisão rápida

- **Tem iOS ou Mac:** login equivalente, exclusão de conta e IAP para conteúdo digital entram no projeto inteiro.
- **Tem Mac App Store:** confira se os recursos do app funcionam em sandbox antes de prometer o destino.
- **Tem Windows fora da Store:** compre o certificado OV cedo; o Azure Artifact Signing não atende empresas do Brasil (conferido em 2026-11-25).
