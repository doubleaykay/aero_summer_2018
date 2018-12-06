import time

import matplotlib.gridspec
import matplotlib.mlab
import matplotlib.pyplot
import numpy as np

import pickle
import argparse

def read_bin(filename):
    a = np.fromfile(filename, dtype='i1')
    b0 = np.bitwise_and(a,15)
    b1 = np.bitwise_and(a,15<<4) >> 4
    c = np.stack((b0,b1))

    return c.T.reshape(-1)

# get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location directory to read from")
parser.add_argument("-c", "--channel", help="channel to read from")
parser.add_argument("-t", "--title", help="plot title")
parser.add_argument("-d", "--description", help="description to show on plot")
parser.add_option("-o", "--outname", dest="outname", default=None, type=str, help="Name of file that figure will be saved under.")
args = parser.parse_args()

dir = args.input + '/' + args.channel

file_freq = dir + '/freq.dat'
file_sti_times = dir + '/sti_times.dat'
file_psd = dir + '/psd.dat'
file_vars = dir + '/vars'

# load vars from intermediate file processing script via pickle
file_vars = open(file_vars, 'r')
bins, st0, sr, cfreq, num_fft = pickle.load(file_vars)
file_vars.close()

if args.title == None:
    title = args.input.split('/')[-2]
else:
    title = args.title

if args.description == None:
    description = 'Freq Binning 4, Time Binning 2, 4-big Amp Binning'
else:
    description = args.description

matplotlib.rc('axes', hold=False)

# Figure setup
f = matplotlib.pyplot.figure(figsize=(7, np.min([np.max([4, 1]), 7])), dpi=128)

gridspec = matplotlib.gridspec.GridSpec(1, 1)

ax = f.add_subplot(gridspec[0])

# initial vmin and vmax values
vmin = 0
vmax = 0

# load data
sti_psd_data = read_bin(file_psd)
sti_psd_data = 10 * sti_psd_data.reshape((-1, (num_fft / 2))).T

freq_axis = np.fromfile(file_freq)
freq_axis = freq_axis[:1024]

sti_times = np.fromfile(file_sti_times)

for p in np.arange(1):
    # determine image x-y extent
    extent = (
        0,
        bins,
        np.min(freq_axis) / 1e3,
        np.max(freq_axis) / 1e3,
    )

    # determine image color extent (5th to 95th percentile)
    Pss = sti_psd_data[np.nonzero(sti_psd_data)]
    vmin = np.real(np.percentile(Pss, 5))
    vmax = np.real(np.percentile(Pss, 95))

    # plot data
    im = ax.imshow(sti_psd_data, cmap='gray', origin='lower', extent=extent, interpolation='nearest', vmin=vmin, vmax=vmax, aspect='auto')

    ax.set_ylabel('f (Hz)', fontsize=8)

    #set y axis range
    ymin = 0
    ymax = 5000

    # plot dates
    tick_spacing = np.arange(bins / 8, bins, bins / 8)
    ax.set_xticks(tick_spacing)
    tick_labels = []

    for s in tick_spacing:
       tick_time = sti_times[s]

       if tick_time == 0:
           tick_string = ''
       else:
           gm_tick_time = time.gmtime(np.real(tick_time))
           tick_string = '%02d:%02d:%02d' % (gm_tick_time[3], gm_tick_time[4], gm_tick_time[5])
           tick_labels.append(tick_string)

    ax.set_xticklabels(tick_labels)

    # set the font sizes
    tl = ax.get_xticklabels()

    for tk in tl:
        tk.set_size(8)
    del tl

    tl = ax.get_yticklabels()

    for tk in tl:
        tk.set_size(8)
    del tl

# create a time stamp
start_time = st0 / sr
srt_time = time.gmtime(start_time)
sub_second = int(round((start_time - int(start_time)) * 100))
timestamp = "%d-%02d-%02d %02d:%02d:%02d.%02d UT" % (srt_time[0], srt_time[1], srt_time[2], srt_time[3], srt_time[4], srt_time[5], sub_second)

# add and modify aspects of plot post-plotting
f.suptitle('%s %s %4.2f MHz' % (title, timestamp, cfreq / 1E6), fontsize=10)

ax.set_xlabel('time (UTC)', fontsize=8)

tl = ax.get_xticklabels()
for tk in tl:
    tk.set_size(8)
del tl
tl = ax.get_yticklabels()
for tk in tl:
    tk.set_size(8)
del tl

gridspec.update()

f.tight_layout()

f.subplots_adjust(top=0.95, right=0.88)
cax = f.add_axes([0.9, 0.12, 0.02, 0.80])
f.colorbar(im, cax=cax)

f.text(0.005, 0.005, description, size='x-large')

if args.outname:
    fname, ext = os.path.splitext(args.outname)
    if ext == '':
        ext = '.png'
    matplotlib.pyplot.savefig(fname+ext, dpi=300)

# save and show plot
#matplotlib.pyplot.savefig(dir_plot)
matplotlib.pyplot.show()
