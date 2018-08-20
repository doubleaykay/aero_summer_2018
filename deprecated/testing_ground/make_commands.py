import os

dir = '/media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_drf'
test = [x[1] for x in os.walk(dir)]
drf = test[0]

f = open('run_all.sh', 'w+')


p11 = 'python /home/anoush/labelle_to_dRF/compression/sti_intermediate_file.py -i /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_drf/'
# drf folder name
p12 = ' -o /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/3_compressed/'
# drf folder name
p13 = ' -n 2048 -b 1000 -c ant'
# channel number

p21 = 'python /home/anoush/labelle_to_dRF/compression/binning.py -i /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/3_compressed/'
# drf folder name
p22 = ' -c ant'
# channel number

p31 = 'python /home/anoush/labelle_to_dRF/compression/plot.py -i /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/3_compressed/'
# drf folder name
p32 = ' -c ant'
# channel number
p33 = ' -b '
# bit depth

for a in drf:
    folder = a
    channel = 0
    while channel <= 3:
        command1 = p11 + folder + p12 + folder + p13 + str(channel)
        command2 = p21 + folder + p22 + str(channel)
        command31 = p31 + folder + p32 + str(channel) + p33 + 'raw'

        f.write(command1 + '\n')
        f.write(command2 + '\n')
        f.write(command31 + '\n')

        bit = 1
        while bit <= 8:
            command32 = p31 + folder + p32 + str(channel) + p33 + str(bit)
            f.write(command32 + '\n')
            bit += 1

        channel += 1
    del command1, command2, command31, command32, channel, bit

f.close()
