# 📁 Scripts de Processamento — Eventos

Esta pasta contém três scripts escritos em **Python**, utilizados em processos operacionais reais durante eventos.  
Eles foram executados **em produção** e automatizam tarefas essenciais como ETL, geração de certificados e envio de e-mails.

---

## 📌 Arquivos disponíveis

### 1. **etl_evento.py**
Responsável pelo processo completo de **ETL (Extract, Transform, Load)**.

### 🔄 Funcionamento:
- **Extração:**  
  Obtém dados diretamente do banco de dados MySQL do evento.

- **Transformação:**  
  Padroniza, limpa e consolida os dados para uso posterior.

- **Carga:**  
  Gera um arquivo **`data.csv`** contendo os dados tratados, gravado **na raiz do projeto**.

### 📂 Resultado:
- Arquivo **`data.csv`** contendo os dados dos participantes e eventos.

---

### 2. **gerador_certificado.py**
Script responsável pela **geração automática dos certificados**.

### 🧾 Funcionamento:
- Lê o arquivo **`data.csv`** produzido pelo ETL;
- Calcula horas de participação e monta as informações necessárias;
- Utiliza templates pré-definidos para renderizar os certificados;
- **Gera os certificados na pasta `certificados/`** (ou equivalente, dependendo da estrutura do projeto).

### 📁 Resultado:
- Certificados individuais armazenados na pasta **`certificados/`**.

---

### 3. **send_mail.py**
Responsável pelo **envio automatizado de e-mails** aos participantes.

### ✉️ Funcionamento:
- Lê o arquivo **`data.csv`** para obter:
  - nome do participante  
  - e-mail  
  - arquivo do certificado correspondente  
- Busca cada certificado na pasta **`certificados/`**;
- Envia o e-mail com o certificado anexado;
- Utiliza uma conta de e-mail configurada (SMTP) para realizar o envio.

### 📬 Resultado:
- Certificados enviados automaticamente para todos os participantes listados no CSV.

---

## 🎯 Objetivo da pasta

Agrupar todos os scripts que compõem o fluxo automatizado de pós-evento:

1. **ETL** — consolidação dos dados do evento  
2. **Geração de certificados**  
3. **Envio automatizado de e-mails com certificado aos participantes**

Esse fluxo foi executado **em produção**, garantindo agilidade e confiabilidade na emissão e envio dos certificados.

---
