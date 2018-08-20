#command
c1 = 'python /home/anoush/digital_rf/python/tools/drf_sti.py -f 1 -n '
#n value goes here
c2 = ' -b '
#b value goes here
c3 = ' -v -y 0:5000 --colormap gray --scale 595 -p /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/2_converted/20170918-0955-0957-TLK-INT -c ant1:0 -o /home/anoush/Desktop/working/test/'
#name value goes here: 'nNUM-bNUM.png'

# open script
script = open('bin_test_plot_2.sh', 'w')

#write commands
n = 100
b = 100
while n <= 10240:
    while b <= 5000:
        command = c1 + str(n) + c2 + str(b) + c3 + 'n' + str(n) + '-b' + str(b) + '.png'
        script.write(command + '\n')
        b += 100
    n += 100
    b = 100

# close script
script.close()
