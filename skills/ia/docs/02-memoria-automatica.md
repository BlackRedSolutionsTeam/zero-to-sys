# Memória automática

> Notas que o próprio Claude Code escreve sobre o seu projeto, a partir das suas correções, e relê nas sessões seguintes.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/memory (seção "Auto memory") |
| **Categoria** | Memória entre sessões |
| **Tipo** | Pasta de arquivos Markdown mantida pelo agente |
| **Onde vale** | Claude Code. Codex tem "memories" locais, desligadas por padrão (developers.openai.com/codex/memories); conferido em 2026-11-24 |
| **Equivalente em outras ferramentas** | Codex: memories (acima). GitHub Copilot: Copilot Memory guarda fatos do repositório e preferências do usuário, em todos os planos pagos (docs.github.com, "About GitHub Copilot Memory"); conferido em 2026-11-24. Para instruções que você escreve, o equivalente é o `AGENTS.md` |
| **Verificado em** | 2026-11-24 |

## O que é

Cada sessão do Claude Code começa com a janela de contexto vazia. A memória automática é o que o agente guarda sozinho para a próxima: suas preferências, correções que você deu e contexto do projeto que não dá para tirar do código.

Os arquivos ficam em `~/.claude/projects/<projeto>/memory/`. O `<projeto>` vem do repositório git, então todos os worktrees e subpastas do mesmo repositório compartilham a mesma pasta. Dentro dela há um `MEMORY.md`, que é um índice de uma linha por memória, e arquivos de tópico. No início da sessão carregam as primeiras 200 linhas ou 25 KB do `MEMORY.md`, o que vier primeiro. Os arquivos de tópico só são lidos quando o agente precisa.

É texto puro. O comando `/memory` abre a pasta e tem um botão para ligar e desligar o recurso (grava `autoMemoryEnabled` em `~/.claude/settings.json`). Para desligar por variável de ambiente: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

## Por que usar

- **Sem esforço:** o agente anota sem você precisar escrever nada.
- **Guarda correções:** a documentação lista o tipo `feedback` ("corrections you give Claude") entre as notas.
- **Auditável:** são arquivos Markdown que você lê, edita e apaga.
- **Fora do repositório:** não suja o git com preferências pessoais.

## Quando usar

- Correções e preferências suas e contexto do projeto que não dá para tirar do código (a documentação lista os tipos `user`, `feedback`, `project` e `reference`).
- Preferências pessoais: a memória é local à máquina e o `CLAUDE.md` é o arquivo do time.
- Contexto que mudou e não está no código (ex.: "a migração do módulo X está congelada até o fim do mês").

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Projeto de longa duração | ✅ Ótimo | A documentação a descreve como acúmulo de conhecimento entre sessões |
| Trabalho em paralelo (worktrees) | ✅ Ótimo | A memória é do repositório e vale em todos os worktrees |
| Regra do time | ❌ Evite | A memória é local e pessoal; regra do time vai no `CLAUDE.md` versionado |
| Regra que não admite exceção | ❌ Evite | É contexto, não imposição. Use hook ou `deny` |

## Quando é bom

- **Ligada por padrão** em sessões locais.
- **Índice curto:** o `MEMORY.md` carrega pequeno e o resto só quando preciso.
- **Sobrevive à limpeza:** os arquivos de memória ficam fora da rotina que apaga transcrições antigas.

## Quando é ruim

- **Não é compartilhada:** a documentação diz que ela é local à máquina e que os arquivos não vão para outras máquinas nem para ambientes na nuvem. Ponha o que precisa viajar no `CLAUDE.md`.
- **Limite de leitura:** só as primeiras 200 linhas ou 25 KB do índice carregam. Índice inchado perde o final.
- **Subagentes não carregam:** a documentação diz que o subagente não recebe a memória automática do projeto (ele pode ter a própria, pelo campo `memory`).
- **Em alguns ambientes fica desligada:** a documentação cita sessões em que o recurso não pode ser ligado. Confira o botão em `/memory`.

## Como começar

Já vem ligada por padrão nas versões atuais. Para ver e mexer:

```text
/memory
```

Para dizer ao agente o que guardar, fale normalmente:

```text
lembre que os testes de integração só rodam com o banco local ligado
```

Desligar em um projeto, em `.claude/settings.json`:

```json
{ "autoMemoryEnabled": false }
```

Estrutura da pasta, como descrita na documentação:

```text
~/.claude/projects/<projeto>/memory/
├── MEMORY.md        índice, uma linha por memória
└── ...              arquivos de tópico criados pelo agente
```

## Combina com / alternativas

Combina com:
- [CLAUDE.md e AGENTS.md](01-claude-md-agents-md.md): o arquivo é seu e do time; a memória é do agente.
- [Gestão de contexto](06-gestao-de-contexto.md): a memória é recarregada do disco depois de compactar.

Alternativas:
- Escrever a decisão no `CLAUDE.md` (versionado, compartilhado com o time) ou numa skill.
- `claude --resume` e `claude --continue`: retomam a conversa inteira, não só as notas.

## Decisão rápida

- **Use se:** você trabalha sozinho no mesmo projeto por muito tempo e quer que o agente lembre das suas correções.
- **Evite se:** a informação precisa chegar ao time inteiro ou valer sempre sem falha; escreva no `CLAUDE.md` ou num hook.

Fontes das recomendações: code.claude.com/docs/en/memory (seção "Auto memory" e a tabela "CLAUDE.md vs auto memory") e best-practices.
