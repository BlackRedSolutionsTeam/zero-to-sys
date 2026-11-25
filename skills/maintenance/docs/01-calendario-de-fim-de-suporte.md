# Calendário de fim de suporte

> Versão sem suporte não recebe correção de segurança: saiba a data de cada peça da stack antes que ela vença e planeje a troca com pelo menos 6 meses de folga.

| | |
|---|---|
| **Referência** | Node.js Release Working Group (github.com/nodejs/Release); Microsoft .NET Support Policy (dotnet.microsoft.com/platform/support/policy/dotnet-core); Python Developer's Guide, Status of Python versions (devguide.python.org/versions); PostgreSQL Versioning Policy (postgresql.org/support/versioning); Django (djangoproject.com/download); Laravel (laravel.com/docs/13.x/releases, Support Policy); Rails (rubyonrails.org/maintenance); Angular (angular.dev/reference/releases); Next.js (nextjs.org/support-policy); Spring Boot (api.spring.io/projects/spring-boot/generations) |
| **Categoria** | Manutenção |
| **Tipo** | Tabela de consulta e prática de planejamento |
| **Vale para** | Node, .NET, Python, PostgreSQL, Django, Laravel, Rails, Angular, Next.js e Spring Boot |
| **Verificado em** | 2026-11-25 |

## O que é

Todo runtime, framework e banco tem uma data a partir da qual o projeto deixa de receber correções, inclusive de segurança. Depois dela, uma falha nova fica aberta para sempre. Este doc reúne as datas, com a situação **em 2026-11-25**, e diz como consultar de novo, porque elas mudam.

## Por que usar

- **Segurança:** versão sem suporte é alvo fácil (OWASP A06, veja a skill `security`, doc 08).
- **Orçamento:** saltar uma versão maior por ano custa menos que saltar três de uma vez.
- **Conformidade:** auditoria e cliente grande perguntam a versão e a data de suporte.

## Quando usar

- Ao assumir um projeto, para saber o que já venceu.
- Na rotina trimestral ([doc 07](07-rotina-trimestral-de-saude.md)).
- Antes de começar um projeto novo, para escolher a versão com mais tempo de vida.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas peças; a imagem do build e o runtime são o que vence |
| MVP de SaaS | ✅ Ótimo | Escolher a versão certa no início evita migração cedo |
| SaaS em crescimento | ✅ Ótimo | Vários serviços, cada um com sua data |
| Sistema interno/corporativo | ✅ Ótimo | Costuma ficar parado anos e vencer sem ninguém ver |
| API/integração | ✅ Ótimo | Exposta à internet; falha no runtime é falha da API |
| App mobile com backend | ✅ Ótimo | O backend vence mesmo que o app esteja estável |
| Projeto com suporte estendido pago contratado | 🟡 Serve | Dá mais prazo, mas a conta sobe a cada ano |

## Quando é bom

- **Consultar a fonte oficial** na hora, e anotar a data da conferência.
- **Usar versão LTS** (suporte longo) em produção.
- **Fixar a versão** em arquivo, para que a data seja de uma versão conhecida.

## Quando é ruim

- **Decidir pela memória.** As datas mudam: o Next.js 15 teve a janela de segurança estendida até 2027-01-31.
- **Esperar o último dia.** Atualização maior leva semanas; comece 6 meses antes.
- **Confiar em tabela de terceiros sem conferir.** Este doc usa só fonte oficial; se citar outra, diz por quê.
- **Rodar versão "Current"/STS em produção** sem plano de subir logo: o ciclo é curto (24 meses no .NET STS, 6 meses no Node ímpar).

## Como começar

### Como ler as tabelas

- 🔴 **Fora de suporte:** a data já passou em 2026-11-25. Entra na migração agora.
- 🟠 **Vence em até 90 dias:** a data cai até 2027-02-23. Entra no planejamento deste trimestre, com a migração já em andamento.
- Sem marca: mais de 90 dias de prazo. Se faltar menos de 6 meses, entra no próximo trimestre (regra do fim do doc).

### Runtimes e banco

