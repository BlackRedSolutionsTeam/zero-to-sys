# Segredos e configuração

> Prática de manter chaves, senhas e configurações fora do código, separadas por ambiente e fáceis de trocar.

| | |
|---|---|
| **Site** | https://12factor.net/config e https://infisical.com |
| **Categoria** | Segurança e configuração |
| **Tipo** | Prática, com ferramentas de apoio |
| **Stack** | Independente; variáveis de ambiente, gerenciadores de segredos da plataforma ou da nuvem, Infisical |
| **Preço** | Prática: sem custo. Infisical: grátis (5 identidades, 3 ambientes, projetos ilimitados), Pro US$ 20 por identidade/mês no plano anual. AWS Secrets Manager: US$ 0,40 por segredo/mês e US$ 0,05 por 10 mil chamadas de API (us-east-1); GCP Secret Manager: 6 versões ativas e 10 mil acessos grátis por mês, depois US$ 0,06 por versão ativa/mês e US$ 0,03 por 10 mil acessos; Azure Key Vault Standard: US$ 0,03 por 10 mil operações (East US) (páginas e tabelas públicas de preços, conferido em 2026-11-24) |
| **Licença** | Não se aplica à prática. Infisical: MIT, exceto as pastas `ee/`, com licença própria (LICENSE no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

Configuração é tudo que muda entre ambientes (endereço do banco, chaves de API). Segredo é a parte sensível dela. A regra do método 12-factor é guardar a configuração no ambiente, não no código.

Níveis, do mais simples ao mais completo: arquivo `.env` local fora do Git; variáveis de ambiente da plataforma (Vercel, Railway, Coolify, GitHub Actions); gerenciador de segredos (Infisical, ou o da nuvem); e, em ambiente grande, rotação automática e credenciais temporárias.

## Por que usar

- **Evita vazamento:** segredo no Git é difícil de remover de verdade.
- **Troca simples:** rotacionar uma chave não exige novo deploy de código.
- **Ambientes separados:** desenvolvimento, homologação e produção não compartilham chaves.
- **Acesso controlado:** só quem precisa lê o segredo, com registro de acesso.
- **Auditoria** do que foi lido ou alterado, nas ferramentas que oferecem.

## Quando usar

- Em todo projeto, desde o primeiro commit.
- Antes de abrir o repositório ao time ou ao público.
- Ao integrar APIs de terceiros, banco e pagamento.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | 🟡 Serve | Poucos segredos; variáveis do build bastam |
| MVP / protótipo | ✅ Ótimo | Variáveis da plataforma e `.env` fora do Git |
| SaaS pequeno | ✅ Ótimo | Variáveis por ambiente; rotacione chaves ao sair alguém |
| SaaS em crescimento | ✅ Ótimo | Gerenciador de segredos com acesso por papel |
| Sistema corporativo | ✅ Ótimo | Gerenciador da nuvem, rotação e auditoria |
| Chave que o front-end precisa | ❌ Evite | Tudo no navegador é público; use só chaves públicas |
| Repositório público | ✅ Ótimo | Varredura de segredos e nenhuma chave no histórico |
| Time grande | ✅ Ótimo | Acesso por papel e registro de leitura |

## Quando é bom

- **Simples de começar:** variáveis de ambiente já existem em toda plataforma.
- **Gerenciadores dão histórico** de versões e de quem acessou.
- **Credenciais temporárias** (OIDC no CI) eliminam a chave fixa.
- **Padrão conhecido**, sem lock-in no nível básico.

## Quando é ruim

- **`.env` commitado:** apagar depois não limpa o histórico; considere a chave comprometida e troque.
- **Segredo na imagem Docker ou em log:** fica acessível a quem tiver a imagem ou o log.
- **Variáveis de ambiente vazam** em telas de debug e dumps de erro; filtre o que o app expõe.
- **Compartilhar por chat ou e-mail** espalha o segredo sem controle.
- **Uma chave para tudo:** se vaza, vaza tudo. Uma chave por serviço e ambiente.
- **Ferramenta nova sem dono:** um gerenciador de segredos sem responsável vira mais um ponto de falha.
- **Planos pagos de ferramentas** têm preço por identidade; calcule antes.

## Como começar

1. Adicione `.env` ao `.gitignore` e crie um `.env.example` sem valores.
2. No CI, use os secrets do repositório e autenticação OIDC quando possível.
3. Ative a varredura de segredos do GitHub no repositório (chamada de secret scanning; grátis em repositórios públicos, e em repositórios privados de organização exige o GitHub Secret Protection nos planos Team ou Enterprise Cloud; documentação do GitHub, conferido em 2026-11-24).
4. Se o segredo vazou, revogue e gere outro; não basta apagar o commit.

```bash
echo ".env" >> .gitignore
cp .env .env.example   # depois apague os valores do exemplo
```

Valide as variáveis obrigatórias na inicialização do app, falhando cedo se faltar alguma.

## Combina com / alternativas

- [GitHub Actions](07-github-actions.md): secrets do repositório e OIDC.
- [Segurança base](12-seguranca-base.md): menor privilégio e rotação.
- [PaaS](01-paas.md), [Coolify e Dokploy](02-vps-coolify-dokploy.md): variáveis por ambiente no painel (Dokploy integra Vault e Infisical).
- Alternativas: gerenciadores da [nuvem grande](03-nuvem-grande.md); HashiCorp Vault em ambiente com time dedicado.

## Decisão rápida

- **Use se:** o sistema tem qualquer chave, senha ou token (ou seja, sempre).
- **Evite se:** a tentação é colocar um segredo no código ou na imagem "só por enquanto". Isso nunca vale a pena.
