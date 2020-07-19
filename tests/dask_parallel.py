from timeit import timeit
from time import sleep

from dask.distributed import Client, LocalCluster

import fungraph
import numpy as np

def addmany(*args):
    return sum(args)

def slowadd(x, y, timeseconds=1):
    sleep(timeseconds)
    return x + y

def localclient():
    cluster = LocalCluster(n_workers=8,
                           processes=True,
                           threads_per_worker=1,
                           memory_limit='auto')
    return Client(address=cluster)

def main():
    args = [fungraph.fun(slowadd, x=np.random.uniform(), y=np.random.uniform())
            for _ in range(8)
            ]
    f = fungraph.fun(addmany, *args)
    #print(timeit(f.compute)) # would take about 8 seconds
    with localclient():
        print(timeit(f.compute, number=1)) # should take about 1 second


if __name__ == '__main__':
    main()