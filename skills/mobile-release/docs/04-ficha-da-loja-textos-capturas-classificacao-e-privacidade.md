# Ficha da loja: textos, capturas, classificação etária e privacidade

> A ficha incompleta ou que não bate com o app é o motivo mais simples de reprovação; preencha tudo antes de pedir revisão.

| | |
|---|---|
| **Referência** | https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications, https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions, https://support.google.com/googleplay/android-developer/answer/9866151, https://support.google.com/googleplay/android-developer/answer/10787469 |
| **Categoria** | Ficha da loja |
| **Tipo** | Checklist de metadados |
| **Vale para** | Qualquer app publicado na App Store e na Play Store |
| **Verificado em** | 2026-11-25 |

## O que é

Os dados que o usuário e a revisão veem: nome, descrições, ícone, capturas de tela, categoria, classificação etária, política de privacidade e declaração de dados coletados.

## Por que usar

- A Apple exige metadados completos, URLs funcionais e sem texto de exemplo (diretriz 2.1) e que reflitam o app com precisão (2.3).
- A declaração de privacidade errada gera reprovação e pode derrubar o app depois.

## Quando usar

- Antes do primeiro envio à revisão e a cada versão que muda dados coletados ou conteúdo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App com conta de usuário | ✅ Ótimo | Pede política de privacidade, exclusão de conta e conta demo para a revisão |
| App com conteúdo gerado por usuário | ✅ Ótimo | Exige denúncia, bloqueio e filtro (Apple 1.2) |
| App sem coleta de dados | 🟡 Serve | Ainda precisa de política de privacidade e da declaração "não coleta" |

## Quando é bom

- **Apple, capturas:** de 1 a 10 por tamanho, `.jpeg`, `.jpg` ou `.png`, sem transparência; obrigatório pelo menos um tamanho de iPhone com Dynamic Island (display médio, por exemplo 1179x2556) e, se o app roda em iPad, um de 13 polegadas (2064x2752 ou 2048x2732). Enviando o maior tamanho, a Apple reduz para os demais (2026-11-25).
- **Google, gráficos:** ícone 512x512 PNG (até 1024 KB), imagem de destaque 1024x500, de 2 a 8 capturas de telefone com lados entre 320 e 3.840 px; nome do app de até 30 caracteres, descrição curta de até 80 e descrição completa de até 4.000 (support.google.com/googleplay/android-developer/answer/9859152, lida em 2026-11-25; caracteres de largura total e meia largura contam igual; evite repetição de palavras-chave, que pode levar à suspensão do app). Para recomendações com destaque, no mínimo 4 capturas de 1080 px ou mais (support.google.com/googleplay/android-developer/answer/9866151, 2026-11-25).
- **Apple, faixas etárias:** 4+, 9+, 13+, 16+ e 18+; o desenvolvedor responde ao questionário no App Store Connect (UGC, mensagens, navegação web, jogos de azar, loot box, controles parentais). Quem não respondeu às novas perguntas até 31/01/2026 ficou impedido de enviar atualizações. No Brasil há valores específicos de classificação.
- **Google, Data safety:** obrigatório para todo app, com política de privacidade mesmo se não coleta dados; inclui o que os SDKs de terceiros coletam e se há mecanismo de exclusão.

## Quando é ruim

- **Capturas que não mostram o app real** reprovam por metadados enganosos.
- **Rótulo de privacidade desatualizado** depois de adicionar SDK de analytics ou anúncios.
- **Classificação etária baixa demais** para app com chat ou conteúdo de usuário.
- **ECA Digital (Lei 15.211/2025, em vigor desde 17/03/2026):** o app que pode ser usado por crianças e adolescentes deve considerar o sinal de faixa etária que as lojas fornecem por API (a Apple expõe a Declared Age Range API no Brasil). Confira o texto da lei e a ANPD antes de definir o público; política de privacidade na skill `legal`, doc [02](../../legal/docs/02-politica-de-privacidade-e-o-mapa-de-dados.md), e LGPD na skill `security`, doc [09](../../security/docs/09-lgpd-na-pratica.md).

## Como começar

Checklist da ficha:

1. Nome, subtítulo e descrição com o que o app faz de verdade, sem comparar com outros apps nem citar outra plataforma.
2. Ícone sem cantos arredondados desenhados (a loja aplica a máscara) e sem transparência no iOS.
3. Capturas reais, uma por fluxo principal, no idioma da loja (pt-BR).
4. URL da política de privacidade pública, também acessível dentro do app (Apple 5.1.1(i)).
5. URL de suporte e e-mail de contato que respondem.
6. Questionário de classificação etária respondido na Apple e na Google (IARC).
7. Data safety e rótulos de privacidade (App Privacy) iguais ao que o app e os SDKs coletam.
8. Conta demo com dados de exemplo e back-end ligado, informada nas notas para a revisão (Apple 2.1).
9. Para exclusão de conta, URL web de solicitação na Data safety (doc [05](05-regras-de-revisao-que-mais-reprovam.md)).

Telas de loja bonitas: skill `design-systems` (tipo "app mobile").

## Combina com / alternativas

- Política de privacidade: skill `legal`, doc [02](../../legal/docs/02-politica-de-privacidade-e-o-mapa-de-dados.md); LGPD: skill `security`, doc [09](../../security/docs/09-lgpd-na-pratica.md).
- Ferramentas de capturas: Fastlane `snapshot`/`deliver`, ou capturas do simulador.

## Decisão rápida

- **Revise a ficha inteira se:** o app ganhou SDK, login social, chat ou pagamento.
- **Evite** copiar a descrição de concorrente ou prometer funções que ainda não existem.
