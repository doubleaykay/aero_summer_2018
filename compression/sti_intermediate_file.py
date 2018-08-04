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
import argparse

"""Generate processed intermediate file that can be used to generate a spectral time intensity plot.
Intermediate file is as compressed as possible. Data processing is based on the method from the MIT Haystack digital_rf drf.sti.py tool,
so everything is written to be as similar to drf_sti.py as possible. It has been simplified for the purposes of AERO."""

#get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of drf directory to read from")
parser.add_argument("-o", "--output", help="location of directory to output to")
parser.add_argument("-n", "--num_fft", help="number of FFT bins")
parser.add_argument("-c", "--channel", help="drf channel to read from")
parser.add_argument("-b", "--bins", help="number of time bins")
args = parser.parse_args()

# IO variables
dir_in = args.input
dir_out = args.output #folder to place output files in
psd_txt = dir_out + '/raw/psd.txt'
freq_txt = dir_out + '/freq.txt'
vars_txt = dir_out + '/vars.txt'
sti_times_txt = dir_out + '/sti_times.txt'

# processing variables
channel = args.channel
bins = args.bins #1000
frames = 1
num_fft = args.num_fft #2048
integration = 1
decimation = 1

# open digital RF path
dio = drf.DigitalRFReader(dir_in)

# get sampling rate
sr = dio.get_properties(channel)['samples_per_second']

# get data bounds
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

# calculations for processing
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

# convert arrays to numpy arrays
psd = numpy.array(psd)
freq = numpy.array(freq)

# frequency binning happens here

# take log10 of the psd array
psd = numpy.log10(psd)

# save data to files
psd.tofile(psd_txt, '\n')
freq.tofile(freq_txt, '\n')

# pickle sti_psd data
file_sti_times = open(sti_times_txt, 'rw+')
pickle.dump(sti_times, sti_times_txt)
file_sti_times.close()

# save variables to file
file_vars = open(path_vars, 'rw+')
vars = [bins, st0, sr, path, psd_txt, freq_txt, cfreq, num_fft, sti_times_txt]
pickle.dump(vars, file_vars)
file_vars.close()
