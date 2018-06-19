import digital_rf as drf
import numpy as np
import os
import sys

samples_since_epoch = 15255949800000000 #need to get this from the code in metadata.py

#parameters
#filename from command line argument
file = sys.argv[1]
#define data type (u2 = 2byte (16bit) unsigned integer)
type = np.dtype('u2, u2, u2, u2')
#prompt user for the antenna they wish to read
antenna = "f" + str((input("What antenna (1 to 4) do you want to read from? ") - 1))
#prompt user for the number of chunks they want to read at a time
chunks = input("What chunk size do you want to read at a time? ")

#read data
data = np.fromfile(file, type, count=chunks)
#print(data[antenna])

writer = drf.DigitalRFWriter(
    '/media/anoush/DEB0D65EB0D63D29/_AERO/DRF_TEST_5', dtype=np.dtype('u2'), subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=samples_since_epoch, sample_rate_numerator=10000000,
    sample_rate_denominator=1, is_complex=False
)

writer.rf_write(data[antenna])
writer.close()
