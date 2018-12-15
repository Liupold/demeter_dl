from harvester.Core import HarvesterEngine
from time import sleep

x = HarvesterEngine("http://www.ovh.net/files/1Mb.dat")
print(x.done)
x.Download(False)
print(x.downloading)
sleep(0.5)
print(x.done)
