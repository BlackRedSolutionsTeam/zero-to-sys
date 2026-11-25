---
name: legal
description: 'Guia o lado jurídico de um produto digital no Brasil sem substituir advogado: política de privacidade, termos de uso, contrato de SaaS, cookies, aceite versionado, direitos do titular e contrato de operador. Use quando pedirem "política de privacidade", "termos de uso" ou "banner de cookies".'
---

# legal

Guia para quem precisa dos documentos e dos registros jurídicos do produto: o que existe, o que o sistema precisa mostrar e onde guardar o aceite. **Não substitui advogado.** Os docs trazem modelos de estrutura, não texto jurídico pronto; o texto final, a base legal e as cláusulas de responsabilidade são decisão do advogado e da empresa. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim, exemplos e decisão rápida.

## Como usar esta skill

1. **Descubra o que o produto precisa** ([doc 01](docs/01-documentos-que-um-saas-ou-site-precisa.md)): site, loja, SaaS B2C ou B2B, app.
2. **Monte o mapa de dados** e escreva a política a partir dele ([doc 02](docs/02-politica-de-privacidade-e-o-mapa-de-dados.md)).
3. **Defina termos e contrato** com o que o sistema consegue cumprir ([doc 03](docs/03-termos-de-uso-e-contrato-de-saas.md)).
4. **Se há analytics, pixel ou terceiros no site**, classifique os cookies e monte o banner ([doc 04](docs/04-cookies-aviso-categorias-e-consentimento.md)).
5. **Registre o aceite por versão** ([doc 05](docs/05-aceite-versionado.md)).
6. **Abra o canal do titular** e decida o encarregado ([doc 06](docs/06-direitos-do-titular-e-canal-do-encarregado.md)).
7. **Venda B2B com dado de terceiros?** Contrato de operador e lista de suboperadores ([doc 07](docs/07-contrato-de-operador-b2b-e-suboperadores.md)).
8. **Leve tudo a um advogado** antes de publicar ([doc 08](docs/08-quando-procurar-advogado.md)).

## Qual documento por tipo de produto

| Produto | Documentos |
|---|---|
| Site de conteúdo | Privacidade, cookies (se houver analytics ou pixel) |
| Loja online | Termos de venda, privacidade, cookies, arrependimento |
| SaaS B2C | Termos, privacidade, cookies, aceite versionado, canal do titular |
| SaaS B2B | Termos ou contrato, privacidade, contrato de operador, suboperadores |
| App mobile | Os do SaaS, com URL pública da política |
| Sistema interno | Aviso de privacidade e política de uso |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Documentos necessários | [docs/01-documentos-que-um-saas-ou-site-precisa.md](docs/01-documentos-que-um-saas-ou-site-precisa.md) | Matriz por tipo de projeto |
| Política de privacidade | [docs/02-politica-de-privacidade-e-o-mapa-de-dados.md](docs/02-politica-de-privacidade-e-o-mapa-de-dados.md) | Inventário de dados e estrutura da política |
| Termos e contrato | [docs/03-termos-de-uso-e-contrato-de-saas.md](docs/03-termos-de-uso-e-contrato-de-saas.md) | Cláusulas e o que o sistema suporta |
| Cookies | [docs/04-cookies-aviso-categorias-e-consentimento.md](docs/04-cookies-aviso-categorias-e-consentimento.md) | Categorias, banner e consentimento |
| Aceite versionado | [docs/05-aceite-versionado.md](docs/05-aceite-versionado.md) | Tabelas, fluxo de nova versão |
| Direitos do titular | [docs/06-direitos-do-titular-e-canal-do-encarregado.md](docs/06-direitos-do-titular-e-canal-do-encarregado.md) | Canal, fila, prazos, encarregado |
| Contrato de operador | [docs/07-contrato-de-operador-b2b-e-suboperadores.md](docs/07-contrato-de-operador-b2b-e-suboperadores.md) | DPA, suboperadores, transferência internacional |
| Advogado | [docs/08-quando-procurar-advogado.md](docs/08-quando-procurar-advogado.md) | Gatilhos e pacote para levar |

## Checklist

- [ ] Política de privacidade em URL fixa, com data e versão, linkada no rodapé e no cadastro, baseada no mapa de dados.
- [ ] Termos de uso e, se houver venda, regras de cancelamento, arrependimento e reembolso que o sistema realmente cumpre.
- [ ] Nenhuma tag não necessária baseada em consentimento (anúncio, pixel, analytics com perfil) carrega antes do aceite; o primeiro nível do banner tem "Rejeitar cookies não necessários" com o mesmo destaque de aceitar; há link "Preferências de cookies" no rodapé.
- [ ] Aceite gravado por usuário, documento e versão, sem edição de linhas antigas.
- [ ] Canal do titular público, com prazo e responsável; encarregado indicado ou dispensa decidida com o advogado.
- [ ] Lista de suboperadores atualizada, com país, e contrato de operador nos clientes B2B.
- [ ] Documentos revisados por advogado antes do primeiro usuário real, com a data da revisão anotada.

## Regras de uso

- **Não substitui advogado.** Diga isso ao usuário; nunca entregue texto de cláusula como pronto para publicar.
- **O sistema cumpre o que o documento diz.** Cláusula sem recurso correspondente (cancelar, exportar, apagar) é promessa falsa.
- **Fonte oficial e data.** Artigos, resoluções e guias da ANPD conferidos com data; quando só houve resumo de terceiros, o doc diz.
- **Sem texto copiado de outro site.** Modelo de estrutura, sim; texto alheio, não.
- **Fronteiras.** Dado no banco, retenção e auditoria são da `data`; rotas do titular, incidente e criança, da `security`; regras de plano e cobrança, da `product`; telas de aceite e banner, da `design-systems`; e-mails transacionais, da `integrations`.

## Quando a lista não cobre

Regulação setorial (saúde, financeiro, jogos, educação), contratos societários, propriedade intelectual, trabalhista, tributário e nota fiscal ficam fora desta skill. Diga ao usuário que isso é com advogado ou contador especializado.

## Validade dos dados

Leis, resoluções e guias da ANPD foram conferidos em 2026-11-25 (guia de cookies da ANPD, v1.0 de out/2022, lido inteiro no PDF oficial; Resolução CD/ANPD nº 18/2024 no DOU; nº 2/2022 e nº 19/2024 no gov.br/anpd; LGPD e Lei 15.211/2025 no texto atualizado da Câmara dos Deputados, porque o Planalto não respondeu). Os demais docs podem ter conferência própria. A regulamentação dos direitos dos titulares estava em elaboração na agenda 2025-2026. Cada documento tem a linha "Verificado em".
