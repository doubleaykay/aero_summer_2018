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
            else:
                i += 1
    return np.array(data_nibble)
