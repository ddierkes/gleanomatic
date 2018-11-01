FROM puckel/docker-airflow:1.10.0-2 

ENV PYTHONPATH "$PYTHONPATH:/usr/local/airflow"
ENV dags ./dags
ENV lib ./gleanomatic

# Copy lib, dags, and static
COPY ${lib} /usr/local/airflow/gleanomatic
COPY ${dags} /usr/local/airflow/dags

RUN  pip3 install --user -r /usr/local/airflow/gleanomatic/requirements.txt 
RUN  pip3 install --user -r /usr/local/airflow/dags/requirements.txt
