# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:08:47 2019

@author: Mario
"""
import subprocess, sys

if __name__ == "__main__":
    
    #########################################
    ###### DISTRIBUTED COMPUTING SETUP ###### 
    #########################################
    rescanNetwork = True
    if rescanNetwork:
        ret = subprocess.call([sys.executable, r'networkscanner/GUI__DistributedComputingFindWorkers.py'])
        if ret:
            print(ret)
            sys.exit('\n\nSomething went wrong. Check if file "GUI__DistributedComputingFindWorkers.py" is located in working directory.')
            