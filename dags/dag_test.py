from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor

START_DATE = datetime.strptime("{{ start_date }}", "%Y-%m-%d")
SCHEDULE_INTERVAL = None

with DAG(
        dag_id="test",
        schedule_interval=SCHEDULE_INTERVAL,
        start_date=START_DATE,
        catchup=False,
) as dag:
    task_submit = SparkKubernetesOperator(
        task_id='submit',
        namespace="airflow",
        application_file="test.yaml",
        do_xcom_push=True,
        dag=dag
    )

    task_wait = SparkKubernetesSensor(
        task_id='wait',
        namespace="airflow",
        application_name="{{ task_instance.xcom_pull(task_ids='submit')['metadata']['name'] }}",
        dag=dag,
        attach_log=True,
    )

    task_submit >> task_wait
