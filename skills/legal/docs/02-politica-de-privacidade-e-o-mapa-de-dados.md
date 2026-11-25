# Política de privacidade ligada ao mapa de dados real

> A política só pode afirmar o que o sistema faz: monte primeiro o inventário dos dados (o que, para quê, base legal, com quem, por quanto tempo) e deixe o texto sair dele.

| | |
|---|---|
| **Referência** | LGPD, arts. 6 (princípios), 7 e 11 (bases legais), 9 (acesso facilitado), 18, 33 e 37 (planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm); Marco Civil, art. 7, VIII e IX, e art. 15 (registros de acesso por 6 meses) (planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm) |
| **Categoria** | Jurídico |
| **Tipo** | Prática de inventário de dados e estrutura de política |
| **Vale para** | Qualquer sistema que trate dado de pessoa no Brasil |
| **Verificado em** | 2026-11-25 |

> Não substitui advogado. A base legal de cada tratamento e o texto final são decisões jurídicas; aqui está a estrutura e o que o sistema fornece.

## O que é

A **política de privacidade** é o documento público em que o controlador informa o que faz com os dados. O art. 9 da LGPD garante ao titular acesso facilitado a: finalidade específica, forma e duração do tratamento, identificação e contato do controlador, com quem os dados são compartilhados e os direitos do titular. O consentimento é nulo se a informação for enganosa, abusiva ou não tiver sido apresentada de forma clara (art. 9, § 1).

O **mapa de dados** (inventário) é a planilha ou o arquivo por trás dela. É também a base do registro das operações que o art. 37 manda manter.

## Por que usar

- **Texto verdadeiro:** cada frase da política aponta uma linha do inventário.
- **Atualização barata:** quando entra um fornecedor ou campo novo, a mudança aparece no inventário e a política é revisada.
- **Resposta rápida** a titular, cliente B2B e ANPD.

## Quando usar

- Antes de escrever ou revisar qualquer política.
- A cada nova integração, campo de formulário ou mudança de finalidade (art. 9, § 2: finalidade nova exige novo aviso).

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | 🟡 Serve | Inventário de 5 a 10 linhas basta |
| MVP de SaaS | ✅ Ótimo | Mais barato levantar agora que depois do primeiro cliente grande |
| SaaS em crescimento | ✅ Ótimo | Cliente B2B pede o inventário em questionário de segurança |
| Sistema interno | ✅ Ótimo | Dado de RH e de clientes exige finalidade clara |
| App mobile | ✅ Ótimo | SDKs de terceiros coletam sem que ninguém lembre |
| Produto sem dado de pessoa natural | ❌ Evite | Sem tratamento, sem inventário |

## Quando é bom

- **Inventário no repositório**, revisado no mesmo PR que muda dados ou integrações.
- **Uma linha por finalidade**, não por tabela.
- **Linguagem direta**, com quem lê em mente, não só o jurídico (art. 9, § 1).

## Quando é ruim

- **Política descrevendo "dados de navegação" de forma vaga** sem listar o que o analytics realmente envia.
- **Base legal copiada da política de outro site:** a base depende da finalidade real.
- **Esquecer o que não está no banco:** logs, backups, e-mails, planilhas e ferramentas de suporte também tratam dado.
- **Prometer "não compartilhamos dados"** quando o provedor de nuvem e o de e-mail são operadores.

## Como começar

**1. Monte o inventário.** Um arquivo `docs/mapa-de-dados.md` ou tabela, uma linha por tratamento.

| Dado | Finalidade | Base legal (jurídico define) | Onde fica | Quem recebe | Prazo | Titular |
|---|---|---|---|---|---|---|
| E-mail e nome | Criar conta e avisar sobre o serviço | Execução de contrato | Banco principal | Provedor de e-mail | Enquanto a conta existir, mais o prazo legal | Usuário |
| Endereço IP e agente do navegador | Segurança e registro de acesso | Obrigação legal / legítimo interesse | Logs | Provedor de logs | 6 meses (Marco Civil, art. 15) | Usuário |
| Eventos de uso | Melhorar o produto | Legítimo interesse ou consentimento | Analytics | Provedor de analytics | 14 meses | Usuário |

As bases possíveis estão nos arts. 7 e 11 da LGPD (consentimento, obrigação legal, execução de contrato, legítimo interesse, tutela da saúde, entre outras); a escolha cabe ao advogado.

**2. Gere a lista do que existe de fato.** Peça ao projeto, não à memória.

```bash
grep -rEn "analytics|gtag|pixel|sentry|intercom|hotjar|stripe|sendgrid|resend|posthog" package.json src app 2>/dev/null
```

```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND column_name ~* '(email|cpf|cnpj|phone|telefone|nome|name|address|endereco|birth|nascimento|ip)'
ORDER BY table_name, column_name;
```

**3. Estrutura da política** (modelo de estrutura, texto vem do advogado):

1. Quem somos: razão social, CNPJ, endereço, contato do encarregado ou do canal do titular.
2. Quais dados coletamos, agrupados por origem (você nos dá, coletamos automaticamente, recebemos de terceiros).
3. Para que usamos cada grupo e em que base legal.
4. Com quem compartilhamos: categorias e, se possível, a lista de suboperadores (doc [07](07-contrato-de-operador-b2b-e-suboperadores.md)).
5. Transferência para fora do Brasil, se houver (LGPD, art. 33; ver doc [07](07-contrato-de-operador-b2b-e-suboperadores.md)).
6. Por quanto tempo guardamos e como apagamos.
7. Como protegemos (em termos gerais, sem detalhes exploráveis).
8. Direitos do titular e como exercê-los (doc [06](06-direitos-do-titular-e-canal-do-encarregado.md)).
9. Cookies (link para a política de cookies, doc [04](04-cookies-aviso-categorias-e-consentimento.md)).
10. Crianças e adolescentes, se o produto puder tê-los como usuários.
11. Mudanças na política e como avisamos.
12. Data e versão.

**4. Registre a versão** no repositório e mostre-a com data (ver [05](05-aceite-versionado.md)).

**5. Mantenha o inventário vivo.** Item no checklist de PR: "adicionou campo, integração ou fornecedor? Atualizou `mapa-de-dados.md`?".

## Combina com / alternativas

- Minimização, criptografia, retenção e anonimização no banco: [../../data/docs/10-dados-pessoais-e-lgpd.md](../../data/docs/10-dados-pessoais-e-lgpd.md).
- Rotas do titular, registro de acesso, incidente e criança: [../../security/docs/09-lgpd-na-pratica.md](../../security/docs/09-lgpd-na-pratica.md).
- Auditoria de quem acessou: [../../data/docs/07-auditoria-historico-soft-delete.md](../../data/docs/07-auditoria-historico-soft-delete.md).
- Alternativa: ferramenta de gestão de privacidade, que ainda precisa de revisão do advogado.

## Decisão rápida

- **Use se:** o produto coleta qualquer dado de pessoa e a política precisa ser verdadeira.
- **Evite se:** a intenção é colar texto genérico; a política vira prova contra a própria empresa.
