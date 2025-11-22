from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime

def copiar_dados():
    # Conexão para o banco origem
    src_hook = MySqlHook(mysql_conn_id="MysqlOrigem")
    # Conexão para o banco destino
    dst_hook = MySqlHook(mysql_conn_id="Database")

    # Buscar dados da tabela origem
    registros = src_hook.get_records("""select 
	no_user, 
	no_email, 
	co_perfil, 
	no_password, 
	no_telefone, 
	is_activated, 
	ic_interno,
	is_blocked,
	co_validate,
	co_credencial,
	co_create,
	dt_create,
	co_update,
	dt_update,
	ic_ativo,
	ic_hackathon
from tb02_user""")

    # Inserir no banco destino
    if registros:
        for linha in registros:
            insert_sql = """INSERT INTO tb02_user (no_user, no_email, co_perfil, no_password, no_telefone, is_activated, ic_interno, is_blocked, co_validate, co_credencial, co_create, dt_create, co_update, dt_update, ic_ativo, ic_hackathon)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            dst_hook.run(insert_sql, parameters=linha)

with DAG(
    dag_id="etl_tb02_user",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["ETL"],
) as dag:

    tarefa_copiar = PythonOperator(
        task_id="copiar_dados",
        python_callable=copiar_dados
    )
