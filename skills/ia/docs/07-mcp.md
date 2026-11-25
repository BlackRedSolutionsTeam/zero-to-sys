# MCP (Model Context Protocol)

> Protocolo aberto para ligar o agente a sistemas externos (tracker, banco, navegador) por servidores que expõem ferramentas.

| | |
|---|---|
| **Documentação oficial** | https://code.claude.com/docs/en/mcp e https://modelcontextprotocol.io |
| **Categoria** | Integração com ferramentas externas |
| **Tipo** | Servidor local (stdio) ou remoto (HTTP), configurado por CLI ou `.mcp.json` |
| **Onde vale** | Claude Code e muitos outros clientes que seguem o protocolo aberto |
| **Equivalente em outras ferramentas** | O próprio protocolo MCP; a configuração varia por cliente |
| **Verificado em** | 2026-11-24 |

## O que é

MCP é um padrão para o agente chamar ferramentas de outros sistemas. Cada servidor expõe ferramentas (e às vezes recursos e prompts). No Claude Code você adiciona pelo terminal:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --env CHAVE=valor --transport stdio nome -- npx -y pacote-do-servidor
```

Escopos confirmados: `local` (padrão, só você neste projeto, em `~/.claude.json`), `project` (arquivo `.mcp.json` na raiz, vai para o git) e `user` (todos os seus projetos). Outros comandos: `claude mcp list`, `claude mcp get nome`, `claude mcp remove nome`; dentro da sessão, `/mcp` mostra o estado e faz o login por OAuth. Servidores do `.mcp.json` pedem sua aprovação na primeira vez.

SSE está marcado como descontinuado na documentação; prefira HTTP.

## Por que usar

- **Alcança o que o código não mostra:** issue, erro em produção, design, banco de dados.
- **Autenticação pronta:** `/mcp` faz o login por OAuth dos servidores remotos.
- **Padrão aberto:** o mesmo servidor serve a mais de um cliente.
- **Compartilhável:** `.mcp.json` leva a configuração ao time.

## Quando usar

- O sistema não tem CLI que o agente consiga usar.
- Você precisa que o agente leia e escreva num serviço (tracker, wiki, monitoramento).

### Quando o agente deve propor

- **Sinais** (gatilho "keep copying data from a browser tab Claude can't see", features-overview): o agente pediu ao usuário para colar dados de um sistema externo (card, log de erro, tela do design, registro do banco) mais de uma vez; a tarefa depende de consultar esse sistema várias vezes; não existe CLI do serviço ou ela não cobre o que é preciso.
- **O que fazer:** só propor, nunca conectar por conta própria. Diga qual servidor, quem o mantém, que acesso ele pede e o comando `claude mcp add` pronto. Sugira `--scope project` (grava no `.mcp.json`, versionado) quando o time todo usa, e `--scope user` quando é só da pessoa. Credencial sempre por variável de ambiente, nunca escrita no arquivo.
- **Não proponha se:** uma CLI já instalada resolve (`gh`, `az`, `psql`), o dado foi necessário uma vez só, ou o servidor não é oficial do serviço nem de fonte que o usuário conheça.

## Encaixe por tipo de tarefa

| Tipo de tarefa/projeto | Encaixe | Por quê |
|---|---|---|
| Tarefa ligada a um card ou erro externo | ✅ Ótimo | O agente lê o card ou o stack trace direto da fonte |
| Verificação visual (navegador) | ✅ Ótimo | Servidor de navegador permite ver a tela e o console |
| Serviço que já tem CLI (`gh`) | 🟡 Serve | A documentação diz que a CLI "is usually the easiest way in"; MCP é para sistemas sem CLI (best-practices) |
| Servidor desconhecido na base inteira | ❌ Evite | Risco de injeção de prompt e de vazamento (ver abaixo) |

## Quando é bom

- **Escopo claro:** `project` para o time, `user` para o que é só seu.
- **Variáveis de ambiente:** `.mcp.json` aceita `${VAR}` e `${VAR:-padrão}`, então a chave não vai para o git.
- **Controle por ferramenta:** dá para permitir ou negar ferramentas de um servidor nas regras de permissão.

## Quando é ruim

- **Contexto:** servidores conectados colocam nomes e instruções das ferramentas no contexto mesmo sem uso, e a documentação de boas práticas manda desligar os que você não usa (em `/mcp`). Com a busca de ferramentas ("MCP tool search"), padrão em modelos compatíveis, só nomes e instruções entram no início e as definições carregam sob demanda. Ela não é suportada no Microsoft Foundry hospedado no Azure (conferido em code.claude.com/docs/en/mcp em 2026-11-24).
- **Injeção de prompt:** servidor que busca conteúdo externo pode trazer texto malicioso para o contexto do agente. A documentação diz para confiar em cada servidor antes de conectar.
- **Não é auditado pela Anthropic:** ela revisa conectores do diretório, mas não faz auditoria de segurança de servidor de terceiros.
- **Servidores aparecem por vários caminhos:** `.mcp.json`, escopos de usuário, conectores do claude.ai e plugins. Revisar só o `.mcp.json` não mostra tudo.
- **Servidor local roda com seus poderes:** o stdio executa um programa na sua máquina e a sandbox do shell não o cobre.
- **Saída enorme:** respostas grandes consomem contexto. Há aviso quando a saída passa de 10.000 tokens e o limite padrão é 25.000 (`MAX_MCP_OUTPUT_TOKENS`); texto com mais de 50.000 caracteres é salvo em arquivo (conferido em code.claude.com/docs em 2026-11-24).
- **Tempo de inicialização:** `MCP_TIMEOUT` ajusta o limite de partida do servidor (mcp).

## Como começar

```bash
# remoto, com token em variável de ambiente
claude mcp add --transport http api https://api.exemplo.com/mcp \
  --header "Authorization: Bearer $TOKEN_DA_API"

# compartilhado com o time
claude mcp add --scope project --transport http notion https://mcp.notion.com/mcp
```

Resultado em `.mcp.json`:

```json
{
  "mcpServers": {
    "notion": { "type": "http", "url": "https://mcp.notion.com/mcp" }
  }
}
```

Dentro da sessão: `/mcp` para autenticar e ver o estado. Para ver o que cada servidor consome, use `/usage`. Para parar de carregar um servidor sem removê-lo, desligue-o em `/mcp`.

## Combina com / alternativas

Combina com:
- [Permissões e segurança](09-permissoes-e-seguranca.md): regras `allow` e `deny` por ferramenta de MCP.
- [Gestão de contexto](06-gestao-de-contexto.md): MCP é custo fixo da sessão.
- [Prompt e verificação](11-prompt-e-verificacao.md): servidor de navegador dá o check visual.

Alternativas:
- CLI do serviço: com a `gh` instalada e autenticada, o Claude abre PRs e lê comentários sem explicação (best-practices, "Connect the tools Claude needs").
- Hook do tipo `mcp_tool`: chama uma ferramenta de MCP num ponto fixo do ciclo.

## Decisão rápida

- **Use se:** o sistema não tem CLI útil, você usa a integração com frequência e confia no servidor.
- **Evite se:** a CLI resolve, o servidor é desconhecido ou você só precisaria dele uma vez.

Fontes das recomendações: code.claude.com/docs/en/best-practices ("Connect the tools Claude needs"), features-overview ("Build your setup over time", tabela de funcionalidades) e security ("MCP security").
