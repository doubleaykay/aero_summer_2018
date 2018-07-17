import digital_rf as drf
import scipy
from scipy import constants
import numpy as np
from matplotlib import pyplot as plt

#path to existing digital_rf data
path_to_data = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/20180506-0823-0840-TLK-INT/'

#initialize digital_rf reader
reader = drf.DigitalRFReader(path_to_data)

#get channels in data
channels = reader.get_channels()

#get bounds of data (currently using the first channel, need to make this selectable)
bounds = reader.get_bounds(channels[0])

#loop to read through and plot all data
i = 0
while i <= (bounds[1] - bounds[0]):
    vector_size = 128
    data = reader.read_vector(bounds[0] + i, vector_size, channels[0])
    data_fft = np.fft.fft(data)
    plt.plot(data_fft)
    i += vector_size
plt.show()

#close digital_rf reader (once everything is done)
reader.close()
