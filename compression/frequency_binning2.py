import numpy as np

def avg10(array, bins, num_fft, max_freq):
    """Return a frequency binned numpy array of data. Frequency ranges to compress are hard coded,
    and compression is done via a factor-of-10 average.

    :array: numpy array, raw data
    :bins: int, number of time bins
    :num_fft: int, number of FFT frequency bins
    :max_freq: int, maximum frequency of data in Hz"""

    if not len(array) == (bins * num_fft):
        raise ValueError('Incorrect number of time or frequency bins provided.')

    # reshape data array into bins
    # now, the dimentions are: raw[spectra (time bin) number,frequency (FFT bin) number]
    raw = array.reshape((-1,num_fft))

    # initialize empty list to append compressed values to
    compressed = []

    # calculate FFT bin frequency step
    step = round((float(max_freq) / num_fft), 2)

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        # average the first 20 bins
        b = 0
        while b <= 10:
            c = b + 10
            compressed.append(np.average(working[b:c]))
            b += 10
        del b, c

        # do not average the next 103 bins
        for d in working[20:123]:
            compressed.append(d)
        del d

        # average the next 410 bins
        b = 123
        while b <= 523:
            c = b + 10
            compressed.append(np.average(working[b:c]))
            b += 10
        del b, c

        # do not average the next 101 bins
        for d in working[533:634]:
            compressed.append(d)
        del d

        # average the next 390 bins
        b = 634
        while b <= 1014:
            c = b + 10
            compressed.append(np.average(working[b:c]))
            b += 10
        del b, c

        del working
        a += 1

    return np.array(compressed)

# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

avg10(data, 1000, 1024, 5000)
