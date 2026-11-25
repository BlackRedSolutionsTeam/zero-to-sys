# user-experience

Skill para o Claude Code que explica as diferenças de experiência do usuário entre celular, tablet e desktop e como adaptar cada tela a cada um. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por tema ([docs/](docs/)), cada um com a tabela comparativa dos três dispositivos, regras com números e fonte, erros comuns e código.

## Temas cobertos

| Tema | O que responde | Documento |
|---|---|---|
| Contexto de uso | O que muda de fato entre os três dispositivos | [docs/01-contexto-de-uso.md](docs/01-contexto-de-uso.md) |
| Mobile | Como projetar para celular | [docs/02-mobile.md](docs/02-mobile.md) |
| Tablet | Como projetar para tablet | [docs/03-tablet.md](docs/03-tablet.md) |
| Desktop | Como projetar para desktop | [docs/04-desktop.md](docs/04-desktop.md) |
| Breakpoints e layout | Pontos de quebra e como o layout se adapta | [docs/05-breakpoints-e-layout.md](docs/05-breakpoints-e-layout.md) |
| Navegação | Barra inferior, trilho, barra lateral, voltar | [docs/06-navegacao.md](docs/06-navegacao.md) |
| Toque, mouse e teclado | Alvos, hover, gestos, atalhos, foco | [docs/07-toque-mouse-teclado.md](docs/07-toque-mouse-teclado.md) |
| Formulários | Teclado certo, validação, etapas | [docs/08-formularios.md](docs/08-formularios.md) |
| Tabelas e dados | O que a tabela vira no celular, filtros, gráficos | [docs/09-tabelas-e-dados.md](docs/09-tabelas-e-dados.md) |
| Modais, folhas e painéis | Qual camada usar em cada dispositivo | [docs/10-modais-folhas-e-paineis.md](docs/10-modais-folhas-e-paineis.md) |
| Tipografia e densidade | Tamanho de fonte, linha, espaçamento | [docs/11-tipografia-e-densidade.md](docs/11-tipografia-e-densidade.md) |
| Desempenho e rede | Celular lento, rede ruim, offline | [docs/12-desempenho-e-rede.md](docs/12-desempenho-e-rede.md) |
| iOS, Android e web | Diferenças de plataforma; site, PWA ou app | [docs/13-ios-android-web.md](docs/13-ios-android-web.md) |

O [docs/README.md](docs/README.md) tem o índice, um guia "Qual escolher" e a lista do que ficou fora, com o motivo.

## Instalação

A skill é a pasta inteira (`SKILL.md` mais `docs/`). Coloque-a em um destes lugares:

```bash
# Para todos os projetos
ln -s ~/zero-to-sys/skills/user-experience ~/.claude/skills/user-experience

# Só para um projeto
ln -s ~/zero-to-sys/skills/user-experience .claude/skills/user-experience
```

## Como usar

O Claude carrega a skill sozinho quando o pedido é projetar ou revisar uma tela que roda em mais de um tamanho. Também dá para chamar direto com `/user-experience`. Exemplos:

- "Deixa essa tela responsiva."
- "Como essa tabela deve ficar no celular?"
- "/user-experience o sistema vai rodar num tablet no balcão, o que muda?"

Com a skill carregada, o Claude:

1. descobre em quais dispositivos o sistema será usado e qual é o principal;
2. lê o documento de contexto e o do dispositivo principal;
3. escolhe os documentos de tema pela tabela do [SKILL.md](SKILL.md);
4. projeta do menor para o maior, aplicando as regras e o código de cada documento;
5. confere em 360 px, cerca de 768 px e 1280 px ou mais;
6. explica o que muda em cada dispositivo.

## Estrutura

```
user-experience/
├── SKILL.md      guia de decisão e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md             índice, "Qual escolher" e o que ficou fora
    ├── 01-contexto-de-uso.md
    ├── 02-mobile.md … 04-desktop.md        um por dispositivo
    └── 05-… a 13-…                         um por tema que muda entre eles
```

## Como manter

- **Adicionar um tema:** crie `docs/NN-nome.md` com as mesmas seções dos outros (a tabela "Celular, tablet e desktop" é obrigatória) e inclua-o nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Revisar dados:** tamanhos de alvo, pontos de quebra, limites de desempenho e suporte de navegador foram conferidos em 2026-11-24. Cada documento tem a data em "Verificado em"; atualize-a ao revisar.
