import digital_rf as drf
import numpy as np
import argparse
import matplotlib.mlab

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of drf directory to read from")
parser.add_argument("-c", "--channel", help="drf channel to read from")
parser.add_argument("-s", "--start", dest="start", default=None,
                  help="Use the provided start time instead of the first time in the data. format is ISO8601: 2015-11-01T15:24:00Z")
parser.add_argument("-e", "--end", dest="end", default=None,
                  help="Use the provided end time for the plot. format is ISO8601: 2015-11-01T15:24:00Z")
args = parser.parse_args()

# processing vars
channel = args.channel
num_fft = 2048
bins = 1000
frames = 1
integration = 1
decimation = 1

# IO vars
dir_in = args.input

# open digital RF path
dio = drf.DigitalRFReader(dir_in)

# get sampling rate
sr = dio.get_properties(channel)['samples_per_second']

# get data bounds
b = dio.get_bounds(channel)
if args.start:
    dtst0 = dateutil.parser.parse(args.start)
    st0 = (dtst0 - datetime.datetime(1970, 1,
                                     1, tzinfo=pytz.utc)).total_seconds()
    st0 = int(st0 * sr)
else:
    st0 = int(b[0])

if args.end:
    dtst0 = dateutil.parser.parse(args.end)
    et0 = (dtst0 - datetime.datetime(1970, 1,
                                     1, tzinfo=pytz.utc)).total_seconds()
    et0 = int(et0 * sr)
else:
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

data = np.array(psd).astype('float64')

# calculate structure
data = data - data.mean()
diffs = data[1:] - data[:-1]
structure = diffs.sum() / diffs.size

# print results
print(dir_in.split('/')[-2] + ': ' + str(structure))
