# Calendário de fim de suporte

> Versão sem suporte não recebe correção de segurança: saiba a data de cada peça da stack antes que ela vença e planeje a troca com pelo menos 6 meses de folga.

| | |
|---|---|
| **Referência** | Node.js Release Working Group (github.com/nodejs/Release); Microsoft .NET Support Policy (dotnet.microsoft.com/platform/support/policy/dotnet-core); Python Developer's Guide, Status of Python versions (devguide.python.org/versions); PostgreSQL Versioning Policy (postgresql.org/support/versioning); Django (djangoproject.com/download); Laravel (laravel.com/docs, Support Policy); Rails (rubyonrails.org/maintenance); Angular (angular.dev/reference/releases); Next.js (nextjs.org/support-policy); endoflife.date como fonte secundária |
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

- **Decidir pela memória.** As datas mudam: o Next.js 15 teve a janela de segurança estendida até 2027-01-31, e o Django passou a ter outra política a partir de 2028.
- **Esperar o último dia.** Atualização maior leva semanas; comece 6 meses antes.
- **Confiar em tabela de terceiros sem conferir.** Este doc marca o que veio de fonte secundária.
- **Rodar versão "Current"/STS em produção** sem plano de subir logo: o ciclo é curto (24 meses no .NET STS, 6 meses no Node ímpar).

## Como começar

### Runtimes e banco (fonte oficial)

| Peça | Versão | Situação em 2026-11-25 | Fim de suporte |
|---|---|---|---|
| Node.js | 20 | Sem suporte | 2026-04-30 |
| Node.js | 22 | Maintenance LTS | 2027-04-30 |
| Node.js | 24 | Maintenance LTS (desde 2026-10-20) | 2028-04-30 |
| Node.js | 26 | Active LTS (desde 2026-10-28) | 2029-04-30 |
| .NET | 8 (LTS) | Sem suporte | 2026-11-10 |
| .NET | 9 (STS) | Sem suporte | 2026-11-10 |
| .NET | 10 (LTS) | Com suporte | 2028-11-14 |
| .NET | 11 (STS) | Lançado em 2026-11-10 | 2028-11-14 |
| Python | 3.10 | Sem suporte | 2026-10 |
| Python | 3.12 | Só correções de segurança | 2028-10 |
| Python | 3.13 | Só correções de segurança | 2029-10 |
| Python | 3.14 | Com suporte | 2030-10 |
| Python | 3.15 | Lançado em 2026-10-09 | 2031-10 |
| PostgreSQL | 14 | Sem suporte | 2026-11-12 |
| PostgreSQL | 15 | Com suporte | 2027-11-11 |
| PostgreSQL | 16 | Com suporte | 2028-11-09 |
| PostgreSQL | 17 | Com suporte | 2029-11-08 |
| PostgreSQL | 18 | Com suporte | 2030-11-14 |
| PostgreSQL | 19 | Lançado em 2026-11-19 | 2031-11-19 |

Notas:

- **Node:** as fases (Active, Maintenance) e as datas vêm do `schedule.json` do repositório `nodejs/Release`; versões ímpares (25) nunca viram LTS, e o 25 já encerrou em 2026-06-01. Fim das datas das versões de Node pode ser ajustado pelo projeto.
- **Python:** as datas de fim de vida são marcadas como agendadas e podem ser ajustadas. A 3.11 aparece com fim em 2027-10 na tabela da endoflife.date (fonte secundária; a tabela do devguide não a trouxe na conferência).
- **PostgreSQL:** política de 5 anos por versão maior, com uma versão menor final. Rode sempre a menor mais recente da sua maior.
- **.NET:** LTS tem 3 anos, STS tem 24 meses.

### Frameworks

| Framework | Versão | Situação em 2026-11-25 | Fim do suporte de segurança |
|---|---|---|---|
| Django | 4.2 LTS | Sem suporte | 2026-04-07 |
| Django | 5.2 LTS | Só segurança | 2028-04 |
| Django | 6.0 | Com suporte | 2027-04 |
| Django | 6.1 | Com suporte | 2027-12 |
| Laravel | 11 | Sem suporte | 2026-03-12 |
| Laravel | 12 | Só segurança (correções de bugs acabaram em 2026-08-13) | 2027-02-24 |
| Laravel | 13 | Com suporte | 1º trimestre de 2028 |
| Rails | 8.0 | Sem suporte | 2026-11-07 |
| Rails | 8.1 | Com suporte | 2027-10-10 |
| Angular | 20 | LTS, acaba em 3 dias | 2026-11-28 |
| Angular | 21 | LTS | 2027-06 |
| Angular | 22 | Active | 2028-06 |
| Next.js | 14 | Sem suporte | encerrado (a página não dá data) |
| Next.js | 15 | Maintenance LTS | 2027-01-31 |
| Next.js | 16 | Active LTS | até sair a próxima maior |
| Spring Boot (fonte secundária) | 3.5 | Sem suporte | 2026-06-30 |
| Spring Boot (fonte secundária) | 4.0 | Com suporte | 2026-12-31 |
| Spring Boot (fonte secundária) | 4.1 | Com suporte | 2027-07-31 |

Notas:

- **Spring Boot:** a página oficial não trouxe a tabela de suporte na conferência; as datas são da endoflife.date. Confira em spring.io/projects/spring-boot antes de afirmar a um cliente.
- **Laravel 13:** a página oficial dá "Q1 2026 / Q3 2027 / Q1 2028"; a data exata (2028-03-17) vem da endoflife.date.
- **React e Vue:** não têm calendário de fim de suporte por versão maior publicado como tabela; acompanhe o anúncio de cada versão.

### Consultar de novo

```bash
curl -s https://raw.githubusercontent.com/nodejs/Release/main/schedule.json
curl -s https://endoflife.date/api/postgresql.json
curl -s https://endoflife.date/api/dotnet.json
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
