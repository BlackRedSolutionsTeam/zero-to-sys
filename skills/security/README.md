# security

Skill para o Claude Code que cuida da segurança no nível da aplicação: login, sessão, recuperação e 2FA, papéis e permissões, OWASP no código, rate limit, upload, dependências e LGPD na prática. Ela reúne um guia de decisão ([SKILL.md](SKILL.md)) e um documento por prática ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Escolha do login | Senha, link mágico, social, passkeys, SSO | [docs/01-escolha-do-login.md](docs/01-escolha-do-login.md) |
| Sessão e tokens | Cookie, JWT, expiração e revogação | [docs/02-sessao-e-tokens.md](docs/02-sessao-e-tokens.md) |
| Recuperação e 2FA | Recuperar conta e segundo fator | [docs/03-recuperacao-e-2fa.md](docs/03-recuperacao-e-2fa.md) |
| Papéis e permissões | Autorização no servidor, RBAC, ownership | [docs/04-papeis-e-permissoes.md](docs/04-papeis-e-permissoes.md) |
| OWASP no código | Ataques comuns e a defesa de cada um | [docs/05-owasp-no-codigo.md](docs/05-owasp-no-codigo.md) |
| Rate limit | Limitar tentativas e abuso | [docs/06-rate-limit.md](docs/06-rate-limit.md) |
| Upload de arquivos | Receber arquivo sem abrir brecha | [docs/07-upload-de-arquivos.md](docs/07-upload-de-arquivos.md) |
| Dependências vulneráveis | Auditar e atualizar pacotes | [docs/08-dependencias-vulneraveis.md](docs/08-dependencias-vulneraveis.md) |
| LGPD na prática | Consentimento, exportar e apagar dados | [docs/09-lgpd-na-pratica.md](docs/09-lgpd-na-pratica.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/security ~/.claude/skills/security
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/security`. Exemplos:

- "Qual login uso nesse SaaS e como guardo a sessão?"
- "Admin e recepcionista veem coisas diferentes. Como faço as permissões?"
- "/security revisa a segurança das rotas deste projeto."

Com a skill carregada, o Claude:

1. descobre quem usa o sistema e o que cada papel pode fazer;
2. escolhe login e sessão e confere o checklist de cada rota;
3. aplica rate limit, upload seguro e auditoria de dependências;
4. confere o que a LGPD pede em tela e rota;
5. pede os testes de negação à skill `quality`.

## Estrutura

```
security/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-escolha-do-login.md
    ├── 02-sessao-e-tokens.md
    ├── 03-recuperacao-e-2fa.md
    ├── 04-papeis-e-permissoes.md
    ├── 05-owasp-no-codigo.md
    ├── 06-rate-limit.md
    ├── 07-upload-de-arquivos.md
    ├── 08-dependencias-vulneraveis.md
    └── 09-lgpd-na-pratica.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Padrões e versões foram conferidos em 2026-11-24. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
