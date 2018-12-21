import dateutil.parser as dp
import os
import numpy as np

drf_folder = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_drf'

output = [dI for dI in os.listdir(drf_folder) if os.path.isdir(os.path.join(drf_folder,dI))]
drf = [s for s in output if 'POL' not in s]
drf = np.sort(drf)

times = []

for k in drf:
    date = k.split('-')[0]
    start = dp.parse(date + k.split('-')[1])
    end = dp.parse(date + k.split('-')[2])

    times.append(int((end - start).total_seconds()))

mins = []
for k in times: mins.append(k / 60)

spb = []
for k in times: spb.append(k / 1000.)
