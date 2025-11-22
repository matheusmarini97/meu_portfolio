# Sistema de Envio de Emails  

## Visão Geral

Esta aplicação é responsável por gerenciar e enviar emails a partir de uma fila de emails no banco de dados.  
Ela processa dois tipos de envios simultaneamente:

1.  **Envios imediatos** – Emails sem data de envio definida (`dh_envio = NULL`).
2.  **Envios agendados** – Emails com data de envio definida (`dh_envio < data/hora atual`).

O sistema utiliza **multiprocessing** para rodar ambos processos em paralelo.

* * *

## Tecnologias Utilizadas

- **Python 3.10+**
- **SQLAlchemy** para ORM e acesso ao banco
- **Yagmail** para envio de emails via SMTP
- **Multiprocessing** para execução paralela
- **ZoneInfo** para controle de fuso horário (`America/Sao_Paulo`)
- **Logging** para monitoramento de atividades

* * *

## Estrutura do Projeto

```
├── main.py             # Script principal que roda os processos
├── database.py         # Configuração do banco de dados
├── model.py            # Definição do modelo FilaEmail
├── config.py           # Configuração da string de conexão do banco
├── yagemail.py         # Função de envio de emails
└── requirements.txt    # Dependências da aplicação
```

* * *

## Variáveis de Ambiente

Para configuração do banco de dados (MySQL):

| Variável | Descrição |
| --- | --- |
| `DB_PORT` | Porta do banco de dados |
| `DB_USER` | Usuário do banco |
| `DB_HOST` | Endereço do servidor do banco |
| `DB_PASSWORD` | Senha do banco |
| `DB_SCHEMA` | Nome do schema/banco |  
| `MAIL_USER` | Nome do usuario gmail |  
| `MAIL_PASS` | Senha de aplicativo do gmail |  
| `MAIL_MESSAGE_FROM` | Mensgem que vai no from |  
| `TABLENAME` | Nome da tabela de emails do banco |  


* * *

## Configuração do Banco de Dados

- `database.py` usa SQLAlchemy para criar:
    
    - `engine` – conexão com o MySQL
    - `SessionLocal` – fábrica de sessões
    - `Base` – classe base para modelos ORM
- Conexão com MySQL:
    

```python
engine = create_engine(connection_string(), echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

## Modelo de Dados - `FilaEmail`

Tabela: `tb74_fila_email`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `nu_mail` | Integer | Identificador único do email (PK, autoincrement) |
| `nu_user` | Integer | ID do usuário que enviou o email |
| `no_email` | String(100) | Email do destinatário |
| `no_assunto` | String(200) | Assunto do email |
| `no_conteudo` | String(4000) | Conteúdo do email |
| `ic_enviado` | Integer | Indicador de envio (0 = não enviado, 1 = enviado) |
| `dh_create_at` | DateTime | Data de criação do registro (default: NOW) |
| `dh_envio` | DateTime | Data e hora programada para envio (nullable para envios imediatos) |
| `dh_enviado` | DateTime | Data e hora em que o email foi enviado (nullable até envio) |

## Função de Envio de Emails - `yagemail.py`

```python
def send_email(to: str, subject: str, contents: str):
```

Envia um email utilizando o SMTP configurado via `yagmail`.

### Parâmetros

- `to` (str): Destinatário do email
- `subject` (str): Assunto do email
- `contents` (str): Corpo do email (texto ou HTML)

### Processo

1.  Cria conexão SMTP com o usuário e senha configurados.
2.  Envia o email para o destinatário especificado.
3.  Define o cabeçalho `From` com o conteudo das variaveis de ambiente `MAIL_MESSAGE_FROM <MAIL_USER>`.
4.  Fecha a conexão SMTP após o envio.

## Fluxo do Sistema

1.  `main.py` inicializa dois processos em paralelo usando `multiprocessing`:
    
    - `envios_imediatos()` – processa emails sem data de envio (`dh_envio = NULL`)
    - `envios_agendados()` – processa emails com data de envio definida (`dh_envio < data/hora atual`)
2.  Cada função entra em loop infinito:
    
    - Abre uma sessão do banco de dados (`SessionLocal`)
    - Consulta `FilaEmail` para encontrar emails não enviados (`ic_enviado != 1`)
    - Se houver emails:
        - Envia o email usando `send_email(to, subject, contents)`
        - Marca o email como enviado (`ic_enviado = 1`) e atualiza `dh_enviado`
        - Salva as alterações no banco (`session.commit()`)
    - Se não houver emails:
        - Aguarda 2 segundos (`sleep(2)`)
        - Loga mensagem de fila vazia (uma vez por loop contínuo)
3.  Repete continuamente, garantindo que novos emails na fila sejam processados imediatamente.
    

* * *

## Logging

- A aplicação utiliza o módulo `logging` do Python para monitorar atividades.
    
- Configuração:
    
    - Nível: `INFO`
    - Formato: `%(asctime)s [%(levelname)s] %(message)s`
    - Saída: console (`sys.stdout`)
- Eventos registrados:
    
    - Emails enviados (imediatos ou agendados)
    - Mensagem indicando que a fila está vazia
    - Erros de commit ou rollback no banco de dados
