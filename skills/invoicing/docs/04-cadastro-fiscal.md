# Cadastro fiscal

> Guarde no cadastro tudo o que a nota exige e valide antes de emitir: dado fiscal errado vira rejeição ou imposto errado.

| | |
|---|---|
| **Referência** | https://www.gov.br/receitafederal (NCM), https://concla.ibge.gov.br (CNAE), https://www.confaz.fazenda.gov.br (CFOP, ajustes SINIEF), https://www.gov.br/nfse (Lista de Serviços da LC 116/2003) |
| **Categoria** | Dados |
| **Tipo** | Modelagem do cadastro de cliente, produto e serviço para nota fiscal |
| **Vale para** | Qualquer sistema que emite NFS-e, NF-e ou NFC-e |
| **Verificado em** | 2026-11-25 |

## O que é

Antes de emitir, o sistema precisa de dados que não existem num cadastro comum:

- **Cliente (tomador ou destinatário):** CPF ou CNPJ, nome ou razão social, endereço completo com código IBGE do município, e-mail, inscrição estadual quando contribuinte de ICMS.
- **Produto:** **NCM** (código de 8 dígitos da mercadoria), unidade, origem e tributação (ICMS, PIS, COFINS).
- **Operação:** **CFOP** (código da natureza da operação, por exemplo venda dentro ou fora do estado).
- **Serviço:** item da lista da LC 116/2003, código tributário do município, **alíquota de ISS** e se há retenção.
- **Empresa:** **CNAE** (atividade econômica), regime, inscrições ([doc 01](01-qual-nota-emitir.md)).

## Por que usar

- **Menos rejeição:** a maioria das rejeições é dado fiscal inválido, não erro de código.
- **Uma regra por item:** o catálogo diz como cada item é tributado, em vez de decidir na hora da venda.
- **Reforma tributária:** IBS e CBS ganham campos na NF-e e na NFS-e; um cadastro bem modelado absorve isso.

## Quando usar

- Ao modelar o cadastro de clientes e do catálogo.
- Ao ver rejeição por CNPJ, NCM, CFOP ou código de serviço.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Loja virtual | ✅ Ótimo | Cada produto precisa de NCM, origem e tributação |
| SaaS B2B | ✅ Ótimo | Cliente pessoa jurídica exige CNPJ válido e endereço fiscal |
| SaaS B2C com serviço | 🟡 Serve | Muitas vezes CPF e e-mail bastam; confira a regra do município |
| Sistema interno | ✅ Ótimo | Poucos itens, regras estáveis |
| MEI | 🟡 Serve | Poucos campos |
| Site de conteúdo | ❌ Evite | Sem venda |

## Quando é bom

- **Validar na entrada:** CPF, CNPJ e CEP validados no cadastro, não na emissão.
- **Consulta de CNPJ e CEP:** preenche o endereço e reduz erro de digitação.
- **Tributação no catálogo:** NCM, CFOP padrão e alíquota por item, com histórico (skill `data`, doc 07).

## Quando é ruim

- **Campo único de endereço:** a nota exige rua, número, bairro, município, UF e código IBGE separados.
- **Alíquota fixa no código:** muda por município, item e regime.
- **Inventar NCM ou CFOP:** o código errado muda o imposto; quem define é o contador.
- **Guardar só o endereço atual:** a nota emitida precisa dos dados da data da emissão; copie os dados na nota, não aponte para o cadastro vivo.

## Como começar

```sql
create table cliente_fiscal (
  cliente_id uuid primary key references clientes(id),
  tipo_pessoa text not null check (tipo_pessoa in ('fisica', 'juridica')),
  documento varchar(14) not null,
  nome_ou_razao_social text not null,
  email text not null,
  logradouro text not null,
  numero text not null,
  complemento text,
  bairro text not null,
  codigo_municipio_ibge char(7) not null,
  uf char(2) not null,
  cep char(8) not null,
  inscricao_estadual text,
  contribuinte_icms text not null default 'nao_contribuinte'
);

create table item_fiscal (
  item_id uuid primary key references itens(id),
  tipo text not null check (tipo in ('servico', 'produto')),
  descricao_fiscal text not null,
  ncm char(8),
  cfop_dentro_do_estado char(4),
  cfop_fora_do_estado char(4),
  origem smallint,
  item_lista_servico text,
  codigo_tributario_municipio text,
  aliquota_iss numeric(5,2),
  iss_retido boolean not null default false
);
```

Validação do CNPJ e do CPF (dígitos verificadores) no servidor:

```ts
export function cnpjValido(valor: string): boolean {
  const cnpj = valor.replace(/\D/g, "");
  if (cnpj.length !== 14 || /^(\d)\1+$/.test(cnpj)) return false;
  const digito = (base: string, pesos: number[]) => {
    const soma = base.split("").reduce((total, n, i) => total + Number(n) * pesos[i], 0);
    const resto = soma % 11;
    return resto < 2 ? 0 : 11 - resto;
  };
  const d1 = digito(cnpj.slice(0, 12), [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  const d2 = digito(cnpj.slice(0, 13), [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]);
  return d1 === Number(cnpj[12]) && d2 === Number(cnpj[13]);
}
```

Valide a completude antes de emitir e devolva erro por campo (skill `api`, doc 03):

```ts
export function camposFaltando(cliente: ClienteFiscal): string[] {
  const obrigatorios: (keyof ClienteFiscal)[] = ["documento", "nome_ou_razao_social", "logradouro", "numero", "bairro", "codigo_municipio_ibge", "uf", "cep", "email"];
  return obrigatorios.filter((campo) => !cliente[campo]);
}
```

Os dados de pessoa física são dados pessoais: veja o [doc 07](07-guarda-de-xml-e-lgpd.md) e a skill `data`, doc 10.

## Decisão rápida

| Dúvida | Resposta |
|---|---|
| NCM, CFOP ou alíquota | Contador define; o sistema só guarda e aplica |
| Onde guardo a tributação | No item do catálogo, com histórico |
| Cliente muda de endereço | A nota antiga mantém o endereço da época |
| Cadastro incompleto | Bloqueie a emissão e mostre os campos faltando |
