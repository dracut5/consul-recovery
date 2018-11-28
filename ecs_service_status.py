#!/usr/bin/env python3


import boto3 


session = boto3.Session(region_name='us-east-1')
ecs_client = session.client('ecs')


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def discovery():
        succesStatus = "(service {}) has reached a steady state."
        failedServices = []
        clusterList = ecs_client.list_clusters()
        for clusterArn in clusterList["clusterArns"]:
            clusterName = clusterArn.split('/',1)[1]
            serviceList = [x.split('/',1)[1] for x in ecs_client.list_services(cluster=clusterName, maxResults=100)['serviceArns']]
            for b in list(chunks(serviceList,10)):
                for service in  ecs_client.describe_services(cluster=clusterName, services=b)['services']:
                     lastEvent = service['events'][0]
                     if lastEvent['message'] == succesStatus.format(service['serviceName']):
                          continue
                     else:
                          failedServices.append(service['serviceName'])

        return failedServices

for f in discovery():
    print(f)

