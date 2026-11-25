# Construir, comprar ou gerar o painel

> Para um painel que só lista e edita registros, uma ferramenta pronta entrega em dias; para ações de negócio com auditoria e papéis finos, o painel próprio no mesmo código do produto costuma ser mais seguro.

| | |
|---|---|
| **Referência** | retool.com/pricing; github.com/refinedev/refine; github.com/marmelab/react-admin e react-admin-ee.marmelab.com; github.com/filamentphp/filament; djangoproject.com/download; github.com/railsadminteam/rails_admin; github.com/SoftwareBrothers/adminjs; directus.com/pricing e o arquivo `license` do repositório directus/directus; appsmith.com/pricing |
| **Categoria** | Decisão |
| **Tipo** | Comparação de opções |
| **Vale para** | Qualquer sistema que precise de uma área interna para a equipe |
| **Verificado em** | 2026-11-25 |

## O que é

O painel administrativo é a área interna do **sistema que você está criando**, usada pela equipe para gerenciar usuários, empresas, assinaturas, configurações, filas, logs e suporte. Não é a tela de CRUD do usuário final. Esta decisão é o passo 2 do [roteiro](13-roteiro-de-construcao-por-stack.md).

Três caminhos para ter o painel:

- **Construir:** telas próprias no mesmo repositório do produto, com o seu design system e as suas regras de negócio.
- **Gerar a partir do modelo:** um framework de admin lê o modelo de dados e gera listas e formulários (Django Admin, Filament, Rails Admin, AdminJS, Directus).
- **Comprar ou montar com low-code:** ferramenta visual conectada ao banco e às APIs (Retool, Appsmith) ou biblioteca de componentes de admin (Refine, React Admin).

## Por que decidir antes

- O painel mexe em dados de clientes: errar a escolha vira retrabalho de permissão e auditoria depois.
- Ferramenta pronta acelera o CRUD, mas a ação de negócio ("estornar", "reprocessar", "entrar como cliente") quase sempre pede código seu.
- Licença e preço mudam o custo por pessoa da equipe e o que pode ser hospedado.

## Comparação (conferida em 2026-11-25)

| Opção | Tipo | Licença | Preço e limites | Stack |
|---|---|---|---|---|
| Painel próprio | Construir | Sua | Só o tempo de desenvolvimento | A do produto |
| Retool | Low-code | Proprietária | Free: US$ 0, até 5 usuários. Team: construtor US$ 10 (anual) ou US$ 12 (mensal) por mês; usuário interno US$ 5 ou US$ 7. Business: construtor US$ 50 ou US$ 65; usuário interno US$ 15 ou US$ 18. Enterprise sob consulta. Auto-hospedagem só no Enterprise. SSO, SCIM e 2FA só no Enterprise | Qualquer banco ou API |
| Appsmith | Low-code | Edição Community de código aberto; a página de preços não informa o nome da licença (não conferido) | Free: US$ 0, até 5 usuários na nuvem. Business: US$ 15 por usuário por mês, até 99 usuários, com papéis personalizados e logs de auditoria. Enterprise: US$ 2.500 por mês para 100 usuários, com SSO SAML/OIDC | Qualquer banco ou API |
| Refine | Biblioteca React | MIT | Gratuito; a página do repositório não cita edição paga. Última versão encontrada: `@refinedev/core@5.0.12` (2026-04-02) | React |
| React Admin | Biblioteca React | MIT no núcleo | Gratuito. Edição Enterprise: Team 145 euros por mês (até 2 desenvolvedores), Business 290 euros (até 10), Corporate a partir de 590 euros, cobrança anual. Última versão: v5.15.7 (2026-11-13) | React |
| Filament | Gerador | MIT | Gratuito. Versão v5.12.0 (2026-11-21); o README pede Laravel 11 ou superior, PHP 8.2 ou superior e Livewire 3 (confira a matriz da versão 5 na documentação) | Laravel |
| Django Admin | Gerador embutido | BSD (licença do Django; não reconferida nesta data) | Gratuito. Django 6.1.3 é a versão atual; 5.2 LTS segue com suporte até abril de 2028 | Django |
| Rails Admin | Gerador | MIT | Gratuito. O README testa Ruby 2.7 a 3.4; a versão atual e a compatibilidade com Rails não foram conferidas | Rails |
| AdminJS | Gerador | MIT | Gratuito; versão atual não conferida | Node |
| Directus | Camada de dados com painel | `license` do repositório: Monospace Sustainable Core License 1.0 (MSCL-1.0). Permite uso interno e proíbe uso concorrente com a oferta comercial do licenciador; a regra de receita não aparece no texto lido | Core US$ 89 por mês (anual) ou US$ 99 (mensal), 3 usuários; Team US$ 588 ou US$ 698; Enterprise sob consulta. A página tem valores diferentes entre tabela e FAQ para o Team. Auto-hospedagem em todos os planos; concessão gratuita para organizações com receita abaixo de US$ 5 milhões e menos de 50 funcionários | Banco SQL próprio dele |

