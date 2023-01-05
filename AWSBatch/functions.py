"""
Functions being used in weather.py script
"""

import aioboto3
import os


async def upload(filename: str, bucket: str, key: str):
    """
    Function to upload file to S3 bucket
    :param filename: file to upload
    :param bucket: S3 bucket name
    :param key: full filepath to file on S3 bucket
    :return: Nothing
    """
    with open(filename, 'rb') as f:
        session = aioboto3.Session()
        async with session.client("s3") as s3:
            await s3.upload_fileobj(f, bucket, key)


def remove_files_by_extension(directory: str, extension: str):
    """
    :param directory: name of directory where files should be deleted
    :param extension: extension of files to be removed
    :return:
    """
    filelist = os.listdir(directory)
    for file in filelist:
        if file.endswith(f'.{extension}'):
            os.remove(file)

