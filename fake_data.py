import digital_rf as drf
import scipy
from scipy import constants
import numpy as np

#path to existing digital_rf data
path_to_data = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/20180506-0823-0840-TLK-INT/'

#initialize digital_rf reader
reader = drf.DigitalRFReader(path_to_data)

#get channels in data
channels = reader.get_channels()

#get bounds of data (currently using the first channel, need to make this selectable)
bounds = reader.get_bounds(channels[0])

#read data into variable
data = reader.read_vector(bounds[0], 128, channels[0])
print(data)

#close digital_rf reader (once everything is done)
reader.close()
