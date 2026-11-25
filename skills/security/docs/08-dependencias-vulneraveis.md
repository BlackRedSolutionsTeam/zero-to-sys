# Dependências vulneráveis

> Quase todo o código de produção é de terceiros: audite as dependências a cada PR, mantenha-as atualizadas por robô e bloqueie o que for crítico.

| | |
|---|---|
| **Referência** | OWASP Top 10, A06 Vulnerable and Outdated Components; documentação oficial do npm (`npm audit`, provenance), pip-audit, NuGet Audit (Microsoft Learn), Composer (`composer audit`), govulncheck (go.dev), OWASP Dependency-Check, GitHub Dependabot e secret scanning (docs.github.com), Renovate (docs.renovatebot.com) |
| **Categoria** | Segurança |
| **Tipo** | Prática de segurança da cadeia de suprimentos |
| **Vale para** | Node, Python, .NET, PHP e Go; automação com GitHub Actions e Dependabot |
| **Verificado em** | 2026-11-24 |

## O que é

Seu sistema usa centenas de pacotes (diretos e os que eles puxam, os transitivos). Se um deles tem uma falha conhecida, seu sistema herda a falha. Se um deles é trocado por um pacote malicioso, é um ataque de cadeia de suprimentos (supply chain).

Duas frentes: achar falhas já publicadas (auditoria) e não deixar entrar pacote suspeito (revisão).

## Por que usar

- **Barato:** a auditoria roda em segundos no CI.
- **Falha antiga é a mais explorada:** quem ataca procura versões com CVE conhecido.
- **Atualizar pouco e sempre** dói menos que atualizar tudo depois de dois anos.

## Quando usar

- Desde o primeiro commit: ligue Dependabot e a auditoria no CI.
- Antes de adicionar qualquer pacote novo.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas dependências em produção, mas o build usa muitas |
| MVP de SaaS | ✅ Ótimo | Custo mínimo, protege dados de clientes |
| SaaS em crescimento | ✅ Ótimo | Mais pacotes, mais superfície; exige política de severidade |
| Sistema interno/corporativo | ✅ Ótimo | Auditoria e conformidade pedem esse registro |
| API/integração | ✅ Ótimo | Exposta à internet; falha em lib de HTTP ou JSON é grave |
| App mobile com backend | ✅ Ótimo | Vale para o app e para a API |
| Qualquer um, sem lockfile e com versões `latest` | ❌ Evite | Cada instalação pode trazer um código diferente |

## Quando é bom

- **Lockfile commitado** (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `composer.lock`, `go.sum`): todo ambiente instala as mesmas versões. No CI, use instalação fiel ao lockfile (`npm ci`).
- **Atualização em PRs pequenos**, revisados e testados pelo CI.
- **Pouca dependência:** cada pacote é um risco. Não instale uma lib para uma função de três linhas.
- **Política de severidade escrita:** todo mundo sabe o que bloqueia.

## Quando é ruim

- **Ignorar o alerta** porque "é só dev": o build roda na sua máquina e no CI, onde estão os segredos.
- **Aceitar PR do robô sem olhar** testes falhando.
- **Pacote com nome parecido** (typosquatting, como `reqeusts` no lugar de `requests`): confira o nome, o autor, os downloads e o repositório antes de instalar.
- **Suprimir alerta sem registro** do motivo e do prazo.
- **Alerta sem contexto:** nem toda falha afeta o seu uso. Avalie, mas registre a decisão.

## Como começar

### Comandos de auditoria

| Stack | Comando | Observação |
|---|---|---|
| npm | `npm audit --audit-level=high` | Sai com erro a partir do nível indicado; `--omit=dev` ignora devDependencies |
| pnpm | `pnpm audit --audit-level high` | Mesma ideia do npm |
| Python | `pip-audit -r requirements.txt` | Sai com 1 se achar vulnerabilidade |
| .NET | `dotnet list package --vulnerable --include-transitive` | Sem `--include-transitive`, olha só os diretos |
| PHP | `composer audit --locked` | Sai com 1 se achar problema |
| Go | `govulncheck ./...` | Instalar com `go install golang.org/x/vuln/cmd/govulncheck@latest`; só alerta o que seu código realmente chama |
| Qualquer (Java e outros) | `dependency-check --scan . --failOnCVSS 7` | OWASP Dependency-Check; baixa a base do NVD, uma chave de API (`--nvdApiKey`) acelera |

No .NET, o `dotnet restore` já avisa (códigos NU1901 a NU1904, de baixa a crítica). Para barrar só high e critical: `<WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>`.

### Dependabot

Arquivo `.github/dependabot.yml`: alertas de segurança ficam em Settings, Code security; as atualizações de versão vêm deste arquivo.

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      dev-dependencies:
        dependency-type: "development"
    cooldown:
      default-days: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns:
          - "*"
```

`cooldown` espera alguns dias depois do lançamento antes de propor a versão, o que dá tempo de um pacote malicioso ser detectado e removido. Para outros ecossistemas troque o `package-ecosystem` (`pip`, `nuget`, `composer`, `gomod`).

### Renovate (alternativa)

App gratuito, com mais opções de agrupamento. Arquivo `renovate.json`:

```json
{
  "extends": ["config:recommended"]
}
```

### Passo de CI

```yaml
name: Dependências
on:
  pull_request:
  schedule:
    - cron: "0 7 * * 1"

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm audit --audit-level=high
```

O `schedule` roda toda segunda: vulnerabilidade nova aparece sem ninguém mexer no código. Marque o job como obrigatório no PR, como em [quality gates no CI](../../quality/docs/07-quality-gates-no-ci.md).

### Política de severidade

| Severidade | O que fazer |
|---|---|
| Crítica | Bloqueia o PR e o deploy; corrige no mesmo dia |
| Alta | Bloqueia o PR; corrige em poucos dias (a regra `--audit-level=high` acima) |
| Média | Abre issue com dono e prazo; não bloqueia |
| Baixa | Resolve junto das atualizações normais |

Exceção só com registro: qual alerta, por que não afeta, quem decidiu, até quando.

### Cadeia de suprimentos e segredos

- **Proveniência (provenance) do npm:** quem publica pacote pelo GitHub Actions pode assinar a origem (`npm publish --provenance`, com permissão `id-token: write`). Quem consome confere com `npm audit signatures`.
- **GitHub secret scanning:** procura chaves e tokens commitados. É gratuito em repositório público; em privado exige o plano com GitHub Secret Protection. A push protection bloqueia o `git push` que contém um segredo conhecido. Se vazar, revogue a chave primeiro (veja [segredos](../../infra/docs/09-segredos-e-configuracao.md)).
- Fixe versões (sem `latest`, sem `*`) e revise o diff do lockfile no PR.

## Combina com / alternativas

- [OWASP no código](./05-owasp-no-codigo.md): componentes vulneráveis é um item do Top 10.
- [Upload de arquivos](./07-upload-de-arquivos.md): bibliotecas de imagem e de antivírus também entram na auditoria.
- [Quality gates no CI](../../quality/docs/07-quality-gates-no-ci.md): onde o job de auditoria vira obrigatório.
- [GitHub Actions](../../infra/docs/07-github-actions.md) e [segurança base](../../infra/docs/12-seguranca-base.md).
- Alternativas pagas ou com plano limitado de scanners (Snyk e similares): confira o plano grátis antes.

## Decisão rápida

- **Use se:** o projeto tem qualquer dependência; ligue lockfile, Dependabot e auditoria no CI desde o início.
- **Evite se:** a ideia é auditar só de vez em quando; sem automação, o alerta chega tarde.
