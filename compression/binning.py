import numpy as np

import argparse
import os
from pathlib2 import Path

"""Functions and code to bin data into specific bit depth."""

def bin(raw, depth, low, high):
    """Bin data into specified bit-depth.
    :raw: array, data
    :depth: int, bit depth (i.e. 8, 4, etc)
    :low: int, minimum value of data
    :high: int, maximum value of data
    Returns a numpy array with binned data."""

    max_in_depth = 2 ** depth
    bin_range = np.linspace(low, high, max_in_depth)
    data = []
    for b in raw:
        i = 0
        while i <= (max_in_depth - 2):
            if (bin_range[i] <= b < bin_range[i+1]):
                data.append(i)
                i += 1
                break
            elif (b <= low):
                data.append(0)
                break
            elif (b >= high):
                data.append(max_in_depth - 1)
                break
            else:
                i += 1
    return np.array(data)

# Begin program

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of directory to read from")
parser.add_argument("-c", "--channel", help="drf channel to read from")
args = parser.parse_args()

# IO variables
dir = args.input + '/' + args.channel
data = np.loadtxt(dir + '/raw/psd.txt')

psd8 = dir + '/8_bit/psd8.txt'
psd7 = dir + '/7_bit/psd7.txt'
psd6 = dir + '/6_bit/psd6.txt'
psd5 = dir + '/5_bit/psd5.txt'
psd4 = dir + '/4_bit/psd4.txt'
psd3 = dir + '/3_bit/psd3.txt'
psd2 = dir + '/2_bit/psd2.txt'
psd1 = dir + '/1_bit/psd1.txt'

# ensure outputs exist
if not os.path.exists(dir + '/8_bit'):
    os.makedirs(dir + '/8_bit')
if not os.path.exists(dir + '/7_bit'):
    os.makedirs(dir + '/7_bit')
if not os.path.exists(dir + '/6_bit'):
    os.makedirs(dir + '/6_bit')
if not os.path.exists(dir + '/5_bit'):
    os.makedirs(dir + '/5_bit')
if not os.path.exists(dir + '/4_bit'):
    os.makedirs(dir + '/4_bit')
if not os.path.exists(dir + '/3_bit'):
    os.makedirs(dir + '/3_bit')
if not os.path.exists(dir + '/2_bit'):
    os.makedirs(dir + '/2_bit')
if not os.path.exists(dir + '/1_bit'):
    os.makedirs(dir + '/1_bit')

if not Path(psd8).is_file():
    f = open(psd8, 'w+')
    f.close()
    del f
if not Path(psd7).is_file():
    f = open(psd7, 'w+')
    f.close()
    del f
if not Path(psd6).is_file():
    f = open(psd6, 'w+')
    f.close()
    del f
if not Path(psd5).is_file():
    f = open(psd5, 'w+')
    f.close()
    del f
if not Path(psd4).is_file():
    f = open(psd4, 'w+')
    f.close()
    del f
if not Path(psd3).is_file():
    f = open(psd3, 'w+')
    f.close()
    del f
if not Path(psd2).is_file():
    f = open(psd2, 'w+')
    f.close()
    del f
if not Path(psd1).is_file():
    f = open(psd1, 'w+')
    f.close()
    del f

bin(data, 8, -4, 4).tofile(psd8, '\n')
bin(data, 7, -4, 4).tofile(psd7, '\n')
bin(data, 6, -4, 4).tofile(psd6, '\n')
bin(data, 5, -4, 4).tofile(psd5, '\n')
bin(data, 4, -4, 4).tofile(psd4, '\n')
bin(data, 3, -4, 4).tofile(psd3, '\n')
bin(data, 2, -4, 4).tofile(psd2, '\n')
bin(data, 1, -4, 4).tofile(psd1, '\n')
