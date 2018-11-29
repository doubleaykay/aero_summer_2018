import argparse
import digital_rf as drf
import numpy as np

import matplotlib.mlab

import os
from pathlib2 import Path

import pickle

"""
AERO Data Compressor

This script reads digital_rf data and applies the complete aero_summer_2018
compression scheme, returning three binary files which can be read by the
plotting tool to generate spectral plots.

Outputs:
BINARY psd.bin -- spectral data
BINARY freq.bin -- frequency axis data
BINARY sti_times.bin -- time axis data

Written by Anoush Khan, summer/winter 2018.
"""

# FUNCTIONS
# split array in half
def split_list(a_list):
    """
    Splits a list in half.
    :a_list: list, input
    Returns two lists, first/second halves
    """
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
    """
    Takes and array and averages it by a factor.
    :array: list, raw
    :factor: int, factor to average array by
    :expand: bool, whether or not to repeat averaged array factor times
    """
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

# frequency scheme4 function
def freq_scheme4(array, expand, bins, num_fft):
    """
    Applys frequency binning to PSD data for specific, hardcoded frequencies.
    :array: numpy ndarray, raw data
    :expand: bool, whether or not to repeat averaged sections
    :bins: int, number of spectra
    :num_fft: int, number of data points in spectra
    """
    # bins = 1000
    # num_fft = 1024

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

# time scheme2 function
def time_scheme2(array, bins, num_fft):
    """
    Applies time binning to PSD data for specific, hardcoded time ranges
    :array: numpy ndarray, raw data
    :bins: int, number of spectra
    :num_fft: int, number of data points in spectra
    """
    # bins = 1000
    # num_fft = 1024

    # reshape into two axis: axis zero is time, axis 1 is frequency
    # then take the transpose, so that axis zero is frequency
    raw = array.reshape((-1,num_fft)).T

    # create new array
    new = np.zeros(raw.shape)

    # don't time average in frequency bins 0 to 124
    new[0:124,...] = raw[0:124,...]

    # time average in frequency bins 124 to 288
    factor1 = 5
    a = 124
    while a <= 288:
        # b = a + 1
        compress = raw[a,...]
        new[a,...] = binning(compress, factor1, expand=True)
        a += 1
    del a

    # don't time average in frequency bins 288 to 862
    new[288:862,...] = raw[288:862,...]

    # time average in frequency bins 862 to 1024
    factor2 = 5
    a = 862
    while a <= 1023:
        # b = a + 1
        compress = raw[a,...]
        new[a,...] = binning(compress, factor2, expand=True)
        a += 1
    del a

    # transpose back to the original array shape
    new1 = new.T

    # ensure that the array is the correct shape
    if new1.shape == (bins, num_fft):
        # make array one dimensional again
        new2 = new1.reshape((1,-1))
        return new2
    else:
        raise RuntimeError('Output array is the wrong shape, something went wrong.')

# amplitude binning function
def amp_bin(raw, depth, low, high):
    """
    Bin data into specified bit-depth.
    :raw: array, data
    :depth: int, bit depth (i.e. 8, 4, etc)
    :low: int, minimum value of data
    :high: int, maximum value of data
    Returns a numpy array with binned data.
    """

    max_in_depth = 2 ** depth
    bin_range = np.linspace(low, high, max_in_depth)
    data = []
    for b in raw:
        i = 0
        while i <= (max_in_depth - 2):
            if (bin_range[i] <= b < bin_range[i+1]):
                data.append(i)
                i += 1
                break
            elif (b <= low):
                data.append(0)
                break
            elif (b >= high):
                data.append(max_in_depth - 1)
                break
            else:
                i += 1
    return np.array(data)

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
channel = args.channel
dir_in = args.input
dir_out = args.output + '/' + channel

out_freq = dir_out + '/freq.dat'
out_sti_times = dir_out + '/sti_times.dat'
out_psd = dir_out + '/psd.dat'
out_vars = dir_out + '/vars'

# ensure outputs exist
if not os.path.exists(dir_out):
    os.makedirs(dir_out)

if not os.path.exists(dir_out):
    os.makedirs(dir_out)

if not Path(out_freq).is_file():
    f = open(out_freq, 'w+')
    f.close()
    del f

if not Path(out_sti_times).is_file():
    f = open(out_sti_times, 'w+')
    f.close()
    del f

if not Path(out_psd).is_file():
    f = open(out_psd, 'w+')
    f.close()
    del f

if not Path(out_vars).is_file():
    f = open(out_vars, 'w+')
    f.close()
    del f

# READ DIGITAL_RF DATA AND CONVERT INTO SPECTRAL DATA
# processing variables
bins = args.bins # def 1000
frames = 1
num_fft = args.num_fft # def 2048
integration = decimation = 1

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
            data, NFFT=num_fft, Fs=float(sample_freq), detrend=detrend_fn,
            scale_by_freq=False)
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
write_bin(freq).tofile(out_freq)
write_bin(sti_times).tofile(out_sti_times)

# save vars for plotting later
file_out_vars = open(out_vars, 'rw+')
vars = [bins, st0, sr, cfreq, num_fft]
pickle.dump(vars, file_out_vars)
file_out_vars.close()

# FREQUENCY BINNING (FREQ_SCHEME4)
psd_freq = freq_scheme4(psd, True, bins, (num_fft/2))

# TIME BINNING (TIME_SCHEME2)
psd_time = time_scheme2(psd_freq, bins, (num_fft/2))

# LOG10
psd_log10 = np.log10(psd_time)

# 4-BIT AMPLITUDE BINNING
psd_amp = amp_bin(psd_log10[0], 4, -4, 4)

# SAVE PSD_AMP TO BINARY
write_bin(psd_amp).tofile(out_psd)
