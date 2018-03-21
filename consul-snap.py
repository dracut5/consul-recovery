#!/usr/bin/env python3


from urllib.request import urlopen
from datetime import datetime
import os
import boto3

consulAddrPort = os.environ['CONSUL_ADDRESS'] if 'CONSUL_ADDRESS' in os.environ.keys() else "127.0.0.1:8500"
consulSnapUrl = 'http://{}/v1/snapshot'.format(consulAddrPort)
bucketS3 = 'terraform-signnow-dev-remote-states'
KeyS3 = 'backup/consul-cl01/'+ datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S") + '_snapshot.tar.gz'

response = urlopen(consulSnapUrl)
snapArchive = response.read()

###Use env vars for AWS credentials 
s3 = boto3.resource('s3')
s3.Bucket(bucketS3).put_object(Key=KeyS3, Body=snapArchive)



