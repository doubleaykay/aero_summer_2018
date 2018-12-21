a = 'python plot_compressed.py -c ant1 -t Compressed -i /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/compressed/'

# 20170915-0726-0728-TLK-INT

b = '/ -o /media/anoush/5358359c-0dd3-4f0f-89a8-9716f7c6869d/_data/plots2/'

# 20170915-0726-0728-TLK-INT

c = '/after.png'


d = ['20170917-0952-0955-TLK-INT',
'20180506-0823-0840-TLK-INT-A',
'20170918-0955-0957-TLK-INT',
'20180506-0823-0840-TLK-INT-B',
'20170915-0726-0728-TLK-INT',
'20180120-0726-0733-TLK-INT',
'20180506-0823-0840-TLK-INT-C',
'20170917-0929-0934-TLK-INT',
'20180325-0919-0927-TLK-INT']


f = open('after_plots_2.sh', 'a')

for k in d:
    path = a + k + b + k + c
    f.write(path + '\n')

f.close()
