# Atualização automática de dependências

> Deixe um robô abrir PRs pequenos de atualização, deixe o CI provar que nada quebrou e automatize só o que é seguro: patch e minor com testes verdes. Versão maior sempre passa por uma pessoa.

| | |
|---|---|
| **Referência** | Renovate (docs.renovatebot.com: Configuration Options, Preset Config); GitHub Dependabot (docs.github.com: Dependabot options reference, Automating Dependabot with GitHub Actions) |
| **Categoria** | Manutenção |
| **Tipo** | Prática de automação |
| **Vale para** | npm, pnpm, pip, NuGet, Composer, Go, Docker e GitHub Actions, em repositório GitHub (Renovate também em GitLab, Azure DevOps e outros) |
| **Verificado em** | 2026-11-25 |

## O que é

Um robô lê os manifestos do repositório (`package.json`, `.csproj`, `requirements.txt`, `Dockerfile`, workflows), descobre versões novas e abre um PR para cada uma, ou para um grupo. O CI roda os testes no PR. Se tudo passa e a regra permite, o PR entra sozinho. O que muda a rotina é o tamanho: dez PRs pequenos por mês em vez de uma atualização gigante por ano.

A configuração básica de Dependabot e Renovate, o cooldown e a auditoria de vulnerabilidades estão na skill `security` ([doc 08](../../security/docs/08-dependencias-vulneraveis.md)). Aqui entram as regras de merge e o ajuste fino.

## Por que usar

- **Dívida não acumula:** subir uma versão por vez custa minutos.
- **Segurança chega rápido:** a correção vem em PR, sem ninguém lembrar.
- **Histórico limpo:** cada PR tem changelog e o motivo da mudança.

## Quando usar

- Desde o primeiro commit, junto do lockfile.
- Em projeto antigo, depois de zerar o atraso à mão (a primeira leva de PRs de um projeto atrasado vira uma enxurrada).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas dependências; agrupe tudo em um PR semanal |
| MVP de SaaS | ✅ Ótimo | Automerge de patch e minor economiza tempo de quem trabalha sozinho |
| SaaS em crescimento | ✅ Ótimo | Agrupamento e limite de PRs mantêm a fila revisável |
| Sistema interno/corporativo | ✅ Ótimo | Deixa rastro de atualização para auditoria |
| API/integração | ✅ Ótimo | Mantém as libs de HTTP e JSON em dia |
| App mobile com backend | 🟡 Serve | Dependências nativas do app pedem revisão manual |
| Projeto sem testes automatizados | ❌ Evite automerge | O robô não sabe se quebrou; sem testes, só PR com revisão |

## Quando é bom

- **CI obrigatório** na branch principal (skill `quality`, [doc 07](../../quality/docs/07-quality-gates-no-ci.md)): sem gate verde, nada entra.
- **Grupos:** devDependencies e GitHub Actions em um PR só.
- **Espera após o lançamento** (cooldown no Dependabot, `minimumReleaseAge` no Renovate): pacote malicioso costuma ser retirado nos primeiros dias.
- **Limite de PRs abertos:** a fila nunca passa de 5 a 10.

## Quando é ruim

- **Automerge sem testes ou sem branch protection:** o robô quebra a produção sozinho.
- **Automerge de versão maior:** mudança que quebra compatibilidade pede leitura do guia de migração.
- **Ignorar PRs:** dez PRs parados viram cinquenta, e o robô vira ruído.
- **Dois robôs no mesmo repositório:** escolha um. Dependabot e Renovate abrem PRs duplicados.
- **Fixar tudo em `ignore`** para a notificação sumir: a dívida só fica escondida.

## Como começar

### Qual escolher

| | Dependabot | Renovate |
|---|---|---|
| Onde roda | Nativo do GitHub, sem instalar | App (gratuito) ou autohospedado |
| Plataformas | GitHub | GitHub, GitLab, Azure DevOps, Bitbucket e outras |
| Agrupamento e regras | Grupos por padrão, tipo e dependência | Muito mais regras (`packageRules`) |
| Painel | Aba Insights, Dependency graph | Issue "Dependency Dashboard" |
| Automerge | Por workflow do Actions | Nativo (`automerge`) |

Regra: **repositório só no GitHub e time pequeno, Dependabot; vários repositórios, regras finas ou fora do GitHub, Renovate.**

### Política de merge (vale para os dois)

| Tipo de update | Dependência | Regra |
|---|---|---|
| patch | devDependency ou GitHub Action | Automerge com CI verde |
| patch | produção | Automerge com CI verde, se há testes de integração |
| minor | devDependency | Automerge com CI verde |
| minor | produção | Revisão rápida de uma pessoa |
| major | qualquer | Sempre revisão; segue o [doc 03](03-atualizar-versao-maior-do-framework.md) se for framework |
| Runtime, framework, banco | qualquer | Nunca automático; é projeto, não PR |
| Correção de segurança | qualquer | Prioridade; severidade pela skill `security` |

