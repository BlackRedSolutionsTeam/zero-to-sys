# design

Skill para o Claude Code que escolhe e aplica UI kits e ícones gratuitos para deixar sites e apps com visual profissional. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por ferramenta ([docs/](docs/)), explicando quando usar, para que tipo de site, quando é bom, quando é ruim e por quê.

## Ferramentas cobertas

Só entrou o que passa em três critérios: qualidade real, visual profissional e boa variedade grátis.

| Ferramenta | Papel | Documento |
|---|---|---|
| shadcn/ui | Base de componentes funcionais e acessíveis em React | [docs/01-shadcn-ui.md](docs/01-shadcn-ui.md) |
| Magic UI | Seções e componentes animados para marketing | [docs/02-magic-ui.md](docs/02-magic-ui.md) |
| Aceternity UI | Efeitos visuais de destaque para landing pages | [docs/03-aceternity-ui.md](docs/03-aceternity-ui.md) |
| HyperUI | Blocos Tailwind em HTML, para qualquer framework | [docs/04-hyperui.md](docs/04-hyperui.md) |
| Lucide | Ícones padrão, traço único | [docs/05-lucide.md](docs/05-lucide.md) |
| Phosphor | Ícones com seis pesos | [docs/06-phosphor.md](docs/06-phosphor.md) |
| Tabler Icons | Catálogo grande de ícones | [docs/07-tabler-icons.md](docs/07-tabler-icons.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que foi avaliado e saiu, com o motivo.

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/design ~/.claude/skills/design
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é criar ou redesenhar uma interface web, ou escolher componentes e ícones. Também dá para chamar direto com `/design`. Exemplos:

- "Monta a landing page do produto, com visual profissional."
- "Qual UI kit eu uso para um painel admin em React?"
- "/design redesenha a home deste site institucional em Astro."

Com a skill carregada, o Claude:

1. identifica o tipo de site e a stack do projeto;
2. escolhe as ferramentas pela tabela do [SKILL.md](SKILL.md);
3. lê o documento de cada ferramenta escolhida antes de instalar;
4. monta a interface seguindo as regras de uso (um set de ícones por projeto, animação só em página de marketing, só itens grátis, adaptar à marca);
5. explica a escolha em uma ou duas frases.

## Estrutura

```
design/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md             índice, "Qual escolher" e o que saiu da lista
    ├── 01-shadcn-ui.md
    ├── 02-magic-ui.md
    ├── 03-aceternity-ui.md
    ├── 04-hyperui.md
    ├── 05-lucide.md
    ├── 06-phosphor.md
    └── 07-tabler-icons.md
```

## Como manter

- **Adicionar uma ferramenta:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua a ferramenta nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover uma ferramenta:** apague o documento, tire-a das três tabelas e dos links em "Combina com / alternativas" dos outros documentos, e registre o motivo em `docs/README.md`.
- **Revisar dados:** preços, licenças e números foram verificados em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
