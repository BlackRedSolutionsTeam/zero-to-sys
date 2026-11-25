# Quando procurar advogado

> Use os modelos desta skill para chegar ao advogado com o trabalho feito; procure-o antes de publicar, de vender para empresa grande e sempre que a lei muda o produto.

| | |
|---|---|
| **Referência** | LGPD, arts. 7, 11, 14, 33, 41, 42 e 48 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); CDC, art. 51; Lei 15.211/2025, ECA Digital, em vigor desde 17/03/2026, fiscalizada pela ANPD (conferida por notícias e páginas do Senado e da ANPD, não no texto da lei); Resolução CD/ANPD nº 15/2024 (incidente) |
| **Categoria** | Jurídico |
| **Tipo** | Lista de gatilhos e preparação para a conversa |
| **Vale para** | Qualquer produto digital vendido no Brasil |
| **Verificado em** | 2026-11-25 |

> Esta skill não substitui advogado e não dá parecer. Este documento existe para dizer quando o texto de um modelo deixa de bastar.

## O que é

Uma lista dos momentos em que a decisão é jurídica, não técnica, e do que levar para a conversa. Procure advogado ou escritório com prática em direito digital e proteção de dados; para tributos e nota fiscal, contador.

## Por que usar

- **Uma decisão errada custa mais** que a consulta: multa, ação de consumidor, perda de contrato.
- **Quem responde pelo dano é a empresa** (LGPD, art. 42), não o modelo copiado.
- **Chega preparado:** com inventário, fluxos e perguntas, a hora do advogado rende.

## Quando usar

Procure advogado:

| Situação | Por quê |
|---|---|
| Antes de publicar política, termos e contrato pela primeira vez | Texto final e base legal de cada tratamento (LGPD, arts. 7 e 11) |
| Tratar dado sensível (saúde, biometria, origem, religião) | Regras mais estritas (art. 11) |
| Público com crianças e adolescentes | Consentimento do responsável (art. 14) e o ECA Digital, vigente desde 17/03/2026 |
| Vender a empresa grande, saúde, financeiro ou governo | Contratos próprios, auditoria, cláusulas de responsabilidade |
| Guardar dado ou usar fornecedor fora do Brasil | Mecanismo do art. 33 e cláusulas-padrão da ANPD |
| Incidente de segurança com dado pessoal | Comunicação à ANPD e ao titular (art. 48) com prazo curto; ver skill `security` |
| Pedido ou reclamação de titular que você não sabe responder | Prazo corre (art. 19) |
| Notificação da ANPD, do Procon ou ação judicial | Prazo e defesa |
| Mudar o uso do dado (nova finalidade, venda de dados, IA treinada com dados dos usuários) | Base legal e aviso novo |
| Decidir encarregado, dispensa de pequeno porte e relatório de impacto | Resolução da ANPD tem exceções |
| Marketplace, pagamento próprio, split, criptoativos, jogos de azar | Regulação setorial |
| Marca, domínio e propriedade intelectual | Registro e conflito |
| Contrato com sócios, funcionários e freelancers que escrevem o código | Titularidade do código e confidencialidade |

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo simples | 🟡 Serve | Revisão pontual da política e do banner |
| MVP de SaaS | ✅ Ótimo | Revisão dos documentos antes de cobrar |
| SaaS B2B em crescimento | ✅ Ótimo | Contrato de operador e negociação de contratos |
| Saúde, financeiro, educação infantil | ✅ Ótimo | Regras mais rígidas desde o início |
| Protótipo sem usuário real | ❌ Evite | Gaste depois, antes do primeiro usuário real |

## Quando é bom

- **Contratar uma vez e manter:** revisão inicial e consulta avulsa na mudança.
- **Levar tudo pronto:** inventário de dados, fluxo do sistema, lista de suboperadores, cópia dos documentos atuais e dúvidas escritas.
- **Pedir parecer por escrito** nas decisões importantes (base legal, dispensa, transferência).

## Quando é ruim

- **Esperar a notificação chegar** para procurar.
- **Pedir ao advogado para escrever sem explicar o produto:** sai texto genérico.
- **Tratar o parecer como eterno:** lei, regulamento da ANPD e produto mudam.
- **Pagar por texto que o sistema não cumpre.**

## Como começar

**1. Prepare o pacote** (produzido pelos docs desta skill):

- Mapa de dados e lista de cookies (docs [02](02-politica-de-privacidade-e-o-mapa-de-dados.md) e [04](04-cookies-aviso-categorias-e-consentimento.md)).
- Documentos atuais e fluxo de cadastro e cobrança (docs [01](01-documentos-que-um-saas-ou-site-precisa.md) e [03](03-termos-de-uso-e-contrato-de-saas.md)).
- Lista de suboperadores e países (doc [07](07-contrato-de-operador-b2b-e-suboperadores.md)).
- Como o sistema atende o titular (doc [06](06-direitos-do-titular-e-canal-do-encarregado.md)).
- Plano de incidente (skill `security`).

**2. Perguntas para levar:**

1. Qual a base legal de cada linha do inventário?
2. Precisamos indicar encarregado ou nos enquadramos como agente de pequeno porte?
3. Como o consentimento deve ser colhido e provado?
4. Qual o prazo para guardar aceites, logs e dados fiscais?
5. Os fornecedores no exterior exigem qual mecanismo de transferência?
6. As cláusulas de cancelamento, reembolso e limite de responsabilidade estão de acordo com o CDC?
7. Qual texto devo mostrar ao menor de idade e ao responsável?
8. Precisamos de relatório de impacto?

**3. Depois da revisão:** atualize os documentos, publique a versão nova (doc [05](05-aceite-versionado.md)), registre a data no mapa de dados e marque a próxima revisão (a cada ano ou a cada mudança grande de produto).

## Combina com / alternativas

- Incidente e prazos: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Dados no banco: [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).
- Alternativa de custo menor: orientação de entidades como Sebrae ou associação de startups para a base; ainda assim o texto final precisa de revisão.
- Este doc não cobre tributos, nota fiscal e registro de empresa: contador.

## Decisão rápida

- **Use se:** o produto vai ter usuário real, dado sensível, criança, empresa grande ou fornecedor no exterior.
- **Evite se:** o produto ainda é protótipo sem usuário e sem dado real; adie a consulta, não a preparação.
