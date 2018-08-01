import numpy as np

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
