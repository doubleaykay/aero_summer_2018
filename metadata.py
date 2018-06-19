import digital_rf as drf
import sys
import os
import datetime

#get filename from command line argument
path =  os.path.splitext(sys.argv[1])[0]
filename = path.split("/")[path.count('/')]

#get date and start/end times in human readable format from filename
UTdate = filename.split("-")[0]
UTstart = filename.split("-")[1]
UTend = filename.split("-")[2]

#convert human readable start date and time into seconds since UNIX epoch
y = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%Y'))
m = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%m'))
d = int(datetime.datetime.strptime(str(UTdate), '%Y%m%d').strftime('%d'))
h = int(datetime.datetime.strptime(str(UTstart), '%H%M').strftime('%H'))
M = int(datetime.datetime.strptime(str(UTstart), '%H%M').strftime('%M'))

sec_since_epoch = int((datetime.datetime(y,m,d,h,M) - datetime.datetime(1970,1,1)).total_seconds())
print(sec_since_epoch)
