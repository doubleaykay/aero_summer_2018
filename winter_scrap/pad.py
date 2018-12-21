import dateutil.parser as dp
import os
import numpy as np
import digital_rf as drf

p1 = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/splits/20170915-0726-0728-TLK-INT/ant1' #18
p2 = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/splits/20170917-0952-0955-TLK-INT/ant1' #12
p3 = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/splits/20170918-0955-0957-TLK-INT/ant1' #18

channel = 'ant1'
freq = 10000000

epoch = dp.parse('1970, 1, 1')
p1d = dp.parse('20170915 0728')
p2d = dp.parse('20170917 0955')
p3d = dp.parse('20170918 0957')

p1s = (int((p1d - epoch).total_seconds()) * freq) + 1
p2s = (int((p2d - epoch).total_seconds()) * freq) + 1
p3s = (int((p3d - epoch).total_seconds()) * freq) + 1

# 18x zeros
a = np.zeros([1800000000])

# 12x zeros
b = np.zeros([1200000000])

# p1
p1w = drf.DigitalRFWriter(
    p1, dtype=np.dtype('u2'),
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=p1s,
    sample_rate_numerator=freq, sample_rate_denominator=1,
    is_complex=False
)

p1w.rf_write(a.astype('u2'))
p1w.close()

# p2
p1w = drf.DigitalRFWriter(
    p2, dtype=np.dtype('u2'),
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=p2s,
    sample_rate_numerator=freq, sample_rate_denominator=1,
    is_complex=False
)

p1w.rf_write(b.astype('u2'))
p1w.close()

# p3
p1w = drf.DigitalRFWriter(
    p3, dtype=np.dtype('u2'),
    subdir_cadence_secs=3600, file_cadence_millisecs=1000,
    start_global_index=p3s,
    sample_rate_numerator=freq, sample_rate_denominator=1,
    is_complex=False
)

p1w.rf_write(a.astype('u2'))
p1w.close()
