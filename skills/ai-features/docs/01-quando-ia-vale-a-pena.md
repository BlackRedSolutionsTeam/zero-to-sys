# Quando IA vale a pena e quando regra comum resolve

> Use LLM quando a entrada é texto livre ou ambígua e a resposta tolera pequenos erros; se uma regra, uma consulta ou um filtro resolvem, escreva o código comum, que é mais barato, rápido e previsível.

| | |
|---|---|
| **Referência** | https://platform.claude.com/docs/en/about-claude/models/choosing-a-model, https://platform.claude.com/docs/en/test-and-evaluate/develop-tests |
| **Categoria** | Decisão de produto |
| **Tipo** | Critério de decisão antes de integrar IA |
| **Vale para** | Qualquer sistema que pense em pôr chat, assistente, resumo, extração ou classificação com LLM |
| **Verificado em** | 2026-11-25 |

## O que é

LLM (modelo de linguagem grande) é uma função probabilística: a mesma entrada pode gerar saídas diferentes, cobra por token e leva segundos para responder. Código comum é determinístico, quase de graça e responde em milissegundos. Este doc ajuda a decidir qual dos dois usar em cada funcionalidade.

Exemplo dos docs desta skill: um sistema de agendamento de clínica que quer (1) resumir a anotação de uma consulta, (2) extrair data e médico de uma mensagem de WhatsApp, (3) responder dúvidas com base nas regras da clínica e (4) calcular o valor da consulta com convênio.

## Por que decidir antes

- IA custa por uso, e o custo cresce com o número de usuários, não com o tamanho da equipe.
- Erro de LLM é raro, mas existe; em dinheiro, saúde e lei ele precisa de revisão humana.
- Cada chamada adiciona latência, dependência de um provedor externo e dado pessoal saindo do seu servidor (LGPD).

## Quando usar IA

- **Texto livre vira dado:** extrair campos de e-mail, mensagem, nota fiscal em PDF, currículo.
- **Classificar ou rotear** por significado: tipo de chamado, urgência, intenção da mensagem.
- **Resumir e reescrever:** resumo de consulta, resposta sugerida para o atendente.
- **Responder perguntas sobre documentos** que mudam (manual, políticas, base de conhecimento), com RAG ([doc 04](04-rag-chunking-embeddings-pgvector.md)).
- **Tarefas com muitas variações** em que escrever regras seria interminável.

## Quando regra comum resolve

| Necessidade | Use em vez de LLM |
|---|---|
| Cálculo de preço, imposto, desconto, comissão | Função com testes de unidade |
| Validar CPF, e-mail, data, CEP | Validação por formato e dígito verificador |
| Busca por nome, filtro, ordenação | Consulta SQL ou busca de texto do Postgres |
| Fluxo com passos fixos (cadastro, checkout) | Formulário e máquina de estados |
| Permissão e regra de acesso | Código de autorização (skill `security`) |
| Alerta quando um número passa de um limite | Regra e agendador |
| Respostas fixas para 10 perguntas | Menu ou FAQ estático |

Regra prática: se você consegue escrever a regra em 10 linhas e ela acerta quase sempre, não use LLM.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Busca semântica ou resumo ajudam, mas não são essenciais |
| MVP de SaaS | ✅ Ótimo | Um recurso de IA bem escolhido diferencia o produto com pouco código |
| SaaS em crescimento | ✅ Ótimo | Extração, classificação e assistente reduzem trabalho manual de suporte |
| Sistema interno/corporativo | ✅ Ótimo | Muito texto livre (e-mails, laudos, contratos) para estruturar |
| API/integração | 🟡 Serve | Útil para normalizar entrada suja; evite no caminho crítico síncrono |
| App mobile com backend | 🟡 Serve | A chamada vai pelo backend, nunca com a chave no app |
| Sistema financeiro ou de saúde com decisão automática | ❌ Evite | Sem revisão humana, um erro raro vira dano; use IA só para sugerir |

## Quando é bom

- **Reduz trabalho repetitivo** que hoje uma pessoa faz lendo texto.
- **Falha de forma segura:** o resultado é uma sugestão que a pessoa confirma.
- **Dá para medir:** existe uma resposta certa conhecida e você consegue montar um conjunto de testes ([doc 06](06-avaliacao-e-regressao-de-prompt.md)).
- **Custo por uso cabe no preço do produto:** conta feita antes ([doc 08](08-custo-cache-limites-e-fallback.md)).

## Quando é ruim

- **Exige 100% de acerto** (cálculo, permissão, dinheiro): LLM não garante.
- **Latência importa muito:** várias chamadas em sequência levam segundos.
- **Dados que não podem sair do servidor** e não há provedor com contrato adequado (doc 07).
- **Ninguém vai medir qualidade:** o recurso piora sem ninguém perceber.
- **IA só para "ter IA":** custo e risco sem ganho para o usuário.

## Como começar

Responda por escrito, antes de codar:

1. Qual tarefa do usuário isto elimina ou acelera?
2. Qual é a resposta certa, e quem confere? (Se ninguém, volte ao início.)
3. O que acontece quando a IA erra? (Sugestão revisável é o caso bom.)
4. Quanto custa por uso e quantos usos por mês? (Conta do doc 02 e do doc 08.)
5. Quais dados pessoais entram no prompt? (Doc 07.)
6. Qual é o plano sem IA, se o provedor cair?

Padrão recomendado: **código comum onde der, LLM só no trecho ambíguo**. Exemplo na clínica: o LLM extrai `{ data, medico, especialidade }` da mensagem (doc 03); o código valida a data, consulta a agenda e calcula o valor.

## Combina com / alternativas

- [Provedor e modelo](02-provedor-e-modelo.md): depois de decidir que vale a pena.
- Regras e validação no código: skill `coding`.
- Busca textual e semântica no banco: skill `data` e [doc 04](04-rag-chunking-embeddings-pgvector.md).
- Alternativas sem LLM: regras, SQL, expressões regulares, modelos de classificação clássicos, formulários melhores.

## Decisão rápida

- **Use se:** a entrada é texto livre, a saída é revisável e o custo por uso cabe no preço.
- **Evite se:** uma regra de 10 linhas resolve, ou o erro raro causa dano sem revisão humana.
