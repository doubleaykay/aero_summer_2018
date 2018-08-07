import numpy as np

psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

data = np.loadtxt(psd_txt)

max_freq = 5000
bin_cadence = round((float(max_freq) / len(data) * 1000), 2)
