# Cloudflare com IaC (OpenTofu e Terraform)

> DNS e regras da Cloudflare descritos em código versionado, com token de escopo mínimo.

| | |
|---|---|
| **Referência** | registry.terraform.io/providers/cloudflare/cloudflare, github.com/cloudflare/terraform-provider-cloudflare, developers.cloudflare.com/fundamentals/api |
| **Categoria** | Borda |
| **Tipo** | Prática de infraestrutura como código |
| **Vale para** | Projetos com OpenTofu ou Terraform que querem DNS e regras revisáveis no Git |
| **Verificado em** | 2026-11-25 |

## O que é

IaC (infraestrutura como código) é descrever recursos em arquivos e deixar uma ferramenta aplicar. Aqui o recurso é a Cloudflare: zona, registros DNS, regras de redirecionamento, cache e segurança. O **provider** é o plugin que fala com a API da Cloudflare. Funciona igual no OpenTofu e no Terraform; veja a escolha da ferramenta em [IaC](../../infra/docs/06-iac-opentofu-pulumi.md).

Versão conferida em 2026-11-25: o provider `cloudflare/cloudflare` está na série 5 (v5.29.0, publicada em 10 de novembro de 2026 segundo o changelog). A série 5 renomeou recursos: o registro DNS é `cloudflare_dns_record` (antes `cloudflare_record`) e as regras usam `cloudflare_ruleset`. Ao subir de versão, leia o guia de migração.

## Por que usar

- **Revisão por pull request:** mudar um CNAME vira diff.
- **Reprodutível:** recriar staging e produção com o mesmo código.
- **Sem deriva:** o painel deixa de ser a fonte da verdade.
- **Auditoria:** o Git mostra quem mexeu no DNS.

## Quando usar

- Mais de um ambiente (produção e staging) ou mais de uma pessoa mexendo no DNS.
- Regras de WAF, cache e redirect que não podem sumir por clique errado.
- Já usa IaC para a VPS ou o banco.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucos registros; painel resolve, IaC é opcional |
| MVP de SaaS | 🟡 Serve | Comece com DNS em código; regras depois |
| SaaS em crescimento | ✅ Ótimo | Vários ambientes e regras de segurança versionadas |
| Sistema interno/corporativo | ✅ Ótimo | Auditoria e revisão de mudanças |
| API/integração | ✅ Ótimo | DNS, rate limit e redirects em código |
| App mobile com backend | 🟡 Serve | A borda da API vale código; o resto é painel |
| Domínio pessoal de uma página | ❌ Evite | Custo de manter o estado maior que o ganho |

## Quando é bom

- Mudanças pequenas e frequentes de DNS com histórico.
- Combina com o mesmo repositório da infra da VPS.
- `plan` mostra o que muda antes de aplicar.

## Quando é ruim

- **Edição manual no painel** cria deriva; o próximo `apply` desfaz ou conflita.
- **Estado com segredo:** o arquivo de estado pode conter dados sensíveis; guarde em local remoto com acesso restrito, nunca no Git.
- **Token amplo demais:** vazou, vale a conta inteira.
- **Registro sem `content`:** desde a v5.29.0 o provider exige `content` em registros A, AAAA, CNAME, MX, NS e TXT na hora do plan.

## Como começar

Token de API com escopo mínimo, no painel em Manage Account, API Tokens, Create Token (conferido na documentação em 2026-11-25):

1. Prefira token **de conta** para uso em automação, assim não depende de uma pessoa.
2. Comece do modelo "Edit zone DNS" ou do zero. Adicione só as permissões de que o código precisa (DNS, e, se for usar regras, a permissão de edição de rulesets da zona; confira o nome exato na lista de permissões do painel).
3. Em Zone Resources, limite à zona `clinica-exemplo.com.br`.
4. Defina data de expiração e, se o CI tem IP fixo, filtro de IP.
5. Copie o segredo uma vez e guarde no gerenciador de segredos. Teste com `GET /user/tokens/verify`.

```bash
export CLOUDFLARE_API_TOKEN="valor-do-token"
```

Estrutura de arquivos:

```
cloudflare/
  versions.tf
  variables.tf
  dns.tf
  rules.tf
```

`versions.tf`:

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 5.29"
    }
  }
}

provider "cloudflare" {}
```

O provider lê `CLOUDFLARE_API_TOKEN` do ambiente, então o token não aparece no código.

`variables.tf`:

```hcl
variable "zone_id" {
  type = string
}

variable "origin_ip" {
  type = string
}
```

`dns.tf`, com app, API e staging atrás do proxy (um `for_each` cria os três):

```hcl
resource "cloudflare_dns_record" "origem" {
  for_each = toset(["app", "api", "staging"])
  zone_id  = var.zone_id
  name     = each.key
  type     = "A"
  content  = var.origin_ip
  ttl      = 1
  proxied  = true
}
```

`ttl = 1` significa automático e é o valor usado em registros com proxy. Registros só DNS (cinza), como o de e-mail, precisam de TTL próprio e `proxied = false`.

`rules.tf`, redirecionando `www` para o domínio principal:

```hcl
resource "cloudflare_ruleset" "redirect_www" {
  zone_id = var.zone_id
  name    = "redirect-www"
  kind    = "zone"
  phase   = "http_request_dynamic_redirect"

  rules = [{
    action      = "redirect"
    description = "www para o domínio principal"
    expression  = "(http.host eq \"www.clinica-exemplo.com.br\")"
    enabled     = true
    action_parameters = {
      from_value = {
        status_code           = 301
        preserve_query_string = true
        target_url = {
          expression = "concat(\"https://clinica-exemplo.com.br\", http.request.uri.path)"
        }
      }
    }
  }]
}
```

Rodar:

```bash
tofu init
tofu plan -var "zone_id=ID_DA_ZONA" -var "origin_ip=203.0.113.10"
tofu apply -var "zone_id=ID_DA_ZONA" -var "origin_ip=203.0.113.10"
```

No Terraform, troque `tofu` por `terraform`.

**Importar o que já existe.** Antes do primeiro `apply`, traga os recursos criados no painel para o estado, senão o provider tenta criá-los de novo. Os formatos de ID vêm do provider:

```bash
tofu import 'cloudflare_dns_record.origem["app"]' 'ID_DA_ZONA/ID_DO_REGISTRO'
tofu import cloudflare_ruleset.redirect_www 'zones/ID_DA_ZONA/ID_DO_RULESET'
```

O ID do registro sai de `GET /zones/{zone_id}/dns_records` na API. Depois do import, rode `plan` e ajuste o código até o plano ficar sem mudanças. Se a zona também for gerenciada pelo código, o import é `cloudflare_zone` com o ID da zona.

## Combina com / alternativas

- [IaC com OpenTofu e Pulumi](../../infra/docs/06-iac-opentofu-pulumi.md): estado remoto, módulos e CI.
- [R2, Email Routing e extras](09-r2-email-routing-e-extras.md): o que mais pode ir para código.
- Alternativas: Pulumi com o provider da Cloudflare, ou Wrangler para recursos de Workers.

## Decisão rápida

- **Use se:** há mais de um ambiente, mais de uma pessoa no DNS, ou regras que não podem se perder.
- **Evite se:** o domínio tem meia dúzia de registros que nunca mudam e ninguém mais mexe neles.
