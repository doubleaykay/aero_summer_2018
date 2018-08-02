import sys
import traceback

import digital_rf as drf
import matplotlib.gridspec
import matplotlib.mlab
import matplotlib.pyplot
import numpy
import numpy.fft
import scipy
import scipy.signal

import pickle

"""Generate processed intermediate file that can be used to generate a spectral time intensity plot.
Intermediate file is as compressed as possible. Data processing is based on the method from the MIT Haystack digital_rf drf.sti.py tool,
so everything is written to be as similar to drf_sti.py as possible. It has been simplified for the purposes of AERO."""


channel = 'ant0'
path = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/20180506-0823-0840-TLK-INT/'
bins = 1000
frames = 1
num_fft = 2048
integration = 1
decimation = 1

path_to_output = '/home/anoush/Desktop/working/intermediate_test' #folder to place output files in
path_psd_txt = path_to_output + '/psd.txt'
path_psd_bin = path_to_output + '/psd'
path_freq_txt = path_to_output + '/freq.txt'
path_freq_bin = path_to_output + '/freq'
path_vars = path_to_output + '/vars'
path_sti_times = path_to_output + '/sti_times.txt'

file_vars = open(path_vars, 'rw+')

# open digital RF path
dio = drf.DigitalRFReader(path)

# initialize outside the loop to avoid memory leak

sr = dio.get_properties(channel)['samples_per_second']

# initial time info
b = dio.get_bounds(channel)

st0 = int(b[0])
et0 = int(b[1])

# get metadata
mdt = dio.read_metadata(st0, et0, channel)
try:
    md = mdt[mdt.keys()[0]]
    cfreq = md['center_frequencies'].ravel()
except (IndexError, KeyError):
    cfreq = 0.0

blocks = bins * frames

samples_per_stripe = num_fft * integration * decimation
total_samples = blocks * samples_per_stripe

if total_samples > (et0 - st0):
    print 'Insufficient samples for %d samples per stripe and %d blocks between %ld and %ld' % (samples_per_stripe, blocks, st0, et0)

stripe_stride = (et0 - st0) / blocks

bin_stride = stripe_stride / bins

start_sample = st0

#psd and freq arrays
psd = []
freq = []

#function to split array in half
def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

#create sti_times array for use when plotting
sti_times = numpy.zeros([bins], numpy.complex128)

for b in numpy.arange(bins):
    data = dio.read_vector(start_sample, samples_per_stripe, channel)

    if decimation > 1:
        data = scipy.signal.decimate(data, decimation, ftype='fir')
        sample_freq = sr / decimation
    else:
        sample_freq = sr

    detrend_fn = matplotlib.mlab.detrend_none

    try:
        psd_data, freq_axis = matplotlib.mlab.psd(
            data, NFFT=num_fft, Fs=float(sample_freq), detrend=detrend_fn, scale_by_freq=False)
    except:
        traceback.print_exc(file=sys.stdout)

    #append only second half of processed data
    psd1, psd2 = split_list(psd_data)
    freq1, freq2 = split_list(freq_axis)
    psd.append(psd2)
    freq.append(freq2)

    sti_times[b] = start_sample / sr

    start_sample += stripe_stride

#convert arrays to numpy arrays
psd = numpy.array(psd)
freq = numpy.array(freq)

#take log10 of the psd array
psd = numpy.log10(psd)

#save data to files
psd.tofile(path_psd_bin)
psd.tofile(path_psd_txt, '\n')
freq.tofile(path_freq_bin)
freq.tofile(path_freq_txt, '\n')

# pickle sti_psd data
file_sti_times = open(path_sti_times, 'rw+')
pickle.dump(sti_times, file_sti_times)
file_sti_times.close()

#save variables to file
vars = [bins, st0, sr, path, path_psd_txt, path_freq_txt, cfreq, num_fft, path_sti_times]
pickle.dump(vars, file_vars)
file_vars.close()
