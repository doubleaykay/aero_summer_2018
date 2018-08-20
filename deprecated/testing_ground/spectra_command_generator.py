import os
import digital_rf as drf

dir = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/'

drf_sti = 'python /home/anoush/digital_rf/python/tools/drf_sti.py'

args = '-f 1 -n 2048 -b 1000 -v -y 0:5000 --colormap gray --scale 595'

#scale is '-y 0:5000' for INT, '-y 0:10000' for POL

output_path = '/home/anoush/Desktop/working/'

#get list of directories in specified folder
os.chdir(dir)
subdirs = next(os.walk('.'))[1]

# open script
script = open('plot.sh', 'w')

i = 0
while i <= len(subdirs) - 1:
    path = '-p ' + dir + subdirs[i]

    reader = drf.DigitalRFReader(str(subdirs[i]))
    ch = reader.get_channels()
    u = 0
    while u <= len(ch) - 1:
        channel = '-c' + ' ' + ch[u] + ':0'
        output_dir = output_path + 'gen/' + subdirs[i]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output = '-o ' + output_path + 'gen/' + subdirs[i] + '/' + ch[u] + '.png'
        command = drf_sti + ' ' + args + ' ' + path + ' ' + channel + ' ' + output

        script.write(command + '\n')
        u += 1

    i += 1



# close script
script.close()