Valores em dólar e euro, sem impostos e sem conversão para real. Confirme na página antes de propor orçamento.

## Quando usar

- **Painel próprio:** a equipe vai agir sobre dinheiro, acesso ou dados pessoais com regras do produto, e você precisa de auditoria e papéis finos.
- **Gerador do framework (Django Admin, Filament):** o produto já está no framework e o painel é cadastro e consulta para pouca gente.
- **Retool ou Appsmith:** protótipo interno rápido, relatórios e telas que a própria equipe monta, sem tocar no produto.
- **Refine ou React Admin:** você quer telas próprias em React sem escrever tabela, filtro e formulário do zero.
- **Directus:** o banco já existe e a equipe precisa editar conteúdo e dados com papéis sem programar.

## Para que tipo de projeto

| Tipo de projeto | Encaixe | Por quê |
|---|---|---|
| Site de conteúdo | ✅ Ótimo | Directus ou o admin do CMS resolvem |
| MVP de SaaS | ✅ Ótimo | Django Admin, Filament ou Retool Free cobrem o começo |
| SaaS em crescimento | ✅ Ótimo | Painel próprio ou Refine com ações de negócio |
| Sistema interno/corporativo | 🟡 Serve | Low-code serve, mas o custo por usuário cresce |
| API/integração | 🟡 Serve | Painel de chaves e uso é pequeno; gerador basta |
| App mobile com backend | ✅ Ótimo | A equipe usa web; o painel é independente do app |
| Dinheiro e dados sensíveis sem auditoria na ferramenta | ❌ Evite | Sem log de quem fez o quê, não passa em revisão |

## Quando é bom

- **Gerador:** de graça, rápido e já respeita o modelo.
- **Low-code:** montar uma tela de consulta leva horas.
- **Biblioteca React:** liberdade visual sem reescrever a mecânica de lista.
- **Painel próprio:** reaproveita auth, papéis e auditoria do produto.

## Quando é ruim

- **Gerador com permissão por modelo** não cobre "pode estornar até R$ 500".
- **Low-code com recurso essencial só no plano caro:** no Retool, SSO e 2FA são exclusivos do Enterprise (conferido hoje). Calcule o plano que a segurança exige, não o que a vitrine mostra.
- **Ferramenta conectada direto ao banco de produção** passa por cima das regras do produto. Prefira ligar a uma API interna ou a um usuário de banco só de leitura.
- **Licença não livre:** leia o texto antes de hospedar para terceiros (caso do Directus).

## Como começar

Exemplo mínimo com Filament, um recurso de clientes (PHP):

```php
php artisan make:filament-resource Cliente --generate
```

Exemplo com React Admin:

```tsx
import { Admin, Resource, ListGuesser } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";

export const App = () => (
  <Admin dataProvider={simpleRestProvider("/api/interna")}>
    <Resource name="clientes" list={ListGuesser} />
  </Admin>
);
```

Em qualquer escolha, a API interna que o painel chama exige papel e grava auditoria ([doc 03](03-quem-acessa-papeis-e-menor-privilegio.md) e [doc 06](06-auditoria-do-que-a-equipe-faz.md)).

## Combina com / alternativas

- Layout das telas: [design-systems, doc 03](../../design-systems/docs/03-admin-crud.md).
- Stack do produto: skill `stacks`.
- Pastas do painel dentro do projeto: skill `architecture`.

## Decisão rápida

- **Use gerador** se o framework já tem um e o painel é cadastro para poucas pessoas.
- **Use Retool ou Appsmith** para consulta e relatório rápidos, aceitando o custo por pessoa e a segurança limitada nos planos baixos.
- **Use painel próprio** (com Refine ou React Admin se quiser acelerar) quando houver dinheiro, dado pessoal ou ação de risco.
- **Evite** ligar ferramenta visual direto no banco de produção com usuário de escrita.
