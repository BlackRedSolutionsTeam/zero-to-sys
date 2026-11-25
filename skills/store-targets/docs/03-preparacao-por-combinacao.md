# Lista de preparação por combinação de destinos

> Some as regras de todos os destinos escolhidos, aplique a mais exigente ao projeto inteiro e registre tudo num `docs/STORES.md`.

| | |
|---|---|
| **Referência** | [doc 02](02-regras-que-mudam-o-projeto.md) |
| **Categoria** | Destinos de publicação |
| **Tipo** | Modelo de arquivo e combinações comuns |
| **Vale para** | Todo projeto com pelo menos uma loja |
| **Verificado em** | 2026-11-25 |

## O que é

Um arquivo no projeto que diz para onde ele vai, o que cada destino exige e o que já está pronto. Ele vive em `docs/STORES.md` para ficar junto do `ARCHITECTURE.md` e ser lido pelo agente.

## Por que usar

- A regra mais exigente vale para todos. Se o projeto vai para o iOS, o login equivalente e a exclusão de conta entram também no Android e na web, porque a conta é a mesma.
- O agente e o time consultam um só lugar antes de mexer em login, pagamento, permissões e build.

## Como montar

1. Liste os destinos escolhidos ([doc 01](01-escolher-os-destinos.md)).
2. Para cada linha da matriz do [doc 02](02-regras-que-mudam-o-projeto.md), marque se algum destino escolhido exige a regra.
3. Toda regra marcada entra no projeto inteiro, não só no destino que a exige.
4. Escreva o `docs/STORES.md` com o modelo abaixo.

## Modelo do `docs/STORES.md`

```markdown
# Destinos de publicação

Conferido em: AAAA-MM-DD

## Destinos
- [x] App Store (iPhone e iPad)
- [x] Google Play
- [ ] Microsoft Store
- [ ] Mac App Store
- [ ] Download direto no desktop
- [x] Web

Vende algo digital no app: sim (assinatura Pro)
Tem conta de usuário: sim

## Contas
- [ ] Apple Developer (organização, D-U-N-S): responsável, data do pedido
- [ ] Google Play Console (organização): responsável, data do pedido

## Regras aplicadas ao projeto inteiro
- [ ] Login: e-mail e senha + Google + Sign in with Apple (Apple 4.8)
- [ ] Exclusão de conta no app e por link web (Apple 5.1.1(v), Google)
- [ ] Assinatura Pro via IAP e Play Billing com RevenueCat; web com Stripe/Pix
- [ ] Política de privacidade numa URL pública e dentro do app
- [ ] Permissões pedidas no momento do uso, com texto de finalidade
- [ ] Denúncia e bloqueio em conteúdo de usuário (Apple 1.2)

## Técnico por destino
- iOS: Xcode 26+, Privacy Manifest, bundle id `com.empresa.app`
- Android: API alvo 36, AAB, Play App Signing, package `com.empresa.app`

## Links oficiais
- https://developer.apple.com/app-store/review/guidelines/
- https://support.google.com/googleplay/android-developer/
```

## Combinações comuns

| Combinação | O que muda no projeto desde o início |
|---|---|
| Só App Store e Google Play | Login equivalente, exclusão de conta no app e na web, IAP + Play Billing (RevenueCat), contas abertas na semana 1, 12 testadores se a conta Google for pessoal |
| Celular + web | As regras de cima valem também na web (conta única); venda na web pode usar Stripe ou Pix, mas o app não pode levar o usuário a pagar por fora sem a regra do país permitir |
| Windows + macOS | Assinatura de código nos dois desde o primeiro build de teste; sandbox se for Mac App Store; atualizador próprio só fora das lojas |
| Todos os destinos | Back-end e conta únicos, regras mais exigentes em tudo, CI com runners macOS e Windows, uma ficha de loja por destino e um calendário com as datas de SDK mínimo de cada loja |

## Quando é ruim

- O arquivo envelhece: as regras mudam várias vezes por ano. Atualize a data "Conferido em" a cada lançamento.

## Decisão rápida

- **Sempre** gere o `docs/STORES.md` quando houver ao menos uma loja.
- **Avise o usuário** quando uma regra de um destino muda o comportamento dos outros (exemplo: Sign in with Apple também na web).
