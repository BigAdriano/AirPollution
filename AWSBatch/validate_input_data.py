"""
Script to validate data stored in .json files on S3 bucket, transform them and save as .parquet files on S3
by using Spark
"""

from constraints import BUCKET, JSON_SCHEMA, FOLDER, CITIES
import run_and_configure_spark
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


def run_json_validation():
    """
    Function to validate data stored in .json files on S3 bucket, transform them and save as .parquet files on S3
    by using Spark
    :return:
    """

    spark = run_and_configure_spark.set_spark()
    cities_df = spark.createDataFrame(CITIES)

    df = spark.read.schema(JSON_SCHEMA).option("multiline", "true") \
        .json(f's3a://{BUCKET}/{FOLDER}/*.json')

    df2 = df.withColumn("li", explode(col("list"))).drop(col("list"))

    df3 = df2.select("coord.lat", "coord.lon", "li.components.co", "li.components.nh3", "li.components.no",
                     "li.components.no2", "li.components.o3", "li.components.pm10", "li.components.pm2_5",
                     "li.components.so2", "li.dt")

    df4 = df3.na.drop("any")
    df5 = df4.withColumn("datetime_UTC", from_unixtime(col('dt'), "MM-dd-yyyy HH:mm:ss"))
    df6 = df5.withColumn("dt2", df5["dt"].cast(StringType()))

    df6 = df6.join(cities_df, ["lat", "lon"], "left")

    df6.write.partitionBy("dt2").parquet(f"s3a://{BUCKET}/parquet")
