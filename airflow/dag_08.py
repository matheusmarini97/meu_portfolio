from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import csv
import pandas as pd
import re
import os

# Caminho onde o CSV será salvo
CSV_PATH = "/opt/airflow/csv/aniversariantes.csv" 

def transformation():
    df = pd.read_csv(CSV_PATH)

    df = df.drop([  "ra", 
                    "periodo_letivo", 
                    "codigo_do_curso", 
                    "codigo_habilitação", 
                    "habilitacao", 
                    "situacao_matrícula", 
                    "codigo_matriz_curricular",
                    "tipo_matrícula", 
                    "matriz_curricular", 
                    "turno", 
                    "data_matrícula", 
                    "coeficiente_rendimento", 
                    "cod_instituicao_destino",
                    "motivo_transferencia",
                    "ano_referência",
                    "codigo_usuario",
                    "email",
                    "data_solicitação_alteração",
                    "resultado",
                    "telefone",
                    "polo",
                    "cod_tipo_curso",
                    "gestor_polo"], axis=1)

    df = df[df['curso'] != 'Pensionato']

    df = df.drop_duplicates(subset='aluno', keep='first')

    dicionario_turma = {
        r'.*01.*|.*02.*' : '1º Ano',
        r'.*03.*|.*04.*' : '2º Ano',
        r'.*05.*|.*06.*' : '3º Ano',
        r'.*07.*|.*08.*' : '4º Ano',
        r'.*09.*|.*10.*' : '5º Ano'
    }

    df['turma'] = df['turma'].replace(regex=dicionario_turma)

    df['nascimento'] = df['nascimento'].str[3:5]

    df = df.sort_values(by=['nascimento', 'curso', 'turma', 'aluno'])

    dicionario_data = {
        r'01' : 'Janeiro',
        r'02' : 'Fevereiro',
        r'03' : 'Março',
        r'04' : 'Abril',
        r'05' : 'Maio',
        r'06' : 'Junho',
        r'07' : 'Julho',
        r'08' : 'Agosto',
        r'09' : 'Setembro',
        r'10' : 'Outubro',
        r'11' : 'Novembro',
        r'12' : 'Dezembro',
    }

    df['nascimento'] = df['nascimento'].replace(regex=dicionario_data)

    df = df.where(pd.notnull(df), None)

    return df



def load():
    df = transformation()
    # Conexão MySQL definida no Airflow (Admin -> Connections)
    hook = MySqlHook(mysql_conn_id="MysqlOrigem")

    for _, row in df.iterrows():
        query = ''' INSERT INTO aniversariantes (aluno, curso, turma, sexo, nascimento)
                    VALUES (%s, %s, %s, %s, %s)
        '''
        params = (row['aluno'], row['curso'], row['turma'], row['sexo'], row['nascimento'])
        hook.run(query, parameters=params)

# Definição da DAG
with DAG(
    dag_id="transformLoadAniversariantesCsv",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["ETL"],
) as dag:

    tarefa_exportar = PythonOperator(
        task_id="exportar_tb02_user",
        python_callable=load
    )
