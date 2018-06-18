import numpy as np

#filename TODO pull from command line arg
file = "/media/anoush/DEB0D65EB0D63D29/_AERO/working/20180506-0823-0840-TLK-INT.dat"

#define data type (u2 = 2byte (16bit) unsigned integers)
type = np.dtype('u2')

#read data
print(np.fromfile(file, type, count=4))
