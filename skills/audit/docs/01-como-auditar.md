# Como auditar um projeto existente

> Descubra a stack e o estado do projeto lendo o que já existe, confronte cada área com o checklist da skill dela, anote a evidência de cada resposta e marque "não verificado" no que não deu para provar.

| | |
|---|---|
| **Referência** | OWASP Application Security Verification Standard, ASVS 5.0.0 (owasp.org/www-project-application-security-verification-standard); Google Engineering Practices, "How to do a code review" (google.github.io/eng-practices); DORA, "Software delivery performance metrics" (dora.dev/guides/dora-metrics); documentação oficial do Git, npm e GitHub CLI |
| **Categoria** | Auditoria |
| **Tipo** | Prática de diagnóstico somente leitura |
| **Vale para** | Qualquer projeto com código em repositório Git, em qualquer stack |
| **Verificado em** | 2026-11-24 |

## O que é

Auditar é responder, com prova, "como este projeto está hoje" em cada área: estrutura, código, dados, API, testes, segurança, infraestrutura, experiência de uso. O agente faz isso sozinho, sem perguntar ao usuário o que dá para descobrir lendo o repositório.

O padrão de medida é o checklist de cada skill do plugin. A auditoria só diagnostica. Quem corrige é a skill da área, depois, em PRs separados.

Exemplo usado nos três documentos: um sistema de agendamento de clínica (pacientes, profissionais, agendamentos).

## Por que usar

- **Ponto de partida honesto:** sem diagnóstico, a correção vira palpite.
- **Evidência:** "tem teste" sem arquivo e linha é opinião. Com evidência, qualquer pessoa confere.
- **Sem estrago:** como a auditoria só lê, pode rodar em projeto de produção.

## Quando usar

- Ao assumir um projeto que você não conhece.
- Antes de reorganizar, trocar de hospedagem ou abrir o projeto para mais gente.
- Antes de uma entrega grande ou de uma auditoria externa.
- Periodicamente (a cada trimestre, por exemplo) para ver se o projeto melhorou ou piorou.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Poucas áreas se aplicam (dados e API podem nem existir); marque "não se aplica" |
| MVP de SaaS | ✅ Ótimo | Dívida invisível (segurança, backup) aparece cedo e custa pouco |
| SaaS em crescimento | ✅ Ótimo | Muitas áreas, muita gente mexendo; o diagnóstico alinha o time |
| Sistema interno/corporativo | ✅ Ótimo | Costuma ter pouca documentação e dono trocado |
| API/integração | ✅ Ótimo | Contrato, erros e idempotência são fáceis de checar |
| App mobile com backend | ✅ Ótimo | Vale para o backend e a experiência; versões antigas do app pedem atenção a versionamento |
| Projeto sem repositório Git nem acesso ao código | ❌ Evite | Sem código para ler, só dá para listar perguntas; a auditoria vira entrevista |

## Quando é bom

- **Lê antes de perguntar.** Manifesto, configuração e histórico respondem quase tudo.
- **Uma pergunta por área, com uma resposta objetiva** (ok, atenção, falta, não verificado).
- **Toda resposta com evidência:** `arquivo:linha` ou a saída resumida de um comando.
- **Áreas independentes em paralelo,** cada uma com seu agente.

## Quando é ruim

- **Corrigir no meio da auditoria.** Mistura diagnóstico e mudança, e o relatório deixa de refletir o estado inicial.
- **Responder "ok" por suposição.** Se o projeto tem pasta `tests/`, isso não prova que os testes passam.
- **Rodar o que escreve:** migration, deploy, seed, script de limpeza.
- **Auditar sem saber a stack.** Os checklists mudam com ela.

## Como começar

### Passo 1: descobrir a stack e o estado

Comandos de leitura, nesta ordem:

```bash
git status --short
git log --oneline -20
git log --since="90 days ago" --format="%an" | sort | uniq -c | sort -rn
git ls-files | head -200
ls -a
```

Depois leia o que existir: `package.json`, `*.csproj`, `pyproject.toml`, `go.mod`, `composer.json`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, `.env.example`, `README`, `CLAUDE.md`, `AGENTS.md`, `ARCHITECTURE.md`, `BACKLOG.md`.

Resuma em cinco linhas antes de seguir: linguagem e framework, banco, onde roda, quem mexeu nos últimos 90 dias, o que o README promete.

### Passo 2: pegar o checklist de cada área

Abra o `SKILL.md` de cada skill e procure a seção "Checklist". Cada item vira uma pergunta da auditoria.

