"""
Script to validate data - compare data in .parquet files to data in Athena
"""

from datetime import datetime
import io
import time
import boto3
import datacompy
import run_and_configure_spark
from constraints import BUCKET, PARQUET_TABLE_NAME, DATABASE_NAME, S3_STAGING_DIR, FINAL_REPORTS_FOLDER
import os
import pandas as pd
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

s3_client = boto3.client('s3', region_name='us-east-1')
s3_resource = boto3.resource('s3')
athena_client = boto3.client("athena", region_name='us-east-1')
bucket = s3_resource.Bucket(BUCKET)


def query_athena(query, database_name, output_location):
    """
    Function to run data_partition part
    :param output_location: location where output from Athena query will be stored
    :param database_name: Athena database name
    :param query: SQL query for Athena
    :return: query_response: response from the server
    """

    query_response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": database_name},
        ResultConfiguration={
            "OutputLocation": output_location,
            "EncryptionConfiguration": {"EncryptionOption": "SSE_S3"},
        }
    )
    return query_response


def transform_athena_to_pd(athena_results_filepath, time_sleep=0):
    """
    Function to read data from csv file and to transform them into Pandas DataFrame
    :param athena_results_filepath: path to csv file with results, stored on S3
    :param time_sleep: wait time in seconds, default: 0
    :return:
    """
    time.sleep(time_sleep)
    prefix_objs = bucket.objects.filter(Prefix=athena_results_filepath)
    counter = 0
    for obj in prefix_objs:
        if str(obj.key).endswith('.csv'):
            body = obj.get()['Body'].read()
            temp = io.BytesIO(body)
            athena_pd = pd.read_csv(temp, encoding='utf8')
            try:
                athena_pd.drop(columns='dt2', inplace=True)
            except:
                pass
            counter += 1
    if counter == 0:
        athena_pd = None

    return athena_pd


def save_final_report(filepath, report, folder):
    """
    Function for saving final report on S3
    :param filepath: final file path
    :param report: string with report from datacompy
    :param folder: folder name where report should be placed
    :return: Nothing
    """
    with open(filepath, 'w') as csv_file:
        csv_file.write(report)

    s3_resource.meta.client.upload_file(Filename=filepath,
                                        Bucket=BUCKET,
                                        Key=folder + filepath)

    os.remove(filepath)


def data_reconcile():
    """
    Function to run data_reconciliation part
    :return: Nothing
    """

    spark = run_and_configure_spark.set_spark()

    df = spark.read.parquet(f's3a://{BUCKET}/parquet/dt2=*/*.parquet')
    print(df.show())
    df_pd = df.toPandas()

    query_parquet = f"SELECT * FROM {PARQUET_TABLE_NAME}"

    parquet_response = query_athena(query_parquet, DATABASE_NAME, S3_STAGING_DIR)
    athena_results_filepath_parquet = f'athena_results/' + parquet_response['QueryExecutionId'] + '.csv'
    athena_parquet_pd = transform_athena_to_pd(athena_results_filepath_parquet, 10)

    s3_resource.Object(BUCKET, athena_results_filepath_parquet).delete()
    s3_resource.Object(BUCKET, f'{athena_results_filepath_parquet}.metadata').delete()

    compare_parquet = datacompy.Compare(df_pd, athena_parquet_pd,
                                        join_columns=['city', 'dt'], abs_tol=0.00000)
    compare_parquet.matches(ignore_extra_columns=False)
    save_final_report(f'parquet_table_comparison_{datetime.today()}',
                      compare_parquet.report(), FINAL_REPORTS_FOLDER)

    if compare_parquet.count_matching_rows() != len(df_pd) \
            or compare_parquet.count_matching_rows() != len(athena_parquet_pd):
        print('Some differences in number of matching rows in compared DataFrames found - .parquet type')
        raise Exception('Parquet DataFrames are not the same!')


