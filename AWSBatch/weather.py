"""
Script to download data from OpenWeather portal and save it on S3 bucket as .json
"""

import os.path
import json
import requests
from constraints import CITIES, API_KEY, BUCKET, FOLDER
from functions import upload, remove_files_by_extension
import asyncio
import boto3

start = 1606488670
end = 1606747870


def load_data():
    """
    Function to download data from OpenWeather portal and save it on S3 bucket as .json
    :return:
    """
    for element in CITIES:
        counter = 0
        city = element['city']
        lon = element['lon']
        lat = element['lat']
        endpoint = f'http://api.openweathermap.org/data/2.5/air_pollution/' \
                   f'history?lat={lat}&lon={lon}&start={start}&end={end}&appid={API_KEY}'
        res = requests.get(endpoint)
        data = res.json()

        if os.path.isdir('./temp'):
            pass
        else:
            os.makedirs('./temp')

        filename = f'{city}.json'
        filepath = f'./temp/{filename}'
        with open(filepath, 'w') as data_final:
            data_final.write(json.dumps(data))
        # await upload(filepath, BUCKET, f'{INPUT_DIRECTORY}/{filename}')
        client = boto3.client("s3")
        client.upload_file(filepath, BUCKET, f'{FOLDER}/{filename}')
        counter += 1


def load_initial_data():
    """
    Function to call load_data() and remove_files_by_extension('./temp/', '.json')
    :return:
    """
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(load_data())
    load_data()
    remove_files_by_extension('./temp/', '.json')
