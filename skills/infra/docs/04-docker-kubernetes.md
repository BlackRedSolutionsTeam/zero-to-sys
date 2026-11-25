# Docker e Kubernetes

> Docker empacota o app para rodar igual em qualquer lugar; Kubernetes orquestra muitos contêineres, e na maioria dos projetos ainda não é necessário.

| | |
|---|---|
| **Site** | https://www.docker.com e https://kubernetes.io |
| **Categoria** | Contêineres |
| **Tipo** | Empacotamento (Docker) e orquestração (Kubernetes) |
| **Stack** | Qualquer linguagem; Kubernetes roda em nuvem, VPS ou local |
| **Preço** | Docker Engine e Kubernetes são grátis; Kubernetes gerenciado cobra pelo cluster: EKS US$ 0,10 por hora (suporte padrão); GKE US$ 0,10 por hora, com crédito de US$ 74,40 por mês por conta de cobrança, que cobre um cluster zonal ou Autopilot; AKS camada Free sem taxa do plano de controle e camada Standard a US$ 0,10 por hora (East US). Docker Desktop: Personal US$ 0, Pro US$ 9, Team US$ 15 e Business US$ 24 por usuário/mês no plano anual; uso grátis só em projeto open source não comercial ou em empresa com menos de 250 funcionários e menos de US$ 10 milhões de receita anual (páginas de preços e termos de cada fornecedor, conferido em 2026-11-24) |
| **Licença** | Kubernetes: Apache 2.0 (CNCF). Docker Engine: Apache 2.0 (repositório moby/moby) (arquivos LICENSE no GitHub, conferido em 2026-11-24) |
| **Verificado em** | 2026-11-24 |

## O que é

**Docker** cria uma imagem com o app e suas dependências. A mesma imagem roda no seu notebook, no CI e em produção. O arquivo `Dockerfile` descreve como construí-la.

**Kubernetes** é o orquestrador: decide em quais máquinas rodar contêineres, reinicia os que caem, escala e faz atualização gradual. Na página oficial de releases, a versão estável mais recente na data da verificação era a 1.37 (patch 1.37.2, de 2026-10-13); o projeto mantém as três últimas versões menores. Na mesma página (kubernetes.io/releases e kubernetes.io/releases/patch-releases), a 1.34 aparece entre as versões em fim de vida, com 1.34.13 como último patch e fim de vida em 2026-10-27, data já passada na verificação. A 1.35 tem fim de vida em 2027-02-28.

## Por que usar

- **Mesmo artefato em todo lugar:** acaba o "na minha máquina funciona".
- **Portabilidade:** troca de PaaS, VPS ou nuvem sem reescrever o app.
- **Base de quase tudo:** PaaS, Coolify, Dokploy e nuvens aceitam imagem Docker.
- **Kubernetes:** atualização gradual, auto-recuperação e escala horizontal em sistemas grandes.

## Quando usar

- Docker: quase todo projeto com back-end, a partir do MVP.
- Kubernetes: vários serviços, equipe de plataforma e carga que justifica a operação.
- Compose para ambiente local com banco e dependências.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site estático / blog | ❌ Evite | Não precisa de contêiner |
| MVP / protótipo | ✅ Ótimo | Docker sim, com Dockerfile simples; Kubernetes não |
| SaaS pequeno | ✅ Ótimo | Docker sim; Kubernetes seria custo sem retorno |
| SaaS em crescimento | 🟡 Serve | Prefira contêineres gerenciados da nuvem; Kubernetes só com time para operar |
| Sistema corporativo | ✅ Ótimo | Kubernetes faz sentido com vários times e serviços |
| Time de 1 a 5 devs | ❌ Evite | Kubernetes consome tempo que deveria ir ao produto |
| App monolítico único | ✅ Ótimo | Um contêiner basta |
| Dezenas de microsserviços | ✅ Ótimo | É o caso para o qual Kubernetes foi feito |

## Quando é bom

- **Docker:** imagem pequena, build repetível e padrão de mercado.
- **Kubernetes:** padrão para orquestração, com enorme ecossistema e suporte nos três grandes provedores.
- **Multi-stage build** reduz a imagem final e a superfície de ataque.

## Quando é ruim

- **Kubernetes é pesado:** a curva é alta, e rede, armazenamento, atualização do cluster e segurança viram trabalho contínuo.
- **Custo fixo do cluster:** além dos nós, há controle, balanceador e monitoramento.
- **Imagem inchada e insegura:** base grande, rodar como root e `latest` sem fixar versão trazem risco.
- **Segredo na imagem:** nunca coloque chave em `ENV` ou `COPY` no Dockerfile (veja [segredos](09-segredos-e-configuracao.md)).
- **Dados em contêiner sem volume** somem ao reiniciar; banco em produção é melhor gerenciado.
- **Atualizar sempre o cluster:** cada versão tem cerca de um ano de suporte; ficar parado deixa sem correções.

## Como começar

Dockerfile mínimo com usuário sem privilégio (exemplo genérico; adapte à linguagem):

```dockerfile
FROM node:22-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
USER node
CMD ["node", "server.js"]
```

```bash
docker build -t meu-app .
docker run --rm -p 3000:3000 meu-app
```

Para Kubernetes, só comece pelo serviço gerenciado do seu provedor, nunca instalando o cluster à mão em produção, e só depois de esgotar PaaS e contêineres gerenciados.

## Combina com / alternativas

- [GitHub Actions](07-github-actions.md): build e publicação da imagem.
- [Segurança base](12-seguranca-base.md): varredura de imagem e atualização de dependências.
- [PaaS](01-paas.md), [Coolify e Dokploy](02-vps-coolify-dokploy.md): rodam a imagem sem Kubernetes.
- Alternativas: Docker Compose (um servidor), Docker Swarm (Dokploy usa) ou o serviço de contêineres da nuvem.

## Decisão rápida

- **Use se (Docker):** o projeto tem back-end ou precisa rodar igual em vários ambientes. **Use se (Kubernetes):** há muitos serviços, um time que opere o cluster e necessidade real de escala.
- **Evite se:** o projeto é estático (sem contêiner) ou tem poucos serviços e poucas pessoas (sem Kubernetes).
