FROM apache/airflow:2.3.0

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
ADD .aws/credentials .aws/credentials

