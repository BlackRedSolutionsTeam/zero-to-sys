# Segurança base

> Conjunto mínimo de práticas que fecha as falhas mais comuns da infraestrutura: acessos, rede, criptografia e dependências.

| | |
|---|---|
| **Site** | https://owasp.org e https://cheatsheetseries.owasp.org |
| **Categoria** | Segurança |
| **Tipo** | Prática (lista de verificação) |
| **Stack** | Independente |
| **Preço** | Sem custo de licença; custo é tempo da equipe |
| **Licença** | Não se aplica. Fontes lidas em 2026-11-24: OWASP Top 10:2025 (top10.owasp.org), OWASP Cheat Sheet Series (Authentication, Secrets Management, Transport Layer Security, Database Security, Docker Security, Logging), documentação do GitHub (Dependabot), manual do UFW (manpages.ubuntu.com), guia do OpenSSH da Ubuntu Server, documentação da Cloudflare (proteção da origem) e guia de IAM da AWS. |
| **Verificado em** | 2026-11-24 |

## O que é

Não é um produto. É uma lista de hábitos que reduz muito o risco com pouco esforço. Segurança de código da aplicação (validação de entrada, autenticação) é assunto da skill de coding e de stacks; aqui fica a camada de infra.

Os quatro eixos: **menor privilégio** (cada pessoa e serviço com o mínimo de acesso), **rede** (só o necessário fica exposto), **criptografia** (TLS em trânsito e dados criptografados em repouso) e **atualização** (sistema, imagens e dependências em dia).

## Por que usar

- **Erro básico está na lista oficial de riscos:** o OWASP Top 10:2025 traz Broken Access Control (A01), Security Misconfiguration (A02) e Software Supply Chain Failures (A03) entre as três primeiras categorias; chave exposta, porta aberta, senha fraca e componente desatualizado cabem nelas.
- **Custa pouco no começo** e muito depois.
- **Clientes e contratos exigem.**
- **Reduz o dano** quando algo vaza: o acesso comprometido tem pouco poder.
- **Facilita auditoria** e resposta a incidente.

## Quando usar

- Desde o primeiro deploy, não depois do primeiro susto.
- Antes de armazenar dado pessoal ou de pagamento.
- A cada nova integração, conta ou servidor.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ✅ Ótimo | HTTPS, 2FA nas contas e dependências em dia bastam |
| MVP / protótipo | ✅ Ótimo | Segredos fora do código, 2FA e banco fechado |
| SaaS pequeno | ✅ Ótimo | Menor privilégio, backup e atualização de dependências |
| SaaS em crescimento | ✅ Ótimo | Separação de ambientes, auditoria e varredura contínua |
| Sistema corporativo | ✅ Ótimo | Rede privada, papéis, registro de acesso e revisão periódica |
| Servidor próprio (VPS) | ✅ Ótimo | Firewall, SSH por chave e atualizações são sua tarefa |
| Dados pessoais ou financeiros | ✅ Ótimo | Exige o máximo da lista e, em geral, revisão jurídica (LGPD) |
| Requisito regulatório específico (PCI, HIPAA) | ❌ Evite | Esta lista não basta; exige processo e consultoria própria |

## Quando é bom

- **Itens simples e de alto retorno:** 2FA, TLS e atualização automática.
- **Independe de fornecedor:** vale em PaaS, VPS ou nuvem.
- **Cada camada ajuda a outra:** borda, rede, identidade e dado.
- **Mensurável:** dá para checar item por item.

## Quando é ruim

- **Lista não é garantia:** sem revisão periódica, regras ficam velhas.
- **Segurança em excesso paralisa:** bloqueios sem critério levam a atalhos perigosos.
- **Permissões amplas "só por enquanto"** viram permanentes; revise e remova.
- **Confiar só na borda:** a Cloudflare não corrige uma senha fraca nem um bucket aberto.
- **Atualizar sem teste** quebra produção; use homologação e o pipeline.
- **Não cobre regulação específica:** PCI, HIPAA e similares exigem mais.

## Como começar

Lista mínima, em ordem. Cada item traz a fonte que o sustenta.

