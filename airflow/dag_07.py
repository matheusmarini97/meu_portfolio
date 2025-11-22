from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime
import csv
import os

# Caminho onde o CSV será salvo
CSV_PATH = "/opt/airflow/csv/aniversariantes.csv" 

def exportar_tb02_user():
    # Conexão MySQL definida no Airflow (Admin -> Connections)
    hook = MySqlHook(mysql_conn_id="Database")
    
    # Consulta os dados da tabela
    registros = hook.get_records("""
        SELECT * FROM Aniversariantes
    """)
    
    if registros:
        
        # Salvar no CSV
        with open(CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Cabeçalho
            writer.writerow([
                "ra", 
                "aluno", 
                "periodo_letivo", 
                "codigo_do_curso", 
                "curso",
                "codigo_habilitação", 
                "habilitacao", 
                "turma", 
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
                "sexo",
                "nascimento",
                "gestor_polo"
            ])
            # Dados
            writer.writerows(registros)
        print(f"{len(registros)} registros salvos em {CSV_PATH}")
    else:
        print("Nenhum registro encontrado.")

# Definição da DAG
with DAG(
    dag_id="extractAniversariantesCsv",
    start_date=datetime(2025, 8, 15),
    schedule=None,
    catchup=False,
    tags=["ETL"],
) as dag:

    tarefa_exportar = PythonOperator(
        task_id="exportar_tb02_user",
        python_callable=exportar_tb02_user
    )