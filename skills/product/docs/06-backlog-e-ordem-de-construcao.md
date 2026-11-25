# Backlog e ordem de construção

> Monte o backlog em fatias verticais pequenas, com o primeiro item andando de ponta a ponta e os itens que destravam outros no começo.

| | |
|---|---|
| **Referência** | Alistair Cockburn, "Walking Skeleton" (alistair.cockburn.us); Richard Lawrence e Peter Green, "Patterns for Splitting User Stories" (humanizingwork.com); Mike Cohn, "User Stories Applied" (2004); Bill Wake, critérios INVEST, "INVEST in Good Stories, and SMART Tasks" (2003) |
| **Categoria** | Produto |
| **Tipo** | Prática de planejamento |
| **Vale para** | Qualquer sistema com tela, API e banco; equipe pequena ou um dev com agente de IA |
| **Verificado em** | 2026-11-24 |

## O que é

Backlog é a lista de coisas a construir. "Ordem de construção" quer dizer que a lista já está na sequência em que o código será escrito.

Quatro ideias sustentam essa lista:

- **Fatia vertical:** cada item atravessa dados, API e tela e entrega algo que o usuário consegue usar. O contrário é a fatia horizontal: "fazer todo o banco primeiro", depois toda a API, depois todas as telas. Nesse caminho nada funciona até o fim.
- **Walking skeleton (esqueleto andante):** termo de Alistair Cockburn. É uma implementação mínima que faz uma ação real de ponta a ponta. Ela prova que as peças se conectam. O primeiro item do backlog é esse esqueleto.
- **Destravar primeiro:** login e cadastro base vêm antes do que depende deles.
- **Dependência explícita:** cada item diz de quais outros depende.

## Por que usar

- **Algo usável cedo:** o cliente vê o sistema funcionando já nos primeiros itens.
- **Risco aparece cedo:** problema de integração, de deploy ou de permissão surge no item 1, não na véspera da entrega.
- **PR pequeno:** item pequeno vira PR pequeno e fácil de revisar.
- **Dá para parar:** se o prazo apertar, o que já foi entregue está completo e funciona.

## Quando usar

- Depois de ter o escopo do MVP e as histórias com critérios de aceite.
- Antes de escrever a primeira linha de código.
- Sempre que entrar uma demanda nova: ela entra na lista e ganha lugar na ordem.

No zero-to-sys, esse backlog é a entrada do ciclo por funcionalidade do orquestrador. Para cada item, na ordem: dados, API, tela, qualidade, deploy em staging. Só depois vem o próximo item.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site/landing | 🟡 Serve | Poucos itens e quase sem dependência; uma lista curta basta |
| MVP de SaaS | ✅ Ótimo | Esqueleto cedo e fatias pequenas validam a ideia sem desperdício |
| SaaS em crescimento | ✅ Ótimo | Muitas demandas pedem ordem, dependência e item pequeno |
| Sistema interno | ✅ Ótimo | Cadastro base e permissões destravam quase todo o resto |
| API/integração | 🟡 Serve | A fatia atravessa dados e API; a "tela" pode ser um teste de contrato |
| App mobile | ✅ Ótimo | Publicar na loja é lento; vale ter o esqueleto rodando logo |
| Protótipo descartável de uma tarde | ❌ Evite | Planejar a ordem custa mais do que fazer |

## Quando é bom

- **Item entrega valor sozinho:** dá para demonstrar e testar.
- **Cabe em 1 a 2 dias**, ou num PR pequeno e revisável. Passou disso, divida.
- **Dependências visíveis:** ninguém começa um item sem o que ele precisa.
- **Risco na frente:** o que é mais incerto (pagamento, integração externa, regra complexa) entra cedo, quando ainda dá tempo de mudar de plano.
- **Prioridade por valor e por risco:** entre dois itens livres, faça primeiro o que o cliente mais quer ou o que mais pode dar errado.

Como dividir uma história grande (padrões de Richard Lawrence):

- **Passos do fluxo:** primeiro o caminho mais simples, depois os demais.
- **Regras de negócio:** uma regra por item.
- **Variações de dados:** um tipo de dado por vez.
- **Operações:** criar, ver, editar e apagar em itens separados.
- **Caminho feliz primeiro**, tratamento de erros e casos raros depois.
- **Simples antes do complexo:** versão básica agora, refinamentos depois.

