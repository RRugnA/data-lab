from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

default_args = {
  'owner': 'raphael',
  'start_date': datetime(2024, 1, 1),
  'retries': 1,
}

with DAG(
  '01_mongo_to_silver_supabase',
  default_args = default_args,
  schedule_interval = '@daily',
  catchup = False
) as dag:
  
  # Task que transforma o JSON bruto em colunas estruturadas
  transform_raw_to_silver = PostgresOperator(
    task_id = 'transform_movies_json_to_silver',
    postgres_conn_id = 'supabase_conn', # Vamos configurar essa conexão na interface
    sql = """
          CREATE OR REPLACE VIEW moviews_estructured AS
          SELECT
            _airbyte_raw_id,
            _airbyte_extracted_at,
            ("cast"->>0) as first_actor,
            (imdb->>'rating')::float as rating,
            (imdb->>'votes')::int as total_votes,
            title,
            year
          FROM raw_movies;
    """
  )

  transform_raw_to_silver