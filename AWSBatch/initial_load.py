"""
file to create initial_load dag needed in Apache Airflow
"""

import weather
import validate_input_data
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.batch import BatchOperator
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta


# choose proper dates for initial_load dag
today_date = date.today()
today_str = today_date.strftime('%Y-%m-%d')
ten_years_before_date = today_date - relativedelta(years=10)
ten_years_before_str = ten_years_before_date.strftime('%Y-%m-%d')
yesterday_date = today_date - relativedelta(days=1)
yesterday_str = yesterday_date.strftime('%Y-%m-%d')

days_ago = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once',
}

dag = DAG('initial_load', default_args=default_args)

t1 = PythonOperator(
    task_id='initial_load',
    python_callable=weather.load_initial_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='validate_json_task',
    python_callable=validate_input_data.run_json_validation,
    dag=dag,
)

t1 >> t2