### Dependabot com automerge

`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "07:00"
      timezone: "America/Sao_Paulo"
    open-pull-requests-limit: 5
    cooldown:
      default-days: 3
      semver-major-days: 30
      semver-minor-days: 7
    groups:
      dev-minor-patch:
        dependency-type: "development"
        update-types:
          - "minor"
          - "patch"
    ignore:
      - dependency-name: "node"
        update-types: ["version-update:semver-major"]
```

`.github/workflows/dependabot-automerge.yml`:

```yaml
name: Dependabot automerge
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  automerge:
    runs-on: ubuntu-latest
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    steps:
      - id: metadata
        uses: dependabot/fetch-metadata@v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
      - if: steps.metadata.outputs.update-type != 'version-update:semver-major'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

O `--auto` só efetiva o merge quando os checks obrigatórios passam: ligue **branch protection com checks obrigatórios** em Settings, Branches, e **Allow auto-merge** em Settings, General. Sem isso, o merge sai na hora. Fixe `dependabot/fetch-metadata` por tag exata ou SHA, como em [GitHub Actions](../../infra/docs/07-github-actions.md).

Notas conferidas na documentação (2026-11-25): sem `cooldown`, o Dependabot já aplica 3 dias nas atualizações de versão (não nas de segurança); `open-pull-requests-limit` vale 5 por padrão e as atualizações de segurança têm limite próprio de 10; sem `time`, o horário é sorteado e é UTC se não houver `timezone`. Se o repositório usa merge queue, o `GITHUB_TOKEN` não consegue entrar na fila: use token de GitHub App.

Outros ecossistemas: troque o `package-ecosystem` por `pip`, `nuget`, `composer`, `gomod`, `docker` ou `github-actions`.

### Renovate com automerge

`renovate.json`:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended", "helpers:pinGitHubActionDigests"],
  "timezone": "America/Sao_Paulo",
  "schedule": ["before 7am on monday"],
  "minimumReleaseAge": "3 days",
  "prConcurrentLimit": 5,
  "packageRules": [
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "groupName": "dev dependencies",
      "automerge": true
    },
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "minimumReleaseAge": "14 days",
      "automerge": false
    },
    {
      "matchPackageNames": ["node", "postgres"],
      "matchUpdateTypes": ["major"],
      "enabled": false
    }
  ]
}
```

Conferido na documentação e executado (2026-11-25): o `renovate.json` acima passou no `renovate-config-validator --strict` do Renovate 44.261.3 (`npx --package renovate renovate-config-validator --strict`), e um horário inválido no mesmo campo foi recusado com "Invalid schedule". Rode o mesmo comando antes de commitar qualquer mudança de configuração.

- `schedule` aceita texto como `before 7am on monday` e usa o `timezone` da configuração;
- `automerge` vale `false` por padrão; `matchUpdateTypes` limita o alcance; `automergeType` padrão é `pr`.
- `config:recommended` liga o Dependency Dashboard, agrupa monorepos conhecidos e aplica regras da comunidade; `config:best-practices` soma pin de digest de Docker e Actions, PR de migração de configuração e espera de 3 dias em pacotes npm.
- `minimumReleaseAge` exige que a fonte do pacote informe a data de lançamento; enquanto o prazo não passa, o PR fica com o status "pending" (`renovate/stability-days`).
- `platformAutomerge` vale `true` por padrão e, quando ligado, o Renovate não consegue respeitar `automergeSchedule`; desligue se o horário importa.
- Instale o app no repositório (github.com/apps/renovate), mesmo caminho do onboarding PR, e revise o PR de configuração inicial.

### Dia a dia

1. Segunda de manhã: olhar o Dashboard ou a lista de PRs abertos do robô.
2. Fechar o que o automerge não pegou: ler o changelog, rodar, aprovar.
3. PR de major vira card de manutenção, não é fechado em silêncio.
4. Alerta de segurança fura a fila.

## Combina com / alternativas

- Skill `security`, [dependências vulneráveis](../../security/docs/08-dependencias-vulneraveis.md): auditoria no CI e política de severidade.
- Skill `quality`, [gates no CI](../../quality/docs/07-quality-gates-no-ci.md): o que torna o automerge seguro.
- Skill `infra`, [GitHub Actions](../../infra/docs/07-github-actions.md): workflows e permissões.
- Alternativa: atualizar à mão a cada trimestre; só serve em projeto minúsculo e exige o [doc 07](07-rotina-trimestral-de-saude.md).

## Decisão rápida

- **Use se:** o projeto tem CI com testes e lockfile.
- **Evite automerge se:** não há testes; mantenha só os PRs, com revisão.
