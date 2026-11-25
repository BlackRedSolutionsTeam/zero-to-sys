# domains

Skill para o Claude Code que cuida do domínio do sistema: registrar (Registro.br e registrars), configurar o DNS, organizar subdomínios por ambiente, publicar os registros de e-mail (SPF, DKIM, DMARC), manter o HTTPS e não perder o domínio por renovação ou transferência. Ela reúne um guia ([SKILL.md](SKILL.md)) e um documento por tópico ([docs/](docs/)).

## Tópicos cobertos

| Tópico | Papel | Documento |
|---|---|---|
| Registrar o domínio | Registro.br, registrars, titularidade | [docs/01-escolher-e-registrar-o-dominio.md](docs/01-escolher-e-registrar-o-dominio.md) |
| DNS | Registros, TTL e propagação | [docs/02-dns-registros-e-propagacao.md](docs/02-dns-registros-e-propagacao.md) |
| Subdomínios e ambientes | app, api, staging, www x apex | [docs/03-subdominios-e-ambientes.md](docs/03-subdominios-e-ambientes.md) |
| E-mail do domínio | MX, SPF, DKIM, DMARC | [docs/04-email-do-dominio-spf-dkim-dmarc.md](docs/04-email-do-dominio-spf-dkim-dmarc.md) |
| Certificados | HTTPS, renovação, CAA | [docs/05-certificados-e-https.md](docs/05-certificados-e-https.md) |
| Renovação e segurança | Auto-renovação, lock, 2FA, transferência | [docs/06-renovacao-seguranca-e-transferencia.md](docs/06-renovacao-seguranca-e-transferencia.md) |
| Migrar DNS | Trocar de provedor sem queda | [docs/07-migrar-dns-sem-queda.md](docs/07-migrar-dns-sem-queda.md) |

O [docs/README.md](docs/README.md) tem o índice e um guia "Por onde começar".

## Instalação

A skill vem junto com o plugin `zero-to-sys` (veja o [README principal](../../README.md#instalação)). Para usar só esta skill, linke a pasta:

```bash
git clone https://github.com/BlackRedSolutionsTeam/zero-to-sys ~/zero-to-sys
ln -s ~/zero-to-sys/skills/domains ~/.claude/skills/domains
```

## Como usar

O Claude carrega a skill sozinho quando o pedido bate com o tema dela. Também dá para chamar direto com `/domains`. Exemplos:

- "Registra o domínio .com.br da clínica e aponta para o servidor."
- "O e-mail do sistema está caindo no spam. Configura SPF, DKIM e DMARC."
- "/domains vou trocar o DNS de provedor sem derrubar o site."

Com a skill carregada, o Claude:

1. confere se o domínio já existe e em nome de quem;
2. registra ou aponta, com o DNS na Cloudflare por padrão;
3. organiza os subdomínios por ambiente;
4. publica os registros de e-mail e o CAA;
5. confere o checklist (renovação, lock, 2FA, alerta de expiração).

## Estrutura

```
domains/
├── SKILL.md      guia de decisão, checklist e regras de uso, lido pelo Claude
├── README.md     este arquivo
└── docs/
    ├── README.md     índice e "Por onde começar"
    ├── 01-escolher-e-registrar-o-dominio.md
    ├── 02-dns-registros-e-propagacao.md
    ├── 03-subdominios-e-ambientes.md
    ├── 04-email-do-dominio-spf-dkim-dmarc.md
    ├── 05-certificados-e-https.md
    ├── 06-renovacao-seguranca-e-transferencia.md
    └── 07-migrar-dns-sem-queda.md
```

## Como manter

- **Adicionar um tópico:** crie `docs/NN-nome.md` com as mesmas seções dos outros documentos e inclua o tópico nas tabelas do `SKILL.md`, deste README e do `docs/README.md`.
- **Remover um tópico:** apague o documento, tire-o das três tabelas e dos links em "Combina com / alternativas" dos outros documentos.
- **Revisar dados:** Preços e prazos do Registro.br e dos registrars foram conferidos em 2026-11-25. Cada documento tem a data na linha "Verificado em"; atualize-a ao revisar.
