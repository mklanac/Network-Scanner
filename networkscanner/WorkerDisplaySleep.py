# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 23:43:57 2019

@author: Mario
"""


def sleepNode(*args, **kwargs):
    import subprocess
    
    callSys = 'powercfg /change monitor-timeout-ac 30'
    CREATE_NO_WINDOW = 0x08000000
    subprocess.call(callSys, creationflags=CREATE_NO_WINDOW)
    
    return (dispy_node_name, 'SleepNode')
    
    
if __name__ == '__main__':
    import dispy, sys, time
    #import numpy as np
    import scipy.io as sio
    
    #DisplaySleepMinutes = str(sys.argv[1])
    
    
    mfile = sio.loadmat('DCdata.mat')  
    hostIP = str(mfile['hostIP'][0,0][0])
    numWorkers = int(mfile['IPaddress'][0].shape[0])
    
    IPaddress = []
    
    for i in range(numWorkers):
        PowerOption = mfile['EE'][0][i]
        if(PowerOption==1 or PowerOption==3):
            IPaddress.append(str(mfile['IPaddress'][0,i][0]))
        
    if not IPaddress:
        sys.exit()
    
    cluster = dispy.JobCluster(sleepNode, nodes=IPaddress, ip_addr=hostIP)
    jobs = []
    time.sleep(5)
    for IP in IPaddress:
        job = cluster.submit_node(IP)
        jobs.append(job)
    #cluster.wait() # wait for all scheduled jobs to finish
    for job in jobs:
        host, n = job() # waits for job to finish and returns results
        print('%s (%s) executed job %s at %s with function %s' % (host, job.ip_addr, job.id,
                                                         job.start_time, n))
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
    #cluster.print_status()      
    cluster.close()