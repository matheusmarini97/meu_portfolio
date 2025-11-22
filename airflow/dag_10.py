from airflow.decorators import dag, task
from airflow.macros import ds_add
from pathlib import Path
import yfinance
import pendulum

tickers = [
    'AAPL',
    'MSFT',
    'GOOG',
    'TSLA'
]

@task()
def extract_data(ticker, ds=None, ds_nodash=None):
    file_path = f'/opt/airflow/csv/{ticker}/{ticker}_{ds_nodash}.csv'
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    hist = yfinance.Ticker(ticker).history(
        interval = '1h',
        start = ds_add(ds, -1),
        end = ds,
        prepost = True
    ).to_csv(file_path)

@dag(
        schedule='0 0 * * 2-6',
        start_date= pendulum.datetime(2025, 8, 21, tz='UTC'),
        catchup=True
        )
def get_stocks_dag():
    for tk in tickers:
        extract_data.override(task_id=tk)(tk)

dag = get_stocks_dag()