import numpy as np
import digital_rf as drf
import matplotlib.mlab

"""Generate processed intermediate file that can be used to generate a spectral time intensity plot.
Intermediate file is as compressed as possible. Data processing is based on the method from the MIT Haystack digital_rf drf.sti.py tool,
so everything is written to be as similar to drf_sti.py as possible. It has been simplified for the purposes of AERO."""

#initialize IO
path_to_data = '' #path to digital_rf data to read
path_to_output = '/home/anoush/Desktop/working/intermediate_test' #folder to place output files in
path_psd_txt = path_to_output + '/psd.txt'
path_psd_bin = path_to_output + '/psd'
path_freq_txt = path_to_output + '/freq.txt'
path_freq_bin = path_to_output + '/freq'

#initialize reader and parameters
reader = drf.DigitalRFReader(path_to_data) #initialize digital_rf reader
channel = reader.get_channels() #get channels in data
bounds = reader.get_bounds(channels[0]) #get bounds of data (currently using the first channel, need to make this selectable)
num_fft = 2048 #number of FFT bins
integration = 1 #number of rasters to integrate for each plot
decimation = 1 #decimation factor
samples_per_stripe = num_fft * integration * decimation #number of samples to read per loop
sr = reader.get_properties('ant0')['samples_per_second'] #get sample rate from digital_rf metadata
sample_freq = sr / decimation #factor in decimation if there is any

#psd and freq arrays
psd = []
freq = []

#function to split array in half
def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

#loop to read through all data
i = 0
while i <= (bounds[1] - bounds[0]):
    data = reader.read_vector(bounds[0] + i, samples_per_stripe, channel[0])
    psd_temp, freq_temp = matplotlib.mlab.psd(data, NFFT=num_fft, Fs=float(sample_freq), detrend=detrend_fn, scale_by_freq=False)

    #append only second half of processed data
    psd1, psd2 = split_list(psd_temp)
    freq1, freq2 = split_list(freq_temp)
    psd.append(psd2)
    freq.append(freq2)

    i += samples_per_stripe

#convert arrays to numpy arrays
psd = np.array(psd)
freq = np.array(freq)

#take log10 of the psd array
psd = np.log10(psd)

#save data to files
psd.tofile(path_psd_bin)
psd.tofile(path_psd_txt, '\n')
freq.tofile(path_freq_bin)
freq.tofile(path_freq_txt, '\n')
