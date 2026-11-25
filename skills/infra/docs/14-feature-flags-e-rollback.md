# Feature flags e rollback (PostHog, Unleash, GrowthBook, Flagsmith e OpenFeature)

> Publicar o código sem ligar a funcionalidade, liberar aos poucos e ter um jeito rápido de voltar atrás quando algo der errado.

| | |
|---|---|
| **Site** | https://openfeature.dev, https://posthog.com, https://www.getunleash.io, https://www.growthbook.io, https://www.flagsmith.com |
| **Categoria** | Operação |
| **Tipo** | Prática de liberação (flag simples) e serviços de feature flag; OpenFeature é uma especificação |
| **Stack** | Flag simples vale para qualquer stack; os serviços têm SDKs para as linguagens mais comuns; OpenFeature tem SDKs por linguagem |
| **Preço** | PostHog: 1 milhão de requisições de flag grátis por mês, depois cobrança por requisição (posthog.com/feature-flags/pricing, conferido em 2026-11-24). Flagsmith: plano grátis de até 50 mil requisições por mês (flagsmith.com/pricing, conferido em 2026-11-24). Unleash: versão aberta autohospedada grátis (1 projeto, 2 ambientes), plano pago a US$ 75 por usuário por mês (getunleash.io/pricing, conferido em 2026-11-24). GrowthBook: plano Starter grátis e autohospedagem grátis; Pro a US$ 40 por usuário por mês (growthbook.io/pricing, conferido em 2026-11-24); o limite de usuários do Starter não foi conferido |
| **Licença** | OpenFeature: projeto da CNCF, em incubação. Unleash: AGPL-3.0 (LICENSE do repositório). GrowthBook: núcleo MIT, com pastas Enterprise sob licença própria. Flagsmith: maior parte BSD-3-Clause. PostHog: MIT, exceto a pasta `ee/` (conferido em 2026-11-24 no GitHub e em buscas) |
| **Verificado em** | 2026-11-24 |

## O que é

**Feature flag** (chave de funcionalidade) é um `if` que decide, em tempo de execução, se um trecho do sistema está ligado. O código entra em produção desligado e você liga depois, sem novo deploy. Isso separa duas coisas: **deploy** (o código chegou ao servidor) e **release** (a pessoa passou a ver a funcionalidade).

**Rollback** é voltar a um estado anterior que funcionava. Com flag, o rollback de uma funcionalidade é desligar a chave, em segundos.

**OpenFeature** é uma API padrão e neutra para avaliar flags. Seu código chama a API, e você troca o serviço por trás sem reescrever.

## Por que usar

- **Risco menor:** funcionalidade nova com defeito é desligada sem novo deploy.
- **Liberação gradual:** 5% dos usuários, depois 50%, depois todos.
- **Sem branch longa:** o código incompleto vai para a `main` escondido atrás da flag.
- **Testar em produção com segurança:** só a equipe interna vê a funcionalidade.

## Quando usar

- Funcionalidade grande ou arriscada (novo fluxo de agendamento).
- Quando a clínica piloto precisa ver a novidade antes das outras.
- Para um botão de emergência que desliga algo caro ou instável (kill switch).
- Para testar duas versões de uma tela.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ❌ Evite | Publicar e voltar o deploy basta |
| MVP de SaaS | 🟡 Serve | Variável de ambiente ou tabela simples resolve; serviço é exagero |
| SaaS em crescimento | ✅ Ótimo | Liberação por empresa e por percentual, com histórico de quem mudou |
| Sistema interno/corporativo | ✅ Ótimo | Liberar por setor ou perfil antes de abrir para todos |
| API/integração | ✅ Ótimo | Versão nova de um comportamento só para alguns clientes |
| App mobile | ✅ Ótimo | Não dá para voltar a versão da loja rápido; a flag desliga sem nova versão |
| Time sem rotina de limpeza | ❌ Evite | Flag esquecida vira dívida e código morto |

## Quando é bom

- **Reversão rápida,** sem pipeline e sem pedir aprovação de novo deploy.
- **Por empresa:** a clínica A usa o novo fluxo, a B continua no antigo.
- **Integração contínua de verdade:** todos commitam na `main` todo dia.
- **Medição:** com [analytics](13-analytics-de-produto.md), você compara o grupo com e sem a flag.

## Quando é ruim

