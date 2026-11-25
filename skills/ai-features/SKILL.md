---
name: ai-features
description: Guia para pôr IA e LLM dentro do produto (chat, assistente, RAG, extração de dados, classificação, resumo, agente com ferramentas) de forma útil, barata e segura — quando IA vale a pena e quando regra comum resolve, escolha de provedor e modelo com preço conferido (Claude Haiku 5.5, Sonnet 5.5, Opus 5.5 e Fable 5.2), prompts e saída estruturada com validação, RAG com embeddings e pgvector, ferramentas e agentes, avaliação com conjunto de testes, guardrails contra injeção de prompt e LGPD, custo, cache e limites por usuário, streaming, filas e timeouts. Use sempre que o usuário pedir "colocar IA no sistema", "chatbot", "assistente no produto", "integrar com a API do Claude", "RAG", "busca semântica", "embeddings", "pgvector", "extrair dados de PDF ou e-mail com IA", "classificar com LLM", "saída em JSON do modelo", "agente com ferramentas", "quanto custa a API de IA", "prompt injection" ou "streaming de resposta". Não é sobre usar IA para escrever o código (skill ia) e não repete segurança geral (security), banco (data), filas (integrations), testes (quality) nem observabilidade (infra).
---

# ai-features

Guia para quem vai pôr chat, assistente, RAG, extração ou classificação com LLM dentro do sistema. A skill `ia` trata do agente que escreve o código; esta trata de IA como funcionalidade do produto. IA custa por uso, erra de vez em quando e recebe texto de usuários: por isso cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Confirme que IA é a ferramenta certa** ([doc 01](docs/01-quando-ia-vale-a-pena.md)). Se uma regra de 10 linhas resolve, não use LLM.
2. **Escolha provedor e modelo** ([doc 02](docs/02-provedor-e-modelo.md)): comece no menor modelo que passa nos seus testes e faça a conta de custo por uso. A chave de API fica só no backend.
3. **Defina o contrato de saída** ([doc 03](docs/03-prompts-saida-estruturada-e-validacao.md)): esquema JSON na API e validação no código antes de agir.
4. **Se o conteúdo vem de documentos**, monte o RAG ([doc 04](docs/04-rag-chunking-embeddings-pgvector.md)), com pgvector primeiro e filtro por empresa. Se cabe no contexto, use cache em vez de RAG.
5. **Se o modelo precisa agir no sistema**, use poucas ferramentas e confirmação humana ([doc 05](docs/05-ferramentas-e-agentes-no-produto.md)).
6. **Crie a avaliação antes de lançar** ([doc 06](docs/06-avaliacao-e-regressao-de-prompt.md)): 30 a 50 casos reais, nota por código, rodando no CI.
7. **Proteja** ([doc 07](docs/07-guardrails-injecao-e-lgpd.md)): injeção de prompt, menor privilégio e dados pessoais.
8. **Controle o custo** ([doc 08](docs/08-custo-cache-limites-e-fallback.md)): registre `usage`, use cache, dê orçamento por usuário e tenha fallback sem IA.
9. **Desenhe a interface** ([doc 09](docs/09-streaming-filas-e-timeouts.md)): streaming para chat, fila para tarefa longa, timeout e estados de erro.

## Qual abordagem por necessidade

| Necessidade | Abordagem | Modelo inicial |
|---|---|---|
| Extrair campos de texto livre | Saída estruturada com esquema (doc 03) | `claude-haiku-5-5` |
| Classificar ou rotear mensagens | Saída com `enum` (doc 03) | `claude-haiku-5-5` |
| Responder dúvidas sobre manuais e políticas | RAG com pgvector (doc 04) ou contexto longo com cache | `claude-sonnet-5-5` |
| Assistente que consulta e age no sistema | Ferramentas com confirmação humana (doc 05) | `claude-sonnet-5-5` |
| Tarefa longa e difícil, agente de várias etapas | Fila e orçamento por tarefa (docs 05, 09) | `claude-opus-5-5` |
| Raciocínio que o Opus 5.5 não resolve nos testes | Subir de modelo só com prova (doc 06) | `claude-fable-5-2` |
| Processar milhares de documentos sem urgência | Batch API, 50% de desconto (doc 08) | Haiku 5.5 ou Sonnet 5.5 |
| Chat com resposta aparecendo aos poucos | Streaming SSE (doc 09) | `claude-sonnet-5-5` |

