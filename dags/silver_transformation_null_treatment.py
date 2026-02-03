from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

default_args = {
  'owner': 'raphael',
  'start_date': datetime(2024, 1, 1),
  'retries': 1,
}

with DAG(
  '02_mongo_to_silver_supabase_null_treatment',
  default_args = default_args,
  schedule_interval = '@daily',
  catchup = False
) as dag:
  
  # Task que transforma o JSON bruto em colunas estruturadas
  transform_raw_to_silver = PostgresOperator(
    task_id = 'transform_movies_json_to_silver',
    postgres_conn_id = 'supabase_conn', # Conexão configurada na interface
    sql = """
          CREATE OR REPLACE VIEW movies_structured AS
            SELECT 
                _airbyte_raw_id,
                _airbyte_extracted_at,
                ("cast"->>0) as first_actor, 
                -- Tratamento para strings vazias antes da conversão
                CASE 
                    WHEN (imdb->>'rating') = '' THEN NULL 
                    ELSE (imdb->>'rating')::float 
                END as rating,
                CASE 
                    WHEN (imdb->>'votes') = '' THEN NULL 
                    ELSE (imdb->>'votes')::int 
                END as total_votes,
                title,
                year
          FROM raw_movies;
    """
  )

  transform_raw_to_silver