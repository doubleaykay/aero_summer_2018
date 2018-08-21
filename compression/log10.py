import numpy as np
import argparse

def log10(array):
    return np.log10(array)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of file to read from")
args = parser.parse_args()

in_file = args.input
out_file = in_file.split('.')[0] + '_log10.txt'

f = open(out_file, 'w+')
log10(np.loadtxt(in_file)).tofile(f, '\n')
f.close()
