import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

def export_silver_to_csv():
    # Inicializa o Hook com a conexão do Supabase que você já configurou
    pg_hook = PostgresHook(postgres_conn_id='supabase_conn')
    
    # Query para buscar os dados que você limpou (Camada Silver)
    sql_query = "SELECT * FROM movies_structured"
    
    # Converte o resultado diretamente para um DataFrame do Pandas
    df = pg_hook.get_pandas_df(sql_query)
    
    # Define o caminho do arquivo (dentro do container do Airflow)
    file_path = '/usr/local/airflow/dags/movies_export.csv'
    
    # Salva o CSV
    df.to_csv(file_path, index=False)
    print(f"Arquivo exportado com sucesso para: {file_path}")