1. **2FA** em GitHub, provedor de nuvem, registrador de domínio, e-mail e painéis (Coolify, Dokploy, Cloudflare). Fonte: OWASP Authentication Cheat Sheet: MFA é "by far the best defense against the majority of password-related attacks"; AWS IAM: "require MFA" para usuário IAM e usuário raiz.
2. **Menor privilégio:** usuário da aplicação no banco sem poder de administrador; papéis de nuvem por função; credenciais da conta raiz protegidas. Fontes: OWASP Database Security Cheat Sheet: "employ the principle of least privilege" e evitar contas administrativas embutidas; AWS IAM: "grant only the permissions required to perform a task" e seção própria para proteger as credenciais do usuário raiz. (A afirmação "nenhuma conta raiz no dia a dia" foi retirada: a página da AWS manda proteger as credenciais e remete a outra página, que não foi lida.)
3. **Rede:**
   - **Banco isolado:** banco sem IP público ou limitado por lista de IPs. Fonte: OWASP Database Security: "The application's backend database should be isolated from other servers" e regras de firewall limitando a porta a hosts específicos.
   - **Firewall:** liberar só 80 e 443 e restringir o SSH. Fonte: manual do UFW (política padrão de entrada é negar; veja o exemplo abaixo).
   - **SSH por chave:** o guia do OpenSSH da Ubuntu Server descreve a autenticação por chaves criptográficas, sem senha, e a reforça com 2FA (U2F/FIDO ou TOTP). O guia não manda desativar a senha; essa etapa fica a seu critério.
   - **Origem só atrás da Cloudflare:** a Cloudflare lista três formas na página "Protect your origin server": liberar só os IPs da Cloudflare (avaliada como moderadamente segura e "vulnerable to IP spoofing"), Authenticated Origin Pulls e Cloudflare Tunnel (avaliado como muito seguro; exige o `cloudflared` na origem). Prefira as duas últimas à lista de IPs. Veja [Cloudflare](08-cloudflare.md).
4. **TLS** em toda conexão e redirecionamento de HTTP para HTTPS. Fonte: OWASP Transport Layer Security Cheat Sheet: "TLS should be used for all pages, not just those that are considered sensitive"; site público escuta na porta 80 e redireciona com 301, de preferência com HSTS. Em API, a página manda desativar o HTTP e falhar a requisição sem criptografia, em vez de redirecionar. Para o banco: OWASP Database Security: "Configure the database to only allow encrypted connections".
5. **Segredos** fora do código ([doc 09](09-segredos-e-configuracao.md)). Fonte: OWASP Secrets Management Cheat Sheet: não embutir segredos em `ENV` ou `ARG` do Docker; "You should regularly rotate secrets"; "Secrets must have the minimum privileges assigned to them".
6. **Dependências:** ative a atualização automática de dependências no repositório e a varredura de imagens Docker.
   - **Dependabot:** o GitHub pede o arquivo `.github/dependabot.yml`, que "must start with `version: 2`". A documentação marca como obrigatórias só as chaves `version` e `updates`; em cada item de `updates` você informa `package-ecosystem`, `directory` (ou `directories`) e `schedule.interval`.
   - **Varredura de imagens:** OWASP Docker Security Cheat Sheet (regra 9): "Container scanning tools are especially important"; reescaneie também no registro e em produção.
   - **Teste antes de publicar:** OWASP Vulnerable Dependency Management Cheat Sheet: atualizar a dependência primeiro em ambiente de teste e só então enviar para produção.
   - **Risco coberto:** OWASP Top 10:2025, A03 Software Supply Chain Failures.
7. **Contêiner sem root e versão fixa.** Fonte: OWASP Docker Security Cheat Sheet: regra 2, usuário sem privilégios é "the best way" de evitar escalada de privilégio; regra 9, "Ensure the base image version is pinned" (versão fixa não se atualiza sozinha; revise com regularidade). Não exponha `/var/run/docker.sock` a outros contêineres (regra 1). O item "imagem enxuta" foi retirado: a página não o cobre.
8. **Backup e logs de acesso.** Fontes: OWASP Database Security: "Configure a regular backup of the database", com permissões e, de preferência, criptografia; OWASP Logging Cheat Sheet: registre "Authentication successes and failures", proteja os logs e respeite o prazo de retenção; OWASP Top 10:2025, A09 Security Logging & Alerting Failures. A parte "testado" foi retirada daqui por falta de fonte lida; o [doc 11](11-backup-e-recuperacao.md) trata do assunto.

Em servidor Linux, exemplo de firewall com UFW. O manual do UFW diz que o padrão ao instalar é negar a entrada, que `ufw default allow|deny|reject [incoming|outgoing|routed]` muda a política e que habilitar o firewall pode derrubar conexões SSH em andamento; por isso a regra do SSH vem antes do `enable`. Este exemplo libera a 22 para todos; para restringir, informe um IP de origem na regra.

```bash
sudo ufw default deny incoming
sudo ufw allow 22/tcp && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw enable
```

## Combina com / alternativas

- [Segredos e configuração](09-segredos-e-configuracao.md), [Cloudflare](08-cloudflare.md) e [Backup](11-backup-e-recuperacao.md): peças desta base.
- [GitHub Actions](07-github-actions.md): varredura e atualização no pipeline.
- [Docker e Kubernetes](04-docker-kubernetes.md): contêiner sem root e versão fixa.
- Alternativas e complementos: OWASP Top 10 e Cheat Sheet Series (fontes desta ficha); auditoria externa quando o risco ou o contrato pedir.

## Decisão rápida

- **Use se:** o sistema tem usuário, dado ou dinheiro envolvido (ou seja, sempre).
- **Evite se:** a intenção é tratar esta lista como certificação. Para exigência regulatória, busque quem faça auditoria e processo formal.
