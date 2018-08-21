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

def scheme1(array, expand):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in freq_binning(working[0:20], 10, expand=expand):
            compressed.append(d)
        del d

        # do not average the next 103 bins
        for d in working[20:123]:
            compressed.append(d)
        del d

        for d in freq_binning(working[123:533], 10, expand=expand):
            compressed.append(d)
        del d

        # do not average the next 101 bins
        for d in working[533:634]:
            compressed.append(d)
        del d

        for d in freq_binning(working[634:1024], 10, expand=expand):
            compressed.append(d)
        del d

        del working
        a += 1

    return np.array(compressed)

def scheme2(array, expand):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in freq_binning(working[0:20], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[20:124], 2, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[124:524], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[524:634], 2, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[634:774], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[774:864], 10, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[864:1024], 20, expand=expand):
            compressed.append(d)
        del d

        del working
        a += 1

    return np.array(compressed)

def scheme3(array, expand):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in freq_binning(working[0:20], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[20:124], 2, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[124:524], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[524:632], 4, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[632:634], 2, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[634:774], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[774:864], 10, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[864:1024], 20, expand=expand):
            compressed.append(d)
        del d

        del working
        a += 1

    return np.array(compressed)

def scheme4(array, expand):
    bins = 1000
    num_fft = 1024

    raw = array.reshape((-1,num_fft))

    compressed = []

    a = 0
    while a <= (raw.shape[0] - 1):
        working = raw[a,...]

        for d in freq_binning(working[0:20], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[20:124], 2, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[124:524], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[524:616], 4, expand=expand):
            compressed.append(d)
        del d #2600 to 3000

        for d in freq_binning(working[616:776], 20, expand=expand):
            compressed.append(d)
        del d

        for d in freq_binning(working[776:864], 8, expand=expand):
            compressed.append(d)
        del d #increase to 4ish

        for d in freq_binning(working[864:1024], 20, expand=expand):
            compressed.append(d)
        del d

        del working
        a += 1

    return np.array(compressed)

# TESTING CODE
# # IO variables
# dir = '/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw'
# psd_txt = dir + '/psd.txt'
# scheme1_txt = dir + '/freq_binned/scheme1.txt'
# scheme2_txt = dir + '/freq_binned/scheme2.txt'
# scheme3_txt = dir + '/freq_binned/scheme3.txt'
# scheme4_txt = dir + '/freq_binned/scheme4.txt'
# scheme1_ne_txt = dir + '/freq_binned/scheme1_ne.txt'
# scheme2_ne_txt = dir + '/freq_binned/scheme2_ne.txt'
# scheme3_ne_txt = dir + '/freq_binned/scheme3_ne.txt'
# scheme4_ne_txt = dir + '/freq_binned/scheme4_ne.txt'
#
# # load data from psd_txt
# data = np.loadtxt(psd_txt)
#
# # run scheme 1
# f = open(scheme1_txt, 'w+')
# np.log10(scheme1(data, True)).tofile(f, '\n')
# f.close()
#
# # run scheme 1 no expansion
# f = open(scheme1_ne_txt, 'w+')
# np.log10(scheme1(data, False)).tofile(f, '\n')
# f.close()
#
# # run scheme 2
# f = open(scheme2_txt, 'w+')
# np.log10(scheme2(data, True)).tofile(f, '\n')
# f.close()
#
# # run scheme 2 no expansion
# f = open(scheme2_ne_txt, 'w+')
# np.log10(scheme2(data, False)).tofile(f, '\n')
# f.close()
#
# # run scheme 3
# f = open(scheme3_txt, 'w+')
# np.log10(scheme3(data, True)).tofile(f, '\n')
# f.close()
#
# # run scheme 3 no expansion
# f = open(scheme3_ne_txt, 'w+')
# np.log10(scheme3(data, False)).tofile(f, '\n')
# f.close()
#
# # run scheme 4
# f = open(scheme4_txt, 'w+')
# np.log10(scheme4(data, True)).tofile(f, '\n')
# f.close()
#
# # run scheme 4 no expansion
# f = open(scheme4_ne_txt, 'w+')
# np.log10(scheme4(data, False)).tofile(f, '\n')
# f.close()
