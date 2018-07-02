#!/usr/bin/env python3


from datetime import datetime
import requests
import argparse
import boto3


parser = argparse.ArgumentParser()
parser.add_argument("--host",required=True)
parser.add_argument("--snapshot",required=True)
args = parser.parse_args()

consulRestoreUrl =  'http://{}/v1/snapshot'.format(args.host)
snap = open(args.snapshot, 'rb')
requests.put(consulRestoreUrl,data=snap.read())
snap.close()
