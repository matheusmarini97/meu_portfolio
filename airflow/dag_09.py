from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.macros import ds_add
from airflow.models import DAG
from datetime import datetime
import pandas as pd
import os

with DAG(
    dag_id='weatherDag',
    start_date=datetime(2025, 8, 17),
    schedule='0 0 * * 1',
    tags=['DAG']
) as dag:

####################################################

    def data_extract(data_interval_end):
        city = 'London'
        country = 'UK'

        api_key = 'A9ZZHJPX4QZJCW7QT26GW2YMT'

        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city},{country}/{data_interval_end}/{ds_add(data_interval_end, 7)}?unitGroup=metric&include=days&key={api_key}&contentType=csv'

        df = pd.read_csv(url)

        folder_path = f'/opt/airflow/csv/weather/semana={data_interval_end}'

        df.to_csv(folder_path + f'/{data_interval_end}_dados_brutos.csv')
        df[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(folder_path + f'/{data_interval_end}_temperaturas.csv')
        df[['datetime', 'description', 'icon']].to_csv(folder_path + f'/{data_interval_end}_condicoes.csv')

####################################################

    task_1 = BashOperator(
        task_id = 'make_folder',
        bash_command = 'mkdir -p "/opt/airflow/csv/weather/semana={{data_interval_end.strftime("%Y-%m-%d")}}"'
    )

    task_2 = PythonOperator(
        task_id = 'data_extract',
        python_callable = data_extract,
        op_kwargs = {'data_interval_end' : '{{data_interval_end.strftime("%Y-%m-%d")}}'}
    )


    task_1 >> task_2