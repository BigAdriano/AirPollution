"""
File with initial_load_aws_batch DAG in Airflow
"""

from airflow.providers.amazon.aws.operators.batch import BatchOperator
from airflow import DAG
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta

# choose proper dates for daily_load dag
today_date = date.today()
today_str = today_date.strftime('%Y-%m-%d')
yesterday_date = today_date - relativedelta(days=1)
yesterday_str = yesterday_date.strftime('%Y-%m-%d')
day_today = datetime.today()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': day_today,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once',
}

params = {
    "start_date": yesterday_str
}

dag = DAG('initial_load_aws_batch', default_args=default_args, params=params)

t1 = BatchOperator(
    task_id="submit_batch_job",
    job_name='aogloza_initial_load',
    job_queue='adrian_queue',
    job_definition='adrian_job',
    overrides={},
    region_name='us-east-1',
    max_retries=120,
    dag=dag,
)


