"""
DAG describing Hive pipeline
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.dataproc_operator import DataprocWorkflowTemplateInstantiateOperator

PROJECT_ID = 'wmt-data-search'
TEMPLATE_ID = 'wlt-demo-wf'
REGION_ID = 'us-central1'

start_date = datetime(2019, 1, 1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': start_date,
    'email': ['airflow-monitoring@somedomain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(dag_id='simple_dataproc_workflow',
         default_args=default_args,
         start_date=start_date,
         schedule_interval=None) as dag:

    run_hive = DataprocWorkflowTemplateInstantiateOperator(
        task_id='RunHiveWorkflow',
        project_id=PROJECT_ID,
        region=REGION_ID,
        template_id=TEMPLATE_ID
    )

    load_data = DummyOperator(
        task_id='DummyTask'
    )

    load_data >> run_hive