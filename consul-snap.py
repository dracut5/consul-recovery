#!/usr/bin/env python3


from urllib.request import urlopen
from datetime import datetime
import os
import boto3


def removeCopies(keepCopies, s3, bucketS3, prefix):
    
    files = []
    for obj in s3.Bucket(bucketS3).objects.filter(Prefix=prefix):
       files.append(obj.key)

    files.sort()
    if files[0] == prefix: 
        files.pop(0)
    copies = len(files)
    
    while copies > keepCopies:
        delFile = files.pop(0)
        s3.Object(bucketS3, delFile).delete()
        copies -= 1


def mainFunc(event, context):

    consulAddrPort = os.environ['CONSUL_ADDRESS']
    bucketS3 = os.environ['BUCKET']
    bucketS3path = os.environ['BUCKET_PATH'] if 'BUCKET_PATH' in os.environ.keys() else ''
    keepCopies = int(os.environ['COPIES']) if 'COPIES' in os.environ.keys() else 50   

    consulSnapUrl = 'http://{}/v1/snapshot'.format(consulAddrPort)
    KeyS3 = bucketS3path + datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S") + '_snapshot.tar.gz'

    response = urlopen(consulSnapUrl)
    snapArchive = response.read()

    s3 = boto3.resource('s3')
    s3.Bucket(bucketS3).put_object(Key=KeyS3, Body=snapArchive)

    removeCopies(keepCopies, s3, bucketS3, bucketS3path)

    return bucketS3 + '/' + KeyS3


if __name__ == '__main__':
    result = mainFunc('input', 'context')
    print(result) 
