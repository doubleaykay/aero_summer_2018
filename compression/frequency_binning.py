import numpy as np

def freq_binning(array, factor, expand=False):
    # check that array length is a factor of the factor provided
    if not (len(array) % factor) == 0:
        raise ValueError('Length of array is not a multiple of ' + str(factor) + '!')

    # bin by frequency
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

def scheme1(array):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in freq_binning(working[0:20], 10, expand=True):
            compressed.append(d)
        del d

        # do not average the next 103 bins
        for d in working[20:123]:
            compressed.append(d)
        del d

        for d in freq_binning(working[123:533], 10, expand=True):
            compressed.append(d)
        del d

        # do not average the next 101 bins
        for d in working[533:634]:
            compressed.append(d)
        del d

        for d in freq_binning(working[634:1024], 10, expand=True):
            compressed.append(d)
        del d

        del working
        a += 1

    return compressed

# IO variables
dir = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw'
psd_txt = dir + '/psd.txt'
new_txt = dir + '/psd_freq_binned.txt'

# load data from psd_txt
data = np.loadtxt(psd_txt)

f = open(new_txt, 'w+')
np.log10(np.array(scheme1(data))).tofile(f, '\n')
f.close()
