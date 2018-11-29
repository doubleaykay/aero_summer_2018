# read drf
# convert to spectral data (sti_intermediate_file.py)
# store freq and sti_times array as binary using write_bin() for plotting tool
# take psd array to be processed
# apply frequency binning scheme 4
# apply time binning scheme 2
# take log 10
# apply 4-bit amplitude binning
# store as binary

import argparse
import digital_rf as drf
import numpy as np

"""
AERO Data Compressor

This script reads digital_rf data and applies the complete aero_summer_2018
compression scheme, returning three binary files which can be read by the
plotting tool to generate spectral plots.

Outputs:
BINARY psd.bin -- spectral data
BINARY freq.bin -- frequency axis data
BINARY sti_times.bin -- time axis data
"""

#get arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="location of drf directory to read from")
parser.add_argument("-o", "--output", help="location of directory to output to")
parser.add_argument("-n", "--num_fft", nargs='?', const=2048, type=int, default=2048, help="number of frequency bins (i.e. number of data points in spectra)")
parser.add_argument("-c", "--channel", help="drf channel to read from")
parser.add_argument("-b", "--bins", nargs='?', const=1000, type=int, default=1000, help="number of time bins (i.e. number of spectra)")
args = parser.parse_args()
