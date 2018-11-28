#!/usr/bin/env python3


from datetime import datetime
import requests
import os
import boto3
import json

def rotateRepo(elasticAddrPort, month, year):
 
    yearString = str(year)

    if month in range(1,4):
        repo = 'first_quarter_' + yearString
    elif month in range(4,7):
        repo = 'second_quarter_' + yearString
    elif month in range(7,10):
        repo = 'third_quarter_' + yearString
    elif date.month in range(10,13):
        repo = 'fourth_quarter_' + yearString
    
    repoInfo = requests.get('http://{}/_cat/repositories'.format(elasticAddrPort))
    repoList = []
    for r in repoInfo.text.splitlines():
        repoList.append(r.split()[0])

    if repo not in repoList:
        repoUrl = 'http://{}/_snapshot/{}'.format(elasticAddrPort,repo)
        repoData = {
            "type": "fs",
            "settings": {
                "location": repo
                }
            }
        requests.put(repoUrl, json=repoData)
        print("New repo {} was created.".format(repo))
    else:
        print("Repo exists, continue...")
     
    return repo 


def createSnap():
   
    elasticAddrPort = os.environ['ES_ADDRESS'] if 'ES_ADDRESS' in os.environ.keys() else 'localhost:9200'
    date = datetime.now()

    repo = rotateRepo(elasticAddrPort, date.month, date.year)

    snapUrl = 'http://{}/_snapshot/{}/snapshot_{}'.format(elasticAddrPort,repo,datetime.strftime(date, "%Y.%m.%d"))
    
    data = {
        "ignore_unavailable": "true",
        "partial": "true",
        "include_global_state": "false"
        }

    r3 = requests.put(snapUrl, json=data)
    return r3.json()


if __name__ == '__main__':
    result = createSnap()
    print(result)

