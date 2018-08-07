import numpy as np

def bin_freq(array, max_freq):
    # calculate bin cadence
    bin_cadence = round((float(max_freq) / len(array) * 1000), 2)




# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

bin_freq(data, 5000)
