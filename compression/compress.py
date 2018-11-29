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

# binary packing function
def write_bin(raw):
    """
    Returns a numpy array that is binary packed.
    :raw: numpy array of raw data
    """
    a = raw.astype('i1')
    b = a.reshape((-1,2))

    b[:,1] = b[:,1] << 4

    c = np.bitwise_or(b[:,0], b[:,1]).astype('i1')

    return c

# binning function for frequency and time binning
def binning(array, factor, expand=False):
    # check that array length is a factor of the factor provided
    if not (len(array) % factor) == 0:
        raise ValueError('Length of array is not a multiple of ' + str(factor) + '!')

    # bin
    compressed = []
    a = 0
    while a <= (len(array) - factor):
        b = (a + factor)
        if expand:
            i = 1
            while i <= factor:
                compressed.append(np.average(array[a:b]))
                i += 1
        if not expand:
            compressed.append(np.average(array[a:b]))
        a += factor

    # check new length as opposed to original array; return array if okay to do so
    if expand:
        if len(compressed) == len(array):
            return compressed
        else:
            raise RuntimeError('Compression did not work, as new list is not as long as original list.')
    if not expand:
        if float(len(array)) / float(len(compressed)) == factor:
            return compressed
        else:
            raise RuntimeError('Compression did not work, as new and old list lengths are not related by given factor.')

def freq_scheme4(array, expand):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in binning(working[0:20], 20, expand=expand):
            compressed.append(d)
        del d

        for d in binning(working[20:124], 2, expand=expand):
            compressed.append(d)
        del d

        for d in binning(working[124:524], 20, expand=expand):
            compressed.append(d)
        del d

        for d in binning(working[524:616], 4, expand=expand):
            compressed.append(d)
        del d #2600 to 3000

        for d in binning(working[616:776], 20, expand=expand):
            compressed.append(d)
        del d

        for d in binning(working[776:864], 8, expand=expand):
            compressed.append(d)
        del d #increase to 4ish

        for d in binning(working[864:1024], 20, expand=expand):
            compressed.append(d)
        del d

        del working
        a += 1

    return np.array(compressed)

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
write_bin(freq).tofile(dir_out + '/freq.dat')
write_bin(sti_times).tofile(dir_out + 'sti_times.dat')

# FREQUENCY BINNING (FREQ_SCHEME4)
