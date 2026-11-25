# GitHub Actions

> Automação de testes, build e deploy dentro do GitHub, acionada por push, pull request ou agenda.

| | |
|---|---|
| **Site** | https://github.com/features/actions |
| **Categoria** | CI/CD |
| **Tipo** | Plataforma de integração e entrega contínua |
| **Stack** | Qualquer linguagem; workflows em YAML; runners Linux, macOS e Windows |
| **Preço** | Grátis em repositório público (runners padrão). Em privado, valor incluído por mês: US$ 12 (GitHub Free, cerca de 2.000 min Linux), US$ 18 (Pro e Team, cerca de 3.000 min); depois US$ 0,006 por minuto (Linux, 2 núcleos) |
| **Licença** | Serviço proprietário |
| **Verificado em** | 2026-11-24 |

## O que é

É o CI/CD do GitHub. Você cria arquivos em `.github/workflows/`, e a cada evento o GitHub executa os passos: instalar dependências, testar, construir a imagem, publicar e fazer deploy.

A cobrança em repositório privado usa um valor em dólar incluído no plano; os minutos por mês são uma conversão baseada no preço do Linux de 2 núcleos. Runners próprios (self-hosted) não têm custo de minutos.

## Por que usar

- **Já está onde o código está:** sem outra ferramenta nem outro login.
- **Marketplace grande** de ações prontas.
- **Ambientes e aprovações:** deploy em produção pode exigir revisão humana.
- **Autenticação sem chave fixa:** OIDC com a nuvem evita guardar credenciais de longa duração.
- **Grátis no público** e com cota generosa no privado.

## Quando usar

- Todo projeto hospedado no GitHub, desde o MVP.
- Testes e lint em cada pull request.
- Build de imagem Docker e deploy automático.
- Plano de IaC no pull request.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ✅ Ótimo | Build e publicação em poucas linhas |
| MVP / protótipo | ✅ Ótimo | Testes e deploy simples |
| SaaS pequeno | ✅ Ótimo | Cota incluída costuma bastar |
| SaaS em crescimento | ✅ Ótimo | Ambientes, aprovações e runners maiores |
| Sistema corporativo | ✅ Ótimo | Com ambientes protegidos e OIDC |
| Código fora do GitHub | ❌ Evite | Use o CI do repositório de origem |
| Builds muito longos e frequentes | 🟡 Serve | Custo por minuto soma; considere runner próprio |
| Mono-repositório enorme | 🟡 Serve | Exige filtros por caminho para não rodar tudo |

## Quando é bom

- **Integração nativa** com pull request, issues e releases.
- **Matrizes de teste** em várias versões ao mesmo tempo.
- **Cache de dependências** acelera os builds.
- **Boa documentação** e muitos exemplos.

## Quando é ruim

- **Ação de terceiros é risco de cadeia de suprimentos:** fixe a versão pelo hash do commit e prefira ações verificadas.
- **Segredo mal tratado vaza em log:** use secrets do GitHub e não imprima variáveis.
- **Permissões padrão amplas:** reduza o `GITHUB_TOKEN` com `permissions:` no workflow.
- **Custo em privado** cresce com builds longos; é cobrado pelo minuto de runner.
- **Preso ao GitHub:** os workflows não migram sem reescrita.
- **Pipeline lento** desanima o time: use cache e execute só o que mudou.

## Como começar

Arquivo `.github/workflows/ci.yml` (exemplo genérico; ajuste comandos e versões):

```yaml
name: ci
on: [pull_request]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm test
```

Para deploy, use ambiente (`environment: production`) com aprovação, e autenticação OIDC com a nuvem em vez de chave fixa. Versões mais recentes das ações oficiais nos releases do GitHub em 2026-11-24: checkout v7.0.1 e setup-node v7.1.0. Para manter as ações atualizadas, crie `.github/dependabot.yml` com `version: 2` e uma entrada `package-ecosystem: "github-actions"`, `directory: "/"` e `schedule.interval: "weekly"` (documentação do GitHub).

## Combina com / alternativas

- [Docker e Kubernetes](04-docker-kubernetes.md): build e publicação de imagem.
- [OpenTofu ou Pulumi](06-iac-opentofu-pulumi.md): plano no PR.
- [Segredos e configuração](09-segredos-e-configuracao.md) e [segurança base](12-seguranca-base.md): permissões e varredura de dependências.
- Alternativas: deploy direto do Git pelo [PaaS](01-paas.md) (sem pipeline próprio), GitLab CI ou outros, se o código estiver lá.

## Decisão rápida

- **Use se:** o código está no GitHub e você quer testes e deploy automáticos.
- **Evite se:** o repositório está em outra plataforma que já tem CI, ou os builds são tão pesados que o custo por minuto passa de um runner próprio.
