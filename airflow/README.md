# 📄 Projeto de Estudo – DAGs no Apache Airflow

Este repositório contém um conjunto de DAGs desenvolvidas como **projeto de estudo em Apache Airflow**.  
O objetivo principal foi praticar conceitos de **ETL, orquestração de tarefas, integração com bancos de dados, manipulação de arquivos CSV e extração de dados de APIs externas**.

Cada DAG apresentada neste projeto tem um propósito específico, seja replicação de dados entre bancos MySQL, transformação de arquivos CSV, geração de relatórios, ou extração de dados financeiros e meteorológicos.  
Todas as DAGs foram criadas para fins de aprendizado e experimentação, servindo como exemplos práticos do uso do Airflow em diferentes cenários de integração e processamento de dados.

---

## 🟦 DAG 01 – `apiDag`

A DAG **`apiDag`** tem como objetivo realizar um fluxo simples de tarefas que envolve a preparação de diretórios para armazenar arquivos de execução diária.  
Ela cria uma estrutura de pastas nomeadas dinamicamente com base no `data_interval_end`, garantindo que cada execução do pipeline tenha um diretório próprio e organizado.

Essa DAG funciona como uma etapa de **preparação e organização do ambiente**, servindo de suporte para outros processos que dependem de diretórios estruturados antes de iniciar suas atividades.

---
## 🟦 DAG 02 – `espelhar_tabelas`

A DAG **`espelhar_tabelas`** tem como objetivo realizar a cópia de dados entre dois bancos MySQL distintos.  
Ela lê registros da tabela `tb01_tipo_perfil` no banco de origem e replica esses dados no banco de destino, garantindo que ambas as bases permaneçam sincronizadas.

Essa DAG funciona como um processo de **espelhamento e integração de dados** entre sistemas, permitindo manter consistência entre duas bases MySQL de forma automatizada.


---

## 🟦 DAG 03 – `etl_csv_to_tb02_user`

A DAG **`etl_csv_to_tb02_user`** tem como objetivo importar dados a partir de um arquivo CSV e carregá-los na tabela `tb02_user` em um banco MySQL.  
Ela lê o arquivo localizado em `/opt/airflow/csv/tb02_user.csv`, converte campos vazios para valores nulos (NULL) e insere cada registro de forma estruturada na tabela de destino.

Essa DAG funciona como um processo de **ingestão e saneamento de dados**, garantindo que informações vindas de arquivos CSV sejam carregadas corretamente no banco e padronizadas antes do armazenamento.

---

## 🟦 DAG 04 – `etl_tb02_user`

A DAG **`etl_tb02_user`** tem como objetivo copiar dados da tabela `tb02_user` entre dois bancos MySQL diferentes.  
Ela consulta todos os registros no banco de origem e realiza a inserção desses mesmos dados no banco de destino, preservando a estrutura completa da tabela e seus campos.

Essa DAG atua como um processo de **replicação e sincronização de dados**, garantindo que a tabela `tb02_user` seja mantida atualizada e consistente entre dois ambientes distintos.

---

## 🟦 DAG 05 – `etl_tb02_user_to_csv`

A DAG **`etl_tb02_user_to_csv`** tem como objetivo exportar dados da tabela `Aniversariantes` presente em um banco MySQL e salvar esses registros em um arquivo CSV.  
Ela realiza a consulta completa da tabela, gera o arquivo `tb02_user.csv` no diretório `/opt/airflow/csv/` e inclui tanto o cabeçalho quanto todos os dados retornados na consulta.

Essa DAG funciona como um processo de **extração e geração de arquivo CSV**, facilitando o uso dos dados exportados em outras ferramentas, análises ou integrações externas.

---

## 🟦 DAG 06 – `executePipeline`

A DAG **`executePipeline`** tem como objetivo orquestrar a execução de um pipeline composto por outras duas DAGs do Airflow.  
Ela dispara, de forma sequenciada, a DAG responsável pela extração dos aniversariantes para CSV (`extractAniversariantesCsv`) e, após sua conclusão, aciona a DAG de transformação e carga (`transformLoadAniversariantesCsv`), aguardando a finalização de cada etapa antes de prosseguir.

Essa DAG funciona como um **pipeline controlador**, garantindo que o fluxo de extração, transformação e carga seja executado de maneira coordenada, segura e na ordem correta.

---
## 🟦 DAG 07 – `extractAniversariantesCsv`

A DAG **`extractAniversariantesCsv`** tem como objetivo extrair os dados da tabela `Aniversariantes` de um banco MySQL e gerar um arquivo CSV com essas informações.  
Ela realiza a consulta completa da tabela, cria o arquivo `aniversariantes.csv` no diretório `/opt/airflow/csv/` e inclui tanto o cabeçalho quanto os registros obtidos.

Essa DAG funciona como um processo de **extração e exportação de dados**, permitindo que informações de aniversariantes estejam disponíveis em formato CSV para outras etapas do pipeline ou sistemas externos.

---
## 🟦 DAG 08 – `transformLoadAniversariantesCsv`

A DAG **`transformLoadAniversariantesCsv`** tem como objetivo transformar os dados contidos no arquivo CSV `aniversariantes.csv` e carregá-los em uma tabela MySQL chamada `aniversariantes`.  
Ela realiza limpeza e filtragem dos dados, remove colunas desnecessárias, exclui duplicidades, agrupa turmas, converte datas de nascimento para o formato de mês por extenso e ordena os registros antes da inserção.

Essa DAG funciona como um processo de **transformação e carga (ETL)**, garantindo que os dados exportados anteriormente estejam estruturados, consistentes e prontos para análise ou consumo por outros sistemas.

---
## 🟦 DAG 09 – `weatherDag`

A DAG **`weatherDag`** tem como objetivo extrair dados meteorológicos semanais de Londres, Reino Unido, a partir da API Visual Crossing, e armazená-los em arquivos CSV.  
Ela cria um diretório específico para cada semana, salva os dados brutos, além de gerar arquivos separados contendo apenas temperaturas e condições meteorológicas.

Essa DAG funciona como um processo de **extração e organização de dados meteorológicos**, permitindo que informações de temperatura e condições climáticas estejam disponíveis de forma estruturada para análises ou integrações futuras.

---

## 🟦 DAG 10 – `get_stocks_dag`

A DAG **`get_stocks_dag`** tem como objetivo extrair dados históricos de ações de empresas específicas (AAPL, MSFT, GOOG e TSLA) utilizando a biblioteca **yfinance**.  
Ela coleta informações com intervalo de 1 hora, cria diretórios separados para cada ação e salva os dados em arquivos CSV diários.

Essa DAG funciona como um processo de **extração e armazenamento de dados financeiros**, permitindo que informações de mercado estejam organizadas e disponíveis para análises, monitoramento ou integração em outros pipelines.
