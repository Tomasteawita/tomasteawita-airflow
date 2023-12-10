from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import smtplib

QUERY_CREATE_TABLE = '''
    CREATE TABLE IF NOT EXISTS tecnica_ml (
    id varchar(100),
    site_id varchar(100),
    title varchar(100),
    price decimal(10,2),
    thumbnail varchar(100),
    create_date date,
    primary key(id, create_date)
);
'''

#def send_error():
#    try:
#        smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
#        smtp_conn.starttls()
#        smtp_conn.login(Variable.get('smtp_from'), Variable.get('smtp_password'))
#        subject = 'ERROR: ETL top tokerns'
#        body_text = 'Error en el proceso ETL, revisar LOGs'
#        message = 'Subject: {}\n\n{}'.format(subject, body_text)
#        smtp_conn.sendmail(Variable.get('smtp_from'), Variable.get('smtp_to'), message)
#        print('Exito')
#    except Exception as exception:
#        print(exception)
#        print('Failure')
#        raise exception

defaul_args = {
    "owner": "Tomasteawita",
    "start_date": datetime(2023, 7, 1),
    "retries": 0,
    "retry_delay": timedelta(seconds = 5),
}

with DAG(
    dag_id = "Meli_to_postgres",
    default_args = defaul_args,
    description = "ETL del top 50 microondas con mayor relevancia",
    schedule_interval = "@daily",
    catchup = False,
) as dag:
    
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="postgres_connection",
        sql=QUERY_CREATE_TABLE,
        dag=dag,
    )

    spark_etl = SparkSubmitOperator(
        task_id = "spark_etl",
        application = f'{Variable.get("spark_scripts_dir")}/ETL_MELI_postgres.py',
        conn_id = "spark_default",
        dag = dag,
        driver_class_path = Variable.get("driver_class_path"),
    )
    
    #send_email_failure = PythonOperator(
    #    task_id = 'enviar_fallo',
    #    python_callable = send_error,
    #    trigger_rule = 'all_failed',  
    #    provide_context = True, 
    #    dag = dag,
    #)

    create_table >> spark_etl