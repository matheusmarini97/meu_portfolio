from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import csv
import os

# Definição da DAG
with DAG(
    dag_id="executePipeline",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["DAG"],
) as dag:

    trigger_csv = TriggerDagRunOperator(
        task_id="gerar_csv",
        trigger_dag_id='extractAniversariantesCsv',
        wait_for_completion=True
    )

    trigger_transformacao = TriggerDagRunOperator(
        task_id="transformar_carga",
        trigger_dag_id='transformLoadAniversariantesCsv',
        wait_for_completion=True
    )

    trigger_csv >> trigger_transformacao