from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="model_train",
    catchup=False,
) as dag:

    train_model = BashOperator(
        task_id='train_model',
        bash_command='tree && python scripts/train.py',
        dag=dag,
    )

    train_model