| | Peça | Versão | Situação em 2026-11-25 | Fim de suporte | Fonte |
|---|---|---|---|---|---|
| 🔴 | Node.js | 20 | Fora de suporte | 2026-04-30 | nodejs/Release, `schedule.json` |
| | Node.js | 22 | Maintenance LTS | 2027-04-30 | nodejs/Release |
| | Node.js | 24 | Maintenance LTS (desde 2026-10-20) | 2028-04-30 | nodejs/Release |
| | Node.js | 26 | Active LTS (desde 2026-10-28) | 2029-04-30 | nodejs/Release |
| 🔴 | .NET | 8 (LTS) | Fora de suporte | 2026-11-10 | Microsoft .NET Support Policy |
| 🔴 | .NET | 9 (STS) | Fora de suporte | 2026-11-10 | Microsoft .NET Support Policy |
| | .NET | 10 (LTS) | Com suporte | 2028-11-14 | Microsoft .NET Support Policy |
| | .NET | 11 (STS) | Lançado em 2026-11-10 | 2028-11-14 | Microsoft .NET Support Policy |
| 🔴 | Python | 3.10 | Fora de suporte | 2026-10-01 | Python Developer's Guide |
| | Python | 3.11 | Só correções de segurança | 2027-10 (agendada) | Python Developer's Guide |
| | Python | 3.12 | Só correções de segurança | 2028-10 (agendada) | Python Developer's Guide |
| | Python | 3.13 | Só correções de segurança | 2029-10 (agendada) | Python Developer's Guide |
| | Python | 3.14 | Correções de bugs e segurança | 2030-10 (agendada) | Python Developer's Guide |
| | Python | 3.15 | Lançado em 2026-10-09 | 2031-10 (agendada) | Python Developer's Guide |
| 🔴 | PostgreSQL | 14 | Fora de suporte | 2026-11-12 | PostgreSQL Versioning Policy |
| | PostgreSQL | 15 | Com suporte | 2027-11-11 | PostgreSQL Versioning Policy |
| | PostgreSQL | 16 | Com suporte | 2028-11-09 | PostgreSQL Versioning Policy |
| | PostgreSQL | 17 | Com suporte | 2029-11-08 | PostgreSQL Versioning Policy |
| | PostgreSQL | 18 | Com suporte | 2030-11-14 | PostgreSQL Versioning Policy |
| | PostgreSQL | 19 | Lançado em 2026-11-19 | 2031-11-19 | PostgreSQL Versioning Policy |

Notas:

- **Node:** as fases (Active, Maintenance) e as datas vêm do `schedule.json` do repositório `nodejs/Release`; versões ímpares (25) nunca viram LTS, e o 25 já encerrou em 2026-06-01.
- **Python:** as datas com "(agendada)" podem ser ajustadas pelos responsáveis de release, segundo o próprio devguide. A 3.10 tem data exata (2026-10-01) porque já encerrou.
- **PostgreSQL:** política de 5 anos por versão maior, com uma versão menor final. Rode sempre a menor mais recente da sua maior.
- **.NET:** a página da Microsoft dá 2028-11-14 tanto para o .NET 10 (LTS) quanto para o .NET 11 (STS).

### Frameworks

| | Framework | Versão | Situação em 2026-11-25 | Fim do suporte de segurança | Fonte |
|---|---|---|---|---|---|
| 🔴 | Django | 4.2 LTS | Fora de suporte | 2026-04-07 | djangoproject.com/download |
| | Django | 5.2 LTS | Só segurança (suporte principal acabou em 2025-12-03) | 2028-04 | djangoproject.com/download |
| | Django | 6.0 | Só segurança (suporte principal acabou em 2026-08-04) | 2027-04 | djangoproject.com/download |
| | Django | 6.1 | Com suporte | 2027-12 | djangoproject.com/download |
| 🔴 | Laravel | 11 | Fora de suporte | 2026-03-12 | Laravel 13.x, Release Notes |
| 🟠 | Laravel | 12 | Só segurança (correções de bugs acabaram em 2026-08-13); vence em 91 dias, um além da faixa | 2027-02-24 | Laravel 13.x, Release Notes |
| | Laravel | 13 | Com suporte (lançado em 2026-03-17) | 2028-03-17 | Laravel 13.x, Release Notes |
| 🔴 | Rails | 8.0 | Fora de suporte | 2026-11-07 | rubyonrails.org/maintenance |
| | Rails | 8.1 | Só segurança (correções de bugs acabaram em 2026-10-10) | 2027-10-10 | rubyonrails.org/maintenance |
| 🟠 | Angular | 20 | LTS, vence em 3 dias | 2026-11-28 | angular.dev/reference/releases |
| | Angular | 21 | LTS | 2027-06 | angular.dev/reference/releases |
| | Angular | 22 | Active | 2028-06 | angular.dev/reference/releases |
| 🔴 | Next.js | 14 | Fora de suporte (a página não dá data) | não informada | nextjs.org/support-policy |
| 🟠 | Next.js | 15 | Maintenance LTS (janela original até 2026-10-21, estendida) | 2027-01-31 | nextjs.org/support-policy |
| | Next.js | 16 | Active LTS | até sair a próxima maior | nextjs.org/support-policy |
| 🔴 | Spring Boot | 3.5 | Fora de suporte aberto (suporte comercial segue) | 2026-06-30 (aberto) | api.spring.io, `ossSupportEndDate` |
| 🟠 | Spring Boot | 4.0 | Com suporte; vence em 36 dias | 2026-12-31 (aberto) | api.spring.io, `ossSupportEndDate` |
| | Spring Boot | 4.1 | Com suporte | 2027-07-31 (aberto) | api.spring.io, `ossSupportEndDate` |
| | Spring Boot | 4.2 | Com suporte (a página do projeto já mostra 4.2.0) | 2027-12-31 (aberto) | api.spring.io, `ossSupportEndDate` |

