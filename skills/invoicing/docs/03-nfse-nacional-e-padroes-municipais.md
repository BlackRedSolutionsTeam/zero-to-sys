# NFS-e nacional e padrões municipais

> A NFS-e passa a ter um padrão único nacional, mas cada município ainda escolhe como emite; confirme o do seu cliente e deixe o emissor tratar a diferença.

| | |
|---|---|
| **Referência** | https://www.gov.br/nfse, https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica, https://doc.focusnfe.com.br (NFSe Nacional), Ato Conjunto RFB/CGIBS nº 4/2026 e nº 7/2026 (cgibs.gov.br), Resolução CGSN nº 191/2026 |
| **Categoria** | Regra fiscal |
| **Tipo** | Padrão de emissão de nota de serviço |
| **Vale para** | Empresas de serviço (SaaS, clínica, agência, escola, consultoria) |
| **Verificado em** | 2026-11-25 |

## O que é

Cada prefeitura criou o próprio sistema de NFS-e, com layout e regras diferentes. O **padrão nacional** é um leiaute único, com o **ADN (Ambiente de Dados Nacional)** guardando todas as notas e um emissor web gratuito no gov.br. Um município pode:

- **aderir ao padrão nacional emitindo no portal nacional;** ou
- **manter sistema próprio e compartilhar os dados** com a plataforma nacional.

Integrar-se ao padrão nacional não equivale a emitir por ele: só quando o município libera a emissão direta a empresa gera a nota no padrão nacional sem passar pelo portal municipal.

## Por que usar

- **Um leiaute só:** menos variação por prefeitura, e é isso que os emissores por API absorvem.
- **MEI:** emite pelo gov.br, de graça.
- **Reforma tributária:** IBS e CBS entram primeiro no leiaute nacional.

## Quando usar

- Antes de escolher o emissor, para checar se o município do cliente aceita o padrão nacional.
- Ao receber uma rejeição de município com sistema próprio.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| SaaS com clientes em vários municípios | ✅ Ótimo | O emissor cobre padrão nacional e municipais pela mesma API |
| Sistema interno de uma só empresa | ✅ Ótimo | Um município, um padrão; fácil de validar |
| MEI prestador de serviço | ✅ Ótimo | Emissor web do gov.br, sem custo |
| Município com sistema próprio sem integração | 🟡 Serve | Emite pelo emissor por API que suporte aquela prefeitura |
| Venda de produto | ❌ Evite | NFS-e é só serviço; veja o [doc 01](01-qual-nota-emitir.md) |

## Quando é bom

- **Municípios aderindo:** a lei da reforma tributária (LC 214/2025) obriga municípios e o Distrito Federal a autorizarem a emissão no padrão nacional a partir de 1º de janeiro de 2026 (material da Receita Federal); a lista de aderentes passava de mil e quatrocentos municípios em notícia recente, sem número oficial fixo.
- **Webhook e XML iguais:** no emissor, a rota de NFS-e nacional (`nfsen` no Focus NFe) devolve o mesmo tipo de status.
- **Recebimento:** o Focus NFe também recebe NFS-e nacionais emitidas contra o seu CNPJ.

## Quando é ruim

- **Município que ainda não libera a emissão direta:** a nota sai no portal municipal, com os layouts de lá.
- **Cronograma da reforma muda:** o Ato Conjunto RFB/CGIBS nº 7/2026 adiou prazos de destaque de IBS e CBS na NFS-e (veja abaixo); não codifique data fixa.
- **Dados do cliente errados:** código de serviço e item da LC 116 errados geram rejeição ou imposto errado.

## Como começar

### Datas que importam

Conferidas em 2026-11-25 no texto do Ato Conjunto RFB/CGIBS nº 7, de 11/11/2026 (publicado no site do CGIBS, em vigor na publicação), que altera o Ato Conjunto RFB/CGIBS nº 4, de 30/07/2026. Os dois PDFs foram lidos no site do CGIBS (cgibs.gov.br). A data vale para os fatos geradores a partir dela.

