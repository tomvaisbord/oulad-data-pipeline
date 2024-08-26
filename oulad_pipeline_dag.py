from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from sqlalchemy import create_engine
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

# Initialize the DAG
dag = DAG(
    'oulad_pipeline',
    default_args=default_args,
    description='A pipeline to process OULAD data',
    schedule_interval=None,
)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("OULAD Pipeline") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

# Task 1: Extract and load data to HDFS
extract_and_load_to_hdfs = BashOperator(
    task_id='extract_and_load_to_hdfs',
    bash_command='unzip -o /home/tom1989/Downloads/anonymisedData.zip -d /hdfs/destination && '
                 'hdfs dfs -rm -r -f /hdfs/target_directory/* && '
                 'hdfs dfs -put /hdfs/destination/* /hdfs/target_directory',
    dag=dag,
)

# Task 2: Aggregate student scores
def aggregate_student_scores():
    df = spark.read.csv("hdfs://localhost:9000/hdfs/target_directory/studentAssessment.csv", header=True, inferSchema=True)
    agg_df = df.groupBy("id_student").avg("score")
    pandas_df = agg_df.toPandas()
    # Save the DataFrame to a CSV file to be loaded in the next task
    pandas_df.to_csv('/tmp/aggregated_scores.csv', index=False)

aggregate_student_scores_task = PythonOperator(
    task_id='aggregate_student_scores',
    python_callable=aggregate_student_scores,
    dag=dag,
)

# Task 3: Load data to MySQL
def load_to_sql():
    db_connection_string = 'mysql+pymysql://tom1989:s5426304@localhost/oulad_db'
    engine = create_engine(db_connection_string, echo=True)

    # Read the CSV file generated in the previous task
    pandas_df = pd.read_csv('/tmp/aggregated_scores.csv')

    # Load the data into the MySQL table
    pandas_df.to_sql('aggregated_scores', con=engine, if_exists='replace', index=False)

load_to_sql_task = PythonOperator(
    task_id='load_to_sql',
    python_callable=load_to_sql,
    dag=dag,
)

# Define the task dependencies
extract_and_load_to_hdfs >> aggregate_student_scores_task >> load_to_sql_task
