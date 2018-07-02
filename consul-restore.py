#!/usr/bin/env python3


import requests
import argparse
import sys
import os
import boto3

try:
    action = sys.argv.pop(1)
except IndexError:
    print("First argument shoulb be 'list' or 'restore'.")
    exit()

def getS3bucket(profile, bucket):
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    backupBucket = s3.Bucket(bucket)

    return backupBucket

def restore(host, bucket, snapshot, profile):
    tmpFile = "/tmp/consul_snapshot.tar.gz"
    bucket = getS3bucket(profile, bucket)
    consulRestoreUrl =  'http://{}/v1/snapshot'.format(host)
    with open(tmpFile, 'wb') as data:
        bucket.download_fileobj(snapshot, data)
    with open(tmpFile, 'rb') as data:
        requests.put(consulRestoreUrl, data=data.read())
    os.remove(tmpFile)
 
def s3List(bucket, bucketPath, profile):
    bucket = getS3bucket(profile, bucket)
    for object in bucket.objects.filter(Prefix=bucketPath):
        print(object)

parser = argparse.ArgumentParser()
parser.add_argument("--bucket")
parser.add_argument("--profile")

if action == "list":
    parser.add_argument("--bucket_path")
    args = parser.parse_args()
    s3List(args.bucket, args.bucket_path, args.profile)
elif action == "restore":
    parser.add_argument("--consul_address",required=True)
    parser.add_argument("--snapshot",required=True)
    args = parser.parse_args()
    restore(args.consul_address, args.bucket, args.snapshot, args.profile)

