import numpy as np
from matplotlib import pyplot

data = np.loadtxt('/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/raw/freq_binned/time_binned/scheme1.txt')
data = data.reshape((-1, 1024)).T

freq_axis = np.loadtxt('/home/anoush/Desktop/working/freq_binning/20170917-0929-0934-TLK-INT/ant1/freq.txt')
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
