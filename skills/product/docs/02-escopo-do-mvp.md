# Escopo do MVP

> Decidir o que entra, o que fica de fora e o que vem depois, para entregar o menor produto que resolve o problema principal de ponta a ponta.

| | |
|---|---|
| **Referência** | MoSCoW, do método DSDM (Dai Clegg, criador da técnica, com Richard Barker, *CASE Method Fast-Track: A RAD Approach*, 1994). *Shape Up*, Ryan Singer, Basecamp, 2019 (basecamp.com/shapeup). *The Lean Startup*, Eric Ries, 2011 (origem do termo MVP) |
| **Categoria** | Produto |
| **Tipo** | Prática de priorização e corte de escopo |
| **Vale para** | Qualquer projeto novo, antes de escolher stack ou desenhar telas |
| **Verificado em** | 2026-11-24 |

## O que é

MVP (produto mínimo viável) é a menor versão do sistema que resolve o problema principal do cliente do começo ao fim. Não é uma versão ruim. É uma versão curta e completa.

O escopo é a lista do que será feito. Para fechá-lo, use três grupos: **Dentro** (entra agora), **Fora** (não será feito, e todos sabem) e **Depois** (será feito, mas não nesta entrega).

Duas ideias ajudam a decidir:

- **MoSCoW:** classifica cada item em Must (obrigatório), Should (importante, mas dá para esperar), Could (bom ter) e Won't (não nesta entrega). O MVP é basicamente o Must.
- **Apetite:** do Shape Up. Em vez de perguntar "quanto tempo isso leva?", você diz "quanto tempo isso vale?". O prazo é fixo e o escopo se ajusta a ele.

## Por que usar

- **Entrega mais cedo:** o cliente usa de verdade e corrige a rota com dado real.
- **Menos retrabalho:** você não constrói o que ninguém pediu.
- **Conversa clara com o cliente:** "Fora" e "Depois" por escrito evitam o "achei que estava incluso".
- **Prazo honesto:** o apetite força a escolha em vez de esconder o atraso.

## Quando usar

- No início de qualquer projeto, logo após a entrevista com o cliente.
- Quando a lista de pedidos cresce e o prazo não.
- Quando o cliente diz "quero tudo".
- Antes de estimar, de escolher a stack e de montar o backlog.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site / landing | 🟡 Serve | O escopo já é pequeno; basta separar o que é página agora e o que é blog depois |
| MVP de SaaS | ✅ Ótimo | É o caso de uso central: provar o valor antes de construir o resto |
| SaaS em crescimento | ✅ Ótimo | Cada nova funcionalidade vira um mini escopo com apetite próprio |
| Sistema interno | ✅ Ótimo | Atenda a dor principal do setor e deixe relatórios e perfis para a segunda rodada |
| API / integração | 🟡 Serve | Defina quais rotas e quais parceiros entram; o contrato costuma ser mais rígido |
| App mobile | ✅ Ótimo | Publicar em loja é lento; começar pequeno reduz o custo de cada revisão |
| Contrato com escopo fechado e regulatório | ❌ Evite | Quando a lei ou o contrato exige tudo, não há o que cortar; planeje por entregas |

## Quando é bom

- **O problema principal é claro** e cabe numa frase.
- **O cliente aceita** começar manual e automatizar depois.
- **Há prazo ou orçamento fixo.**
- **Dá para medir o uso** nas primeiras semanas.

## Quando é ruim

- **Cortar qualidade em vez de funcionalidade:** tela quebrada e sem validação não é MVP, é protótipo mal feito.
- **MVP que não fecha o ciclo:** se o usuário não consegue ir do início ao fim, o produto não resolve nada.
- **Tudo vira Must:** se nada fica de fora, não houve priorização.
- **"Depois" sem dono:** vira lixeira. Reveja a lista após cada entrega.
- **Esquecer o básico:** MVP pequeno ainda precisa de segurança e de dados protegidos (veja abaixo).

## Como começar

