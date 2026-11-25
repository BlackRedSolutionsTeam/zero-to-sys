# Contas: Apple Developer e Google Play

> Sem as duas contas pagas não há app nas lojas; a de organização exige D-U-N-S e leva dias, então abra as contas antes de terminar o app.

| | |
|---|---|
| **Referência** | https://developer.apple.com/programs/enroll/, https://support.google.com/googleplay/android-developer/answer/6112435, https://support.google.com/googleplay/android-developer/answer/14151465 |
| **Categoria** | Conta e identidade |
| **Tipo** | Cadastro e verificação |
| **Vale para** | App Expo, Flutter ou nativo que vai para a App Store e a Play Store |
| **Verificado em** | 2026-11-25 |

## O que é

Cada loja exige uma conta de desenvolvedor. O nome da conta aparece como vendedor do app: na Apple, o nome legal da organização; no Google, o nome do desenvolvedor da ficha.

| | Apple Developer Program | Google Play Console |
|---|---|---|
| Custo | US$ 99 por ano (o valor pode variar por região e aparece na moeda local na inscrição) | US$ 25, pagos uma única vez |
| Pessoa física | Sim | Sim, com teste fechado obrigatório se criada depois de 13/11/2023 |
| Organização | D-U-N-S obrigatório, site público, e-mail do domínio da empresa | D-U-N-S obrigatório; exigida para algumas categorias (financeiro, saúde, VPN, governo) |
| Isenção | Sem fins lucrativos, ensino credenciado e governo (fee waiver) | Não há |
| Cartão | Cobrado após a verificação | Visa, Mastercard, American Express; pré-pago não aceito |

## Por que usar

- A conta de organização separa o app do CPF do dono: o vendedor é a empresa e a conta sobrevive à saída de uma pessoa.
- Apple e Google validam identidade antes de liberar a publicação, então começar cedo evita travar o lançamento.

## Quando usar

- No começo do projeto, em paralelo ao desenvolvimento.
- Antes de gerar o primeiro build assinado, porque certificados e chaves nascem na conta.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| App de uma empresa | ✅ Ótimo | Conta de organização, com a empresa como vendedora |
| App de agência para cliente | ✅ Ótimo | Conta do cliente, com a agência como membro; evita transferência depois |
| Projeto pessoal ou MVP solo | 🟡 Serve | Pessoa física; na Google, 12 testadores por 14 dias antes da produção |
| App de finanças, saúde, VPN ou governo | ✅ Ótimo | Na Google exige organização |
| App só para a equipe da empresa | ❌ Evite | Distribuição privada (Apple Business Manager, Play privado) é outro caminho, fora desta skill |

## Quando é bom

- **Apple (organização):** exige entidade legal (sem DBA, nome fantasia ou filial), D-U-N-S de nove dígitos, site público funcionando e e-mail do domínio da empresa; quem se inscreve precisa ter poder de vincular a empresa a contratos (developer.apple.com/programs/enroll, 2026-11-25).
- **Google (pessoal, criada depois de 13/11/2023):** Produção e pré-registro ficam desativados até um teste fechado com pelo menos 12 testadores inscritos de forma contínua por 14 dias; o pedido de produção leva em geral até 7 dias de análise (support.google.com/googleplay/android-developer/answer/14151465, 2026-11-25).
- **Google (verificação de desenvolvedor):** a partir de 30/09/2026 o Brasil está entre os primeiros países em que apps só instalam em aparelhos certificados se o desenvolvedor estiver registrado e verificado, mesmo fora da Play Store. Registre o app no Play Console ou no Android Developer Console.

## Quando é ruim

- **D-U-N-S** é emitido pela Dun & Bradstreet e pode levar dias ou semanas; a página da Apple não informa prazo de aprovação.
- **Nome da conta** não muda fácil: o nome legal digitado na inscrição vira o vendedor.
- **Conta pessoal na Google** atrasa o primeiro lançamento em pelo menos 14 dias.
- **Taxa não é reembolsada** na Google se os dados da verificação forem inválidos.

## Como começar

Ordem recomendada:

1. Defina quem é o dono legal do app (empresa ou pessoa) e o e-mail de domínio próprio.
2. Peça ou consulte o D-U-N-S da empresa (developer.apple.com/enroll/duns-lookup).
3. Ative 2FA na Apple Account e na conta Google que será a dona.
4. Inscreva-se na Apple e na Google no mesmo dia; guarde o comprovante.
5. Na Google com conta pessoal, recrute os 12 testadores já na primeira semana (doc [03](03-builds-e-envio-eas-submit-testflight-play.md)).
6. Dê acesso aos demais como membros (Users and Access na Apple, Users and permissions na Google), nunca compartilhe a senha da conta dona.

## Combina com / alternativas

- Privacidade: skill `legal`, doc [02](../../legal/docs/02-politica-de-privacidade-e-o-mapa-de-dados.md); LGPD: skill `security`, doc [09](../../security/docs/09-lgpd-na-pratica.md).
- Cadastro de CNPJ e domínio: skill `domains`.
- Alternativa para app interno: distribuição privada das lojas, fora do escopo.

## Decisão rápida

- **Use conta de organização se:** há empresa, ou o app é de finanças, saúde, VPN ou governo.
- **Use conta pessoal se:** é projeto solo e você aceita os 14 dias de teste na Google.
- **Evite** publicar com a conta pessoal de um desenvolvedor contratado: a transferência depois é trabalhosa.
