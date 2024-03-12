from airflow import DAG
from airflow.operators.bash import BashOperator


DESCRIPTION = "Description for train dag"
DOC_MD = """
Train dag for demo
"""

with DAG(
    dag_id="model_train",
    description=DESCRIPTION,
    catchup=False,
    doc_md=DOC_MD,
) as dag:

    train_model = BashOperator(
        task_id='train_model',
        bash_command='python scripts/train.py',
        dag=dag,
    )

    train_model