| Área | Skill | Onde ler |
|---|---|---|
| Produto | `product` | [SKILL.md](../../product/SKILL.md) |
| Estrutura de pastas | `architecture` | [SKILL.md](../../architecture/SKILL.md) |
| Código | `coding` | [SKILL.md](../../coding/SKILL.md) |
| Banco | `data` | [SKILL.md](../../data/SKILL.md) |
| API | `api` | [SKILL.md](../../api/SKILL.md) |
| Testes | `quality` | [SKILL.md](../../quality/SKILL.md) |
| Segurança | `security` | [SKILL.md](../../security/SKILL.md) |
| Telas e dispositivos | `user-experience` | [SKILL.md](../../user-experience/SKILL.md) |
| Produção | `infra` | [SKILL.md](../../infra/SKILL.md) |
| Agente de IA | `ia` | [SKILL.md](../../ia/SKILL.md) |

Se uma skill não tiver a seção "Checklist" (a `quality` usa a definição de pronto, no doc 08), use no lugar dela as "Regras de uso" do `SKILL.md` e a linha "Evite se" de cada doc da skill. Anote no relatório que o checklist formal não existe para aquela área.

### Passo 3: coletar evidência

Cada pergunta recebe uma destas respostas, sempre com evidência:

| Resposta | Quando | Evidência |
|---|---|---|
| ok | Foi visto e atende | `src/appointments/route.ts:14` ou saída do comando |
| atenção | Existe, mas incompleto ou fraco | O que existe e o que falta |
| falta | Não existe | O comando que procurou e não achou (`rg -n "tenant_id" prisma/`, sem resultado) |
| não verificado | Não deu para provar | O motivo (sem acesso, exige rodar algo que escreve) |

Procure por padrão, não por pasta. Exemplo para a pergunta "toda consulta filtra por clínica?":

```bash
rg -n "findMany|findFirst|select .* from" src --glob "!*.test.*"
rg -n "clinicId|clinic_id" src | head -40
```

Se uma rota do exemplo (`GET /appointments`) lista agendamentos sem filtrar por clínica, isso é achado, com o `arquivo:linha`.

### Passo 4: comandos seguros (somente leitura)

| Pode | Não pode |
|---|---|
| `git log`, `git diff`, `git ls-files`, `git blame` | `git commit`, `git push`, `git reset`, `git clean` |
| `rg`, `cat`, `sed -n`, `ls`, `wc -l` | Qualquer escrita em arquivo do projeto (`sed -i`, `>`, formatadores) |
| `npm audit`, `npm outdated`, `dotnet list package --vulnerable` | `npm audit fix`, `npm install`, `npm update` |
| Linter e checagem de tipos sem correção (`eslint .`, `tsc --noEmit`) | `eslint --fix`, `prettier --write` |
| `gh run list`, `gh pr list` (consulta ao GitHub) | `gh pr merge`, `gh workflow run` |
| Testes só se usarem banco local ou descartável | Migration, seed, deploy, qualquer comando contra produção |

Regra de bolso: se o comando muda arquivo, banco ou servidor, não rode. Se não souber, trate como proibido.

### Passo 5: o que fazer quando não dá para verificar

- Escreva **não verificado** e o motivo. Nunca "ok".
- Diga o que seria preciso para verificar (acesso ao painel da hospedagem, uma cópia do banco, uma variável de ambiente).
- Itens "não verificado" entram no relatório com o mesmo destaque dos demais. Muitos deles já são um achado: o projeto não deixa ninguém provar.

### Passo 6: índice de código e agentes em paralelo

- Em base grande ou desconhecida, ligue um índice antes de começar: veja [code-indexes](../../code-indexes/SKILL.md). Com ele, "onde é feita a checagem de permissão?" vira uma consulta, não 30 leituras.
- Em base pequena, `rg` basta.
- Quando houver ferramenta de subagentes, dispare um agente por área (dados, API, testes, segurança, infra), cada um com o checklist da skill, o resumo do Passo 1 e a regra "só leitura, evidência em toda resposta". Peça de volta uma tabela no formato do [próximo documento](02-relatorio-e-status.md).
- Quem junta é você: confira os "ok" por amostragem (abra 2 evidências por área) antes de entregar.

## Combina com / alternativas

- [02-relatorio-e-status.md](02-relatorio-e-status.md): o formato em que as respostas são entregues.
- [03-priorizacao-e-plano.md](03-priorizacao-e-plano.md): o que fazer com os achados.
- Skill `zero-to-sys`, seção "Projeto existente": a ordem de skills para um projeto que já tem código.
- Skill `code-indexes`: índice de código para bases grandes.
- Skill `quality`, [doc 09](../../quality/docs/09-verificacao-pelo-agente.md): como provar com comando e saída, a mesma disciplina de evidência.
- Alternativa: o OWASP ASVS como checklist de segurança mais profundo, quando a área de segurança pede nível de verificação formal.
- Alternativa: o DORA Quick Check (dora.dev) para medir o processo de entrega, não o código.

## Decisão rápida

- **Use se:** existe código para ler e você precisa saber o estado antes de mudar algo.
- **Evite se:** o pedido é só uma feature pequena e isolada; use a skill da área direto.
