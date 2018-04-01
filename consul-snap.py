#!/usr/bin/env python3


from urllib.request import urlopen
from datetime import datetime
import os
import boto3


def saveCopies():
    keys=[]

    consulAddrPort = os.environ['CONSUL_ADDRESS']
    bucketS3 = os.environ['BUCKET']
    bucketS3path = os.environ['BUCKET_PATH'] if 'BUCKET_PATH' in os.environ.keys() else ''
    n = 10
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketS3)
    for obj in bucket.objects.filter(Prefix='test/'):
       keys.append(obj.key)
    #print(keys)
    keys.sort()
    keys.pop(0)
    print("Sorted")
    print(keys) 
    s3.Object(bucketS3, keys[0]).delete()
      
   

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
    #result = mainFunc('input', 'context')
    #print(result) 
    saveCopies()
