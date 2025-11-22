from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime

def copiar_dados() -> None:
    # Conexão para o banco origem
    src_hook = MySqlHook(mysql_conn_id="MysqlOrigem")
    # Conexão para o banco destino
    dst_hook = MySqlHook(mysql_conn_id="Database")

    # Buscar dados da tabela origem
    registros = src_hook.get_records("SELECT no_perfil FROM tb01_tipo_perfil")

    # Inserir no banco destino
    if registros:
        for linha in registros:
            insert_sql = "INSERT INTO tb01_tipo_perfil (no_perfil) VALUES (%s)"
            dst_hook.run(insert_sql, parameters=linha)

with DAG(
    dag_id="espelhar_tabelas",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["ETL"],
) as dag:

    tarefa_copiar = PythonOperator(
        task_id="copiar_dados",
        python_callable=copiar_dados
    )