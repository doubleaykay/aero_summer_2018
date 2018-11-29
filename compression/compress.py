# read drf
# convert to spectral data (sti_intermediate_file.py)
# store freq and sti_times array as binary using write_bin() for plotting tool
# take psd array to be processed
# apply frequency binning scheme 4
# apply time binning scheme 2
# take log 10
# apply 4-bit amplitude binning
# store as binary

import argparse
import digital_rf as drf
import numpy as np

"""
AERO Data Compressor

This script reads digital_rf data and applies the complete aero_summer_2018
compression scheme, returning three binary files which can be read by the
plotting tool to generate spectral plots.

Outputs:
BINARY psd.bin -- spectral data
BINARY freq.bin -- frequency axis data
BINARY sti_times.bin -- time axis data
"""

# FUNCTIONS
# split array in half
def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

# BEGIN PROGRAM
#get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of drf directory to read from")
parser.add_argument("-o", "--output", help="location of directory to output to")
parser.add_argument("-n", "--num_fft", nargs='?', const=2048, type=int, default=2048, help="number of frequency bins (i.e. number of data points in spectra)")
parser.add_argument("-c", "--channel", help="drf channel to read from")
parser.add_argument("-b", "--bins", nargs='?', const=1000, type=int, default=1000, help="number of time bins (i.e. number of spectra)")
args = parser.parse_args()

# IO variables
dir_in = args.input
dir_out = args.output + '/' + channel

# READ DIGITAL_RF DATA AND CONVERT INTO SPECTRAL DATA
# processing variables
channel = args.channel
bins = args.bins
frames = 1
num_fft = args.num_fft
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

#create sti_times array for use when plotting
sti_times = np.zeros([bins], np.complex128)

for b in np.arange(bins):
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
psd = np.array(psd)
freq = np.array(freq)

# save freq and sti_times as binary files
