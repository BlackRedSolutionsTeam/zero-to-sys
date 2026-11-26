# Conectar o MCP

> Criar o link pessoal do MCP no Framia e ligá-lo ao Claude, para o agente desenhar o projeto com as mesmas permissões da pessoa.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/connect-ai e https://framia.com.br/pt-br/docs/faq |
| **Categoria** | Acesso |
| **Tipo** | Servidor MCP remoto (HTTP), autenticado pelo próprio endereço |
| **Quem faz** | A pessoa cria o link no app; o comando de conexão pode ser rodado por ela ou pelo agente, com o link que ela passar |
| **Verificado em** | 2026-11-26 |

## O que é o "token"

O Framia não mostra um token separado. A credencial é um **link pessoal**:

```text
https://api.framia.com.br/mcp/k/<sua-chave>
```

Por trás dele há uma chave chamada **Link do MCP**, que aparece em **Ajustes → Chaves MCP** e pode ser revogada. Quem tem o link age como a pessoa em todos os projetos que ela abre.

## Criar o link

1. No app, abra **Conectar IA** no menu da esquerda (ícone de robô).
2. Escolha o cartão **MCP**.
3. Em **Qual IA você usa?**, escolha **Claude**.
4. Clique em **Criar meu link**.
5. Clique em **Copiar**. O link aparece uma vez só; perdeu, crie outro.

Para o Codex, crie o link pela página do Claude e use o comando do Codex abaixo.

## Ligar no Claude Code

Pelo terminal:

```bash
claude mcp add --scope user --transport http framia "https://api.framia.com.br/mcp/k/<sua-chave>"
claude mcp list
```

O `framia` deve aparecer como conectado. Use sempre `--scope user`: vale em todos os projetos e fica fora do repositório.

Pelo painel: digite `/mcp`, adicione um servidor com nome `framia`, tipo HTTP, a URL do link e o escopo **User**.

Abra uma sessão nova depois de adicionar. As ferramentas aparecem como `mcp__framia__<nome>`.

## Ligar no app do Claude

1. **Configurações → Conectores → Adicionar conector personalizado**.
2. Nome: **Framia**. URL: o link. Autenticação: **sem login**.
3. **Adicionar** e, se aparecer, **Vincular**.

## Ligar no Codex

```bash
codex mcp add framia --url "https://api.framia.com.br/mcp/k/<sua-chave>"
codex mcp list
```

Fica salvo em `~/.codex/config.toml`, usado pelo terminal, pela extensão e pelo app. Reinicie o Codex depois de adicionar.

## Testar

Numa conversa nova: "Liste os meus projetos do Framia". O agente chama `list_projects`. Nesta skill, o teste é `list_workspaces`, que também mostra o papel da pessoa em cada equipe.

## Quando não conecta

| Sintoma | O que conferir |
|---|---|
| As ferramentas `mcp__framia__*` não existem | `claude mcp list`; sessão aberta antes de adicionar o servidor; servidor desligado em `/mcp` |
| Servidor aparece com falha | Link colado pela metade (ele só aparece inteiro uma vez); link revogado em **Ajustes → Chaves MCP**. Crie outro |
| Erro `rate_limited` com `retryAfterSec` | Passou de 300 chamadas de ferramenta por minuto. Espere o tempo indicado e junte mudanças em menos chamadas |
| **Você chegou ao limite do plano** | Limite de projetos, páginas, tabelas ou componentes ([doc 01](01-conta-equipe-e-planos.md)) |
| O agente não consegue editar | A pessoa é **Leitor** na equipe ou o projeto está somente leitura |

## Revogar

1. **Ajustes → Chaves MCP**. Cada link aparece como "Link do MCP".
2. **Revogar** e confirme. O acesso cai na hora.
3. Para voltar a usar, crie um link novo em **Conectar IA** e refaça o `claude mcp add`.

Revogue quando o link vazar e quando deixar de usar aquele computador.

## Segurança

- **Trate o link como senha.** Não cole em `.mcp.json` versionado, `CLAUDE.md`, commit, issue, chat nem print.
- **Um link por pessoa.** Cada um do time cria o seu; não compartilhe.
- **Não repita o link na conversa.** O agente que recebeu o link para rodar o comando não o escreve de volta nem o grava em arquivo do projeto.
- **O que o agente pode avisar ao Framia:** `send_feedback` relata falha de ferramenta ao time do Framia, sem nomes, chaves nem conteúdo do projeto.

## O que o MCP não cobre

O **Assistente** dentro do editor é outro caminho: usa uma chave de API da Anthropic ou da OpenAI, cobrada por uso no provedor (**Conectar IA** → **Chave de API**). Ele não é preciso para esta skill e não conta no limite de chamadas do MCP.

## Combina com / alternativas

Combina com:
- [MCP na skill ia](../../ia/docs/07-mcp.md): escopos, custo de contexto e riscos de qualquer servidor MCP.
- [Permissões e segurança](../../ia/docs/09-permissoes-e-seguranca.md): regras `allow` e `deny` por ferramenta, para liberar as leituras do Framia sem pergunta.

Alternativa: desenhar à mão no editor. Serve para ajuste fino; para montar o sistema inteiro, o agente pelo MCP é o caminho.
