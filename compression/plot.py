import time

import matplotlib.gridspec
import matplotlib.mlab
import matplotlib.pyplot
import numpy
import numpy.fft

import pickle

dir = '/home/anoush/Desktop/working/intermediate_test'
dir_plot = dir + '/plot.png'
path_vars = dir + '/vars'

#load vars from intermediate file processing script via pickle
file_vars = open(path_vars, 'r')
bins, st0, sr, path, path_psd_txt, path_freq_txt, cfreq, num_fft, path_sti_times = pickle.load(file_vars)
file_vars.close()

title = 'Digital RF Data'

matplotlib.rc('axes', hold=False)

# Figure setup
f = matplotlib.pyplot.figure(figsize=(7, numpy.min([numpy.max([4, 1]), 7])), dpi=128)

gridspec = matplotlib.gridspec.GridSpec(1, 1)

ax = f.add_subplot(gridspec[0])

#initial vmin and vmax values
vmin = 0
vmax = 0

#read intermediate files
sti_psd_data = numpy.loadtxt(path_psd_txt)
sti_psd_data = 10 * sti_psd_data.reshape((-1, (num_fft / 2))).T
freq_axis = numpy.fromfile(path_freq_txt)
freq_axis = freq_axis[:1024]
sti_times = numpy.loadtxt(path_sti_times)

for p in numpy.arange(1):
    # determine image x-y extent
    extent = (
        0,
        bins,
        numpy.min(freq_axis) / 1e3,
        numpy.max(freq_axis) / 1e3,
    )

    # determine image color extent (5th to 95th percentile)
    Pss = sti_psd_data
    vmin = numpy.real(numpy.percentile(Pss, 5))
    vmax = numpy.real(numpy.percentile(Pss, 95))

    # plot data
    im = ax.imshow(sti_psd_data, cmap='gray', origin='lower', extent=extent, interpolation='nearest', vmin=vmin, vmax=vmax, aspect='auto')

    ax.set_ylabel('f (Hz)', fontsize=8)

    #set y axis range
    ymin = 0
    ymax = 5000

    # plot dates
    tick_spacing = numpy.arange(bins / 8, bins, bins / 8)
    ax.set_xticks(tick_spacing)
    #tick_labels = []

    for s in tick_spacing:
       tick_time = sti_times[s]

       if tick_time == 0:
           tick_string = ''
       else:
           gm_tick_time = time.gmtime(numpy.real(tick_time))
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

# save and show plot
# matplotlib.pyplot.savefig(dir_plot)
matplotlib.pyplot.show()
