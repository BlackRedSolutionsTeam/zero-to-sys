# Linux: Flathub e Snap Store

> No Linux, publique no Flathub (revisão por voluntários, sem taxa) ou na Snap Store (gratuita); os dois exigem sandbox e metadados próprios.

| | |
|---|---|
| **Referência** | https://docs.flathub.org/docs/for-app-authors/requirements, https://docs.flathub.org/docs/for-app-authors/submission, https://snapcraft.io/docs/releasing-to-the-snap-store |
| **Categoria** | Publicação desktop |
| **Tipo** | Requisitos de loja |
| **Vale para** | Apps desktop com usuários Linux |
| **Verificado em** | 2026-11-25 |

## Flathub

- ID em DNS reverso (3 a 5 partes), igual ao `<id>` do MetaInfo, num domínio que você controla (ou `io.github.usuario`).
- MetaInfo válido, arquivo `.desktop` e ícone.
- Permissões mínimas no sandbox e portais XDG quando houver.
- Build sem rede e sem binários no envio; licença declarada.
- Fora: apps só de console ou de bandeja, wrappers finos de site, utilitários de sistema, nightly.
- Código ou empacotamento gerado por IA deve ser declarado; o manifesto não pode ser gerado por IA.
- Envio: PR contra o branch `new-pr` do repositório `flathub/flathub`.

## Snap Store

- Conta gratuita, registro do nome e publicação por canais (stable, candidate, beta, edge).
- Confinamento clássico e algumas interfaces passam por revisão manual.

## Quando é ruim

- Público pequeno para a maioria dos produtos; deixe para depois do Windows e do macOS, salvo se o cliente for Linux.

## Decisão rápida

- **App aberto, com usuários Linux:** Flathub.
- **Ferramenta para servidores Ubuntu:** Snap.
- **Só quer um arquivo:** AppImage no release do GitHub.
