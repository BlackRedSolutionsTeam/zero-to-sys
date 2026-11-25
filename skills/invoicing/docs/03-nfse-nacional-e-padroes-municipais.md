# NFS-e nacional e padrões municipais

> A NFS-e passa a ter um padrão único nacional, mas cada município ainda escolhe como emite; confirme o do seu cliente e deixe o emissor tratar a diferença.

| | |
|---|---|
| **Referência** | https://www.gov.br/nfse, https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica, https://doc.focusnfe.com.br (NFSe Nacional) |
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

Conferidas em 2026-11-25 em notícias que reproduzem o Ato Conjunto RFB/CGIBS nº 7/2026 (publicado no DOU em 13/11/2026, em vigor na publicação). Leia o ato no site do CGIBS antes de fixar uma data com o cliente.

| O que | Data |
|---|---|
| Municípios devem autorizar emissão no padrão nacional | 1º de janeiro de 2026 |
| NFS-e Via | 3 de agosto de 2026 (sem alteração) |
| Serviços gerais de ISS, destaque de IBS e CBS | 1º de outubro de 2026 (sem alteração) |
| Locação de bens, condomínio, bens imateriais fora da LC 116 e demais hipóteses | 1º de janeiro de 2027 |
| Plataformas digitais, subitens 1.03, 1.05 e 1.09 da LC 116 e transporte coletivo municipal (16.01) | 1º de março de 2027 |
| Simples Nacional | Parte em 1º de janeiro e parte em 1º de março de 2027 |

A obrigação do MEI emitir no padrão nacional vale desde 1º de setembro de 2023 para serviço a pessoa jurídica. Para ME e EPP do Simples Nacional, as fontes divergem entre novembro e setembro de 2026 (Resoluções CGSN 191 e 189 de 2026): confirme com o contador.

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
| Prazo da reforma | Peça a data ao contador e confirme no site do CGIBS |
