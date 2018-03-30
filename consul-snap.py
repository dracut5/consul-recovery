#!/usr/bin/env python3


from urllib.request import urlopen
from datetime import datetime
import os
import boto3


def mainFunc(event, context):

    consulAddrPort = os.environ['CONSUL_ADDRESS']
    bucketS3 = os.environ['BUCKET']
    bucketS3path = os.environ['BUCKET_PATH'] if 'BUCKET_PATH' in os.environ.keys() else ''
    consulSnapUrl = 'http://{}/v1/snapshot'.format(consulAddrPort)
    KeyS3 = bucketS3path + datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S") + '_snapshot.tar.gz'

    response = urlopen(consulSnapUrl)
    snapArchive = response.read()

    s3 = boto3.resource('s3')
    s3.Bucket(bucketS3).put_object(Key=KeyS3, Body=snapArchive)

    return bucketS3 + '/' + KeyS3

if __name__ == '__main__':
    mainFunc('input', 'context')

