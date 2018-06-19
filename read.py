import numpy as np
import os
import sys

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
print(data[antenna])
