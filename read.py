import numpy as np
import os
import sys

#parameters
#filename from command line argument
file = sys.argv[1]
#define data type (u2 = 2byte (16bit) unsigned integer)
type = np.dtype('u2')

#read data
print(np.fromfile(file, type, count=4))
