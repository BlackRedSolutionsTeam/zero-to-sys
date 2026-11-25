# Ambiente local

Um documento por tópico, do Compose ao README de onboarding. Versões e imagens foram conferidas em 2026-11-25 nas fontes oficiais.

## Subir

| Prática | O que entrega | Doc |
|---|---|---|
| Docker Compose | Banco, cache, fila e e-mail local | [01-docker-compose-banco-cache-fila-email.md](01-docker-compose-banco-cache-fila-email.md) |
| Devcontainer | Editor dentro de um contêiner padronizado | [02-devcontainer.md](02-devcontainer.md) |

## Configurar

| Prática | O que entrega | Doc |
|---|---|---|
| .env.example e segredos | Variáveis documentadas, nada sensível no Git | [03-env-example-e-segredos-de-desenvolvimento.md](03-env-example-e-segredos-de-desenvolvimento.md) |
| Seeds e dados de teste | Telas cheias no dia 1, sem dado real | [04-seeds-e-dados-de-teste-locais.md](04-seeds-e-dados-de-teste-locais.md) |

## Automatizar

| Prática | O que entrega | Doc |
|---|---|---|
| Scripts de uma linha | `up`, `test`, `reset`, `clean` | [05-scripts-de-uma-linha.md](05-scripts-de-uma-linha.md) |
| Hooks de pré-commit | Formatação, lint e segredos antes do commit | [06-hooks-de-pre-commit-e-formatacao.md](06-hooks-de-pre-commit-e-formatacao.md) |

## Documentar e alinhar

| Prática | O que entrega | Doc |
|---|---|---|
| README de onboarding | Do clone ao sistema rodando | [07-readme-de-onboarding.md](07-readme-de-onboarding.md) |
| Paridade com produção | Mesma versão de banco e runtime | [08-paridade-com-producao.md](08-paridade-com-producao.md) |

## Por onde começar

- **Projeto novo:** 08 (decida as versões) → 01 → 03 → 04 → 05 → 06 → 07.
- **Time com setup demorado:** 02, 05 e 07.
- **"Na minha máquina funciona":** 08.
- **Quer barrar código fora do padrão:** 06.
