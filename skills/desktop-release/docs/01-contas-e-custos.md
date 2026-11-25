# Contas e custos: Microsoft Partner Center e Apple Developer

> Abra as contas antes de terminar o app: a da Microsoft é gratuita no fluxo novo, mas a de empresa leva dias de revisão; a da Apple é a mesma do iOS.

| | |
|---|---|
| **Referência** | https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/open-a-developer-account, https://developer.apple.com/support/enrollment/ |
| **Categoria** | Publicação desktop |
| **Tipo** | Cadastro e verificação |
| **Vale para** | Microsoft Store, Mac App Store e notarização no macOS |
| **Verificado em** | 2026-11-25 |

## O que é

| | Microsoft Partner Center | Apple Developer Program |
|---|---|---|
| Custo | Sem taxa de registro no fluxo novo, Individual ou Company | US$ 99 por ano (moeda local onde houver) |
| Pessoa física | Documento com foto e selfie; só para quem não publica ligado a negócio | Sim |
| Empresa | D-U-N-S (recomendado) ou documentos, e-mail do domínio; revisão de 2 a 5 dias úteis | Entidade legal, D-U-N-S, site público e e-mail do domínio |
| Serve para | Microsoft Store | Mac App Store, iOS e notarização fora da loja |

## Por que usar

- Sem conta Apple paga não há notarização, e o macOS mostra alerta para app baixado sem notarizar.
- A Microsoft não converte conta Individual em Company: escolha certo na primeira vez.

## Quando usar

Na primeira semana do projeto, assim que o destino estiver no `docs/STORES.md` (skill `store-targets`).

## Quando é bom

- **Microsoft, fluxo novo:** comece em storedeveloper.microsoft.com; outros caminhos mostram o fluxo antigo.
- **Apple:** a mesma conta do iOS cobre o Mac.

## Quando é ruim

- **Conta Company obrigatória na Microsoft** quando o app pede dados financeiros para a função principal, ou quando o nome do app ou do publisher soa como empresa (política 10.14).
- **D-U-N-S** pode levar dias ou semanas.

## Como começar

1. Decida pessoa física ou CNPJ (se for empresa, use CNPJ nos dois).
2. Peça o D-U-N-S, se ainda não tiver.
3. Abra o Partner Center pelo fluxo novo e o Apple Developer (ou reaproveite o do iOS).
4. Ative 2FA e dê acesso por papel; nada de senha compartilhada.

## Decisão rápida

- **Empresa:** Company na Microsoft e organização na Apple.
- **Projeto pessoal:** Individual na Microsoft é gratuito; a Apple só se for para o Mac ou para notarizar.
