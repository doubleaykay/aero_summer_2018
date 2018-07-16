import digital_rf as drf
import scipy
from scipy import constants
import numpy as np

#path to existing digital_rf data
path_to_data = "/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/20180506-0823-0840-TLK-INT/"

#initialize digital_rf reader
reader = drf.DigitalRFReader(path_to_data)
