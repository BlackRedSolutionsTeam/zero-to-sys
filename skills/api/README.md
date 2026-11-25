# api

Skill para o Claude Code que define o contrato da API entre front e back: estilo, rotas, status, formato de erro, paginação, versionamento, idempotência, OpenAPI e cliente tipado. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)), explicando quando usar, para que tipo de projeto, quando é bom, quando é ruim e com exemplos prontos.

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Estilo | REST, RPC tipado ou GraphQL | [docs/01-rest-rpc-ou-graphql.md](docs/01-rest-rpc-ou-graphql.md) |
| Rotas, verbos e status | Nomes, métodos e códigos HTTP | [docs/02-rotas-verbos-e-status.md](docs/02-rotas-verbos-e-status.md) |
| Formato de erro | Problem Details, erros por campo | [docs/03-formato-de-erro.md](docs/03-formato-de-erro.md) |
| Paginação e filtros | Listas com limite, cursor e ordenação | [docs/04-paginacao-e-filtros.md](docs/04-paginacao-e-filtros.md) |
| Versionamento | Mudar sem quebrar quem consome | [docs/05-versionamento.md](docs/05-versionamento.md) |
| Idempotência e retries | Clique duplo, rede ruim, webhook repetido | [docs/06-idempotencia-e-retries.md](docs/06-idempotencia-e-retries.md) |
| OpenAPI e documentação | Contrato gerado do código | [docs/07-openapi-e-documentacao.md](docs/07-openapi-e-documentacao.md) |
| Cliente gerado no front | Tipos e chamadas geradas | [docs/08-cliente-gerado-no-front.md](docs/08-cliente-gerado-no-front.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/api ~/.claude/skills/api
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é criar ou mudar rotas, padronizar erros, paginar uma lista ou documentar a API. Também dá para chamar direto com `/api`. Exemplos:

- "Cria as rotas do agendamento a partir do BACKLOG.md."
- "Padroniza o formato de erro da API."
- "/api gera o cliente tipado do front a partir do OpenAPI."

Com a skill carregada, o Claude:

1. descobre quem consome a API;
2. define rotas, status, formato de erro e de lista;
3. protege as operações que não podem repetir;
4. gera o OpenAPI e a documentação;
5. gera o cliente tipado do front e confere o checklist de rota nova.

## Estrutura

```
api/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md                       índice e "Por onde começar"
    ├── 01-rest-rpc-ou-graphql.md
    ├── 02-rotas-verbos-e-status.md
    ├── 03-formato-de-erro.md
    ├── 04-paginacao-e-filtros.md
    ├── 05-versionamento.md
    ├── 06-idempotencia-e-retries.md
    ├── 07-openapi-e-documentacao.md
    └── 08-cliente-gerado-no-front.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** RFCs e bibliotecas foram conferidos em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