Notas:

- **Spring Boot:** a página spring.io/projects/spring-boot não traz a tabela no texto, mas a API pública `https://api.spring.io/projects/spring-boot/generations` (a mesma que alimenta o site) traz `ossSupportEndDate` e `commercialSupportEndDate`. As datas acima são do suporte aberto (OSS). O suporte comercial vai mais longe (3.5 até 2032-06-30; 4.0 até 2027-12-31).
- **Laravel:** a página `laravel.com/docs/13.x/releases` dá a data exata: 13 lançado em 2026-03-17, correções de bugs até Q3 2027 e segurança até 2028-03-17. A página `master` ainda mostra "Q1 2026 / Q3 2027 / Q1 2028"; use a `13.x`.
- **Angular:** o Angular 20 é o único com dia exato; 21 e 22 só têm o mês.
- **Next.js:** a 14 aparece na lista de não suportadas, sem data de encerramento. A Maintenance LTS dura dois anos do lançamento, e a 15 teve a janela estendida até 2027-01-31.
- **React e Vue:** não têm calendário de fim de suporte por versão maior publicado como tabela; acompanhe o anúncio de cada versão.
- **Conferência:** todas as datas acima foram lidas na página ou no arquivo oficial da peça em 2026-11-25.

### Revisão do calendário

- **Última revisão:** 2026-11-25.
- **Próxima revisão:** 2027-02-25 (a cada trimestre, na rotina do [doc 07](07-rotina-trimestral-de-saude.md)). Antes dela, reconfira qualquer linha que passe a cair na faixa de 90 dias.
- **Regra:** a cada revisão, reabra a página oficial de cada peça, atualize "Situação" e as marcas 🔴 e 🟠, e troque a data de "Verificado em". Linha sem fonte oficial deve dizer por quê.

### Consultar de novo

```bash
curl -s https://raw.githubusercontent.com/nodejs/Release/main/schedule.json
curl -s https://api.spring.io/projects/spring-boot/generations
```

Para listar as versões em uso no repositório:

```bash
node -v
dotnet --list-sdks
python3 --version
grep -rE "^FROM " Dockerfile*
grep -E "image:" docker-compose*.yml
```

### Como registrar no projeto

Uma tabela no `README` ou em `docs/manutencao.md`:

| Peça | Versão em uso | Fim de suporte | Conferido em | Ação |
|---|---|---|---|---|
| Node.js | 22 | 2027-04-30 | 2026-11-25 | Subir para 24 até 2027-01 |

Regra prática: **menos de 6 meses para o fim = entra no próximo trimestre; já vencida = entra agora.**

## Combina com / alternativas

- [Atualização automática de dependências](02-atualizacao-automatica-de-dependencias.md): mantém as bibliotecas em dia.
- [Versão maior de framework](03-atualizar-versao-maior-do-framework.md) e [Postgres sem queda](04-atualizar-o-postgres-sem-queda.md): como executar a troca.
- Skill `stacks`: escolhe a versão certa ao começar o projeto.
- Alternativa: suporte comercial estendido de terceiros, quando a troca é inviável por um tempo; custa e não substitui o plano.

## Decisão rápida

- **Use se:** o projeto está em produção por mais de alguns meses.
- **Evite se:** a decisão for só pela memória; consulte a fonte.
