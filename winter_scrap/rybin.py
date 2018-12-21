import numpy as np

def read_bin(filename):
    a = np.fromfile(filename, dtype='i1')
    b0 = np.bitwise_and(a,15)
    b1 = np.bitwise_and(a,15<<4) >> 4
    c = np.stack((b0,b1))

    return c.T.reshape(-1) 
