import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG('runner_test', description='Runner Test',
          schedule_interval=None,
          start_date=datetime.now())

task1 = BashOperator(
        task_id='myTest',
        bash_command='/bin/bash myProject/runner.sh oaiIngest frbstl:fraser',
        dag=dag
)
     
task2= BashOperator(
        task_id='myTest2',
        bash_command='/bin/bash myProject/runner.sh oaiIngest umkc:dl',
        dag=dag
)

task1 >> task2
 

