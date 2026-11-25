# Que documentos um SaaS ou site precisa

> Saiba quais documentos públicos e contratuais o produto precisa ter, onde cada um aparece no sistema e quem escreve o quê, antes de abrir para o primeiro usuário.

| | |
|---|---|
| **Referência** | LGPD, Lei 13.709/2018, arts. 6, 9, 41 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); CDC, Lei 8.078/1990, arts. 6, 46 e 49; Decreto 7.962/2013, arts. 2 a 5 (comércio eletrônico); Marco Civil da Internet, Lei 12.965/2014, arts. 7, 13 e 15 |
| **Categoria** | Jurídico |
| **Tipo** | Mapa de documentos e de onde o sistema os mostra |
| **Vale para** | Site, SaaS B2C e B2B, app mobile com backend, vendidos no Brasil |
| **Verificado em** | 2026-11-25 |

> Este guia não substitui advogado. Ele explica o que existe e o que o sistema precisa mostrar e registrar. O texto final de cada documento é decisão jurídica da empresa.

## O que é

Um produto digital tem quatro grupos de documentos:

- **Públicos, para todo visitante:** política de privacidade, política de cookies, termos de uso e dados do encarregado.
- **Contratuais, para quem contrata:** contrato de SaaS (ou os termos aceitos no cadastro) e, em venda B2B com dado de terceiros, o contrato de operador.
- **De oferta, em venda pelo site:** preço, prazo, forma de cancelamento e arrependimento claros (Decreto 7.962/2013, art. 2 e 4).
- **Internos, que ninguém vê mas a lei pede:** registro das operações de tratamento (LGPD, art. 37), plano de incidente e lista de suboperadores.

## Por que usar

- **Transparência é obrigação:** o titular tem direito a informação facilitada sobre o tratamento (LGPD, art. 9).
- **Contrato que o cliente não pôde ler não vale:** o CDC (art. 46) não obriga o consumidor que não teve oportunidade de conhecer o conteúdo.
- **Cliente B2B pede:** compras de empresas grandes travam sem política, contrato de operador e lista de suboperadores.
- **Loja de apps e meios de pagamento** exigem política de privacidade com URL pública.

## Quando usar

- Antes do primeiro usuário real, mesmo em beta.
- Ao adicionar analytics, pixel, chat ou integração que recebe dado de pessoa.
- Ao começar a cobrar, vender para empresas ou aceitar menores de idade.

## Para que tipo de projeto

| Tipo de projeto | Documentos mínimos | Por quê |
|---|---|---|
| Site de conteúdo sem cadastro | Política de privacidade, política de cookies se houver analytics ou pixel | Coleta só formulário e métricas |
| Site com formulário de contato ou newsletter | Os dois acima, mais texto de finalidade junto ao formulário | A finalidade tem de estar clara onde o dado é pedido |
| Loja ou venda online ao consumidor | Termos de venda, privacidade, cookies, arrependimento, dados da empresa em destaque | CDC e Decreto 7.962/2013 |
| SaaS B2C (conta pessoal) | Termos de uso, privacidade, cookies, canal do titular | Consumidor e titular ao mesmo tempo |
| SaaS B2B | Termos ou contrato de SaaS, privacidade, contrato de operador, lista de suboperadores | O cliente é o controlador dos dados dos usuários dele |
| Sistema interno de uma empresa | Aviso de privacidade interno e política de uso | Dado de funcionário também é pessoal |
| App mobile | Os do SaaS, com URL pública para a loja | Apple e Google pedem link da política |
| Produto sem dado pessoal algum | Termos simples | Raro; confirme antes de pular a privacidade |

## Quando é bom

- **Documentos em URL fixa e versionados**, com data e número da versão (ver [05](05-aceite-versionado.md)).
- **Um mapa de dados real por trás da política** (ver [02](02-politica-de-privacidade-e-o-mapa-de-dados.md)).
- **Rodapé com todos os links**, o mesmo em todas as telas, inclusive a de login e a de cadastro.
- **Dono definido** para cada documento (quem revisa quando o produto muda).

## Quando é ruim

- **Copiar a política de outro site:** descreve dado que você não coleta e omite o que coleta; vira promessa falsa.
- **Gerador automático sem revisão:** serve de rascunho, não de documento final.
- **Documento que o produto não cumpre:** é pior que não ter, porque a promessa passa a ser provável de cobrar.
- **Documentos só em PDF** sem versão e sem data de vigência.

## Como começar

1. Liste os dados que o produto coleta e para quê (doc [02](02-politica-de-privacidade-e-o-mapa-de-dados.md)).
2. Marque o tipo de venda: consumidor (CDC), empresa (contrato) ou os dois.
3. Use a matriz abaixo para ver o que falta.

| Documento | Onde aparece no sistema | Doc |
|---|---|---|
| Política de privacidade | Rodapé, cadastro, formulários, loja de apps | [02](02-politica-de-privacidade-e-o-mapa-de-dados.md) |
| Termos de uso e contrato | Cadastro, checkout, link no rodapé | [03](03-termos-de-uso-e-contrato-de-saas.md) |
| Política de cookies e banner | Primeira visita e rodapé | [04](04-cookies-aviso-categorias-e-consentimento.md) |
| Registro de aceite | Banco de dados e tela de histórico | [05](05-aceite-versionado.md) |
| Canal do titular e encarregado | Rodapé, política, área da conta | [06](06-direitos-do-titular-e-canal-do-encarregado.md) |
| Contrato de operador e suboperadores | Venda B2B, página de confiança | [07](07-contrato-de-operador-b2b-e-suboperadores.md) |

4. Em venda pelo site, mostre em destaque razão social, CNPJ, endereço e contatos, o preço total com despesas extras e a forma de cancelar (Decreto 7.962/2013, art. 2 e 4).
5. Pergunte a um advogado o que a tabela não cobre ([doc 08](08-quando-procurar-advogado.md)).

## Combina com / alternativas

- Mapa de dados e LGPD no banco: [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).
- O que o sistema constrói para cumprir a LGPD: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Regras de cancelamento e cobrança do produto: skill `product`.
- Telas de aceite e banner: skill `design-systems`.
- Alternativa a escrever tudo do zero: modelo de escritório de advocacia especializado em tecnologia, adaptado ao produto.

## Decisão rápida

- **Use se:** o sistema vai ter usuário real, cadastro, cobrança ou qualquer dado de pessoa.
- **Evite se:** a ideia é publicar texto copiado só para "ter o link"; sem advogado e sem mapa de dados, o documento mente.
