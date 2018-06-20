import digital_rf as drf
import numpy as np
import os
import sys
import datetime
import argparse

#get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of file to read from")
parser.add_argument("-o", "--output", help="location of directory to output to")
parser.add_argument("-a", "--antenna", help="antenna number to read (1-4)")
args = parser.parse_args()

#ensure that arguments are passed
try:
    sys.argv[1]
except IndexError:
    print('Arguments required; use -h to see required arguments.')
    sys.exit()

#check if output directory exists, if not, make it
if not os.path.exists(args.output):
    print('Output directory does not exist, making it now...')
    os.makedirs(args.output)
    print('Output directory created.')

#parameters
#path or filename from argparse
file = args.input
#define data type (u2 = 2byte (16bit) unsigned integer)
type = np.dtype('u2, u2, u2, u2')
#antenna number from argparse
antenna = "f" + str((int(args.antenna) - 1))
#prompt user for the number of chunks they want to read at a time
#chunks = input("What chunk size do you want to read at a time? ")
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

#read data in chunks
def read_in_chunks(file_object, chunk_size=10000000):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

f = open(file, 'r')

#create digital_rf writer object
writer = drf.DigitalRFWriter(
    args.output, dtype=np.dtype('u2'),
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=samples_since_epoch, sample_rate_numerator=10000000,
    sample_rate_denominator=1, is_complex=False
)

#pass chunks to writer object to be written
for piece in read_in_chunks(f):
    data = np.frombuffer(piece, type, count=-1)
    writer.rf_write(data[antenna])
writer.close()
