from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os


def set_spark():
    """
    Run Spark with given specification
    :return: spark object
    """

    aws_key_id = ''
    aws_secret = ''
    aws_session = ''

    # read env variables
    with open('.env') as f:
        text = f.read()
    text_lines = text.splitlines()
    for line in text_lines:
        if "=" in line:
            lines = line.split("=")
            env_name = str(lines[0]).upper()
            if env_name == 'AWS_ACCESS_KEY_ID':
                aws_key_id = lines[1]
            if env_name == 'AWS_SECRET_ACCESS_KEY':
                aws_secret = lines[1]
            if env_name == 'AWS_SESSION_TOKEN':
                aws_session = lines[1]

    os.environ['PYSPARK_SUBMIT_ARGS'] = \
        '--packages com.amazonaws:aws-java-sdk-bundle:1.11.372,org.apache.hadoop:hadoop-aws:3.2.3 pyspark-shell'

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("AirPollution") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.3,org.apache.hadoop:hadoop-client:3.3.0") \
        .config("spark.jars.excludes", "com.google.guava:guava") \
        .getOrCreate()

    sc = spark.sparkContext

    sc._jsc.hadoopConfiguration().set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",
                                      "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider")
    sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", aws_key_id)
    sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", aws_secret)
    sc._jsc.hadoopConfiguration().set("fs.s3a.session.token", aws_session)

    sc._jsc.hadoopConfiguration().set("fs.s3.buffer.dir", "/temp")
    sc._jsc.hadoopConfiguration().set("spark.sql.parquet.mergeSchema", "false")

    return spark
