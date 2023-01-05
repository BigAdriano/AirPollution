"""
Script to analyze data from S3 in Spark and create some visualisations
"""


import boto3
import run_and_configure_spark
from constraints import BUCKET
from pyspark.sql.types import *
from pyspark.sql.functions import *
import matplotlib.pyplot as plt


def analyze():
    s3_client = boto3.client('s3', region_name='us-east-1')

    spark = run_and_configure_spark.set_spark()

    df = spark.read.parquet(f's3a://{BUCKET}/parquet/dt2=*/*.parquet')
    df.createOrReplaceTempView("aogloza_parquet_test")
    df2 = spark.sql(
        """
        SELECT city, SUM(pm10_a) AS pm10, SUM(pm2_5_a) AS pm2_5, SUM(no2_a) AS no2, SUM(so2_a) AS so2 , SUM(co_a) AS co
        FROM(
            SELECT city,
            IF(AVG(pm10)>45,1,0) AS pm10_a,
            IF(AVG(pm2_5)>15,1,0) AS pm2_5_a,
            IF(AVG(no2)>25,1,0) AS no2_a,
            IF(AVG(so2)>40,1,0) AS so2_a,
            IF(AVG(co)>4,1,0) AS co_a
            FROM aogloza_parquet_test
            GROUP BY SPLIT(datetime_UTC, ' ')[0], city)
            GROUP BY city
        """
    )
    df2_pd = df2.toPandas()

    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=df2_pd.values, colLabels=df2_pd.columns, loc='center')

    fig.tight_layout()

    plt.savefig('table1.svg')
    # upload first visualisation to S3 bucket
    s3_client.upload_file('table1.svg', {BUCKET}, 'datavisualisation/table1.svg')

    df3 = spark.sql(
        """
        SELECT city, COUNT(*) AS how_many FROM (SELECT city, SPLIT(datetime_UTC, ' ')[0] AS date
        FROM aogloza_parquet_test
        GROUP BY SPLIT(datetime_UTC, ' ')[0], city
        HAVING AVG(pm2_5) > 15)
        GROUP BY city
        ORDER BY how_many DESC
        """
    )
    df3_pd = df3.toPandas()

    colors = ['red']
    plt.bar(df3_pd['city'], df3_pd['how_many'], color=colors)
    plt.title('Ilość dni z przekroczoną normą PM2.5', fontsize=14)
    plt.xlabel('Miasto', fontsize=14)
    plt.ylabel('Ilość dni', fontsize=14)
    plt.grid(True)
    plt.savefig('table2.svg')
    # upload the second visualisation to S3
    s3_client.upload_file('table2.svg', {BUCKET}, 'datavisualisation/table2.svg')