Preços, limites e IDs conferidos em 2026-11-25 em `platform.claude.com`; tabela completa no [doc 02](docs/02-provedor-e-modelo.md).

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Quando IA vale a pena | [docs/01-quando-ia-vale-a-pena.md](docs/01-quando-ia-vale-a-pena.md) | Critério de decisão: LLM ou regra comum |
| Provedor e modelo | [docs/02-provedor-e-modelo.md](docs/02-provedor-e-modelo.md) | Modelos Claude, preço, limites, privacidade, conta de custo |
| Prompts e saída estruturada | [docs/03-prompts-saida-estruturada-e-validacao.md](docs/03-prompts-saida-estruturada-e-validacao.md) | Prompt, JSON Schema, Zod, validação na borda |
| RAG | [docs/04-rag-chunking-embeddings-pgvector.md](docs/04-rag-chunking-embeddings-pgvector.md) | Chunking, embeddings, pgvector, citação |
| Ferramentas e agentes | [docs/05-ferramentas-e-agentes-no-produto.md](docs/05-ferramentas-e-agentes-no-produto.md) | Tool use, laço do agente, confirmação humana |
| Avaliação | [docs/06-avaliacao-e-regressao-de-prompt.md](docs/06-avaliacao-e-regressao-de-prompt.md) | Conjunto de testes, nota, regressão no CI |
| Guardrails e LGPD | [docs/07-guardrails-injecao-e-lgpd.md](docs/07-guardrails-injecao-e-lgpd.md) | Injeção de prompt, menor privilégio, dados pessoais |
| Custo e fallback | [docs/08-custo-cache-limites-e-fallback.md](docs/08-custo-cache-limites-e-fallback.md) | Cache, lote, orçamento por usuário, erros e fallback |
| Streaming e filas | [docs/09-streaming-filas-e-timeouts.md](docs/09-streaming-filas-e-timeouts.md) | SSE, fila de tarefas, timeouts, estados da tela |

## Ligações com as outras skills

| Skill | O que ela cobre aqui |
|---|---|
| `stacks` | SDKs e linguagem do backend que chama a API |
| `data` | pgvector, multiempresa, dados pessoais no banco |
| `security` | Rate limit, permissões, OWASP, LGPD geral |
| `integrations` | Filas e jobs, tempo real, pagamentos para cobrar a franquia de IA |
| `quality` | Pirâmide de testes e quality gates no CI para a avaliação |
| `infra` | Segredos, observabilidade e custo de infraestrutura |
| `ia` | O agente de código (Claude Code); não é o assunto desta skill |

## Checklist

- [ ] Existe um motivo escrito para usar IA e um plano sem IA se o provedor cair.
- [ ] A chave de API está só no backend, em segredo, uma por ambiente.
- [ ] O ID do modelo vem de configuração e o menor modelo que passa nos testes foi o escolhido.
- [ ] A saída que o código lê segue um esquema e é validada antes de uso.
- [ ] Existe um conjunto de avaliação (30 casos ou mais) rodando no CI, com nota mínima.
- [ ] Texto de usuário e de terceiros é tratado como não confiável; ferramentas rodam com as permissões do usuário.
- [ ] Ações de escrita, pagamento ou exclusão pedem confirmação humana.
- [ ] Dado pessoal enviado ao modelo tem base legal e é o mínimo necessário; logs sem dado pessoal.
- [ ] `usage` de cada chamada é registrado por usuário e recurso, com orçamento e alerta de gasto.
- [ ] Limites por usuário, `max_tokens`, tempo e passos de agente definidos.
- [ ] Timeout, retry com limite e fallback testados desligando a chave.
- [ ] A interface tem estados de carregando, erro, limite atingido e botão de parar.

## Regras de uso

- **Preço e modelo só conferidos.** Modelos e preços mudam; confirme em `platform.claude.com` e diga a data da conferência ao usuário.
- **Regra comum primeiro.** Cálculo, permissão e validação ficam no código, não no prompt.
- **Saída do modelo é entrada não confiável.** Valide, escape e nunca monte SQL, HTML ou comando com ela.
- **Sem avaliação, sem lançamento.** Mudar prompt ou modelo sem medir é apostar.
- **Nenhuma segurança só no prompt.** Acesso, limites e confirmações ficam no código.
- **A chave nunca sai do backend.** App e navegador chamam a sua API.
- **Custo é funcionalidade.** Registre tokens desde o primeiro dia.
- **Fronteiras.** Código escrito por IA é da `ia`; segurança geral, banco, filas e infra são das skills citadas acima.

## Quando a lista não cobre

Treinar ou ajustar (fine-tuning) modelos, modelos hospedados em GPU própria, geração de imagem e vídeo, voz em tempo real, visão computacional dedicada e ML clássico ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial do provedor.

## Validade dos dados

Modelos, preços, limites, versões do pgvector e modelos de embedding foram conferidos em 2026-11-25 nas páginas oficiais (`platform.claude.com`, `github.com/pgvector/pgvector`) e mudam com frequência; cada documento tem a linha "Verificado em".
