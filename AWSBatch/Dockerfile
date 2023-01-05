FROM python:3.7-slim-buster

RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 && \
    apt-get update &&\
    apt-get install -y --no-install-recommends openjdk-11-jre && \
    apt-get install ca-certificates-java -y && \
    apt-get clean && \
    update-ca-certificates -f;
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN pip3 install awscli

ADD constraints.py .
ADD functions.py .
ADD initial_load.py .
ADD run_app.py .
ADD validate_input_data.py .
ADD weather.py .
ADD .env .
ADD set_env_variables.py .
ADD run_and_configure_spark.py .
ADD reconcile_data.py .
ADD analyze_data.py .

RUN python3 set_env_variables.py

CMD ["python3","./run_app.py"]
