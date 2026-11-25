# Serena

> Kit de ferramentas MCP que dá ao agente navegação e edição no nível de símbolo (definição, referências, renomear, inserir depois de um símbolo) usando servidores de linguagem, no lugar de ler arquivos inteiros.

| | |
|---|---|
| **Site/repositório** | https://github.com/oraios/serena |
| **Categoria** | LSP/símbolos |
| **Tipo** | Camada LSP (biblioteca própria SolidLSP) ou plugin JetBrains; sem índice de embeddings |
| **Como se conecta** | MCP: `serena setup claude-code` ou `claude mcp add` (veja abaixo) |
| **Linguagens suportadas** | Mais de 40 com o backend LSP (Python, Java, Go, Rust, TypeScript, C/C++, C#, Kotlin, Ruby, PHP e outras); algumas exigem dependências extras |
| **Preço** | Grátis com LSP; o plugin JetBrains é pago, com teste grátis |
| **Licença** | Aplicação GPL-3.0-or-later; SolidLSP em MIT |
| **Verificado em** | 2026-11-24 |

## O que é

Serena roda como servidor MCP e fala com servidores de linguagem (LSP) por baixo. O agente pede "símbolo X" ou "quem referencia X" e recebe só aquele trecho. Também edita por símbolo, o que evita reescrever arquivos grandes. O projeto se descreve como "a IDE do seu agente de código".

O README diz que as ferramentas simbólicas são "muito mais eficientes em tokens" do que ler arquivos, mas não traz número. Também diz que as ferramentas básicas (ler arquivo, buscar padrão, listar pasta, executar shell) costumam vir desligadas em harnesses como o Claude Code, para não duplicar as nativas.

## Por que usar

- **Edição por símbolo**, não só leitura: o README lista ferramentas simbólicas de edição (por exemplo, inserir depois de um símbolo e renomear).
- **Muitas linguagens** pelo mesmo MCP.
- **Ferramentas configuráveis** por YAML, para reduzir o que é anunciado ao modelo.
- **Local por padrão** com LSP.
- Cerca de 31,7 mil estrelas (31.678 no GitHub em 2026-11-24).

## Quando usar

- Base grande em linguagem tipada, com muitas edições localizadas.
- Quando o LSP nativo do Claude Code não cobre a linguagem ou quando se quer edição simbólica.
- Refatorações em que reescrever o arquivo inteiro gastaria contexto.

## Para que tipo de base/tarefa

Cada linha traz o fato do documento que sustenta o encaixe e a fonte dele. A fonte é o README do projeto, salvo indicação.

| Base/tarefa | Encaixe | Por quê |
|---|---|---|
| Base média/grande | ✅ Ótimo | As ferramentas simbólicas são "muito mais eficientes em tokens" que ler arquivos, sem número (README) |
| Refatoração com impacto | ✅ Ótimo | O README lista edição simbólica, como inserir depois de um símbolo e renomear |
| Busca por texto exato | ❌ Evite | As ferramentas básicas de busca de padrão costumam vir desligadas em harnesses como o Claude Code (README) |
| Linguagem pouco comum | ✅ Ótimo | Mais de 40 linguagens com o backend LSP; algumas exigem dependências extras (README) |
| Código que não pode sair da máquina | ✅ Ótimo | Com LSP o funcionamento é local, sem serviço externo (README); o LLM do agente é outra questão |
| Sessão só no terminal sem uv | 🟡 Serve | O README manda instalar com `uv`, não por marketplace |

## Quando é bom

- **Edição simbólica:** o README diz que as ferramentas de edição simbólica são "less error-prone and much more token-efficient" que as alternativas típicas, sem número.
- **Configuração por contexto** (`--context claude-code`) que desliga o que o Claude Code já tem.
- **Opção JetBrains** para quem já trabalha na IDE (Rider e CLion não são suportados, segundo o README).

## Quando é ruim

- **Licença GPL-3.0** na aplicação: confira se serve ao seu uso, principalmente se for distribuir algo junto.
- **Custo de contexto:** meça com `/context` depois de ligar.
- **Partida lenta** do servidor: a documentação de clientes do Serena sugere `MCP_TIMEOUT=60000` (oraios.github.io/serena).
- **O README manda não instalar via marketplace de MCP ou plugin**; use `uv`.
- **Qualidade depende do servidor de linguagem** de cada linguagem.
- Última versão: v2.1.0, de 2026-10-19 (conferido no GitHub em 2026-11-24).

## Como começar

```bash
uv tool install -p 3.13 serena-agent
serena init
serena setup claude-code
```

Manual, para todos os projetos:

```bash
claude mcp add --scope user serena -- serena start-mcp-server --context claude-code --project-from-cwd
```

Só para o projeto atual: `claude mcp add serena -- serena start-mcp-server --context claude-code --project "$(pwd)"`. Confira com `/mcp`.

## Combina com / alternativas

- [LSP nativo do Claude Code](02-lsp-claude-code.md): mais simples, só leitura; use um ou outro para a mesma linguagem, não os dois.
- [CodeGraph](01-codegraph.md): visão ampla e fluxo.
- Sobre MCP em geral e custo de ferramentas no contexto: veja a skill `ia`.

## Decisão rápida

- **Use se:** a base é grande, a linguagem é tipada e você quer editar por símbolo.
- **Evite se:** a base é pequena, a licença GPL é problema, ou o LSP nativo do Claude Code já cobre sua linguagem.
