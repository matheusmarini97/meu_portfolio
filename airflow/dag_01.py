from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='apiDag',
    start_date=datetime(2025, 8, 18),
    schedule='@daily'   
) as dag:
    
    tarefa01 = EmptyOperator(task_id = 'tarefa_1')

    tarefa02 = EmptyOperator(task_id = 'tarefa_2')
    
    tarefa03 = EmptyOperator(task_id = 'tarefa_3')

    tarefa04 = BashOperator(
        task_id = 'cria_pasta',
        bash_command = 'mkdir -p "/opt/airflow/csv/mkdir_dag={{data_interval_end}}"'
    )

    tarefa01 >> [tarefa02, tarefa03]
    tarefa03 >> tarefa04