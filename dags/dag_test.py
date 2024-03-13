import os
import pathlib
from datetime import datetime, timedelta
from os.path import join

# [START import_module]
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor


ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "spark_pi"

with DAG(
    DAG_ID,
    default_args={"max_active_runs": 1},
    description="submit spark-pi as sparkApplication on kubernetes",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    # [START SparkKubernetesOperator_DAG]
    pi_example_path = pathlib.Path(__file__).parent.resolve()
    t1 = SparkKubernetesOperator(
        task_id="spark_pi_submit",
        namespace="default",
        application_file="spark_pi.yaml",
        do_xcom_push=True,
        dag=dag,
    )

    t2 = SparkKubernetesSensor(
        task_id="spark_pi_monitor",
        namespace="default",
        application_name="{{ task_instance.xcom_pull(task_ids='spark_pi_submit')['metadata']['name'] }}",
        dag=dag,
    )
    t1 >> t2
