import digital_rf as drf
import numpy as np
import os
import sys
import datetime

#parameters
#path or filename from command line argument
file = sys.argv[1]
#define data type (u2 = 2byte (16bit) unsigned integer)
type = np.dtype('u2, u2, u2, u2')
#prompt user for the antenna they wish to read
antenna = "f" + str((input("What antenna (1-4) to read from? ") - 1))
#prompt user for the number of chunks they want to read at a time
chunks = input("What chunk size do you want to read at a time? ")
#get filename
path =  os.path.splitext(file)[0]
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
samples_since_epoch = sec_since_epoch * 10000000

#read data
data = np.fromfile(file, type, count=chunks)
#print(data[antenna])

writer = drf.DigitalRFWriter(
    '/media/anoush/DEB0D65EB0D63D29/_AERO/DRF_TEST_5', dtype=np.dtype('u2'),
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=samples_since_epoch, sample_rate_numerator=10000000,
    sample_rate_denominator=1, is_complex=False
)

writer.rf_write(data[antenna])
writer.close()
