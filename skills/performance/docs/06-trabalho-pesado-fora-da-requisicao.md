# Trabalho pesado fora da requisição

> Se a tarefa demora, depende de terceiros ou pode esperar, responda rápido ao usuário e faça o trabalho num worker; este doc diz quando mover, não como montar a fila.

| | |
|---|---|
| **Referência** | Skill `integrations`, doc 05 (filas e jobs) e doc 06 (rotinas agendadas); PostgreSQL docs, `SELECT ... FOR UPDATE SKIP LOCKED`; MDN, status `202 Accepted` (developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/202) |
| **Categoria** | Desempenho |
| **Tipo** | Prática de decisão |
| **Vale para** | Node, Python, .NET, Java, Laravel e Go |
| **Verificado em** | 2026-11-25 |

## O que é

Uma requisição HTTP deve responder em centenas de milissegundos. O que passa disso (gerar PDF, enviar e-mail, importar planilha, chamar API lenta, processar imagem) segue por outro caminho: a requisição grava uma **tarefa** numa fila, responde `202 Accepted` com um identificador e um **worker** (processo separado) executa depois. O cliente consulta o andamento ou recebe um aviso ao fim.

A montagem da fila, o retry, o timeout e a idempotência estão em [filas e jobs](../../integrations/docs/05-filas-e-jobs.md). Este doc cuida da **decisão de mover** e do efeito no desempenho.

## Por que usar

- **Resposta rápida:** o usuário não espera o PDF de 8 segundos para ver "recebemos seu pedido".
- **Isola a lentidão:** terceiro fora do ar não derruba a API; o job tenta de novo.
- **Absorve picos:** mil importações entram na fila e o worker as consome no ritmo que o banco aguenta.
- **Escala separada:** o worker cresce sem a API crescer junto.

## Quando usar

Mova para fora da requisição quando a tarefa:

| Critério | Exemplo |
|---|---|
| Passa de 1 a 2 segundos | Relatório, exportação, PDF, redimensionar imagens |
| Depende de serviço externo | E-mail, WhatsApp, gateway, webhook de saída |
| Pode falhar e precisa de nova tentativa | Cobrança, sincronização com ERP |
| Processa volume | Importar 20 mil linhas |
| Não precisa do resultado na hora | Notificações, recálculo, limpeza |

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Formulário de contato e geração de imagens; poucas tarefas |
| MVP de SaaS | ✅ Ótimo | E-mail e relatórios em job desde cedo evitam tela travada |
| SaaS em crescimento | ✅ Ótimo | Filas separadas por prioridade e workers que escalam sozinhos |
| Sistema interno/corporativo | ✅ Ótimo | Importações e fechamentos longos fora do horário |
| API/integração | ✅ Ótimo | Processamento assíncrono com webhook de retorno |
| App mobile com backend | ✅ Ótimo | O app não deve esperar processamento em rede ruim |
| Tarefa curta e que o usuário precisa ver já | ❌ Evite | A fila só adiciona atraso e complexidade |

## Quando é bom

- **Latência da API cai** e fica estável, porque o trabalho pesado não disputa CPU com as requisições.
- **Retry com recuo** resolve falhas temporárias sem intervenção.
- **Limite de concorrência no worker** protege o banco e as APIs de terceiros.
- **Fila em Postgres** (`SKIP LOCKED`) basta para volume baixo ou médio e evita um serviço novo ([integrations, doc 05](../../integrations/docs/05-filas-e-jobs.md)).

## Quando é ruim

- **Resultado imediato necessário:** se a tela precisa do dado para continuar, a fila complica a experiência.
- **Fila que cresce sem parar:** o worker é mais lento que a entrada. Meça o tamanho da fila e a idade da tarefa mais antiga e alerte.
- **Job sem idempotência:** com retry, o cliente pode receber duas cobranças ou dois e-mails ([API, idempotência](../../api/docs/06-idempotencia-e-retries.md)).
- **Mais peças para operar:** worker, fila, monitoramento e tarefas mortas (dead letter).
- **Perda de contexto:** erro no job não chega ao usuário se ninguém o notifica; defina o que mostrar na falha.

## Como começar

Padrão de resposta da API: aceitar, devolver o identificador e deixar o cliente consultar.

```http
POST /relatorios/mensal HTTP/1.1
Authorization: Bearer ...

HTTP/1.1 202 Accepted
Location: /relatorios/mensal/jobs/9f2c

{"job_id":"9f2c","status":"queued"}
```

```http
GET /relatorios/mensal/jobs/9f2c HTTP/1.1

HTTP/1.1 200 OK

{"job_id":"9f2c","status":"done","url":"https://arquivos.clinica-exemplo.com.br/relatorios/9f2c.pdf"}
```

Roteiro de decisão:

1. Medir a rota ([doc 01](01-medir-primeiro.md)) e confirmar que o tempo está na tarefa, não numa consulta mal feita ([doc 02](02-banco-explain-n-mais-1-e-pool.md)).
2. Se o tempo é CPU do próprio código, ver o [perfil](05-profiling-por-stack.md) antes de mover; às vezes a função tem solução simples.
3. Se continua passando de 1 a 2 segundos ou depende de terceiro, mover para job.
4. Definir o que o usuário vê enquanto espera (barra de progresso, notificação, e-mail com o link) e quando falha.
5. Monitorar duas coisas: tamanho da fila e idade da tarefa mais antiga.

Quando o gargalo é só a espera em chamadas externas na própria requisição, chamar em paralelo e com timeout curto pode bastar, sem fila.

Para tarefas que repetem em horário fixo (fechamento, limpeza), veja [rotinas agendadas](../../integrations/docs/06-rotinas-agendadas.md).

## Combina com / alternativas

- [Filas e jobs](../../integrations/docs/05-filas-e-jobs.md), [rotinas agendadas](../../integrations/docs/06-rotinas-agendadas.md) e [tempo real e notificações](../../integrations/docs/08-tempo-real-e-notificacoes.md) para avisar o fim do job.
- [Escalar](07-escalar-vertical-horizontal-e-replica.md): o worker é a primeira peça que se separa e se multiplica.
- [Importar e exportar planilhas](../../integrations/docs/09-importar-e-exportar-planilhas.md).
- Alternativa sem fila: resposta em streaming ou paginação para exportações médias.

## Decisão rápida

- **Mova** para um worker o que passa de 1 a 2 segundos, depende de terceiro ou precisa de retry.
- **Não mova** o que o usuário precisa ver na hora e é rápido.
- **Sempre:** `202` com identificador, job idempotente e alerta no tamanho da fila.
