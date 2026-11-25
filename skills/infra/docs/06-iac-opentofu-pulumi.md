# IaC (OpenTofu, Terraform e Pulumi)

> Infraestrutura descrita em código versionado: o que existe na nuvem fica no Git, revisável e reproduzível.

| | |
|---|---|
| **Site** | https://opentofu.org, https://developer.hashicorp.com/terraform, https://www.pulumi.com |
| **Categoria** | Infraestrutura como código |
| **Tipo** | Ferramenta de provisionamento declarativo |
| **Stack** | OpenTofu e Terraform: linguagem HCL; Pulumi: TypeScript, Python, Go, C# e outras |
| **Preço** | OpenTofu: grátis. Terraform (HCP Terraform): grátis até 500 recursos gerenciados; pago por recurso/mês: Essentials US$ 0,10, Standard US$ 0,47, Premium US$ 0,99 (página de preços e documentação da HashiCorp, conferido em 2026-11-24). Pulumi: individual grátis (1 usuário), Essentials US$ 40/mês, Pro US$ 400/mês |
| **Licença** | OpenTofu: MPL 2.0. Terraform: BSL 1.1 desde a versão 1.6.0 (não é licença aberta; uso em produção é permitido, exceto oferecer a terceiros um produto que concorra com os da HashiCorp/IBM; cada versão vira MPL 2.0 após 4 anos). Pulumi: Apache 2.0 (arquivos LICENSE no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Em vez de clicar no painel, você escreve arquivos que dizem "quero uma rede, um banco e um serviço". A ferramenta compara com o que existe e mostra o plano de mudança antes de aplicar. O estado fica salvo, de preferência em local remoto e com trava.

**OpenTofu** é o fork aberto do Terraform, mantido sob a Linux Foundation, com a mesma linguagem. A versão 1.13 aparecia como a mais recente na documentação na data da verificação. **Terraform** segue como o mais conhecido, com o maior número de módulos. **Pulumi** usa linguagens de programação comuns, o que ajuda quando há lógica, loops e testes.

## Por que usar

- **Reproduzível:** recriar o ambiente é rodar um comando.
- **Revisável:** mudança de infra passa por pull request.
- **Auditável:** o histórico do Git mostra quem mudou o quê.
- **Evita deriva:** o código é a fonte de verdade.
- **Facilita ambientes iguais** (homologação e produção).

## Quando usar

- A partir do SaaS pequeno, assim que houver mais de um recurso de nuvem.
- Qualquer uso da [nuvem grande](03-nuvem-grande.md).
- Quando é preciso recriar o ambiente com rapidez após uma falha.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Um domínio e um deploy não justificam |
| MVP / protótipo | 🟡 Serve | Opcional; Dockerfile e pipeline versionados bastam |
| SaaS pequeno | 🟡 Serve | Vale para banco, DNS e filas; não é obrigatório |
| SaaS em crescimento | ✅ Ótimo | Muitos recursos e ambientes pedem código |
| Sistema corporativo | ✅ Ótimo | Auditoria e padronização entre equipes |
| Projeto em PaaS puro | 🟡 Serve | Há provedores para algumas plataformas; confira se existe |
| Time sem prática | 🟡 Serve | Comece com poucos recursos e revisão em par |
| Infra com muita lógica | ✅ Ótimo | Pulumi, por usar linguagem de programação |

## Quando é bom

- **Plano antes de aplicar:** você vê o que muda.
- **Ecossistema de provedores:** cobre os grandes e muitos serviços menores.
- **OpenTofu:** sem restrição de uso e com migração direta de Terraform.
- **Pulumi:** reaproveita a linguagem do time e permite testes.

## Quando é ruim

- **Estado é sensível:** guarda dados e às vezes segredos. Use backend remoto com criptografia e trava, nunca no repositório.
- **Mudar na mão quebra tudo:** alteração fora do código gera deriva.
- **`destroy` e troca de recurso apagam dados:** revise sempre o plano, principalmente de banco.
- **Curva de aprendizado** em módulos, estado e importação de recursos existentes.
- **Licença do Terraform:** a BSL 1.1 proíbe oferecer o Terraform a terceiros como produto concorrente dos da HashiCorp; uso interno é permitido.
- **Pulumi Cloud:** os planos pagos cobram por crédito e por recurso gerenciado; dá para usar com estado próprio, sem os recursos da nuvem do Pulumi.

## Como começar

OpenTofu (instalação por Homebrew, listada na página oficial):

```bash
brew install opentofu
tofu init
tofu plan
tofu apply
```

Pulumi (comandos da CLI oficial; `pulumi new`, `pulumi preview` e `pulumi up` constam na referência, e o template `typescript` existe no repositório pulumi/templates, conferido em 2026-11-24):

```bash
pulumi new typescript
pulumi preview
pulumi up
```

Guarde o estado em backend remoto com trava (por exemplo, bucket com criptografia) e rode `plan` automático nos pull requests via [GitHub Actions](07-github-actions.md).

## Combina com / alternativas

- [GitHub Actions](07-github-actions.md): plano no PR, aplicação após aprovação.
- [Segredos e configuração](09-segredos-e-configuracao.md): nunca no código da infra.
- [Nuvem grande](03-nuvem-grande.md), [Cloudflare](08-cloudflare.md) e [Postgres gerenciado](05-postgres-gerenciado.md): têm provedores de IaC.
- Alternativas: Terraform (mesma sintaxe), CloudFormation (só AWS), scripts e painel para o mínimo.

## Decisão rápida

- **Use se:** há mais de um recurso de nuvem, mais de um ambiente ou mais de uma pessoa mexendo na infra.
- **Evite se:** o projeto é um site estático ou um MVP em PaaS simples, onde o painel e o Git já resolvem.
