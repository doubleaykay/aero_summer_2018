import numpy as np

# this following function is the same one used in frequency binning. I should make this into an even futher generalized function...

def time_binning(array, factor, expand=False):
    # check that array length is a factor of the factor provided
    if not (len(array) % factor) == 0:
        raise ValueError('Length of array is not a multiple of ' + str(factor) + '!')

    # bin by time
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

def time_scheme1(array, expand):
    bins = 1000
    num_fft = 1024

    # reshape into two axis: axis zero is time, axis 1 is frequency
    # then take the transpose, so that axis zero is frequency
    raw = array.reshape((-1,num_fft)).T

    # create new array
    new = np.zeros(raw.shape)

    # don't time average in frequency bins 0 to 124
    new[0:124,...] = raw[0:124,...]

    # time average in frequency bins 124 to 288
    factor1 = 10
    a = 124
    while a <= 288:
        # b = a + 1
        compress = raw[a,...]
        if expand:
            new[a,...] = time_binning(compress, factor1, expand=expand)
        if not expand:
            slice_end = len(compress) / factor1
            new[a,0:slice_end] = time_binning(compress, factor1, expand=expand)
        a += 1
    del a

    # don't time average in frequency bins 288 to 862
    new[288:862,...] = raw[288:862,...]

    # time average in frequency bins 862 to 1024
    factor2 = 10
    a = 862
    while a <= 1023:
        # b = a + 1
        compress = raw[a,...]
        if expand:
            new[a,...] = time_binning(compress, factor1, expand=expand)
        if not expand:
            slice_end = len(compress) / factor1
            new[a,0:slice_end] = time_binning(compress, factor1, expand=expand)
        a += 1
    del a

    # transpose back to the original array shape
    new1 = new.T

    # ensure that the array is the correct shape
    if new1.shape == (bins, num_fft):
        # make array one dimensional again
        new2 = new1.reshape((1,-1))
        if expand:
            return new2
        if not expand:
            new3 = new2[new2 != 0]
            return new3
    else:
        raise RuntimeError('Output array is the wrong shape, something went wrong.')

# IO variables
dir = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/freq_binned'
in_txt = dir + '/scheme3.txt'
scheme1_txt = dir + '/time_binned/scheme1.txt'
scheme1_ne_txt = dir + '/time_binned/scheme1_ne.txt'

# load data from psd_txt
data = np.loadtxt(in_txt)

# undo log10 in data (this is temporary and needs to be fixed)
data1 = []
for a in data:
    data1.append(10 ** a)
data1 = np.array(data1)

# run scheme 1
f = open(scheme1_txt, 'w+')
np.log10(time_scheme1(data1, True)).tofile(f, '\n')
f.close()

# run scheme 1 not expanded
f = open(scheme1_ne_txt, 'w+')
np.log10(time_scheme1(data1, False)).tofile(f, '\n')
f.close()
