---
name: security
description: Cuida da segurança no nível da aplicação — escolha do login, sessão e tokens, recuperação de senha e 2FA, papéis e permissões (autorização no servidor, isolamento entre empresas), OWASP no código, rate limit, upload seguro de arquivos, dependências vulneráveis e LGPD na prática. Use sempre que o sistema tiver login, perfis de acesso, upload ou dado pessoal, ou quando o usuário pedir "faz o login", "admin e usuário comum", "permissões", "deixa seguro", "revisa a segurança", "rate limit", "upload de arquivo", "LGPD", "2FA" ou "recuperar senha". Não cuida de WAF, rede, TLS nem segredos do ambiente (skill infra), das tabelas (skill data), nem do lado jurídico da LGPD (advogado).
---

# security

Guia para que só entre quem pode, cada um veja só o que é seu e um erro de código não vire vazamento. A `stacks` escolhe a biblioteca de login e a `infra` protege o ambiente; esta skill cuida do que fica no meio: o código da aplicação. Cada tópico tem um documento em `docs/` com quando usar, para que tipo de projeto, quando é bom, quando é ruim e exemplos prontos.

## Como usar esta skill

1. **Levante quem usa o sistema** na skill `product`: tipos de usuário, o que cada papel faz, se há várias empresas, se há dado pessoal ou sensível.
2. **Escolha o login** pelo público ([doc 01](docs/01-escolha-do-login.md)) e a sessão ([doc 02](docs/02-sessao-e-tokens.md)). Use a biblioteca da stack; nunca escreva criptografia de senha própria.
3. **Modele papéis e permissões** ([doc 04](docs/04-papeis-e-permissoes.md)): toda checagem no servidor, negar por padrão, recurso de outra empresa responde 404.
4. **Cubra recuperação de conta e segundo fator** ([doc 03](docs/03-recuperacao-e-2fa.md)).
5. **Passe o checklist de ataques** ([doc 05](docs/05-owasp-no-codigo.md)) e ponha limites de uso ([doc 06](docs/06-rate-limit.md)).
6. **Se houver upload**, siga o [doc 07](docs/07-upload-de-arquivos.md); **ligue a auditoria de dependências** no CI ([doc 08](docs/08-dependencias-vulneraveis.md)).
7. **Se houver dado pessoal**, transforme os direitos do titular em tela e rota ([doc 09](docs/09-lgpd-na-pratica.md)) e use o lado do banco da skill `data`.
8. **Peça os testes de negação** (papel X não acessa Y; empresa A não vê B) à skill `quality`.

## Qual login usar

| Projeto | Login recomendado | Observação |
|---|---|---|
| Site de conteúdo, landing | Sem login (ou só no painel interno) | Painel do CMS com senha forte e 2FA |
| MVP de SaaS | E-mail e senha + Google | Biblioteca da stack; verificar e-mail |
| SaaS em crescimento | + 2FA e recuperação robusta; passkeys opcionais | Revisar sessão e rate limit |
| Sistema interno, corporativo | SSO da empresa (OIDC ou SAML) | Evite senha própria se a empresa já tem identidade |
| API para parceiros | Chave de API ou OAuth 2.0 | Escopos por chave; rotação |
| App mobile | OIDC com token curto + refresh | Guarde no armazenamento seguro do aparelho |

## Tópicos

