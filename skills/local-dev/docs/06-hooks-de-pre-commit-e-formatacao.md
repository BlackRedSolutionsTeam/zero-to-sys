# Hooks de pré-commit e formatação

> Rode formatador, lint e varredura de segredos antes de o commit nascer, só nos arquivos alterados, e repita na CI para ninguém pular.

| | |
|---|---|
| **Referência** | https://typicode.github.io/husky/ , https://lefthook.dev , https://pre-commit.com e https://git-scm.com/docs/githooks |
| **Categoria** | Qualidade local |
| **Tipo** | Automação com Git hooks |
| **Vale para** | Qualquer repositório Git; escolha a ferramenta pela stack |
| **Verificado em** | 2026-11-25 |

## O que é

Git hook é um script que o Git executa em eventos como o `pre-commit`. As ferramentas abaixo instalam e compartilham os hooks do time (a pasta `.git/hooks` não é versionada):

- **Husky:** hooks para projetos Node, instalados pelo script `prepare` do `package.json`. `npx husky init` cria a pasta `.husky/` e o `prepare`.
- **Lefthook:** binário único, com configuração em `lefthook.yml`, sem depender de Node. A última versão no GitHub em 2026-11-25 era a 2.2.3 (o pacote do npm estava na 2.2.2). Instala com `npm install lefthook --save-dev` e ativa com `npx lefthook install` (ou `lefthook install`, se o binário estiver no PATH).
- **pre-commit:** framework em Python com `.pre-commit-config.yaml`; instala com `pip install pre-commit` e ativa com `pre-commit install`.

Quais ferramentas de formatação e lint usar (Biome, ESLint, Prettier, Ruff, `dotnet format`) é assunto da skill `coding`, doc 09; aqui só ligamos isso ao commit.

## Por que usar

- **Feedback em segundos:** o erro aparece antes do push, não na CI minutos depois.
- **Diff limpo:** ninguém commita código fora do padrão.
- **Segredo barrado cedo:** a varredura roda antes de a chave entrar no histórico.
- **Revisão sobre lógica,** não sobre aspas.

## Quando usar

- Em time com mais de uma pessoa, ou projeto que vai durar.
- Depois de configurar formatador e lint (skill `coding`, doc 09).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Projeto Node/TypeScript | ✅ Ótimo | Husky ou Lefthook com Biome ou ESLint |
| Projeto Python | ✅ Ótimo | pre-commit com Ruff |
| Projeto .NET, Go ou Laravel | ✅ Ótimo | Lefthook roda `dotnet format`, `gofmt` ou Pint |
| Monorepo | ✅ Ótimo | Lefthook filtra por pasta com `glob` |
| Protótipo de um fim de semana | ❌ Evite | A CI e o editor bastam |

## Quando é bom

- **Só nos arquivos staged:** rápido o bastante para não irritar.
- **Mesmo comando da CI:** o hook e a pipeline chamam o `lint` do doc 05.
- **Formata e corrige** quando seguro; o resto só avisa.
- **Instalação automática** no `prepare` ou no passo de onboarding.

## Quando é ruim

- **Hook lento:** teste completo no pré-commit faz o time usar `--no-verify`. Deixe testes para o `pre-push` ou a CI.
- **Única barreira:** hook se pula com `git commit --no-verify`; a CI é a barreira de verdade.
- **Hook que reescreve sem aviso** e confunde o diff.
- **Dois mecanismos juntos** (Husky e pre-commit): escolha um.
- **Hook que não foi instalado:** quem clonou e não rodou `npm install` ou `lefthook install` fica sem proteção.

## Como começar

Husky com npm:

```bash
npm install --save-dev husky
npx husky init
```

`.husky/pre-commit`:

```sh
npx lint-staged
```

`package.json` (com `lint-staged`, que roda o comando só nos arquivos staged):

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,json,css}": "biome check --write --no-errors-on-unmatched"
  }
}
```

Lefthook (não depende de Node):

```yaml
pre-commit:
  jobs:
    - name: biome
      glob: "*.{ts,tsx,js,json}"
      run: npx biome check --write {staged_files}
```

```bash
npm install lefthook --save-dev
npx lefthook install
```

pre-commit (Python):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.6
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
```

```bash
pip install pre-commit
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```

Os `rev` eram as últimas versões publicadas em 2026-11-25 (`ruff-pre-commit` v0.17.6; `gitleaks` v8.30.1; o README do Gitleaks ainda exemplifica com v8.24.2); rode `pre-commit autoupdate` para pegar as versões atuais. O Gitleaks é um detector de segredos; o README dele diz que o projeto está completo e que as próximas versões serão só correções de segurança, então avalie a alternativa que o time preferir.

No Lefthook, `{staged_files}` é substituído pelos arquivos staged (documentado na página `run` da configuração) e `stage_fixed: true` roda `git add` nesses arquivos depois do comando; se o `git add` falhar, o hook falha. Para barrar segredos sem o pre-commit, o Lefthook pode chamar o Gitleaks direto:

```yaml
pre-commit:
  jobs:
    - name: gitleaks
      run: gitleaks git --pre-commit --staged --redact
```

O comando sai com código 1 quando acha um segredo, e o commit é barrado.

Testado em 2026-11-25, em repositório temporário, no macOS arm64 com os binários oficiais do GitHub: Lefthook 2.2.3 (o hook `biome` trocado por um `sed` rodou só no arquivo staged e, com `stage_fixed: true`, o commit já saiu com o arquivo corrigido; `npx lefthook install` pelo pacote npm 2.2.2 também funcionou) e Gitleaks 8.30.1 (`gitleaks git --pre-commit --staged` achou um token de teste e saiu com código 1). Husky, `lint-staged`, pre-commit e Ruff não foram executados; os trechos deles seguem as páginas oficiais.

Repita o mesmo comando na CI (skill `infra`, doc 07); o hook é conforto, a CI é a regra.

## Combina com / alternativas

- Skill `coding`: formatação e lint (doc 09), commits pequenos (doc 11).
- [05-scripts-de-uma-linha.md](05-scripts-de-uma-linha.md): o hook chama o mesmo `lint`.
- [03-env-example-e-segredos-de-desenvolvimento.md](03-env-example-e-segredos-de-desenvolvimento.md): varredura de segredos.
- Skill `ia`, doc 08: hooks do agente de IA, que são outra coisa (rodam nas ações do Claude Code, não nos commits).
- Alternativas: só CI, ou o editor formatando ao salvar.

## Decisão rápida

- **Use se:** o time tem mais de uma pessoa e já definiu formatador e lint.
- **Evite se:** o hook demora mais de alguns segundos ou o projeto é descartável.
