# Regras de certificação e ficha da loja no desktop

> Na Microsoft Store reprovam metadados enganosos, app sem valor claro, código baixado, falta de conta demo e de política de privacidade; na Mac App Store valem as diretrizes do iOS mais a 2.4.5.

| | |
|---|---|
| **Referência** | https://learn.microsoft.com/en-us/windows/apps/publish/store-policies (versão 7.20, 2026-09-14), https://learn.microsoft.com/en-us/windows/apps/publish/beta-testing-and-targeted-distribution, https://developer.apple.com/app-store/review/guidelines/ |
| **Categoria** | Publicação desktop |
| **Tipo** | Lista de verificação por regra |
| **Vale para** | Microsoft Store e Mac App Store |
| **Verificado em** | 2026-11-25 |

## Microsoft Store Policies que mais reprovam

| Política | Exigência | O que fazer |
|---|---|---|
| 10.1 | Título e descrição fiéis; sem palavra-chave extra no nome; app funcional e com valor claro na primeira execução | Revisar a ficha e a tela inicial |
| 10.2.2 | Não baixar e executar código que mude a função descrita | Plugins e scripts só dentro do pacote |
| 10.3.1 | Conta demo se o app exige login | "Notes for certification" |
| 10.5 | Política de privacidade se acessa, coleta ou transmite dados pessoais | URL no Partner Center (skill `legal`) |
| 10.8.1 | Jogos usam a API de compra da Store | App que não é jogo pode usar checkout próprio |
| 10.14 | Conta Company se o app pede dados financeiros | Ver [doc 01](01-contas-e-custos.md) |
| 11.11 | Classificação etária pelo questionário IARC, mantida correta | Responder antes do envio |

## Mac App Store

As diretrizes do iOS que mais reprovam (login equivalente 4.8, exclusão de conta 5.1.1(v), IAP 3.1.1, conteúdo de usuário 1.2) valem também; veja o [doc 05 da mobile-release](../../mobile-release/docs/05-regras-de-revisao-que-mais-reprovam.md). As regras próprias do Mac estão no [doc 03](03-macos-mac-app-store-e-notarizacao.md).

## Testes antes do público

- **Microsoft:** público privado, package flights (app já publicado), códigos promocionais e link direto. Quem baixou não perde o acesso.
- **Apple:** TestFlight também funciona para apps de Mac.

## Quando é ruim

- A certificação da Microsoft leva até 3 dias úteis; depois de aprovada, a ficha aparece em cerca de 15 minutos.
- Política com versão nova algumas vezes por ano: confira a versão antes do envio.

## Decisão rápida

- **Antes de cada envio:** passe pela tabela inteira e pelo checklist da `mobile-release` se o app também vai ao Mac.
