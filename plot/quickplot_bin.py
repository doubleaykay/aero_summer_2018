import numpy as np
from matplotlib import pyplot

def read_bin(filename):
    a = np.fromfile(filename, dtype='i1')
    b0 = np.bitwise_and(a,15)
    b1 = np.bitwise_and(a,15<<4) >> 4
    c = np.stack((b0,b1))

    return c.T.reshape(-1)

# data = np.loadtxt('/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/freq_binned/time_binned/scheme1.txt')

data = read_bin('/home/anoush/Documents/aero_winter/test/ant1/psd.dat')
data = data.reshape((-1, 1024)).T

# freq_axis = np.loadtxt('/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/freq.txt')

freq_axis = read_bin('/home/anoush/Documents/aero_winter/test/ant1/freq.dat')
freq_axis = freq_axis[:1024]

bins = 1000

extent = (
        0,
        bins,
        np.min(freq_axis) / 1e3,
        np.max(freq_axis) / 1e3,
    )

vmin = np.real(np.percentile(data, 5))
vmax = np.real(np.percentile(data, 95))

pyplot.imshow(data, cmap='gray', origin='lower', extent=extent, interpolation='nearest', vmin=vmin, vmax=vmax, aspect='auto')
pyplot.show()
