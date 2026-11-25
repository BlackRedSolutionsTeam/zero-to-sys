---
name: store-targets
description: 'Pergunta no começo do projeto onde ele vai ser publicado (App Store, Google Play, Microsoft Store, Mac App Store, desktop, web) e aplica as regras de todas as lojas escolhidas desde o início, com um docs/STORES.md. Use quando o projeto pode virar app ou ganha um destino novo.'
---

# store-targets

Porta de entrada da publicação. Cada loja tem regras que mudam login, pagamento, pacote e assinatura; descobrir isso no envio obriga a refazer partes do sistema. Esta skill pergunta os destinos antes da stack e transforma as regras deles em tarefas do projeto.

## Como usar esta skill

1. **Pergunte os destinos** ([doc 01](docs/01-escolher-os-destinos.md)), com múltipla escolha, e se o app vende algo digital e tem conta de usuário.
2. **Confira a stack** na tabela destino × stack do doc 01 e avise a skill `stacks` se ela não cobre algum destino.
3. **Marque as regras** dos destinos na matriz do [doc 02](docs/02-regras-que-mudam-o-projeto.md). A mais exigente vale para o projeto inteiro.
4. **Gere o `docs/STORES.md`** com o modelo do [doc 03](docs/03-preparacao-por-combinacao.md) e ponha as regras marcadas no backlog.
5. **Abra as contas na semana 1** e, na hora de publicar, siga para `mobile-release` (iOS e Android) ou `desktop-release` (Windows, macOS, Linux).

## O que escolher por situação

| Situação | Caminho | Por quê |
|---|---|---|
| Só web | Pergunta feita, segue para `infra` | Sem regra de loja |
| Celular (iOS e/ou Android) | Matriz + `mobile-release` | Login, exclusão de conta e IAP desde o início |
| Desktop por loja | Matriz + `desktop-release` | Sandbox no Mac, pacote e certificação na Microsoft |
| Desktop por download | `desktop-release` docs 02 e 03 | Assinatura e notarização evitam o alerta de app não confiável |
| Celular e desktop | Flutter, ou Expo + Tauri/Electron com back-end comum | Uma stack não cobre tudo do mesmo jeito |
| PWA nas lojas | Play (TWA) e Microsoft (PWABuilder) | A Apple reprova site empacotado (4.2) |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Destinos | [docs/01-escolher-os-destinos.md](docs/01-escolher-os-destinos.md) | A pergunta, destino × stack |
| Regras | [docs/02-regras-que-mudam-o-projeto.md](docs/02-regras-que-mudam-o-projeto.md) | Matriz regras × destinos |
| Preparação | [docs/03-preparacao-por-combinacao.md](docs/03-preparacao-por-combinacao.md) | `docs/STORES.md` e combinações comuns |

## Checklist

- [ ] Destinos perguntados e registrados em `docs/STORES.md`.
- [ ] Stack cobre todos os destinos.
- [ ] Contas pedidas (Apple, Google, Microsoft) com D-U-N-S se for empresa.
- [ ] Regras marcadas na matriz viraram itens do backlog.
- [ ] Política de privacidade numa URL pública.
- [ ] Builds de loja sem atualizador próprio.

## Regras de uso

- **Destino antes da stack.** Pergunte sempre, mesmo que o usuário só fale em "app".
- **A regra mais exigente vale para todos.** Conta e back-end são únicos.
- **Regra de loja só conferida na fonte.** Diga a data da conferência; as regras mudam várias vezes por ano.
- **Fronteiras.** Envio e revisão mobile são da `mobile-release`; desktop da `desktop-release`; stack da `stacks`; política de privacidade da `legal`; exclusão de conta e LGPD no código da `security`; web e CI da `infra`.

## Quando a lista não cobre

Steam, consoles, Galaxy Store, Amazon Appstore, Huawei AppGallery, TV, relógio e carro ficam fora. Diga isso ao usuário e use a documentação oficial de cada loja.

## Validade dos dados

Regras, preços e prazos conferidos em 2026-11-25 nas páginas oficiais da Apple, do Google e da Microsoft; cada documento tem a linha "Verificado em".
