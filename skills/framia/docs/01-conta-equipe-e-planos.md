# Conta, equipe e planos

> Criar a conta no Framia, escolher a equipe dona do projeto e conferir se o plano comporta o sistema.

| | |
|---|---|
| **Documentação oficial** | https://framia.com.br/pt-br/docs/first-project, https://framia.com.br/pt-br/docs/teams e https://framia.com.br/pt-br/docs/plans |
| **Categoria** | Acesso |
| **Quem faz** | A pessoa, no navegador ou no app desktop. O agente não cria conta |
| **Verificado em** | 2026-11-26 |

## Criar a conta

1. Abra https://framia.com.br/signup.
2. Preencha nome, e-mail e senha, ou entre com Google, Apple ou GitHub.
3. Se o Framia pedir a verificação de pessoa, marque a caixa acima de **Criar conta**.
4. O app abre no **Início** (https://app.framia.com.br/home). A confirmação do e-mail não bloqueia o uso; enquanto não é feita, o Início mostra **Confirme seu e-mail**, com **Enviar de novo**.

Cada conta nasce com uma equipe pessoal, na seção **Equipes** do menu da esquerda. Web e app desktop são o mesmo app; o desktop acrescenta **IA neste computador**, o login do `gh` ou do `az` em **Repositórios** e **Salvar como** ao exportar.

## Equipe e papéis

O projeto pertence a uma equipe. Nas ferramentas do MCP, equipe se chama workspace (`list_workspaces`, `create_workspace`).

- **Criar equipe:** **Equipes** → **Nova equipe** → **Nome da equipe** → **Criar equipe**. Criar equipe é grátis; quem cria é o administrador.
- **Convidar:** aba **Pessoas** → **Convidar pessoas** → e-mail e papel → **Enviar convite** → **Copiar link**. O Framia não manda e-mail: você envia o link, que vale 7 dias.
- **Convidar só a um projeto:** **Pessoas e convites** no menu **…** do projeto, ou **Convidar** no editor.

| Papel | Pode |
|---|---|
| Administrador | Tudo; define e paga o plano; um por equipe |
| Gestor | Trocar papéis de editores e leitores, remover pessoas |
| Editor | Editar, criar projetos e branches, convidar |
| Leitor | Só abrir |

O cliente que só vai aprovar entra como **Leitor**, ou nem entra: recebe um link de compartilhamento ([doc 10](10-aprovacao-e-passagem-para-o-codigo.md)).

## Planos e limites

| | Starter | Pro | Ultra |
|---|---|---|---|
| Preço | Grátis | R$ 49,90 por mês ou R$ 499 por ano | R$ 129,90 por mês ou R$ 1.299 por ano |
| Projetos, no total | 1 | 3 | 10 |
| Armazenamento | 1 GB | 10 GB | 100 GB |
| Páginas por projeto | 10 | 100 | 1.000 |
| Componentes por projeto | 10 | 100 | Sem limite |
| Tabelas no banco por projeto | 10 | 100 | Sem limite |

- O plano é da pessoa, não da equipe. Cada equipe segue o plano do administrador. Convidar pessoas e agentes é grátis.
- Projetos e armazenamento somam todas as equipes de que a pessoa é responsável; ter mais equipes não multiplica o limite. Projeto na lixeira não conta como projeto.
- Páginas, componentes e tabelas contam por projeto, e cada branch é verificada à parte.
- No limite, o botão de criar fica desativado, com **Você chegou ao limite do plano** e **Ver planos**. O agente recebe o mesmo aviso e para.
- Acima do limite (por exemplo, depois de baixar de plano), nada é apagado: os projetos mais antigos seguem editáveis e os demais ficam somente leitura.
- **Meu plano:** menu da conta, no rodapé do menu da esquerda.

### Qual plano para o protótipo

| Situação | Plano | Por quê |
|---|---|---|
| Experimentar, sistema bem pequeno | Starter | 1 projeto, 10 páginas e 10 tabelas |
| MVP de SaaS | Pro | A organização padrão cria uma página por tela, e um MVP passa de 10 telas e de 10 tabelas |
| Projeto criado de um modelo | Pro | Os modelos trazem de 23 a 32 tabelas e de 26 a 36 telas |
| Vários clientes ao mesmo tempo | Ultra | 10 projetos |

No Starter, um sistema com mais de 10 telas só cabe mudando a organização para **Fluxo por página** ou **Tudo em uma página** ([doc 03](03-comecar-o-projeto.md)). Não mude o plano pelo usuário: mostre o limite e deixe a pessoa decidir.

## Quando é ruim

- **Conta pessoal do desenvolvedor como dona do projeto do cliente:** o projeto conta no plano dela e sai com ela. Crie a equipe do cliente e combine quem é o administrador.
- **Todo mundo como Editor:** cliente que só aprova não precisa editar.

## Combina com

- [Conectar o MCP](02-conectar-o-mcp.md): o passo seguinte.
- [Começar o projeto](03-comecar-o-projeto.md): a equipe escolhida aqui é a dona do projeto.
