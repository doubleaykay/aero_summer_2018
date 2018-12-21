import digital_rf as drf
import numpy as np

import matplotlib.pyplot as plt

dir_in = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/winter/xaa_drf/'
dio = drf.DigitalRFReader(dir_in)
channel = 'ch0'
sr = dio.get_properties(channel)['samples_per_second']
b = dio.get_bounds(channel)
st0 = int(b[0])
et0 = int(b[1])
samples_per_stripe = 2048
start_sample = st0

data = dio.read_vector(start_sample, samples_per_stripe, channel)

amp = []

for k in data:
    a = np.square(k.real) + np.square(k.imag)
    amp.append( np.sqrt( a ) )

plt.plot(amp)
plt.show()