- **Dívida:** cada flag dobra os caminhos de código a testar. Flag velha deve ser removida.
- **Combinações:** muitas flags ligadas ao mesmo tempo geram estados que ninguém testou.
- **Flag em serviço externo** vira dependência: se ele cair, defina o valor padrão (de preferência, desligado).
- **Banco de dados não volta com a flag.** Veja a seção abaixo.
- **Custo por requisição** nos serviços pagos; o SDK que consulta a cada poucos segundos pode consumir o plano grátis.

## Como começar

**Tipos de flag**

| Tipo | Para que serve | Vida |
|---|---|---|
| Release | Esconder funcionalidade pronta ou em construção | Dias a semanas; remova ao liberar para todos |
| Experimento | Comparar duas versões e medir | Até ter resultado |
| Permissão | Funcionalidade por plano ou perfil (veja [papéis e permissões](../../security/docs/04-papeis-e-permissoes.md)) | Longa; é regra de negócio, não flag temporária |
| Kill switch | Desligar algo em emergência | Longa |

**Passo 1: flag simples.** Variável de ambiente para o liga/desliga geral:

```ts
export const novoFluxoAgendamento = process.env.FLAG_NOVO_FLUXO_AGENDAMENTO === "true";
```

**Passo 2: tabela no banco** quando precisar ligar por empresa, sem deploy:

```sql
CREATE TABLE feature_flags (
  chave text NOT NULL,
  empresa_id uuid,
  ligada boolean NOT NULL DEFAULT false,
  percentual integer NOT NULL DEFAULT 100 CHECK (percentual BETWEEN 0 AND 100),
  criada_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (chave, empresa_id)
);
```

```ts
export async function flagLigada(chave: string, empresaId: string): Promise<boolean> {
  const linha = await db.featureFlag.findUnique({
    where: { chave_empresaId: { chave, empresaId } },
  });
  return linha?.ligada ?? false;
}
```

Para percentual, calcule um número estável a partir do id da empresa (um hash dividido por 100) e compare com o percentual. A mesma empresa sempre cai no mesmo lado.

**Passo 3: serviço** quando precisar de painel, histórico, percentual e experimento: PostHog (junto do analytics), Unleash ou Flagsmith (autohospedáveis), GrowthBook (focado em experimentos). Chame as flags pelo OpenFeature se quiser poder trocar de serviço.

**Remover flag velha:** ao liberar para 100%, abra uma tarefa no mesmo dia para apagar o `if`, o caminho antigo e a linha da flag. Dê um nome e um responsável a cada flag, e revise a lista a cada mês.

**Rollback de deploy**

| Onde roda | Como voltar |
|---|---|
| [PaaS](01-paas.md) | Promover no painel a versão anterior (cada deploy fica guardado) |
| Contêiner ([Docker](04-docker-kubernetes.md)) | Publicar de novo a tag anterior da imagem; por isso nunca use só `latest` |
| [GitHub Actions](07-github-actions.md) | Pipeline com opção de implantar uma tag ou commit escolhido |

**Banco de dados e rollback.** Voltar o código é fácil; voltar uma migration que apagou coluna, não. Use **expand and contract** ([migrations](../../data/docs/04-migrations.md)): primeiro adicione (expand), com o código aceitando antigo e novo; migre os dados; só depois remova o antigo (contract), em outro deploy. Assim o código anterior ainda funciona com o banco novo, e o rollback é seguro. Faça backup antes ([backup](11-backup-e-recuperacao.md)).

**Flag ou branch longa?** Flag. Branch com semanas sem integrar gera conflito e entrega arriscada. Commite na `main` pequeno e escondido na flag.

## Combina com / alternativas

- [Analytics de produto](13-analytics-de-produto.md): meça o efeito de cada liberação.
- [Observabilidade](10-observabilidade.md): acompanhe erros após ligar a flag e marque a versão.
- [Migrations](../../data/docs/04-migrations.md): expand and contract.
- [Segredos e configuração](09-segredos-e-configuracao.md): flag por variável de ambiente é configuração.
- Alternativas: sem flag, com deploy pequeno e frequente, e rollback do PaaS.

## Decisão rápida

- **Use se:** a funcionalidade é grande, arriscada ou precisa ir para poucos clientes antes. Comece com variável de ambiente ou tabela, e só adote serviço quando precisar de percentual, painel ou experimento.
- **Evite se:** a mudança é pequena e o rollback do deploy basta, ou se o time não vai remover as flags velhas.
