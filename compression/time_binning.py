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
    a = 124
    while a <= 287:
        b = a + 1
        compress = raw[a:b,...]
        new[a:b,...] = time_binning(compress, 10, expand=expand)
        a += 1
    del a

    # don't time average in frequency bins 288 to 862
    new[288:862,...] = raw[288:862,...]

    # time average in frequency bins 862 to 1024
    a = 862
    while a <= 1023:
        b = a + 1
        compress = raw[a:b,...]
        new[a:b,...] = time_binning(compress, 10, expand=expand)
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
