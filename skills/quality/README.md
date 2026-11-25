# quality

Skill para o Claude Code que define como provar que o sistema funciona: estratégia de testes, testes de unidade, integração com banco, API e contrato, ponta a ponta, acessibilidade e desempenho automáticos, o que barra o PR e a definição de pronto. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com configuração pronta para copiar.

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Pirâmide de testes | O que testar em cada camada | [docs/01-piramide-de-testes.md](docs/01-piramide-de-testes.md) |
| Testes de unidade | Regras de negócio puras | [docs/02-testes-de-unidade.md](docs/02-testes-de-unidade.md) |
| Integração com banco | Banco real, migrations reais, isolamento | [docs/03-testes-de-integracao-com-banco.md](docs/03-testes-de-integracao-com-banco.md) |
| API e contrato | Testar como o cliente usa | [docs/04-testes-de-api-e-contrato.md](docs/04-testes-de-api-e-contrato.md) |
| Ponta a ponta | Fluxos principais com Playwright | [docs/05-ponta-a-ponta-com-playwright.md](docs/05-ponta-a-ponta-com-playwright.md) |
| Acessibilidade e desempenho | axe e Lighthouse CI | [docs/06-acessibilidade-e-desempenho-automaticos.md](docs/06-acessibilidade-e-desempenho-automaticos.md) |
| Quality gates no CI | O que barra o PR | [docs/07-quality-gates-no-ci.md](docs/07-quality-gates-no-ci.md) |
| Definição de pronto | Quando um item está pronto | [docs/08-definition-of-done.md](docs/08-definition-of-done.md) |
| Verificação pelo agente | Como o agente prova o que fez | [docs/09-verificacao-pelo-agente.md](docs/09-verificacao-pelo-agente.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/quality ~/.claude/skills/quality
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é testar uma funcionalidade, configurar o CI de qualidade ou saber se algo está pronto. Também dá para chamar direto com `/quality`. Exemplos:

- "Escreve os testes do agendamento a partir dos critérios de aceite."
- "Configura o Playwright para o fluxo de agendar consulta."
- "/quality o que precisa barrar o PR neste projeto?"

Com a skill carregada, o Claude:

1. lê os critérios de aceite do item;
2. escolhe a camada de cada critério;
3. escreve e roda os testes, conferindo que eles falham sem o código;
4. confere os quality gates do CI;
5. fecha com a definição de pronto e mostra a evidência.

## Estrutura

```
quality/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                                   índice e "Por onde começar"
    ├── 01-piramide-de-testes.md
    ├── 02-testes-de-unidade.md
    ├── 03-testes-de-integracao-com-banco.md
    ├── 04-testes-de-api-e-contrato.md
    ├── 05-ponta-a-ponta-com-playwright.md
    ├── 06-acessibilidade-e-desempenho-automaticos.md
    ├── 07-quality-gates-no-ci.md
    ├── 08-definition-of-done.md
    └── 09-verificacao-pelo-agente.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** comandos e versões foram conferidos em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
