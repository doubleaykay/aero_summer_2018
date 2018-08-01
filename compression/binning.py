import numpy as np

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

# IO variables
dir = '/home/anoush/Desktop/working/intermediate_test/binned/'

data = np.loadtxt('/home/anoush/Desktop/working/intermediate_test/psd.txt')

bin(data, 8, -4, 4).tofile(dir + 'psd8.txt', '\n')
bin(data, 4, -4, 4).tofile(dir + 'psd4.txt', '\n')
bin(data, 2, -4, 4).tofile(dir + 'psd2.txt', '\n')
bin(data, 1, -4, 4).tofile(dir + 'psd1.txt', '\n')