| O que (NFS-e, destaque de IBS e CBS) | Data |
|---|---|
| Serviços sujeitos ao ISS na lista da LC 116 que não caem nas linhas abaixo (Ato 4, art. 1º, III, "d", sem alteração pelo Ato 7) | 1º de outubro de 2026 |
| Plataformas digitais (LC 214/2025, art. 22, § 1º, e §§ 12 a 14) | 1º de março de 2027 (era 1º/12/2026) |
| Subitens 1.03, 1.05 e 1.09 da LC 116 | 1º de março de 2027 (era 1º/12/2026) |
| Subitem 16.01 da LC 116 (transporte coletivo municipal) | 1º de março de 2027 (era 1º/12/2026) |
| Bens imateriais fora da LC 116 e fora do ICMS | 1º de janeiro de 2027 (era 1º/12/2026) |
| Taxas e outras receitas de condomínio edilício | 1º de janeiro de 2027 (era 1º/12/2026) |
| Locações de bens móveis e locações, cessões onerosas e arrendamentos de imóveis | 1º de janeiro de 2027 (era 1º/12/2026) |
| Demais fornecimentos de serviços | 1º de janeiro de 2027 (era 1º/12/2026) |
| Optantes do Simples Nacional | 1º de janeiro de 2027 para as hipóteses "d" a "h" e 1º de março de 2027 para as demais (§ 1º do art. 1º, nova redação) |
| NFS-e Via (Ato 4, inciso XIII) | 3 de agosto de 2026 |

Pelo texto do Ato 4, o Simples Nacional tinha 1º de janeiro de 2027 para tudo; o Ato 7 passou as hipóteses "a" a "c" (plataformas, 1.03, 1.05, 1.09 e 16.01) para 1º de março de 2027. Ainda é lido pelo texto, mas confirme no site do CGIBS se houve ato posterior a 2026-11-25.

Em 2026-11-25 não foi lida uma orientação da CGNFS-e sobre rejeição pelo sistema nacional enquanto o IBS e a CBS não são informados; se o seu fluxo depende disso, leia a nota técnica vigente do portal gov.br/nfse.

### Obrigação de usar o padrão nacional

- **Municípios:** a LC 214/2025 obriga municípios e o Distrito Federal a autorizarem a emissão no padrão nacional a partir de 1º de janeiro de 2026 (material da Receita Federal, não relido nesta revisão); não há número oficial fixo de municípios aderentes.
- **MEI:** vale desde 1º de setembro de 2023 para serviço a pessoa jurídica.
- **ME e EPP do Simples Nacional:** a Resolução CGSN nº 191, de 04/08/2026 (DOU 10/08/2026), altera o art. 59 da Resolução CGSN 140/2018: a ME ou EPP optante usa obrigatoriamente a NFS-e de padrão nacional emitida pelo Emissor Nacional, por emissor web ou por API (§ 1º), com efeitos do art. 1º a partir de **1º de novembro de 2026**. O art. 2º revoga a Resolução CGSN 189/2026, que previa 1º de setembro de 2026; a divergência entre as fontes vinha dessa troca. O texto lido foi a "visão multivigente" do portal do Simples, que informa não substituir o publicado no DOU. A Resolução CGSN 190/2026 (IBS e CBS no Simples) não foi lida; confirme com o contador.

### Emitir NFS-e nacional pelo Focus NFe

A documentação do Focus lista a rota `nfsen` para emitir (DPS, a declaração do prestador), consultar, cancelar e reenviar e-mail; o cancelamento é síncrono. O corpo segue o leiaute nacional; veja os campos obrigatórios em "NFSe Nacional" na documentação deles.

```bash
curl -u "$FOCUS_TOKEN:" -X POST "https://homologacao.focusnfe.com.br/v2/nfsen?ref=pedido-123" \
  -H "Content-Type: application/json" \
  -d @dps.json
```

Em homologação, valide o JSON e a resposta antes de mudar o token e a URL para produção.

### Padrão municipal

Para município fora do padrão nacional, use a rota de NFS-e comum (`nfse`); o emissor monta o layout daquela prefeitura. Os campos variam (código tributário municipal, retenção, item da LC 116); a documentação do emissor diz o que cada município exige.

```bash
curl -u "$FOCUS_TOKEN:" -X POST "https://homologacao.focusnfe.com.br/v2/nfse?ref=pedido-123" \
  -H "Content-Type: application/json" \
  -d @nfse.json
```

## Decisão rápida

| Situação | O que fazer |
|---|---|
| MEI com poucas notas | Emissor web do gov.br |
| Município libera emissão nacional | Rota de NFS-e nacional do emissor |
| Município com sistema próprio | Rota municipal do emissor |
| Não sabe qual é | Consulte o município no portal gov.br/nfse e teste em homologação |
| Prazo da reforma | Leia a tabela deste doc, confirme no site do CGIBS se saiu ato novo e guarde a data em configuração, não no código |