## Quando é ruim

- **Banco, API e telas em blocos separados:** nada roda até o último bloco.
- **Item gigante:** "módulo de agendamento" não é item. Ninguém sabe quando termina.
- **Dependência escondida:** o item 5 só funciona com o 3, mas ninguém anotou.
- **Esqueleto adiado:** deixar o deploy para o fim esconde problemas até a hora pior.
- **Ordem só por gosto:** começar pelo que é divertido e deixar o difícil para o fim.
- **Backlog congelado:** a lista muda quando se aprende algo. Reordene sem culpa.

## Como começar

Modelo de `BACKLOG.md` (copie e preencha):

```markdown
# Backlog

Ordem de construção. Um item por vez: dados, API, tela, qualidade, deploy em staging.
Status: a fazer | em andamento | pronto

| # | Item | História | Depende de | Status |
|---|------|----------|------------|--------|
| 1 | Nome curto da fatia | Como [papel], quero [ação] para [benefício] | - | a fazer |
```

Exemplo para um sistema de agendamento (clínica pequena):

```markdown
| # | Item | História | Depende de | Status |
|---|------|----------|------------|--------|
| 1 | Esqueleto: ver a tela inicial com dado do banco | Como equipe, quero o sistema no ar em staging para provar que as peças se conectam | - | pronto |
| 2 | Login e logout | Como atendente, quero entrar com e-mail e senha para acessar o sistema | 1 | em andamento |
| 3 | Cadastro de profissionais | Como atendente, quero cadastrar profissionais para poder agendar com eles | 2 | a fazer |
| 4 | Cadastro de serviços | Como atendente, quero cadastrar serviços com duração para calcular o horário | 2 | a fazer |
| 5 | Cadastro de clientes | Como atendente, quero cadastrar clientes para vinculá-los a agendamentos | 2 | a fazer |
| 6 | Criar agendamento (caminho feliz) | Como atendente, quero marcar um horário livre para um cliente | 3, 4, 5 | a fazer |
| 7 | Impedir horário em conflito | Como atendente, quero ser avisada se o horário já está ocupado | 6 | a fazer |
| 8 | Cancelar agendamento | Como atendente, quero cancelar um agendamento para liberar o horário | 6 | a fazer |
| 9 | Agenda do dia | Como profissional, quero ver minha agenda do dia para me organizar | 6 | a fazer |
| 10 | Lembrete por e-mail | Como cliente, quero receber um lembrete para não esquecer a consulta | 6 | a fazer |
```

Por que essa ordem: o item 1 é o esqueleto. Os itens 2 a 5 destravam o resto. O item 6 é a história grande "agendar" dividida: primeiro o caminho feliz (item 6), depois a regra de conflito (item 7) e o cancelamento (item 8). O lembrete (item 10) depende de integração com e-mail, que é incerta; se for o maior risco, suba a posição dele.

Checklist rápido por item: cabe em 1 a 2 dias? Entrega algo usável? As dependências estão na coluna? Tem critérios de aceite na história?

## Combina com / alternativas

Combina com:
- [Escopo do MVP](02-escopo-do-mvp.md): define o que entra na lista.
- [Fluxos e jornadas](03-fluxos-e-jornadas.md): mostram as dependências entre passos.
- [Histórias e critérios de aceite](04-historias-e-criterios-de-aceite.md): a coluna História e o "pronto" de cada item.
- [Regras de negócio](05-regras-de-negocio.md): cada regra pode virar um item.
- [Onde registrar](07-onde-registrar.md): onde o `BACKLOG.md` mora.
- [Commits e PRs pequenos](../../coding/docs/11-commits-e-prs-pequenos.md): item pequeno gera PR pequeno.

Alternativas: story mapping (Jeff Patton, "User Story Mapping", 2014) para ver a jornada inteira antes de fatiar; quadro kanban com colunas por status; ferramenta de issues do repositório no lugar de um arquivo.

## Decisão rápida

- **Use se:** o sistema tem mais de uma tela ou regra e você quer algo funcionando cedo, com revisão fácil.
- **Evite se:** é um protótipo descartável ou um site de uma página, onde a ordem não muda nada.
