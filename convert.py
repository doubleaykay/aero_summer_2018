import digital_rf as drf
import sys
import os

#get filename from command line argument
path =  os.path.splitext(sys.argv[1])[0]
filename = path.split("/")[4]

#get date and start/end times in human readable format from filename
UTdate = filename.split("-")[0]
UTstart = filename.split("-")[1]
UTend = filename.split("-")[2]

print(UTdate)
print(UTstart)
print(UTend)

#convert human readable start date and time into second since UNIX epoch
