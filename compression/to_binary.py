import numpy as np
import argparse

def write_bin(filename):
    if '.txt' in filename:
        out = filename[:-4]
    else:
        raise ValueError('Based on provided filename, input is not a text file.')

    a = np.loadtxt(filename, 'i1')
    b = a.reshape((-1,2))

    b[:,1] = b[:,1] << 4

    c = np.bitwise_or(b[:,0], b[:,1]).astype('i1')

    f = open(out, 'wb+')
    c.tofile(f)
    f.close()

    print('Success.')

def read_bin(filename):
    a = np.fromfile(filename, dtype='i1')
    b0 = np.bitwise_and(a,15)
    b1 = np.bitwise_and(a,15<<4) >> 4
    c = np.stack((b0,b1))

    return c.T.reshape(-1)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of file to read from")
args = parser.parse_args()

write_bin(args.input)
