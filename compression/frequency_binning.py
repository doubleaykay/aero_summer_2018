import numpy as np

def bin_freq_avg10(array, max_freq):
    """Bin by frequencies using an average by 10 binning scheme. Returns numpy array of binned values.
    :array: raw data
    :max_freq: int, maximum frequency in data"""

    # calculate bin cadence
    bin_cadence = round((float(max_freq) / len(array) * 1000), 2)




# IO variables
psd_txt = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/psd.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

bin_freq_avg10(data, 5000)
