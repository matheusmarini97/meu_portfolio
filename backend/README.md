# 📘 API de Usuários

API REST criada para estudos, utilizando MySQL como banco de dados, JSON como formato de entrada/saída e Flask como framework.  
Permite criar, listar, atualizar e excluir usuários, seguindo uma arquitetura em camadas.

---

## 🏗 Estrutura da API

| Camada / Arquivo      | Função |
|----------------------|--------|
| **config.py**        | Armazena as configurações da aplicação, como variáveis de ambiente, URL do banco, flags de debug, etc. |
| **entity**           | Define as entidades do sistema, representando os dados de forma abstrata. |
| **model**            | Define os modelos de banco de dados (ORM), mapeando entidades para tabelas. |
| **repository**       | Responsável por acessar o banco de dados e realizar operações CRUD. |
| **service**          | Contém a lógica de negócio da aplicação, validações e regras específicas. |
| **schema**           | Serializa e valida os dados de entrada e saída usando Marshmallow, incluindo validação de campos e regras de senha. |
| **view / controller**| Define os endpoints da API, mapeando URLs para funções de serviço. |
| **exceptions.py**    | Define classes de exceções personalizadas para a aplicação. |
| **handlers.py**      | Trata exceções lançadas pela aplicação e retorna respostas padronizadas para a API. |
| **query.sql**        | Contém a query para criar o schema/tabela no MySQL. |

---

## 💡 Fluxo de execução de uma requisição
Abaixo está o fluxo detalhado de como uma requisição percorre a API:

**1. Cliente faz a requisição HTTP**  
O cliente envia uma requisição GET, POST, PATCH ou DELETE para a API.

**2. View / Controller**  
- Recebe a requisição na rota correspondente.  
- Encaminha os dados para a camada de serviço.

**3. Schema (Marshmallow)**  
- Valida os dados de entrada.  
- Serializa a resposta.  
- Aplica regras de validação, como formato de e-mail e senha.

**4. Service**  
- Aplica a lógica de negócio.  
- Valida regras específicas (ex.: atualização de senha).  
- Decide quais operações serão feitas no banco de dados.

**5. Repository**  
- Executa as operações CRUD no banco.  
- Chama o Model para manipular os dados.

**6. Model**  
- Representa a tabela do banco de dados.  
- Mapeia os dados para entidades.

**7. Banco de Dados (MySQL)**  
- Armazena, atualiza, busca ou deleta os registros.

**8. Handlers de Exceções**  
- Interceptam erros lançados pelas camadas acima.  
- Retornam respostas JSON padronizadas para o cliente.

**9. Resposta Final**  
- O cliente recebe a resposta em JSON.  
- Pode ser os dados solicitados, confirmação de ação ou mensagem de erro.

  ### 🔹 Observações importantes

- A camada **Schema** valida dados obrigatórios, tipos e regras especiais, como a senha.  
- Para atualizar a senha, é obrigatório enviar **senha atual** e **nova_senha** juntos.  
- **Exceptions e Handlers** garantem consistência nas respostas de erro.  
- Esse fluxo é aplicado a todos os endpoints da API (`/usuario`), independentemente do método HTTP.

---

## 🧱 Modelo de Dados (Schema)

O `UsuarioSchema` define os seguintes campos:

| Campo            | Tipo       | Obrigatório | Observações |
|------------------|-----------|-------------|-------------|
| **id**           | Integer   | Não         | Identificador do usuário |
| **nome**         | String    | Sim         | Nome completo |
| **email**        | String    | Sim         | Deve ser um e-mail válido |
| **senha**        | String    | Sim         | Senha atual (necessária apenas para atualizar senha) |
| **nova_senha**   | String    | Não         | Nova senha (necessária apenas para atualizar senha) |
| **idade**        | Integer   | Sim         | Idade do usuário |
| **data_nascimento** | DateTime | Sim      | Data de nascimento |

---

### 🔐 Regras de Senha (senha e nova_senha)

- Mínimo **8 caracteres**  
- Deve conter:
  - Letras **maiúsculas**
  - Letras **minúsculas**
  - **Números**
  - **Símbolos**
- **Não pode conter espaços**  

> Obs.: Para alterar a senha, **é obrigatório enviar ambos os campos**: `senha` (atual) e `nova_senha` (nova).

---

## 📚 Endpoints

### ▶️ Listar Usuários
**GET /usuario**  
Retorna todos os usuários cadastrados.

### ▶️ Criar Usuário
**POST /usuario**  
Cria um novo usuário. Todos os campos obrigatórios devem ser enviados.

### ▶️ Buscar Usuário por ID
**GET /usuario/{id}**  
Retorna um usuário específico.

### ▶️ Atualizar Usuário
**PATCH /usuario/{id}**  
Atualiza parcialmente um usuário. Nenhum campo é obrigatório, exceto quando atualizar a senha, que exige `senha` e `nova_senha`.

### ▶️ Excluir Usuário
**DELETE /usuario/{id}**  
Remove um usuário do sistema.

---


## ⚙️ Observações Finais

- **config.py**: Centraliza todas as configurações da aplicação, como variáveis de ambiente, URL do banco de dados e flags de debug, evitando valores hardcoded espalhados pelo código.

- **exceptions.py**: Contém classes de exceções personalizadas para o sistema, permitindo identificar e tratar erros específicos de forma clara.

- **handlers.py**: Trata todas as exceções lançadas pela aplicação e retorna respostas JSON padronizadas para o cliente, garantindo consistência na comunicação.

- **Arquitetura modular**: A separação em camadas (Entity, Model, Repository, Service, Schema, View) facilita a manutenção, testes e futuras expansões da API.

- **Regras de negócio**: Algumas regras específicas são aplicadas pelo service e schema, como a validação de senha. Para alterar a senha, é obrigatório enviar **senha atual** e **nova_senha** juntos.

- **Banco de dados**: O arquivo `query.sql` contém a query para criar o schema/tabela no MySQL, garantindo que a estrutura necessária esteja pronta antes de rodar a aplicação.
