import numpy as np

def avg10(array, bins, num_fft, max_freq):
    """Return a frequency binned numpy array of data. Does not expand average bins,
    so there is a smaller number of bins than before. Frequency ranges to compress are hard coded,
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

def avg10_plot(array, bins, num_fft, max_freq):
    """Return a frequency binned numpy array of data. Expands bins so that there are
    the same number of bins as before. Output can be plotted with drf_sti.
    Frequency ranges to compress are hard coded, and compression is done via a factor-of-10 average.

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
            i = 0
            while i <= 9:
                compressed.append(np.average(working[b:c]))
                i += 1
            b += 10
        del b, c, i

        # do not average the next 103 bins
        for d in working[20:123]:
            compressed.append(d)
        del d

        # average the next 410 bins
        b = 123
        while b <= 523:
            c = b + 10
            i = 0
            while i <= 9:
                compressed.append(np.average(working[b:c]))
                i += 1
            b += 10
        del b, c, i

        # do not average the next 101 bins
        for d in working[533:634]:
            compressed.append(d)
        del d

        # average the next 390 bins
        b = 634
        while b <= 1014:
            c = b + 10
            i = 0
            while i <= 9:
                compressed.append(np.average(working[b:c]))
                i += 1
            b += 10
        del b, c, i

        del working
        a += 1

    return np.array(compressed)

# IO variables
dir = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw'
psd_txt = dir + '/psd.txt'
new_txt = dir + '/psd_freq_binned.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

new = avg10_plot(data, 1000, 1024, 5000)

f = open(new_txt, 'w+')
np.log10(new).tofile(f, '\n')
f.close()