1. Escreva o problema principal em uma frase: "quem sofre, com o quê".
2. Liste tudo o que o cliente pediu, sem filtrar.
3. Classifique cada item em MoSCoW. O que não é Must sai da entrega.
4. Fixe o apetite: "isto vale 4 semanas".
5. Para cada item Must, pergunte: "dá para fazer à mão por enquanto?". Se sim, faça à mão.
6. Confira o ciclo de ponta a ponta: o usuário consegue completar o trabalho principal só com o que está em Dentro?
7. Confira a lista do que todo MVP precisa e preencha o quadro.

**Como cortar:**

- Corte funcionalidade inteira, nunca a qualidade do que fica. Menos telas, mas cada uma funcionando bem.
- Faça a versão manual antes de automatizar. Exemplo: cobrar por Pix manual e liberar o acesso à mão, antes de integrar um gateway de pagamento.
- Troque o sistema por um processo: confirmação por WhatsApp em vez de notificação automática.
- Diga "ainda não" em vez de "não". O item vai para Depois.

**O que todo MVP precisa, mesmo pequeno:**

- **Login**, se o sistema guarda dado de usuário. Cada pessoa vê só o que é dela.
- **Backup** automático do banco, com restauração testada.
- **Termos de uso e política de privacidade** básicos, com aviso do que é coletado (LGPD).
- **Tratamento de erro** e mensagens claras nas telas principais.

**Modelo de quadro (copie e preencha):**

```markdown
# Escopo do MVP: <nome do sistema>

Problema principal: <quem sofre, com o quê, em uma frase>
Apetite: <tempo que isto vale, ex.: 4 semanas>
Ciclo de ponta a ponta: <do primeiro clique ao resultado final>

## Dentro (Must)
- [ ] <funcionalidade> (manual ou automática?)

## Fora (Won't, e por quê)
- <funcionalidade>: <motivo>

## Depois (Should / Could)
- <funcionalidade>: <gatilho para entrar, ex.: "quando passar de 50 clientes">

## Básico obrigatório
- [ ] Login  - [ ] Backup  - [ ] Termos e LGPD
```

**Exemplo preenchido (agendamento de clínica):**

```markdown
# Escopo do MVP: Agenda da Clínica Sorriso

Problema principal: a recepção perde consultas porque marca tudo no caderno e no WhatsApp.
Apetite: 4 semanas
Ciclo de ponta a ponta: paciente pede horário, recepção confirma, paciente comparece.

## Dentro (Must)
- [ ] Cadastro de paciente (nome, telefone)
- [ ] Agenda por dentista, com horários livres e ocupados
- [ ] Marcar, remarcar e cancelar consulta (feito pela recepção)
- [ ] Lembrete: a recepção envia pelo WhatsApp com um botão que abre a conversa

## Fora (Won't, e por quê)
- Prontuário eletrônico: exige regras de saúde e vira outro projeto
- Convênios e guias: regra muito diferente por operadora

## Depois (Should / Could)
- Pagamento online: hoje a clínica cobra por Pix manual na recepção
- Lembrete automático por WhatsApp: quando passar de 100 consultas por semana
- Agendamento pelo próprio paciente: depois de validar a agenda interna
- Relatório de faltas

## Básico obrigatório
- [x] Login da recepção e dos dentistas  - [x] Backup diário  - [x] Termos e LGPD
```

## Combina com / alternativas

- [01 Entrevista com o cliente](01-entrevista-com-o-cliente.md): fornece o problema e a lista de pedidos.
- [03 Fluxos e jornadas](03-fluxos-e-jornadas.md): desenha o ciclo de ponta a ponta do que ficou em Dentro.
- [04 Histórias e critérios de aceite](04-historias-e-criterios-de-aceite.md): detalha cada item Must.
- [05 Regras de negócio](05-regras-de-negocio.md): regras dos itens que entraram.
- [06 Backlog e ordem de construção](06-backlog-e-ordem-de-construcao.md): ordena o que ficou Dentro.
- [07 Onde registrar](07-onde-registrar.md): onde guardar o quadro.
- Alternativas: matriz valor x esforço, Kano e RICE. Servem para ordenar, mas não substituem a decisão do que fica fora.

## Decisão rápida

- **Use se:** o projeto é novo, o prazo ou o orçamento é limitado e o cliente quer muita coisa de uma vez.
- **Evite se:** o contrato ou a lei exige o sistema completo desde o primeiro dia; nesse caso planeje por entregas, não por corte.
