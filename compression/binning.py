import numpy as np

import argparse

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

dir = args.input + '/' + args.channel
data = np.loadtxt(dir + '/raw/psd.txt')

bin(data, 8, -4, 4).tofile(dir + '/8_bit/psd8.txt', '\n')
bin(data, 7, -4, 4).tofile(dir + '/7_bit/psd7.txt', '\n')
bin(data, 6, -4, 4).tofile(dir + '/6_bit/psd6.txt', '\n')
bin(data, 5, -4, 4).tofile(dir + '/5_bit/psd5.txt', '\n')
bin(data, 4, -4, 4).tofile(dir + '/4_bit/psd4.txt', '\n')
bin(data, 3, -4, 4).tofile(dir + '/3_bit/psd3.txt', '\n')
bin(data, 2, -4, 4).tofile(dir + '/2_bit/psd2.txt', '\n')
bin(data, 1, -4, 4).tofile(dir + '/1_bit/psd1.txt', '\n')
