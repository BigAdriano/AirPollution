"""
Constants used in project
"""

from pyspark.sql.types import *

API_KEY = 'c4ba93233149dacee023ef1aeb7fb8a5'
CITIES = [
    {'city': 'Łódź', 'lat': 51.7592, 'lon': 19.4560},
    {'city': 'Warszawa', 'lat': 52.2297, 'lon': 21.0122},
    {'city': 'Kraków', 'lat': 50.0647, 'lon': 19.9450},
    {'city': 'Wrocław', 'lat': 51.1079, 'lon': 17.0385},
    {'city': 'Poznań', 'lat': 52.4064, 'lon': 16.9252},
    {'city': 'Gdańsk', 'lat': 54.3520, 'lon': 18.6466},
    {'city': 'Katowice', 'lat': 50.2649, 'lon': 19.0238},
    {'city': 'Szczecin', 'lat': 53.4285, 'lon': 14.5528},
    {'city': 'Białystok', 'lat': 53.1325, 'lon': 23.1688},
    {'city': 'Bydgoszcz', 'lat': 53.1235, 'lon': 18.0084},
    {'city': 'Toruń', 'lat': 53.0138, 'lon': 18.5984},
    {'city': 'Zielona Góra', 'lat': 51.9356, 'lon': 15.5062},
    {'city': 'Gorzów Wielkopolski', 'lat': 52.7325, 'lon': 15.2369},
    {'city': 'Opole', 'lat': 50.6683, 'lon': 17.9231},
    {'city': 'Kielce', 'lat': 50.8661, 'lon': 20.6286},
    {'city': 'Rzeszów', 'lat': 50.0412, 'lon': 21.9991},
    {'city': 'Lublin', 'lat': 51.2465, 'lon': 22.5684},
    {'city': 'Olsztyn', 'lat': 53.7784, 'lon': 20.4801}
]

BUCKET = 'adrianoglozatest'
FOLDER = 'input'
INPUT_DIRECTORY = ''
PARQUET_TABLE_NAME = "weather"
DATABASE_NAME = 'athena_adrianogloza'
S3_STAGING_DIR = 's3://adrianoglozatest/athena_results/'
FINAL_REPORTS_FOLDER = 'athena_results/final_results/'

JSON_SCHEMA = StructType([
    StructField('coord',
                StructType([
                    StructField('lat', DoubleType(), True),
                    StructField('lon', DoubleType(), True)]), True),
    StructField('list', ArrayType(StructType([
        StructField('components', StructType([
            StructField('co', DoubleType(), True),
            StructField('nh3', DoubleType(), True),
            StructField('no', DoubleType(), True),
            StructField('no2', DoubleType(), True),
            StructField('o3', DoubleType(), True),
            StructField('pm10', DoubleType(), True),
            StructField('pm2_5', DoubleType(), True),
            StructField('so2', DoubleType(), True)]), True),
        StructField('dt', LongType(), True),
        StructField('main',
                    StructType([
                        StructField('aqi', LongType(), True)]), True)]), True), True)])

