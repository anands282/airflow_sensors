from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from pyspark.sql import SparkSession

# Retrieve AWS credentials from Airflow connections
aws_access_key_id = Variable.get("aws_access_key_id")
aws_secret_access_key = Variable.get("aws_secret_access_key")

# Authenticate with S3
spark = SparkSession.builder \
    .appName("Read from S3") \
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
    .getOrCreate()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    's3_file_sensor_etl',
    default_args=default_args,
    description='A DAG to trigger an ETL task when a file appears in an S3 bucket',
    schedule_interval='@daily',
)

start = EmptyOperator(task_id='start', dag=dag)


def etl_task():
    df = spark.read.parquet("s2a://anands282-bucket/click_stream_data.parquet")
    df.show(truncate=False)


etl = PythonOperator(
    task_id='etl_task',
    python_callable=etl_task,
    dag=dag,
)

s3_sensor = S3KeySensor(
    task_id='s3_file_sensor',
    bucket_name='anands282-bucket',
    bucket_key='click_stream_data.parquet',  # Path to the file you're looking for
    wildcard_match=False,  # Use wildcard to match files
    aws_conn_id='aws_anands282',  # Connection ID to your AWS account
    timeout=18 * 60 * 60,  # Timeout after 18 hours
    poke_interval=60,  # Check every 60 seconds
    mode='poke',
    dag=dag,
)

start >> s3_sensor >> etl
