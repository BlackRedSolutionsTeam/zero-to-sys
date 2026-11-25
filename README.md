# zero-to-sys

Conjunto de skills para o Claude Code que guiam a criação de um sistema do zero até a produção. Cada pasta é uma skill independente: um guia de decisão (`SKILL.md`) e um documento por ferramenta ou prática (`docs/`), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e por quê.

## Instalação

O repositório é um plugin do Claude Code e do Codex: as 34 skills, o agente orquestrador, os 7 especialistas e o executor entram juntos e se atualizam pelo próprio Claude Code. Precisa do Claude Code (CLI, extensão do VS Code ou JetBrains, ou app desktop) ou do Codex instalado. Instruções do Codex em [No Codex](#no-codex).

### 1. Instalar

Dentro do Claude Code:

```text
/plugin marketplace add BlackRedSolutionsTeam/zero-to-sys
/plugin install zero-to-sys@zero-to-sys
```

Ou pelo terminal:

```bash
claude plugin marketplace add BlackRedSolutionsTeam/zero-to-sys
claude plugin install zero-to-sys@zero-to-sys
```

Depois, reinicie o Claude Code (na extensão do VS Code, recarregue a janela).

Por padrão o plugin vale para todos os seus projetos. Para ligar só no projeto atual, e deixar a configuração no repositório para o time inteiro, use `claude plugin install zero-to-sys@zero-to-sys --scope project`.

### 2. Conferir

```bash
claude plugin list
```

O `zero-to-sys@zero-to-sys` deve aparecer como `enabled`. Numa sessão nova, digite `/zero-to-sys:` e as skills aparecem na lista.

### 3. Atualizar e remover

```bash
claude plugin marketplace update zero-to-sys
claude plugin update zero-to-sys@zero-to-sys

claude plugin uninstall zero-to-sys@zero-to-sys
```

### Nomes depois de instalar

Instaladas como plugin, as skills e o agente ganham o prefixo `zero-to-sys:`:

| Peça | Como chamar |
|---|---|
| Skill principal | `/zero-to-sys:zero-to-sys` |
| Skills de área | `/zero-to-sys:stacks`, `/zero-to-sys:architecture`, `/zero-to-sys:coding`, `/zero-to-sys:infra`… |
| Agente orquestrador | `claude --agent zero-to-sys:zero-to-sys` (paralelo) ou `@zero-to-sys:zero-to-sys` |
| Especialistas | `@zero-to-sys:zero-to-sys-arquiteto`, `@zero-to-sys:zero-to-sys-seguranca`… |

Não precisa chamar pelo nome: o Claude carrega cada skill sozinho quando o pedido bate com o tema dela.

### No Codex

O mesmo repositório é um plugin do Codex (manifesto em `plugin.json` e marketplace em `.agents/plugins/marketplace.json`):

```bash
codex plugin marketplace add BlackRedSolutionsTeam/zero-to-sys
codex plugin add zero-to-sys@zero-to-sys
```

Ou, dentro do Codex, `/plugins` e escolha `zero-to-sys`. Abra uma sessão nova depois de instalar. As skills aparecem como `zero-to-sys:<skill>` e são chamadas com `$`, por exemplo `$zero-to-sys:store-targets`; o Codex também as carrega sozinho quando o pedido bate com o tema.

No Codex, use a skill principal no lugar do agente orquestrador: `$zero-to-sys:zero-to-sys` faz a mesma orquestração.

Para atualizar: `codex plugin marketplace upgrade zero-to-sys`. Para remover: `codex plugin remove zero-to-sys@zero-to-sys`.

Quem mantém o repositório: mantenha a versão do `plugin.json` igual à do `.claude-plugin/plugin.json`.

### Sem o sistema de plugins

Quem prefere copiar só algumas peças pode linkar as pastas direto (aí os nomes ficam sem prefixo: `/stacks`, `@zero-to-sys`):

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys

# Skills (todas ou só as que quiser)
mkdir -p ~/.claude/skills
for s in ~/zero-to-sys/skills/*/; do ln -s "$s" ~/.claude/skills/; done

# Agentes (orquestrador e especialistas)
mkdir -p ~/.claude/agents
for a in ~/zero-to-sys/agents/*.md; do ln -s "$a" ~/.claude/agents/; done
```

Para usar só em um projeto, crie os links em `.claude/skills/` e `.claude/agents/` dentro dele. No Codex sem plugin, linke as skills em `~/.agents/skills/` (ou `.agents/skills/` no projeto).

## Skill principal

A skill [zero-to-sys](skills/zero-to-sys/SKILL.md) é a principal. Ela descobre o contexto do projeto (tipo, interface, o que o time sabe, porte, restrições, novo ou existente) e dispara as outras skills na ordem certa, pulando as que não se aplicam. Com a base montada, conduz a construção do backlog item a item (dados, back, tela, testes, staging), cada um fechado por uma definição de pronto. Chame com `/zero-to-sys:zero-to-sys` ou peça "cria um sistema do zero".

## Skills

| Pasta | Skill | O que responde |
|---|---|---|
| [product/](skills/product/) | `product` | O que construir: escopo do MVP, fluxos, regras de negócio, histórias com critérios de aceite e backlog |
| [stacks/](skills/stacks/) | `stacks` | Qual stack usar em cada tipo de projeto e em qual área cada uma funciona melhor |
| [architecture/](skills/architecture/) | `architecture` | Como organizar pastas e arquivos para ser fácil achar e manter, pela documentação oficial de cada stack |
| [data/](skills/data/) | `data` | Como modelar tabelas, migrations, multiempresa, auditoria, índices, transações e LGPD no banco |
| [api/](skills/api/) | `api` | Como desenhar o contrato da API: rotas, erros, paginação, versionamento, OpenAPI e cliente tipado |
| [security/](skills/security/) | `security` | Como proteger a aplicação: login, permissões, OWASP, rate limit, upload, dependências e LGPD |
| [integrations/](skills/integrations/) | `integrations` | Como integrar pagamento, e-mail, WhatsApp, webhooks, filas, rotinas, arquivos e planilhas |
| [audit/](skills/audit/) | `audit` | Como auditar um projeto existente e dizer o que está bom e o que falta |
| [quality/](skills/quality/) | `quality` | Como provar que funciona: testes por camada, ponta a ponta, CI e definição de pronto |
| [coding/](skills/coding/) | `coding` | Como escrever código simples, bem organizado e bem modularizado |
| [user-experience/](skills/user-experience/) | `user-experience` | Como adaptar cada tela a celular, tablet e desktop |
| [design-systems/](skills/design-systems/) | `design-systems` | Qual layout usar em cada tipo de tela, com um exemplo HTML pronto por tipo de sistema |
| [design/](skills/design/) | `design` | Quais UI kits e ícones gratuitos usar para um visual profissional |
| [domains/](skills/domains/) | `domains` | Como registrar e configurar o domínio, o DNS e o e-mail do domínio |
| [cloudflare/](skills/cloudflare/) | `cloudflare` | Como configurar a Cloudflare: DNS, SSL, cache, WAF, Tunnel, Access, Pages e R2 |
| [vps/](skills/vps/) | `vps` | Qual VPS contratar no Brasil e como preparar o servidor |
| [nginx/](skills/nginx/) | `nginx` | Como configurar o nginx com HTTPS, limites, hardening e sem CVE aberto |
| [ai-features/](skills/ai-features/) | `ai-features` | Pôr IA e LLM dentro do produto: provedor, RAG, avaliação, guardrails e custo |
| [invoicing/](skills/invoicing/) | `invoicing` | Emitir NFS-e, NF-e e NFC-e por API e integrar com ERP |
| [search/](skills/search/) | `search` | Busca textual: Postgres, Meilisearch, Typesense ou Elasticsearch |
| [messaging/](skills/messaging/) | `messaging` | Brokers (RabbitMQ, Kafka), outbox, vídeo e chamadas |
| [performance/](skills/performance/) | `performance` | Medir e ganhar desempenho no back, cache, carga com k6 e escala |
| [operations/](skills/operations/) | `operations` | SLO, plantão, runbooks, incidentes, página de status e suporte |
| [maintenance/](skills/maintenance/) | `maintenance` | Fim de suporte, atualização de dependências e framework, dívida técnica |
| [local-dev/](skills/local-dev/) | `local-dev` | Ambiente local, Compose, devcontainer, .env.example e onboarding |
| [legal/](skills/legal/) | `legal` | Termos, política de privacidade, cookies, aceite versionado e contratos |
| [store-targets/](skills/store-targets/) | `store-targets` | Onde o projeto vai ser publicado e o que cada loja exige desde o início |
| [mobile-release/](skills/mobile-release/) | `mobile-release` | Contas, assinatura, EAS, lojas, regras de revisão e push |
| [desktop-release/](skills/desktop-release/) | `desktop-release` | Microsoft Store, Mac App Store, assinatura, notarização e Linux |
| [admin-panel/](skills/admin-panel/) | `admin-panel` | Painel de administração do sistema: papéis internos, auditoria, impersonação e telas de suporte |
| [infra/](skills/infra/) | `infra` | Como montar a infraestrutura de forma escalável e segura |
| [ia/](skills/ia/) | `ia` | Como usar agentes de IA de código da melhor forma |
| [code-indexes/](skills/code-indexes/) | `code-indexes` | Quais ferramentas de indexação de código e economia de tokens usar, e onde cada uma se sai melhor |

## Por onde começar

A ordem abaixo segue a vida de um projeto novo. A skill principal aplica essa ordem sozinha e ajusta por tipo de projeto:

0. **[product/](skills/product/SKILL.md):** defina o que construir: MVP, regras de negócio e backlog.
1. **[store-targets/](skills/store-targets/SKILL.md)** e **[stacks/](skills/stacks/SKILL.md):** diga onde o projeto vai ser publicado e escolha a stack que chega a esses destinos.
2. **[architecture/](skills/architecture/SKILL.md):** monte a estrutura de pastas da stack escolhida.
3. **[data/](skills/data/SKILL.md):** modele as tabelas a partir das regras de negócio.
4. **[ia/](skills/ia/SKILL.md)** e **[code-indexes/](skills/code-indexes/SKILL.md):** prepare o agente (instruções do projeto, skills, índice de código).
5. **[coding/](skills/coding/SKILL.md):** escreva o código seguindo as práticas.
6. **[user-experience/](skills/user-experience/SKILL.md)**, **[design-systems/](skills/design-systems/SKILL.md)** e **[design/](skills/design/SKILL.md):** decida os dispositivos, escolha o layout de cada tela e monte a interface.
7. **[infra/](skills/infra/SKILL.md):** leve para produção.
8. **Construção:** a skill principal pega o primeiro item do `BACKLOG.md` e leva até staging, depois o próximo; cada item fecha com testes de **[quality/](skills/quality/SKILL.md)** e a definição de pronto.

## Agentes

O [agents/zero-to-sys.md](agents/zero-to-sys.md) é o orquestrador. Ele divide a tarefa, dispara em paralelo os especialistas (quantos a máquina aguentar), escolhe o modelo e o esforço de cada chamada, junta os resultados e verifica.

| Agente | Papel | Skills |
|---|---|---|
| [zero-to-sys-arquiteto](agents/zero-to-sys-arquiteto.md) | Produto e sistema | product, stacks, architecture, data, api, admin-panel |
| [zero-to-sys-seguranca](agents/zero-to-sys-seguranca.md) | Segurança e conformidade | security, legal, audit |
| [zero-to-sys-integracoes](agents/zero-to-sys-integracoes.md) | Integrações | integrations, messaging, search, invoicing, ai-features |
| [zero-to-sys-frontend](agents/zero-to-sys-frontend.md) | Interface e experiência | user-experience, design-systems, design |
| [zero-to-sys-qualidade](agents/zero-to-sys-qualidade.md) | Código, testes e ambiente | coding, quality, code-indexes, ia, local-dev, maintenance |
| [zero-to-sys-infra](agents/zero-to-sys-infra.md) | Infraestrutura, operação e desempenho | infra, vps, nginx, cloudflare, domains, operations, performance |
| [zero-to-sys-publicacao](agents/zero-to-sys-publicacao.md) | Publicação nas lojas | store-targets, mobile-release, desktop-release |
| [zero-to-sys-executor](agents/zero-to-sys-executor.md) | Implementa o plano aprovado | coding, quality e as que o pedido listar |

Os especialistas planejam e julgam; o executor implementa. Fluxo de cada parte: especialista planeja → áreas afetadas julgam → executor implementa → qualidade revisa. Modos, ondas e modelos ficam na skill `zero-to-sys` (documentos 01 a 03).

No Claude Code, um subagente não dispara outros agentes. Para o orquestrador rodar os especialistas em paralelo, abra a sessão com ele como agente principal:

```bash
claude --agent zero-to-sys:zero-to-sys
```

Chamado como subagente (`@zero-to-sys:zero-to-sys`), ele devolve o plano de ondas pronto para a sessão principal disparar. Os especialistas também podem ser chamados direto, por exemplo `@zero-to-sys:zero-to-sys-seguranca revisa o login`.

## Como usar

O Claude carrega cada skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto, por exemplo `/zero-to-sys:stacks`, `/zero-to-sys:infra` ou `/zero-to-sys:architecture`. Exemplos:

- "Qual stack eu uso para um SaaS pequeno com painel admin?"
- "Organiza as pastas deste projeto Next.js."
- "Onde eu hospedo esse MVP gastando pouco?"
- "Como faço o Claude gastar menos tokens nesta base grande?"

## Estrutura

```
zero-to-sys/
├── .claude-plugin/
│   ├── plugin.json        manifesto do plugin (nome, versão, descrição)
│   └── marketplace.json   permite instalar direto do GitHub
├── agents/
│   ├── zero-to-sys.md     agente orquestrador
│   └── zero-to-sys-*.md   especialistas e executor
├── skills/
│   ├── zero-to-sys/       skill principal: fases, ondas, modelos e modos dos agentes
│   └── <skill>/           uma pasta por área
│       ├── SKILL.md       guia de decisão e regras de uso, lido pelo Claude
│       └── docs/
│           ├── README.md  índice, "Qual escolher" e o que saiu da lista
│           └── NN-nome.md um documento por ferramenta ou prática
└── README.md
```

## Como manter

- **Nova skill:** crie `skills/<nome>/SKILL.md` (descrição com até 400 caracteres) e `docs/`, e ponha a skill na tabela de um agente especialista em `agents/`. A tabela de skills deste README também ganha uma linha.
- **Novo documento numa skill:** crie `docs/NN-nome.md` com as mesmas seções dos outros e inclua-o na tabela do `SKILL.md` e no `docs/README.md`, se houver.
- **Remover um documento:** apague, tire das tabelas e dos links "Combina com / alternativas" dos outros documentos.
- **Nova versão:** suba o `version` igual em `.claude-plugin/plugin.json` e em `plugin.json`.
- **Modelos e paralelismo:** só em `skills/zero-to-sys/docs/01` a `03`.
- **Revisar dados:** cada documento tem a data em "Verificado em" e cita a fonte oficial; confira na fonte antes de uma decisão que dependa deles.
- **CI:** o workflow `checks` confere versão, links, skills sem agente e tamanho das descrições.
