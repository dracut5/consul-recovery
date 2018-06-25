#!/usr/bin/env python3


from datetime import datetime
import requests
import os
import boto3


def createSnap():
    elasticAddrPort = os.environ['ES_ADDRESS']
    elasticRepo = os.environ['ES_REPO']
    testURL = 'http://{}/_cluster/health?pretty=true'.format(elasticAddrPort)
    snapUrl = 'http://{}/_snapshot/{}/{}_snapshot'.format(elasticAddrPort,elasticRepo,datetime.strftime(datetime.now(), "%Y-%m-%d"))
    
    snapParams = {
        "ignore_unavailable": "true",
        "partial": "true",
        "include_global_state": "false"
        }

    r = requests.get(testURL)
    return r.text


if __name__ == '__main__':
    result = createSnap()
    print(result)

