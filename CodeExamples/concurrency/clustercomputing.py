#!/usr/bin/env python3
# clustercomputing.py
# author: Sébastien Combéfis
# version: March 6, 2016

import dispy
import random
import time

def compute(n):
    result = n ** 2
    time.sleep(random.randint(1, 5))
    return (n, result)

# Initialise the cluster
cluster = dispy.JobCluster(compute)
jobs = []

# Submit jobs to the cluster
for i in range(10):
    job = cluster.submit(random.randint(0, 1000))
    job.id = i
    jobs.append(job)

# Waiting for jobs to be executed
for job in jobs:
    n, result = job()
    print('Job #{} : Le carré de {} est {}'.format(job.id, n, result))