import numpy as np

def avg10(array, bins, num_fft):
    if not len(array) == (bins * num_fft):
        raise ValueError('Incorrect number of time or frequency bins provided.')

# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

avg10(data, 1000, 1024)
