from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import csv
import os

CSV_PATH = "/opt/airflow/csv/tb02_user.csv" 

def importar_csv():
    dst_hook = MySqlHook(mysql_conn_id="Database")

    if not os.path.exists(CSV_PATH):
        print(f"Arquivo CSV não encontrado: {CSV_PATH}")
        return

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        insert_sql = """
            INSERT INTO tb02_user (
                no_user, no_email, co_perfil, no_password, no_telefone,
                is_activated, ic_interno, is_blocked, co_validate, co_credencial,
                co_create, dt_create, co_update, dt_update, ic_ativo, ic_hackathon
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        count = 0
        for row in reader:
            # Converter valores vazios para None (NULL no MySQL)
            row_tratada = [v if v != "" else None for v in row.values()]

            dst_hook.run(insert_sql, parameters=row_tratada)
            count += 1

    print(f"{count} registros importados com valores vazios convertidos para NULL.")

# Definição da DAG
with DAG(
    dag_id="etl_csv_to_tb02_user",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["ETL"],
) as dag:

    tarefa_importar = PythonOperator(
        task_id="importar_csv_mysql",
        python_callable=importar_csv
    )
