import numpy as np

def freq_range_from_bin(bin, cadence):
    end = bin * cadence
    start = end - cadence
    return start, end

def bin_from_freq_range(end_freq, cadence):
    bin = end_freq / cadence
    return bin

def value_range_from_bin(bin, rate):
    rate = rate - 1
    end = (bin * rate) + (bin - 1)
    start = end - rate
    return start, end

def bin_freq_avg10(array, max_freq, rate):
    """Bin by frequencies using an average by 10 binning scheme. Returns numpy array of binned values.
    :array: raw data
    :max_freq: int, maximum frequency in data
    :rate: int, number of values per frequency bin in data"""

    # function to split list into parts
    def split_list(alist, wanted_parts):
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
                 for i in range(wanted_parts) ]

    # calculate bin cadence
    bin_cadence = round((float(max_freq) / len(array) * rate), 2)

    # split into sub-arrays for compression
    c1 = array[:(value_range_from_bin(20, rate)[1] + 1)]
    n1 = array[(value_range_from_bin(21, rate)[0] + 1):(value_range_from_bin(121, rate)[1] + 1)]
    c2 = array[(value_range_from_bin(122, rate)[0] + 1):(value_range_from_bin(532, rate)[1] + 1)]
    n2 = array[(value_range_from_bin(533, rate)[0] + 1):(value_range_from_bin(643, rate)[1] + 1)]
    c3 = array[(value_range_from_bin(644, rate)[0] + 1):]

    print(len(c1), len(n1), len(c2), len(n2), len(c3))

    # define compressed data array
    compressed = []

    # compress c1
    a = split_list(c1, 2)[0]
    b = split_list(c1, 2)[1]

    compressed.append(np.average(a))
    compressed.append(np.average(b))

    compressed = np.array(compressed)
    del a, b

    # do not compress n1
    compressed = np.concatenate((compressed, n1))
    print(compressed.shape)
    print(n1.shape)

    # compress c2

# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

# bin_freq_avg10(data, 5000, 1000)
