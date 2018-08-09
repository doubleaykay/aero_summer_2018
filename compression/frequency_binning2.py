import numpy as np

def avg10(array, bins, num_fft, max_freq):
    if not len(array) == (bins * num_fft):
        raise ValueError('Incorrect number of time or frequency bins provided.')

    # reshape data array into bins
    # now, the dimentions are: raw[spectra (time bin) number,frequency (FFT bin) number]
    raw = array.reshape((-1,num_fft))

    compressed = []

    # calculate FFT bin frequency step
    step = round((float(max_freq) / num_fft), 2)

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        a += 1

    return np.array(compressed)

# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

avg10(data, 1000, 1024, 5000)
