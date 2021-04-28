# Network Scanner
Network Scanner with GUI (PyQt) was written and used in combination with [dispy](https://pypi.org/project/dispy/) to set a local cluster for distributed computing. Network scanner scans the local network, all the devices are listed and you can select devices that you want to use as Workers that will do some task. When you select Workers you can also set the efficiency mode of Workers e.g. at the end of the calculation dispy sends the Workers command to shut down (Command: shutdown -s -t 300 /c "This Worker will shutdown in 300 seconds, please save your work").  


## GIF showing capabilities of GUI 


## Prerequisites

Python >= 3.7, PyQt5, numpy, pandas, scapy

The following command will install the packages:
'''
pip install -r requirements.txt
'''
Before running this command put **requirements.txt** in the directory where the command will be executed. If it is in another directory, specify the path.