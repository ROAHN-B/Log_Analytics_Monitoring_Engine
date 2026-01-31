# To separate configuation from bussiness logice
# code is clean and easy for resuable

from dask.distributed import LocalCluster, Client
import os

def start_dask():
    if os.environ.get('RENDER'):
        return None
    cluster = LocalCluster(
        n_workers=2, threads_per_worker=3, memory_limit="256MB", dashboard_address=":8790"
    )
    return Client(cluster)


# raw data ->[covnvert unstructure data into structure data] -> structured data
# parsing -> Translating
# LocalCluster is a mini distributed cluser in your system, helps to run dask, as were running on mutiple systems.
#local cluster is used by developer in testing phase.
# n_workers = 2
# threads_per_worker = 2

# schedule
# |
# |
# --- worker 1 (2 threads)
# |
# |
# --- worker 2 ( 2 threads)
#  memory limit="1GB"

# client() is methods how python connects with dask cluster(connection between code and dask cluster)
# send tasks to worker with the help of client and process easily.

# LocalCluster -> create workers + schedule it
# Client -> connect code with dask

# LocalCluster -> Infrastructure
# client -> Interface
