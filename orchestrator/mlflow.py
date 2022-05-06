# TODO: the design of the overall pipeline 
from airflow import models
from pathlib import Path
from datetime import datetime, timedelta

# from great_expectations_provider.operators.great_expectations import (
#     GreatExpectationsOperator,)

from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator, BigQueryCheckOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.utils.dates import days_ago

# Assumes existence of the following Airflow Variables
PROJECT_ID = models.Variable.get("gcp_project")
DATASET = models.Variable.get("bigquery_dataset")
TABLE = models.Variable.get("bigquery_table")
SOURCE_TABLE = models.Variable.get("source_table")

# Default DAG args
default_args = {
    "owner": "airflow",
    "catch_up": False,
    "email_on_failure": True, 
    "email_on_retry": False, 
    "email": ["daisuke0582@gmail.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    }

with models.DAG( dag_id="data",
    description="Feature creating operations.",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["dataops"],) as dag:

    """
    Workflows to validate data and create features.
    """

    # Extract data from various sources: Streaming data or ETL data
    extract_data = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        dataset_id=DATASET,
        table_id=TABLE,
        view={
        "query": f"SELECT * FROM `{PROJECT_ID}.{DATASET}.{SOURCE_TABLE}`",
        "useLegacySql": False,
        },
        )
    
    #https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html#check-if-query-result-has-data
    # Check if query result has data
    check_data = BigQueryCheckOperator(
        task_id="execute_bigquery_sql",
        sql=f"SELECT COUNT(*) FROM `{PROJECT_ID}.{DATASET}.{TABLE}`",
        use_legacy_sql=False,
        )

    # # Task relationships
    extract_data >> check_data
