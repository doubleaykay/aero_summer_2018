import os
drf_folder = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/compressed/'

a = 'python /home/anoush/Documents/aero_winter/aero_summer_2018/plot/plot_compressed.py -i /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/compressed/'
# insert folder name
b = ' -c ant1 -o /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/plots/'
# insert folder name
c = '/after.png'

f = open('after_plots.sh', 'a')

output = [dI for dI in os.listdir(drf_folder) if os.path.isdir(os.path.join(drf_folder,dI))]
drf = [s for s in output if 'POL' not in s]

for k in drf:
    t = 'mkdir -p ' + '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/plots/' + k
    f.write(t + '\n')

for k in drf:
    first = a + k + b + k + c
    f.write(first + '\n')

f.close()
