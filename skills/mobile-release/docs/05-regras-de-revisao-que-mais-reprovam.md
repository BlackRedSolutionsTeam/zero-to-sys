# Regras de revisão que mais reprovam

> Login social sem alternativa, venda de conteúdo digital fora do IAP, falta de exclusão de conta e app que é só um site empacotado reprovam a maioria dos primeiros envios.

| | |
|---|---|
| **Referência** | https://developer.apple.com/app-store/review/guidelines/, https://support.google.com/googleplay/android-developer/answer/13327111 |
| **Categoria** | Revisão das lojas |
| **Tipo** | Lista de verificação por regra |
| **Vale para** | App Store e Play Store |
| **Verificado em** | 2026-11-25 |

## O que é

As diretrizes que a Apple (App Review Guidelines) e o Google (políticas do Play) aplicam antes de aprovar. Esta lista junta as que mais derrubam apps de produto; o texto completo e atual está nas páginas oficiais.

## Por que usar

Cada reprovação custa dias. Conferir as regras antes do envio é mais barato que corrigir depois.

## Quando usar

- Antes de cada envio para revisão, principalmente o primeiro.
- Quando o app ganha login, pagamento, conteúdo de usuário ou SDK novo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App com cadastro | ✅ Ótimo | Exclusão de conta dentro do app e login equivalente |
| App que vende conteúdo digital | ✅ Ótimo | Passa pela regra de compra (doc [06](06-pagamento-no-app-link-externo-e-revenuecat.md)) |
| Site empacotado em WebView | ❌ Evite | A Apple rejeita app que é só site (4.2) |
| App de rede social ou comunidade | ✅ Ótimo | Exige denúncia, bloqueio e moderação (1.2) |

## Quando é bom

Regras da Apple (conferidas em 2026-11-25):

| Diretriz | Exigência | O que fazer |
|---|---|---|
| 2.1 Completude | App final, sem placeholders; se tem login, conta demo e back-end no ar | Conta de teste nas notas da revisão |
| 3.1.1 Compras | Conteúdo ou recurso digital desbloqueado no app usa compra no app (IAP); proibido chave de licença, QR code e cripto | Doc [06](06-pagamento-no-app-link-externo-e-revenuecat.md) |
| 4.2 Funcionalidade mínima | Mais que um site empacotado | Recursos nativos e interface própria |
| 4.8 Login | Se o login principal é de terceiros (Google, Facebook), ofereça outra opção equivalente que limite os dados a nome e e-mail e permita e-mail privado | Sign in with Apple, ou só login próprio |
| 5.1.1(i) Privacidade | Link da política nos metadados e dentro do app | Doc [04](04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md) |
| 5.1.1(v) Exclusão | Quem cria conta pode excluí-la dentro do app; sem exigir login se o app não precisa | Botão "Excluir conta" nas configurações |
| 5.1.2 Dados | Sem rastreamento sem a permissão do ATT; sem exigir permissão de notificação ou localização para usar o app | Pedir permissões no momento do uso |
| 1.2 Conteúdo de usuário | Filtro, denúncia, bloqueio e contato publicado | Moderação mínima desde o dia 1 |

Regras do Google (conferidas em 2026-11-25):

- **Exclusão de conta:** quem cria conta no app deve poder excluí-la no app e também por link web, informado na Data safety; dados retidos por segurança ou lei devem constar da política (support.google.com/googleplay/android-developer/answer/13327111).
- **Data safety** completa e política de privacidade (doc [04](04-ficha-da-loja-textos-capturas-classificacao-e-privacidade.md)).
- **API alvo:** Android 16 (API 36) para apps novos e atualizações desde 31/08/2026 (doc [03](03-builds-e-envio-eas-submit-testflight-play.md)).

## Quando é ruim

- **Regras mudam:** a Apple e o Google revisam as diretrizes várias vezes ao ano; releia a página oficial antes de cada lançamento.
- **Revisão é humana** e pode divergir entre envios; responda no Resolution Center com clareza em vez de reenviar igual.
- **Permissão pedida sem uso** e texto de finalidade (purpose string) vago reprovam.

## Como começar

Checklist antes de enviar:

1. App funciona sem crash em aparelho real, com build de produção.
2. Conta demo e back-end ativos; notas explicando fluxos escondidos.
3. Exclusão de conta no app (e URL web para a Google).
4. Login social acompanhado de alternativa equivalente, ou só login próprio.
5. Nada de compra digital por fora do IAP quando a regra exige (doc 06).
6. Privacidade e permissões com texto claro; ATT só se rastreia.
7. Conteúdo de usuário com denúncia e bloqueio.

Back-end da exclusão de conta e retenção legal: skill `security`, docs [03](../../security/docs/03-recuperacao-e-2fa.md) e [09](../../security/docs/09-lgpd-na-pratica.md).

## Combina com / alternativas

- UX por plataforma: skill `user-experience`, doc [13](../../user-experience/docs/13-ios-android-web.md).

## Decisão rápida

- **Passe pela tabela inteira se:** é o primeiro envio ou o app mudou de natureza.
- **Evite** responder à reprovação com texto genérico: cite a diretriz e o que mudou.
