# product

Skill para o Claude Code que transforma o pedido do cliente em produto definido antes de escrever código: escopo do MVP, fluxos, regras de negócio, histórias com critérios de aceite e backlog em ordem de construção. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com modelos prontos para copiar.

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Entrevista | Descobrir problema, público e funcionalidades em linguagem do cliente | [docs/01-entrevista-com-o-cliente.md](docs/01-entrevista-com-o-cliente.md) |
| Escopo do MVP | Dentro, fora e depois; como cortar | [docs/02-escopo-do-mvp.md](docs/02-escopo-do-mvp.md) |
| Fluxos e jornadas | Fluxo principal, erros, estados de tela | [docs/03-fluxos-e-jornadas.md](docs/03-fluxos-e-jornadas.md) |
| Histórias e critérios de aceite | Cada item com Dado / Quando / Então | [docs/04-historias-e-criterios-de-aceite.md](docs/04-historias-e-criterios-de-aceite.md) |
| Regras de negócio | O que pode, o que não pode, máquina de estados | [docs/05-regras-de-negocio.md](docs/05-regras-de-negocio.md) |
| Backlog | Fatias verticais e ordem de construção | [docs/06-backlog-e-ordem-de-construcao.md](docs/06-backlog-e-ordem-de-construcao.md) |
| Onde registrar | `README`, `BACKLOG.md`, issues e o que o agente lê | [docs/07-onde-registrar.md](docs/07-onde-registrar.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/product ~/.claude/skills/product
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é definir o MVP, escrever histórias, levantar regras de negócio ou montar o backlog. Também dá para chamar direto com `/product`. Exemplos:

- "Um cliente quer um sistema de agendamento para a clínica dele. O que entra no MVP?"
- "Escreve as histórias com critérios de aceite para o cadastro de pedidos."
- "/product monta o backlog em ordem de construção para este sistema."

Com a skill carregada, o Claude:

1. lê o que já existe e pergunta só o que for dúvida, em uma ou duas rodadas;
2. fecha um resumo e espera o ok;
3. corta o escopo do MVP, escreve o fluxo principal e as regras de negócio;
4. quebra em histórias com critérios de aceite e ordena o backlog em fatias verticais;
5. registra tudo no repositório (`README`, `BACKLOG.md`, `docs/regras-de-negocio.md`).

## Estrutura

```
product/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                             índice e "Por onde começar"
    ├── 01-entrevista-com-o-cliente.md
    ├── 02-escopo-do-mvp.md
    ├── 03-fluxos-e-jornadas.md
    ├── 04-historias-e-criterios-de-aceite.md
    ├── 05-regras-de-negocio.md
    ├── 06-backlog-e-ordem-de-construcao.md
    └── 07-onde-registrar.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** as referências foram conferidas em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