| Tópico | Documento | Papel |
|---|---|---|
| Escolha do login | [docs/01-escolha-do-login.md](docs/01-escolha-do-login.md) | Métodos, build x buy, guarda de senha |
| Sessão e tokens | [docs/02-sessao-e-tokens.md](docs/02-sessao-e-tokens.md) | Cookie x JWT, expiração, revogação |
| Recuperação e 2FA | [docs/03-recuperacao-e-2fa.md](docs/03-recuperacao-e-2fa.md) | Recuperar conta, TOTP e passkeys |
| Papéis e permissões | [docs/04-papeis-e-permissoes.md](docs/04-papeis-e-permissoes.md) | Autorização no servidor, RBAC, BOLA |
| OWASP no código | [docs/05-owasp-no-codigo.md](docs/05-owasp-no-codigo.md) | Ataque → defesa → onde olhar |
| Rate limit | [docs/06-rate-limit.md](docs/06-rate-limit.md) | Limitar tentativas e abuso |
| Upload de arquivos | [docs/07-upload-de-arquivos.md](docs/07-upload-de-arquivos.md) | Validar, guardar e servir com segurança |
| Dependências vulneráveis | [docs/08-dependencias-vulneraveis.md](docs/08-dependencias-vulneraveis.md) | Auditar e atualizar pacotes |
| LGPD na prática | [docs/09-lgpd-na-pratica.md](docs/09-lgpd-na-pratica.md) | Consentimento, exportar e apagar dados |

## Checklist

- [ ] Senha guardada com hash lento (Argon2id ou bcrypt) pela biblioteca da stack, sem código próprio de criptografia (`grep -ri "md5\|sha1" src`).
- [ ] Cookie de sessão com `HttpOnly`, `Secure` e `SameSite` (ver a configuração de sessão).
- [ ] Toda rota protegida checa autenticação e permissão no servidor, não só na tela (testar com `curl` sem token e com papel errado).
- [ ] Recurso de outra empresa ou de outro usuário responde 404, com teste que prova (suíte de testes de negação).
- [ ] Recuperação de senha com token de uso único, de curta duração e resposta igual exista ou não o e-mail.
- [ ] Rate limit em login, recuperação e rotas de custo alto (resposta 429 após exceder).
- [ ] Consultas parametrizadas, sem concatenar SQL (`grep -rn "SELECT.*+\|\\${" src`).
- [ ] Upload valida tipo pelo conteúdo, tem limite de tamanho e fica fora da pasta pública.
- [ ] Auditoria de dependências no CI e Dependabot (ou equivalente) ligado (`.github/dependabot.yml`).
- [ ] Nenhum segredo no repositório (`git log -p | grep -i "api_key\|secret"`, secret scanning ligado).
- [ ] Se há dado pessoal: telas ou rotas para exportar e apagar os dados da pessoa e registro de consentimento.

## Regras de uso

- **Use a biblioteca da stack para login e sessão.** Auth feito à mão é a fonte mais comum de brecha.
- **Autorização sempre no servidor.** Esconder botão não protege nada; a rota decide.
- **Negar por padrão.** Rota nova nasce protegida; quem libera é uma decisão explícita.
- **404, não 403, para o que é de outro.** Não confirme que o recurso existe.
- **Erro não vaza detalhe.** Resposta genérica para o usuário; detalhe no log (formato na skill `api`).
- **Limite tentativas.** Login, recuperação e criação de conta sem limite é convite para força bruta.
- **Segredo fora do código.** Variáveis de ambiente e gerenciador de segredos (skill `infra`, doc 09).
- **Dependência desatualizada é dívida de segurança.** Auditoria no CI, e atualização regular.
- **LGPD: o código faz a parte técnica.** Base legal, encarregado e contratos pedem advogado; diga isso ao usuário.
- **Fronteiras.** Rede, TLS, WAF e segredos do ambiente são da `infra`; tabelas e criptografia de coluna da `data`; formato de erro da `api`; testes da `quality`.

## Quando a lista não cobre

Pentest, modelagem de ameaças formal, SOC 2 e ISO 27001, PCI DSS (cartão), HIPAA, gestão de identidade corporativa avançada e segurança de IA (prompt injection) ficam fora desta skill. Diga isso ao usuário e cubra com a documentação oficial e, quando for exigência contratual, com especialista.

## Validade dos dados

Padrões (OWASP, RFCs), versões e planos foram conferidos em 2026-11-24. Cada documento tem a linha "Verificado em"; confira a versão da biblioteca de login do projeto antes de copiar uma configuração.
