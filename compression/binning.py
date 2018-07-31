import numpy as np
import pickle

"""Functions and code to bin data into bytes and nibbles."""

def bin_to_bytes(raw, low, high):
    """Bin data into bytes.
    :raw: data array
    :low: int, minimum value of data
    :high: int, maximum value of data
    Returns a numpy array with binned data."""

    byte = np.linspace(low, high, 256)
    data_byte = []
    for b in raw:
        i = 0
        while i <= 254:
            if (byte[i] <= b < byte[i+1]):
                data_byte.append(i)
                i += 1
                break
            elif (b <= low):
                data_byte.append(0)
                break
            elif (b >= high):
                data_byte.append(255)
                break
            else:
                i += 1
    return np.array(data_byte)

def bin_to_nibble(raw, low, high):
    """Bin data into nibbles.
    :raw: data array
    :low: int, minimum value of data
    :high: int, maximum value of data
    Returns a numpy array with binned data."""

    nibble = np.linspace(low, high, 16)
    data_nibble = []
    for b in raw:
        i = 0
        while i <= 14:
            if (nibble[i] <= b < nibble[i+1]):
                data_nibble.append(i)
                i += 1
                break
            elif (b <= low):
                data_nibble.append(0)
                break
            elif (b >= high):
                data_nibble.append(16)
                break
            else:
                i += 1
    return np.array(data_nibble)

# Begin program

# IO variables
dir = '/home/anoush/Desktop/working/intermediate_test'
path_vars = dir + '/vars'
path_file_bytes = dir + '/psd_bytes.txt'
path_file_nibbles = dir + '/psd_nibbles.txt'

# Get variables from pickled file
file_vars = open(path_vars, 'r')
bins, st0, sr, path, path_psd_txt, path_freq_txt, cfreq = pickle.load(file_vars)
file_vars.close()

#data = np.fromfile(path_psd_txt)
data = np.fromfile('/home/anoush/Desktop/working/intermediate_test/psd')

data_b = bin_to_bytes(data, -4, 4)
data_b.tofile(path_file_bytes, '\n')

# data_n = bin_to_nibble(data, -4, 4)
# data_n.tofile(path_file_nibbles, '\n')
