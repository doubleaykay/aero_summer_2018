import numpy as np

def compression_diffs(reference, compressed):
    scale_factor = np.amax(reference) / np.amax(compressed)
    scaled = []
    for b in compressed:
        scaled.append(b * scale_factor)

    diffs = []
    if len(reference) == len(scaled):
        i = 0
        while i <= (len(reference) -1):
            value = abs(reference[i] - scaled[i])
            diffs.append(value)
            i += 1
    else:
        print('Arrays are not equal in length.')

    diffs = np.array(diffs)
    return diffs

# Begin Program
unc = np.loadtxt('/home/anoush/Desktop/working/intermediate_test/psd.txt')
by = np.loadtxt('/home/anoush/Desktop/working/intermediate_test/psd_bytes.txt')
nb = np.loadtxt('/home/anoush/Desktop/working/intermediate_test/psd_nibbles.txt')

unc_by_diffs = compression_diffs(unc, by)
unc_nb_diffs = compression_diffs(unc, nb)

unc_by_diffs.tofile('/home/anoush/Desktop/working/intermediate_test/unc_by_diffs.txt', '\n')
unc_nb_diffs.tofile('/home/anoush/Desktop/working/intermediate_test/unc_nb_diffs.txt', '\n')
