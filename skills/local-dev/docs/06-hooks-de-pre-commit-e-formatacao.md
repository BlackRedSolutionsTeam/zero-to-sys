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
- **Lefthook:** binário único, com configuração em `lefthook.yml`, sem depender de Node. A página oficial mostrava a versão 2.2.3 em 2026-11-25. Instala com `npm install lefthook --save-dev` e ativa com `lefthook install`.
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
    rev: v8.24.2
    hooks:
      - id: gitleaks
```

```bash
pip install pre-commit
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```

Os `rev` vêm dos exemplos dos repositórios oficiais em 2026-11-25 (`ruff-pre-commit` v0.17.6; `gitleaks` v8.24.2, que a página dele só dá como exemplo); rode `pre-commit autoupdate` para pegar as versões atuais. O Gitleaks é um detector de segredos; a documentação dele avisa que o projeto só recebe correções de segurança, então avalie a alternativa que o time preferir. No Lefthook, confira na documentação o parâmetro `{staged_files}` e a opção `stage_fixed` (que re-adiciona ao commit os arquivos corrigidos) antes de usá-los.

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
