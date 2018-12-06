import numpy as np
import argparse

def read_bin(filename):
    a = np.fromfile(filename, dtype='i1')
    b0 = np.bitwise_and(a,15)
    b1 = np.bitwise_and(a,15<<4) >> 4
    c = np.stack((b0,b1))

    return c.T.reshape(-1) 

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="psd file to read")
args = parser.parse_args()

path = args.input
data = read_bin(path)
data = data - data.mean()
diffs = data[1:] - data[:-1]
structure = diffs.sum() / diffs.size

print(path.split('/')[6] + ': ' + str(structure))
