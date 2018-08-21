import numpy as np
import argparse

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

def time_scheme1(array):
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
        new[a,...] = time_binning(compress, factor1, expand=True)
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
        new[a,...] = time_binning(compress, factor2, expand=True)
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

def time_scheme2(array):
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
    factor1 = 5
    a = 124
    while a <= 288:
        # b = a + 1
        compress = raw[a,...]
        new[a,...] = time_binning(compress, factor1, expand=True)
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
        new[a,...] = time_binning(compress, factor2, expand=True)
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

def time_scheme2_ne(array):
    """To be used with frequency binning scheme 4."""

    bins = 1000
    num_fft = 123 #the reduced number of frequency bins

    # reshape into two axis: axis zero is time, axis 1 is frequency
    # then take the transpose, so that axis zero is frequency
    raw = array.reshape((-1,num_fft)).T

    # create new array
    new = np.zeros(raw.shape)

    # don't time average in frequency bins 0 to 54
    new[0:54,...] = raw[0:54,...]

    # time average in frequency bins 54 to 66
    factor1 = 5
    a = 54
    while a <= 66:
        # b = a + 1
        compress = raw[a,...]
        new[a,:200] = time_binning(compress, factor1, expand=False)
        a += 1
    del a

    # don't time average in frequency bins 66 to 116
    new[66:116,...] = raw[66:116,...]

    # time average in frequency bins 116 to 123
    factor2 = 5
    a = 116
    while a <= 122:
        compress = raw[a,...]
        new[a,:200] = time_binning(compress, factor2, expand=False)
        a += 1
    del a

    # transpose back to the original array shape
    new1 = new.T

    # ensure that the array is the correct shape
    if new1.shape == (bins, num_fft):
        # make array one dimensional again
        new2 = new1.reshape((1,-1))
        new3 = new2[new2 != 0]
        return new3
    else:
        raise RuntimeError('Output array is the wrong shape, something went wrong.')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of file to read from")
parser.add_argument("-n", "--ne", help="non-expanded file to read from")
args = parser.parse_args()

in_file = args.input
in_file_ne = args.ne
out_file = in_file.split('.')[0] + '_freq_binned.txt'
out_file_ne = in_file_ne.split('.')[0] + '_freq_binned_ne.txt'

f = open(out_file, 'w+')
time_scheme2(np.loadtxt(in_file)).tofile(f, '\n')
f.close()

f = open(out_file_ne, 'w+')
time_scheme2_ne(np.loadtxt(in_file_ne)).tofile(f, '\n')
f.close()

# IO variables
dir = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/freq_binned'
in_txt = dir + '/scheme4.txt'
in_txt_ne = dir + '/scheme4_ne.txt'
scheme1_txt = dir + '/time_binned/scheme1.txt'
scheme1_ne_txt = dir + '/time_binned/scheme1_ne.txt'

# load expanded data from psd_txt
data = np.loadtxt(in_txt)

# load non-expanded data from psd_txt
data_ne = np.loadtxt(in_txt_ne)

data1 = data
data2 = data_ne

# # run scheme 1
# f = open(scheme1_txt, 'w+')
# np.log10(time_scheme2(data1)).tofile(f, '\n')
# f.close()

# run scheme 1 not expanded
# data2 = data2.reshape((-1,125)).T
f = open(scheme1_ne_txt, 'w+')
np.log10(time_scheme2_ne(data2)).tofile(f, '\n')
f.close()
