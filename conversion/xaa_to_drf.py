import numpy as np
import digital_rf as drf
import dateutil.parser

"""
The 'xaa' datafile provided by the LaBelle Group spans roughly four hours and
contains an AKR event. The sampling frequency was 2MHz, but only 25,000 samples
per second were retained, leaving gaps in the data. However, AERO will be
transmitting continuous data. This script takes the 'xaa' datafile, repeats
every 25,000 samples 80 times to return to the 2MHz sampling frequency,
and then writes the new data in the MIT digital_rf data storage format.

Written by Anoush Khan, winter 2018.
"""

# frequencies
freq = 2000000
small_freq = 25000

# custom numpy datatype
data_type = np.dtype([('r', np.int16), ('i', np.int16)])

# location of input file
file_xaa = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/winter/xaa'

# location of drf out dir
dir = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/winter/xaa_drf/ch0'

# pull in raw data
raw = np.fromfile(file_xaa, data_type)

# keep only data section with AKR event
raw = raw[189000000:]

# now the data starts 2 h, 6 min, and 2 sec after midnight on 2018-06-15
# convert this into seconds and samples since UNIX epoch
UTstart = dateutil.parser.parse('20180615 02:06:02')
epoch = dateutil.parser.parse('1970, 1, 1')
sec_since_epoch = int((UTstart - epoch).total_seconds())
samples_since_epoch = sec_since_epoch * freq

# index of the start of each second of raw data
indx = np.arange(0, np.size(raw), 25000)
indx[1:] = indx[1:] - 1

# create drf writer object
writer = drf.DigitalRFWriter(
    dir, dtype=data_type,
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=samples_since_epoch,
    sample_rate_numerator=freq, sample_rate_denominator=1,
    is_complex=True
)

for i in np.arange(0, np.size(indx)-1):
    # print curent index
    print(i)

    # get a second of raw data
    tmp = raw[indx[i]:indx[i+1]]

    # repeat 25,000 samples 80 times to get to 2,000,000
    # then transpose to single column
    repd = np.tile(tmp, (1,80)).T

    writer.rf_write(repd)

    # print confirmation
    print('Good')
    print('\n')

# close drf writer object
writer.close()
