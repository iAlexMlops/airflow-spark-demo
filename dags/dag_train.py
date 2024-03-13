from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor


DESCRIPTION = "Description for train dag"
DOC_MD = """
train dag for demo
"""

with DAG(
    dag_id="model_train",
    description=DESCRIPTION,
    catchup=False,
    doc_md=DOC_MD,
) as dag:
    task_submit = SparkKubernetesOperator(
        task_id='submit',
        namespace="airflow",
        application_file="sparkapplications/train.yaml",
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
